# 🛠️ LogLens AI — SysAdmin & Security Copilot

[![Hacktoberfest 2026](https://img.shields.io/badge/Hacktoberfest-2026-orange.svg)](https://hacktoberfest.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://www.python.org/)
[![Docker](https://img.shields.io/badge/Docker-Ready-2496ED.svg)](https://www.docker.com/)
[![Powered by Gemma 4](https://img.shields.io/badge/Google-Gemma_4-4285F4.svg)](https://ai.google.dev/)

> **LogLens AI** is an open-source, multimodal system administration assistant that analyzes terminal error traces, system logs, and dashboard screenshots to provide root-cause diagnostics and step-by-step remediation bash commands.

Built for **Hacktoberfest Hack Day Pune x Poona College** under the **Best Use of Gemma 4** track (Google DeepMind).

---

## 📌 Problem Statement

Debugging broken Linux services, systemd failures, network socket collisions, or permission denials often requires context-switching across logs, manual web searches, and visual command-line outputs. Standard text-only tools fail to inspect visual cues from terminal screenshots or monitoring dashboards, leading to longer downtime and troubleshooting fatigue.

---

## 🚀 Key Features

- 👁️ **Multimodal Diagnostics:** Upload raw terminal text logs alongside screenshots of terminal output or monitoring dashboards.
- ⚡ **Gemma 4 Powered:** Leverages Google's lightweight `gemma-4` instruction-tuned open model via the official `google-genai` SDK for low-latency analysis.
- 🔒 **Security Risk Inspection:** Evaluates system logs for open ports, permission flaws, or unhandled exceptions.
- 📦 **Container First:** Fully dockerized with `docker-compose` for reproducible deployments across any Linux environment.
- 🖥️ **Interactive Web Dashboard:** Clean, responsive UI powered by Streamlit for instant drag-and-drop log auditing.

---

## 🏗️ Architecture Overview

```
 ┌───────────────────────────────────────────────────────────────────┐
 │                        USER INTERFACE                             │
 │                    Streamlit Web App (:8501)                       │
 └─────────────────────────────────┬─────────────────────────────────┘
                                   │
                    Log Text & Terminal Screenshots
                                   │
                                   ▼
 ┌───────────────────────────────────────────────────────────────────┐
 │                       FASTAPI / PYTHON CORE                       │
 │        Payload Assembly & Prompt Formatting (google-genai)        │
 └─────────────────────────────────┬─────────────────────────────────┘
                                   │
                       Multimodal REST Request
                                   │
                                   ▼
 ┌───────────────────────────────────────────────────────────────────┐
 │                      GOOGLE GEMINI API                            │
 │                        (Gemma 4 Engine)                           │
 └─────────────────────────────────┬─────────────────────────────────┘
                                   │
                      Structured Audit & Bash Fix
                                   │
                                   ▼
 ┌───────────────────────────────────────────────────────────────────┐
 │                     REMEDIATION REPORT                            │
 │     • Root Cause Analysis                                         │
 │     • Security Risk Assessment                                    │
 │     • Step-by-Step Executable Bash Commands                      │
 └───────────────────────────────────────────────────────────────────┘
```

---

## 🛠️ Tech Stack

- **AI Engine:** Google Gemma 4 (`gemma-4-26b-a4b-it`) via Gemini API
- **SDK:** `google-genai`
- **Frontend / Dashboard:** Streamlit
- **Image Processing:** Pillow (`PIL`)
- **Containerization:** Docker & Docker Compose
- **Platform OS:** Linux (Tested on Manjaro / Arch Linux & Ubuntu)

---

## 🚀 Quickstart Guide

### Prerequisites

- [Docker](https://docs.docker.com/get-docker/) & [Docker Compose](https://docs.docker.com/compose/) installed
- A [Google Gemini API Key](https://aistudio.google.com/)

---

### Option A: Docker Compose Deployment (Recommended)

1. **Clone the Repository:**
   ```bash
   git clone https://github.com/YOUR_GITHUB_USERNAME/loglens-ai.git
   cd loglens-ai
   ```

2. **Configure Environment Variables:**
   Create a `.env` file in the root directory:
   ```bash
   echo "GEMINI_API_KEY=your_gemini_api_key_here" > .env
   ```

3. **Build & Run with Docker Compose:**
   ```bash
   docker compose up --build
   ```

4. **Access the Application:**
   Open your browser and navigate to `http://localhost:8501`.

---

### Option B: Local Python Setup

1. **Clone & Navigate:**
   ```bash
   git clone https://github.com/YOUR_GITHUB_USERNAME/loglens-ai.git
   cd loglens-ai
   ```

2. **Create a Virtual Environment:**
   ```bash
   python -m venv .venv
   source .venv/bin/activate
   ```

3. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Export API Key & Run App:**
   ```bash
   export GEMINI_API_KEY="your_gemini_api_key_here"
   streamlit run app.py
   ```

---

## 🤝 Contributing

Contributions are welcome! This project participates in **Hacktoberfest 2026**.

1. Fork the Project Repository.
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`).
3. Commit your Changes (`git commit -m 'feat: Add some AmazingFeature'`).
4. Push to the Branch (`git push origin feature/AmazingFeature`).
5. Open a Pull Request with proper documentation.

---

## 📄 License

Distributed under the **MIT License**. See `LICENSE` for more information.

---

## 💖 Acknowledgments

- Hosted at **Poona College, Pune** for **Hacktoberfest Hack Day Pune 2026**.
- Special thanks to **Google DeepMind** for model access via Gemini API and **DigitalOcean / DEV** for community support.