# 🛠 LogLens AI — SysAdmin & Security Copilot

[![Hacktoberfest 2026](https://img.shields.io/badge/Hacktoberfest-2026-orange.svg)](https://hacktoberfest.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://www.python.org/)
[![Powered by Gemini](https://img.shields.io/badge/Google-Gemini_API-4285F4.svg)](https://ai.google.dev/)

> **LogLens AI** is a dual-mode, autonomous system administration assistant. It features an **interactive web dashboard** for multimodal log analysis and a **native terminal copilot** that scans host telemetry to generate and execute OS-tailored remediation commands directly on your machine.

Built for **Hacktoberfest Hack Day Pune x Poona College** under the **Best Use of Gemma 4** and **Best Open-Source AI Project** tracks.
<img width="950" height="580" alt="demo" src="https://github.com/user-attachments/assets/e07b3438-1ace-4c3f-b665-30e89fe31a3d" />
---

## 📌 Problem Statement

Debugging broken Linux services, network socket collisions, or missing dependencies usually forces developers into a loop of copying errors, searching the web, and pasting commands. Standard AI wrappers lack context about your specific hardware, OS distribution, and package managers, often hallucinating commands that won't work on your machine (e.g., suggesting `apt` on an Arch system). 

LogLens bridges this gap by acting as an active, environment-aware execution engine.

---

## 🚀 Key Features

- 💻 **Autonomous Execution Engine:** Resolves issues by writing and executing native bash commands directly on your host system with a human-in-the-loop safeguard (`[y/N]` confirmation).
- 🔍 **Context-Aware Telemetry:** Automatically scans `/etc/os-release`, hardware architecture, and installed package managers to tailor commands specifically for your distro (e.g., automatically prioritizing `yay`/AUR over `pacman` for third-party tools).
- 👁 **Multimodal Web Dashboard:** A containerized Streamlit UI allowing drag-and-drop terminal screenshots and raw text logs for visual root-cause diagnostics.
- ⚡ **Resilient Model Routing:** Powered by Google's `google-genai` SDK, featuring automatic fallback logic (Gemma 4 -> Gemini 3.5 Flash -> Gemini 3.1 Flash-Lite) to guarantee uptime during rate limits.
- 📖 **Native Linux Integration:** Ships with a symlink-ready executable and a native `groff` manual page (`man loglens`).

---

## 🏗 Architecture Overview

```text
 ┌───────────────────────────────────────────────────────────────┐
 │                       DUAL INTERFACES                         │
 └──────┬─────────────────────────────────────────────────┬──────┘
        │                                                 │
        ▼                                                 ▼
 ┌──────────────┐                                  ┌─────────────┐
 │ Web UI (GUI) │                                  │ CLI (Agent) │
 │  Streamlit   │                                  │ ./loglens   │
 └──────┬───────┘                                  └──────┬──────┘
        │ (Dockerized)                                    │ (Native Host)
        │                                                 ▼
        │                                          ┌─────────────┐
        │                                          │ OS Scanner  │
        │                                          │ (/etc/os..) │
        ▼                                          └──────┬──────┘
 ┌────────────────────────────────────────────────────────┼──────┐
 │                     GOOGLE GEMINI API                  │      │
 │       (Gemma-4-26b / Gemini 3.5 Flash Fallbacks)       │      │
 └────────────────────────────────┬───────────────────────┴──────┘
                                  │
                                  ▼
 ┌───────────────────────────────────────────────────────────────┐
 │                       REMEDIATION                             │
 │  • Multimodal Diagnostic Report (Web Dashboard)               │
 │  • Executable Bash Commands & Compilation Chains (Terminal)   │
 └───────────────────────────────────────────────────────────────┘
```

---

## 🛠 Tech Stack

- **AI Engine:** Google Gemini API (`gemma-4-26b-a4b-it`, `gemini-3.5-flash`)
- **SDK:** Official `google-genai`
- **Frontend Core:** Streamlit, Pillow (Image Processing)
- **Agent Core:** Python `subprocess`, OS Telemetry, ANSI UI styling
- **Infrastructure:** Docker, Docker Compose, Groff (Man Pages)

---

## 🚀 Installation & Quickstart

### Prerequisites
- Python 3.11+
- [Google Gemini API Key](https://aistudio.google.com/)
- Docker (optional, for Web UI only)

### 1. Clone & Configure
```bash
git clone https://github.com/YOUR_GITHUB_USERNAME/loglens-ai.git
cd loglens-ai

# Set your API Key
echo 'GEMINI_API_KEY="your_api_key_here"' > .env
```

### 2. Set Up the Native CLI Agent
To allow LogLens to safely detect your host OS (Arch/Manjaro, Debian, etc.) and execute commands natively, initialize its local virtual environment:

```bash
# Create an isolated virtual environment
python3 -m venv .venv

# Install dependencies
./.venv/bin/pip install -r requirements.txt

# Make the CLI wrapper executable
chmod +x loglens
```

### 3. Run the CLI Agent
Pass natural language commands directly to the agent. It will analyze your environment, generate the fix, and wait for confirmation before executing.
```bash
./loglens "install feroxbuster from github"
./loglens "pacman won't let me install anything, it says the database is locked"
./loglens "find whatever is running on port 8080 and kill it"
```

### 4. Optional: Run the Web Dashboard
If you want to use the visual drag-and-drop log analyzer, launch the containerized web app:
```bash
docker compose up --build
```
Navigate to `http://localhost:8501`.

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

## 🤝 Contributing
Contributions are welcome! This project participates in **Hacktoberfest 2026**.

1. Fork the Project Repository.
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`).
3. Commit your Changes (`git commit -m 'feat: Add some AmazingFeature'`).
4. Push to the Branch (`git push origin feature/AmazingFeature`).
5. Open a Pull Request.

---

## 📄 License
Distributed under the **MIT License**. See `LICENSE` for more information.

---

## 💖 Acknowledgments
- Hosted at **Poona College, Pune** for **Hacktoberfest Hack Day Pune 2026**.
- Special thanks to **Google DeepMind** for model access.
