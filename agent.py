import os
import re
import sys
import time
import subprocess
from google import genai
from google.genai import types
from system_scanner import get_system_telemetry

# Terminal UI Colors & Styling
c_cyan = '\033[96m'
c_green = '\033[92m'
c_yellow = '\033[93m'
c_red = '\033[91m'
c_magenta = '\033[95m'
c_blue = '\033[94m'
c_bold = '\033[1m'
c_dim = '\033[2m'
c_reset = '\033[0m'
c_clear_line = '\033[K'

BANNER = f"""{c_cyan}{c_bold}
 █░░ █▀█ █▀▀ █░░ █▀▀ █▄░█ █▀
 █▄▄ █▄█ █▄█ █▄▄ ██▄ █░▀█ ▄█  {c_yellow}AI Copilot{c_reset}
{c_dim} Autonomous SysAdmin & Security Terminal Agent{c_reset}
"""

def print_session_header(telemetry):
    print(BANNER)
    pkg_str = ", ".join(telemetry.get('package_managers', ['standard']))
    print(f" {c_bold}OS:{c_reset} {telemetry.get('os_name', 'Linux')} ({telemetry.get('architecture', 'x86_64')}) "
          f"│ {c_bold}Pkg Tools:{c_reset} {c_green}{pkg_str}{c_reset} "
          f"│ {c_bold}Shell:{c_reset} {telemetry.get('shell', '/bin/bash')}")
    print(f"{c_dim} Type your task in plain English. Type 'exit', 'clear', or 'help' to manage.{c_reset}")
    print(f"{c_cyan}{'─' * 68}{c_reset}\n")

def process_query(client, user_query, system_instruction):
    models_to_try = [
        "gemini-4-argon",
        "gemini-3.5-flash",
        "gemini-3.1-flash-lite",
        "gemini-flash-latest"
    ]
    output_text = None

    print(f"{c_cyan}{c_bold}🔍 Analyzing request...{c_reset}")

    for model_name in models_to_try:
        sys.stdout.write(f"\r{c_clear_line}{c_bold}🤖 Routing to {model_name}... {c_reset}")
        sys.stdout.flush()
        try:
            response = client.models.generate_content(
                model=model_name,
                contents=user_query,
                config=types.GenerateContentConfig(
                    system_instruction=system_instruction,
                    temperature=0.1
                )
            )
            output_text = response.text
            sys.stdout.write(f"{c_green}✅ Done{c_reset}\n")
            break
        except Exception as e:
            err_str = str(e)
            if "API_KEY_INVALID" in err_str:
                sys.stdout.write(f"\n{c_red}❌ Invalid Gemini API key.{c_reset}\n")
                return
            sys.stdout.write(f"{c_yellow}⚠ Shifted.{c_reset}")
            sys.stdout.flush()
            time.sleep(1)

    if not output_text:
        print(f"\n{c_red}❌ All model endpoints failed.{c_reset}")
        return

    # Extract bash code block using regex
    match = re.search(r"```(?:bash|sh)\n(.*?)```", output_text, re.DOTALL)
    
    if match:
        command = match.group(1).strip()
        explanation = output_text[:match.start()].replace("1.", "").strip()
        
        if explanation:
            print(f"\n{c_cyan}💡 {explanation}{c_reset}")
        print(f"\n{c_bold}⚡ Proposed Command:{c_reset}")
        print(f"   {c_green}{command}{c_reset}\n")
        
        try:
            confirm = input(f"{c_yellow}Execute on host? [y/N]: {c_reset}").strip().lower()
        except (KeyboardInterrupt, EOFError):
            print(f"\n{c_yellow}⏸ Action cancelled.{c_reset}")
            return

        if confirm == 'y':
            print(f"\n{c_green}🚀 Executing...{c_reset}\n")
            process = subprocess.run(command, shell=True)
            if process.returncode == 0:
                print(f"\n{c_green}✅ Completed successfully.{c_reset}")
            else:
                print(f"\n{c_red}❌ Terminated with exit code {process.returncode}{c_reset}")
        else:
            print(f"{c_yellow}⏸ Aborted.{c_reset}")
    else:
        print(f"\n{c_cyan}ℹ Output:\n{c_reset}", output_text)

def run_agent():
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        print(f"{c_red}❌ GEMINI_API_KEY is not set.{c_reset}")
        sys.exit(1)

    try:
        telemetry = get_system_telemetry()
    except Exception:
        telemetry = {
            "os_name": "Linux",
            "architecture": "x86_64",
            "package_managers": ["bash"],
            "shell": "/bin/bash"
        }

    system_instruction = f"""You are an autonomous Linux Systems Administrator and Security Copilot running on {telemetry.get('os_name', 'Linux')}.
Host Architecture: {telemetry.get('architecture', 'x86_64')}
Available Package Managers: {', '.join(telemetry.get('package_managers', []))}
Default Shell: {telemetry.get('shell', '/bin/bash')}

Your goal is to parse user intent and generate non-interactive Bash commands tailored specifically to this OS distribution.

CRITICAL PACKAGE MANAGER RULES:
1. Standard `pacman` ONLY contains official packages. Many security/admin tools (feroxbuster, rustscan, etc.) are in AUR.
2. If `yay` or `paru` are listed in Available Package Managers, you MUST prefer them for third-party or security tools (e.g. `yay -S --noconfirm <tool>`).
3. If no AUR helper is present and tool is not official, fallback to GitHub source builds (`git clone` -> build).

Format your response strictly as follows:
1. Short explanation (1-2 sentences) of what the fix does.
2. The exact executable command wrapped inside a code block labeled 'bash' or 'sh'.
   Chain multiple commands with `&&` so they execute sequentially in one block. Do NOT use interactive prompts that block STDIN.
"""

    client = genai.Client(api_key=api_key)

    # Mode 1: Single-shot execution if arguments were passed
    if len(sys.argv) > 1:
        query = " ".join(sys.argv[1:])
        process_query(client, query, system_instruction)
        return

    # Mode 2: Interactive REPL shell when run with no arguments
    print_session_header(telemetry)

    while True:
        try:
            prompt_input = input(f"{c_bold}{c_cyan}loglens{c_reset} {c_green}❯{c_reset} ").strip()
        except (KeyboardInterrupt, EOFError):
            print(f"\n{c_dim}Session closed.{c_reset}")
            break

        if not prompt_input:
            continue

        cmd = prompt_input.lower()
        if cmd in ("exit", "quit", ":q"):
            print(f"{c_dim}Exiting LogLens AI.{c_reset}")
            break
        elif cmd == "clear":
            os.system("clear")
            print_session_header(telemetry)
            continue
        elif cmd == "help":
            print(f"{c_cyan}LogLens Commands:{c_reset}")
            print(f"  • Describe any sysadmin task (e.g. 'kill whatever is on port 8080')")
            print(f"  • 'clear' to refresh screen")
            print(f"  • 'exit' or Ctrl+C to quit\n")
            continue

        process_query(client, prompt_input, system_instruction)
        print()

if __name__ == "__main__":
    run_agent()
