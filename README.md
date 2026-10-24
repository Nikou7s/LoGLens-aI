# 🛠 LogLens AI — SysAdmin & Security Copilot

![Hacktoberfest 2026](https://img.shields.io/badge/Hacktoberfest-2026-blueviolet)
![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)
![Python](https://img.shields.io/badge/Python-3.9%2B-blue)
![Powered by Gemini](https://img.shields.io/badge/Powered%20by-Gemini-4285F4)

LogLens AI is a dual-mode, autonomous system administration assistant. It features an interactive web dashboard for multimodal log analysis and a native terminal copilot that scans host telemetry to generate, risk-rate and (with your approval) execute OS-tailored remediation commands directly on your machine.

> Built for **Hacktoberfest Hack Day Pune x Poona College** under the **Best Use of Gemma 4** and **Best Open-Source AI Project** tracks.

<img width="950" height="580" alt="demo" src="https://github.com/user-attachments/assets/7442e1d0-694e-45a0-b24e-88059b1b65da" />


---

## 📌 Problem Statement

Debugging broken Linux services, network socket collisions, or missing dependencies usually forces developers into a loop of copying errors, searching the web, and pasting commands. Standard AI wrappers lack context about your specific hardware, OS distribution, and package managers, often hallucinating commands that won't work on your machine (e.g., suggesting `apt` on an Arch system), and they have no idea whether a suggested command is safe to run.

LogLens bridges this gap by acting as an active, environment-aware execution engine with multiple safety layers between the model and your shell.

---

## 🚀 Key Features

| Feature | What it does |
|---|---|
| 💻 **Autonomous Execution Engine** | Writes native bash commands, runs them on your host through `bash -c`, and streams output live, always behind a human-in-the-loop confirmation. |
| 🔍 **Context-Aware Telemetry** | Detects distro (`/etc/os-release`, incl. `ID_LIKE`), architecture, kernel, user, root/sudo status, init system, container status and installed package managers (pacman, yay, paru, apt, dnf, zypper, apk, pipx, cargo, go...). Rules are generated per distro family, so Arch gets AUR logic and Debian gets `apt-get`. |
| 🛡 **Three-Layer Safety Model** | The model rates every command `low/medium/high`, a code-level regex filter hard-blocks catastrophic commands and escalates dangerous ones, and you confirm. The final risk is the higher of the model's and the filter's. |
| 🔁 **Self-Repair Loop** | If a command fails, the redacted output tail goes back to the model so it can diagnose and propose a corrected command (up to 3 rounds, each needing your approval). |
| 🧠 **Conversation Memory** | Follow-ups like *"now do the same for port 9090"* work. History is capped at the last 16 messages. |
| ✏️ **Edit Before Run** | Press `e` at the confirm prompt to tweak the command in an editable line before it executes. |
| ⚡ **Resilient Model Routing** | Priority-ordered `google-genai` fallback chain. Missing models (404) are skipped for the session, rate-limited ones (429) cool down for 60s, transient 5xx errors get one retry, and an invalid key stops immediately. |
| 🕵️ **Secret Redaction** | Private keys, `password=` / `token:` pairs, AWS and GitHub tokens, bearer tokens and shadow hashes are scrubbed from command output before it is sent back to the model. |
| 🧾 **Local Audit Log** | Every command run or blocked is appended to `~/.loglens_audit.log` (mode 600) with its exit code. Output is never logged. |
| 👁 **Multimodal Web Dashboard** | A containerized Streamlit UI that accepts drag-and-drop terminal screenshots and raw text logs for visual root-cause diagnostics. |
| 📖 **Native Linux Integration** | Ships with a symlink-ready executable and a groff manual page (`man loglens`). |

---

## 🖥 What a Session Looks Like

```text
 █░░ █▀█ █▀▀ █░░ █▀▀ █▄░█ █▀
 █▄▄ █▄█ █▄█ █▄▄ ██▄ █░▀█ ▄█  AI Copilot
 Autonomous SysAdmin & Security Terminal Agent

 OS: Arch Linux (x86_64) │ Pkg Tools: pacman, yay, cargo, go │ Shell: /bin/zsh
 User: nikouls │ Kernel: 6.x.x │ Init: systemd
 Describe a task in plain English. Commands: help · clear · reset · exit (Ctrl+D)
────────────────────────────────────────────────────────────────────

loglens ❯ install feroxbuster
  via gemini-3.5-flash

💡 Installs feroxbuster from the AUR if missing, then prints its version.
🛡  Risk: MEDIUM — installs third-party code (AUR)

⚡ Proposed Command:
   │ command -v feroxbuster >/dev/null 2>&1 || yay -S --needed --noconfirm feroxbuster && feroxbuster --version

Execute on host? [y/N/e]: y

🚀 Executing...
✅ Completed successfully in 41.3s.
```

---

## 🏗 Architecture Overview

┌───────────────────────────────────────────────────────────────┐
│ DUAL INTERFACES │
└──────┬─────────────────────────────────────────────────┬──────┘
│ │
▼ ▼
┌──────────────┐ ┌─────────────┐
│ Web UI (GUI) │ │ CLI (Agent) │
│ Streamlit │ │ ./loglens │
└──────┬───────┘ └──────┬──────┘
│ (Dockerized) │ (Native Host)
│ ▼
│ ┌─────────────┐
│ │ OS Scanner │
│ │ (/etc/os..) │
▼ └──────┬──────┘
┌────────────────────────────────────────────────────────┼──────┐
│ GOOGLE GEMINI API │ │
│ (configurable model chain, auto-fallbacks) │ │
└────────────────────────────────┬───────────────────────┴──────┘
│
▼
┌───────────────────────────────────────────────────────────────┐
│ REMEDIATION │
│ • Multimodal Diagnostic Report (Web Dashboard) │
│ • Executable Bash Commands & Compilation Chains (Terminal) │
└───────────────────────────────────────────────────────────────┘


### CLI agent pipeline

user request
│
▼
┌────────────────────┐ host telemetry + distro-aware system prompt
│ Prompt builder │
└─────────┬──────────┘
▼
┌────────────────────┐ priority list · skip dead models
│ Model router │ 60s quota cooldown · retry on 5xx
└─────────┬──────────┘
▼
┌────────────────────┐ What / Risk / one bash block, or a Need: question
│ Response parser │
└─────────┬──────────┘
▼
┌────────────────────┐ hard-block + HIGH rules (regex)
│ Safety filter │ risk = max(model rating, filter rating)
└─────────┬──────────┘
▼
┌────────────────────┐ y / N / e(dit), or type “yes” for HIGH risk
│ Human confirm │
└─────────┬──────────┘
▼
┌────────────────────┐ bash -c · live output · redacted tail · audit log
│ Executor │
└─────────┬──────────┘
│ exit ≠ 0 → offer diagnosis; tail goes back to the model (max 3 rounds)
▼
✅ done


---

## 🛡 Safety Model

| Tier | Behavior | Examples |
|---|---|---|
| 🚫 **Blocked** | Refused outright, never prompts, never runs. | `rm -rf /`, `rm -rf ~`, `rm -rf /etc`, fork bombs, `chmod -R` or `chown -R` on `/` |
| 🔴 **HIGH** | You must type the full word `yes`. | `dd of=/dev/...`, `mkfs`, `fdisk`, `wipefs`, `shred`, piping into a shell, reboot/shutdown, firewall flush/disable, stopping or restarting sshd or NetworkManager, user deletion, `crontab -r`, LUKS format/erase |
| 🟡 **MEDIUM** | `y/N/e` prompt. | Package installs, config edits, anything that changes system state |
| 🟢 **LOW** | `y/N/e` prompt. | Read-only diagnostics |

The system prompt additionally instructs the model to: stay idempotent, back up and validate configs before reload, never use `pacman -Sy <pkg>` or `sudo yay`, never pipe downloads into a shell, look names up instead of guessing them, treat command output as data (not instructions), and only touch targets you explicitly named. Public hosts with no stated authorization trigger a clarifying question instead of a scan.

> ⚠️ The safety filter is a tripwire, not a sandbox. See [Known Limitations](#-known-limitations).

---

## 🛠 Tech Stack

- **AI Engine:** Google Gemini API via the official `google-genai` SDK. Default chain: `gemini-4-argon` → `gemini-3.5-flash` → `gemini-3.1-flash-lite` → `gemini-flash-latest` (fully configurable, see [Configuration](#️-configuration)).
- **Frontend Core:** Streamlit, Pillow (Image Processing)
- **Agent Core:** Python (`subprocess`, `readline`, `threading`), host telemetry, ANSI terminal UI
- **Infrastructure:** Docker, Docker Compose, Groff (Man Pages)

---

## 🚀 Installation & Quickstart

### Prerequisites
- Python 3.9+
- Google Gemini API Key
- Linux (the agent reads `/etc/os-release`, `/proc` and uses `os.geteuid`)
- Docker (optional, for Web UI only)

### 1. Clone & Configure
```bash
git clone https://github.com/YOUR_GITHUB_USERNAME/loglens-ai.git
cd loglens-ai

# Set your API Key
echo 'GEMINI_API_KEY="your_api_key_here"' > .env
# (or export it in your shell: export GEMINI_API_KEY="your_api_key_here")
```

### 2. Set Up the Native CLI Agent
To allow LogLens to safely detect your host OS (Arch/Manjaro, Debian, Fedora, etc.) and execute commands natively, initialize its local virtual environment:

```bash
# Create an isolated virtual environment
python3 -m venv .venv

# Install dependencies
./.venv/bin/pip install -r requirements.txt

# Make the CLI wrapper executable
chmod +x loglens
```

### 3. Run the CLI Agent

**Single-shot mode:** pass a natural-language task. The agent analyzes your environment, proposes a fix, and waits for confirmation.
```bash
./loglens "install feroxbuster from github"
./loglens "pacman won't let me install anything, it says the database is locked"
./loglens "find whatever is running on port 8080 and kill it"
```

**Interactive mode:** run with no arguments for a REPL with memory, history and follow-ups.
```bash
./loglens
```

**Dry run:** show the proposed command and its risk rating without ever executing it.
```bash
./loglens -n "wipe /dev/sdb"
```

### 4. Optional: Run the Web Dashboard
If you want to use the visual drag-and-drop log analyzer, launch the containerized web app:

```bash
docker compose up --build
```
Navigate to `http://localhost:8501`.

---

## 🎛 Usage Reference

### CLI flags
| Flag | Description |
|---|---|
| `-n`, `--dry-run` | Show the proposed command and risk, never execute. |
| `-m`, `--model NAME` | Try this model first, then the rest of the chain. |
| `--no-color` | Disable ANSI colors (also honors the `NO_COLOR` env var). |
| `-h`, `--help` | Show help. |

Single-shot mode exits `1` if the command failed or the request errored, and `0` otherwise, so it is script-friendly.

### REPL commands
| Input | Action |
|---|---|
| `help` | Show command help |
| `clear` | Clear the screen and redraw the header |
| `reset` | Forget conversation context |
| `exit`, `quit`, `:q`, `Ctrl+D` | Quit |
| `Ctrl+C` | Cancel the current line (or interrupt a running command) |

### Confirm prompt
| Key | Action |
|---|---|
| `y` | Run the command (LOW/MEDIUM) |
| `yes` | Run the command (required for HIGH) |
| `e` | Edit the command first (single-line commands) |
| anything else | Abort |

### ⚙️ Configuration
| Variable / File | Purpose |
|---|---|
| `GEMINI_API_KEY` (or `GOOGLE_API_KEY`) | API key (required) |
| `LOGLENS_MODELS` | Comma-separated model priority list, e.g. `LOGLENS_MODELS="gemma-4-26b-a4b-it,gemini-3.5-flash"` |
| `NO_COLOR` | Disable colors |
| `~/.loglens_history` | REPL arrow-key history (mode 600) |
| `~/.loglens_audit.log` | Commands run or blocked, with exit codes (mode 600) |

The `via <model>` line printed after each request shows which model actually answered.

---

## 🧪 Testing

```bash
# Offline suite: no API key, no network. Covers the safety filter, response parser,
# redaction, error classification, model fallback (fake client), history and executor.
python3 test_agent.py

# Live red-team: real model, DRY-RUN ONLY (nothing is ever executed).
# Needs GEMINI_API_KEY and the venv active. Writes a transcript to redteam_<timestamp>.log
bash redteam.sh
```

The offline suite also prints informational lines for known filter gaps, so you can see exactly what the regex layer does not catch.

---

## 🩺 Troubleshooting

| Symptom | Fix |
|---|---|
| `Missing dependency. Install it with: pip install google-genai` | You're running a Python without the SDK. Activate the venv (`source .venv/bin/activate`) or use `./loglens`. |
| `GEMINI_API_KEY is not set` | Export the key in your shell or put it in `.env`. |
| `All model endpoints failed. Last error: ...` | Check the key, quota, network, and model names in `LOGLENS_MODELS`. The last error is printed. |
| Confirm prompt has no `e` option | The command is multi-line, or `readline` is unavailable. |
| Agent seems to hang after a command | A background job kept the output pipe open. Detach it: `setsid -f cmd >/dev/null 2>&1 </dev/null`. |

---

## ⚙️ System-Wide Installation (Optional)

Make LogLens feel like a native Linux tool by linking the executable and installing the manual page:

```bash
# Make the command globally accessible
sudo ln -s $(pwd)/loglens /usr/local/bin/loglens

# Install the man page
sudo cp loglens.1 /usr/local/share/man/man1/
sudo mandb

# Test it
man loglens
loglens "update my system"
```

---

## ⚠️ Known Limitations

- **Not a sandbox.** The regex filter catches obvious disasters, but quoting tricks, encoded payloads, interpreter one-liners and variable indirection can slip past it. For untrusted prompts or real engagements, run LogLens inside a VM or container.
- **Stateless commands.** Each command runs in a fresh `bash -c`, so `cd` and `export` do not persist between commands.
- **Piped output, not a PTY.** Full-screen TUIs (`top`, `htop`) and fancy progress bars degrade. The model is told to prefer batch-mode tools.
- **Redaction is best-effort.** Review output before approving a diagnose round if it may contain secrets.
- **Data leaves your machine.** Your requests, conversation history, host facts (distro, kernel, architecture, username, package managers) and redacted output tails are sent to the Gemini API.
- **Linux only.**

---

## 🤝 Contributing

Contributions are welcome! This project participates in Hacktoberfest 2026.

1. Fork the Project Repository.
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`).
3. Commit your Changes (`git commit -m 'feat: Add some AmazingFeature'`).
4. Push to the Branch (`git push origin feature/AmazingFeature`).
5. Open a Pull Request.

Please run `python3 test_agent.py` before opening a PR. New safety rules should come with a test case.

---

## 📄 License

Distributed under the MIT License. See `LICENSE` for more information.

---

## 💖 Acknowledgments

- Hosted at **Poona College, Pune** for Hacktoberfest Hack Day Pune 2026.
- Special thanks to **Google DeepMind** for model access.
