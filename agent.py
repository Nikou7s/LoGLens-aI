import os
import sys
import time
import subprocess
from google import genai
from google.genai import types
from system_scanner import get_system_telemetry

# Terminal UI Colors
c_cyan = '\033[96m'
c_green = '\033[92m'
c_yellow = '\033[93m'
c_red = '\033[91m'
c_bold = '\033[1m'
c_reset = '\033[0m'

def run_agent():
    if len(sys.argv) < 2:
        print(f"{c_yellow}Usage: ./loglens \"<your task>\"{c_reset}")
        sys.exit(1)

    user_query = " ".join(sys.argv[1:])
    api_key = os.environ.get("GEMINI_API_KEY")

    if not api_key:
        print(f"{c_red}❌ GEMINI_API_KEY is not set.{c_reset}")
        sys.exit(1)

    telemetry = get_system_telemetry()
    
    system_instruction = f"""You are an autonomous Linux Systems Administrator and Security Copilot running on {telemetry['os_name']}.
Host Architecture: {telemetry['architecture']}
Available Package Managers: {', '.join(telemetry['package_managers'])}
Default Shell: {telemetry['shell']}

Your goal is to parse the user's intent and generate exact, non-interactive Bash commands tailored specifically to this OS distribution.

CRITICAL PACKAGE MANAGER RULES:
1. Standard `pacman` ONLY contains official packages. Many security tools (like feroxbuster, rustscan, etc.) are in the AUR.
2. If `yay` or `paru` are listed in Available Package Managers, you MUST prefer them for third-party or security tools (e.g. use `yay -S --noconfirm <tool>`).
3. If no AUR helper is present and the tool isn't official, fallback to GitHub source builds (`git clone` -> `make`/`cargo build`).

Format your response strictly as follows:
1. Short explanation (1-2 sentences) of what the fix or installation does.
2. The exact executable command wrapped inside a code block labeled 'bash'.
   Chain multiple commands with `&&` so they execute sequentially in one block. Do NOT use interactive commands that block STDIN.
"""

    models_to_try = ["gemini-4-argon", "gemini-3.5-flash", "gemini-3.1-flash-lite", "gemini-flash-latest"]
    client = genai.Client(api_key=api_key)
    output_text = None

    print(f"\n{c_cyan}{c_bold}🔍 Analyzing request...{c_reset}")

    for model_name in models_to_try:
        sys.stdout.write(f"\r{c_bold}🤖 Querying {model_name}... {c_reset}")
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
        except Exception:
            sys.stdout.write(f"{c_yellow}⚠ Failed. Shifting... {c_reset}")
            sys.stdout.flush()
            time.sleep(1)

    if not output_text:
        print(f"\n{c_red}❌ All models failed.{c_reset}")
        sys.exit(1)

    if "```bash" in output_text:
        command = output_text.split("```bash")[1].split("```")[0].strip()
        explanation = output_text.split("```bash")[0].replace("1.", "").strip()
        
        print(f"\n{c_cyan}💡 {explanation}{c_reset}")
        print(f"{c_bold}⚡ Command:{c_reset} {command}\n")
        
        confirm = input(f"{c_yellow}Execute? [y/N]: {c_reset}").strip().lower()

        if confirm == 'y':
            print(f"\n{c_green}🚀 Executing...{c_reset}\n")
            process = subprocess.run(command, shell=True)
            if process.returncode == 0:
                print(f"\n{c_green}✅ Success{c_reset}")
            else:
                print(f"\n{c_red}❌ Failed (exit code {process.returncode}){c_reset}")
        else:
            print(f"{c_yellow}⏸️ Aborted.{c_reset}")
    else:
        print(f"\n{c_cyan}ℹ️ No command generated:\n{c_reset}", output_text)

if __name__ == "__main__":
    run_agent()
