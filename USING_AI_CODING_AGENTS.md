# Using AI Coding Agents to Build and Modify Scripts

A companion guide for the MRS Advanced AI Course  
*Updated May 2026 — information verified against official documentation*

---

## The three agents we demonstrate in this course

| Tool | Made by | What it does | How we use it in the session |
|------|---------|-------------|------------------------------|
| **Claude Code** | Anthropic | An AI coding agent built into the Claude desktop app — reads your project files and writes, improves, and explains code through conversation | Building scripts, improving documentation, running the Tasks in CLAUDE.md |
| **OpenAI Codex** | OpenAI | An AI coding agent available at chatgpt.com/codex — fast and great for quick generation, runs in a cloud sandbox | Generating scripts, exploring alternatives, comparing with Claude Code output |
| **Cowork** | Anthropic | Claude's desktop mode — automates file and task management through conversation, no terminal needed | Demonstrated live: how the course materials themselves were built |

These three agents represent different entry points into AI-assisted coding. You don't need all three — pick the one that fits how you work.

> **GitHub Copilot** is also used during the session specifically for **code review** inside VS Code, as part of the GitHub demonstration. It is not one of the primary coding agents.

---

## Part 1: Claude Code

### What it is

Claude Code is Anthropic's AI coding agent, built into the **Claude desktop app**. Unlike a chatbot, it reads every file in your project folder, understands how scripts relate to each other, and can make changes across multiple files in a single conversation. You talk to it in plain English; it writes, edits, and explains the code.

**In this course we use Claude Code via the Claude desktop app** — open the app, select Claude Code mode, and point it at your project folder. No terminal needed to get started.

### Access requirements

Claude Code requires a **paid Anthropic plan** — the free Claude.ai account does not include it.

| Access route | What you need |
|---|---|
| **Claude Pro** | $20/month subscription at claude.ai |
| **Claude Max** | $100 or $200/month (higher usage limits) |
| **API credits** | Create a free account at console.anthropic.com — new accounts receive ~$5 in free credits, no credit card required |
| **Team / Enterprise** | Ask your organisation's admin |

> **For this course:** API keys and credits will be provided on the day.

### Getting started (2026)

**Recommended for this course — via the desktop app:**

1. Download the Claude desktop app from [claude.ai/download](https://claude.ai/download) and install it
2. Sign in with your Anthropic account (Pro or Max plan required for Claude Code)
3. Open the app and select **Claude Code** from the mode switcher
4. Point it at your project folder — it will read your files and CLAUDE.md automatically

**For those who prefer the terminal — CLI method (also fully supported):**

*Windows* — PowerShell:
```powershell
irm https://claude.ai/install.ps1 | iex
```
Then run `claude` in PowerShell, CMD, or Git Bash from your project folder.

*macOS*
```bash
brew install claude-code
```

*Legacy npm method (still works)*
```bash
npm install -g @anthropic-ai/claude-code
```

### The CLAUDE.md file

When Claude Code opens a project, the first thing it reads is `CLAUDE.md` — a plain text
file in your project folder that tells the agent:
- What the project is and who it's for
- What coding standards to follow
- What to improve and what not to touch
- Ready-to-run improvement tasks it can carry out

The course repository already contains a `CLAUDE.md`. When you open Claude Code (desktop app or CLI) inside the project folder, it absorbs this briefing automatically before doing anything.

### What you can ask Claude Code to do

#### Creating a new script from scratch

```
I'm a market researcher. I have a CSV file called survey_data.csv with a
column called "verbatim" that contains open-ended responses.

Write me a Python script that:
1. Loads the CSV file
2. Sends each response to the Claude API and asks it to assign a theme
   (one of: Product, Support, Pricing, Usability, Other)
3. Adds the theme as a new column
4. Saves the results to a file called survey_data_themed.xlsx

Use the anthropic Python SDK. Load the API key from a .env file.
Follow the documentation standards in CLAUDE.md — heavy commenting,
section headers, a full module docstring.
```

#### Running a ready-made improvement task

```
Please carry out Task C from CLAUDE.md:
Compare 2_openai_responses_api.py and 7_claude_api_demo.py and make
them structurally parallel — same section headings, same variable names
where equivalent, same output format. Do not change the core logic.
```

#### Debugging an error

```
My script is throwing this error when I run it:

  json.decoder.JSONDecodeError: Expecting value: line 1 column 1 (char 0)

Here is the section of code that's failing: [paste the code]

What is causing this? Please fix it and explain what went wrong.
```

#### Improving documentation

```
Please review 8_open_text_categoriser.py against the documentation
standards in CLAUDE.md. Add any missing section comments, improve the
module docstring, and add inline comments on every API parameter.
Do not change any of the logic — only the comments.
```

### Tips for getting the best from Claude Code

- **Start every session by pointing it to CLAUDE.md:** *"Please read CLAUDE.md before we begin."*
- **Be specific about scope.** "Improve the script" is vague. "Add error handling for API failures — do not change any other logic" is safe and clear.
- **Ask it to explain its changes** after every edit.
- **Work on a branch**, not directly on main: *"Please create a branch called improve/documentation before making any changes."*

---

## Part 2: OpenAI Codex

### What it is

OpenAI Codex is OpenAI's AI coding agent, powered by **GPT-5.3-Codex** — a model specifically optimised for agentic coding tasks. It is lightweight, fast, and excellent for quick script generation and exploration.

**In this course we use Codex via the web app at [chatgpt.com/codex](https://chatgpt.com/codex)** — log in with your ChatGPT account, describe your task, and Codex writes and runs code in a cloud sandbox. No installation required.

### Access requirements

| Mode | What you need |
|---|---|
| **ChatGPT account mode** | A Free, Go, Plus, or Pro ChatGPT account — usage draws from your plan's limits |
| **API key mode** | An OpenAI API key — billed per token |

> **For this course:** API keys will be provided. Free ChatGPT accounts also currently receive limited Codex access.

### Installation

Codex requires **Node.js version 22 or later**.

**macOS / Linux**
```bash
npm install -g @openai/codex
```

**macOS (Homebrew)**
```bash
brew install --cask codex
```

**Windows** — WSL2 is recommended for the best experience. See [developers.openai.com/codex/windows](https://developers.openai.com/codex/windows).

### First run

```bash
codex
```

Sign in with your ChatGPT account or enter an API key. Codex reads your current folder and you're ready.

### How Codex differs from Claude Code

| | Claude Code | OpenAI Codex |
|--|-------------|--------------|
| Best for | Methodical, project-wide work; follows CLAUDE.md | Fast generation; quick exploration |
| Project awareness | Deep — reads all files and CLAUDE.md | Good — reads the current folder |
| Model | Claude Sonnet / Opus | GPT-5.3-Codex |
| Auth | Anthropic account or API key | ChatGPT account or OpenAI API key |

### Example prompts for Codex

```
Generate a Python script that calls the Claude API and summarises
a list of open-ended survey responses into five bullet points.
Use python-dotenv for the API key. Add clear comments throughout.
```

```
What's the simplest way to process 200 survey responses through the
OpenAI API without hitting the rate limit?
```

---

## Part 3: Cowork

### What it is

Cowork is Claude's desktop mode — a research preview of Claude running as a desktop
application with access to your files and a sandboxed environment for running code.

Unlike Claude Code and Codex, you don't need a terminal. You work entirely through
conversation. Cowork can read and write files, run Python scripts, create Word documents,
Excel spreadsheets, and PowerPoint presentations, all through plain English instructions.

**This course's materials were built using Cowork.** The agenda, pre-joining guide,
slide deck, and Python scripts were all produced in a Cowork session — which makes it
a live demonstration of what's possible.

### What Cowork can do for market researchers

- Read and analyse existing documents and datasets
- Write and run Python scripts without you touching the terminal
- Create formatted Word documents, slide decks, and spreadsheets
- Search the web and incorporate up-to-date information
- Chain together multiple tasks in a single conversation

### When to use Cowork vs Claude Code

| | Cowork | Claude Code |
|--|--------|-------------|
| Needs a terminal | No | No (desktop app) — optional via CLI |
| Can create Office files | Yes | No (code only) |
| Best for | Task automation, document creation | Code-heavy development |
| Entry level | Lower | Low via desktop app; higher via CLI |

### Access

Cowork is a research preview available within the Claude desktop application.
Visit [claude.ai](https://claude.ai) to download the desktop app.

---

## Part 4: GitHub and GitHub Copilot (for code review)

### Why use GitHub?

- A safe place to store your code — nothing gets lost when you close your laptop
- Version history — you can undo changes and go back to earlier versions
- Works with agents — Claude Code and Codex read your repo structure
- Easy sharing — share a link rather than emailing files

### Getting the course code onto your computer

**https://github.com/KarolynW/Code-for-MRS**

**Option A — Download as ZIP** (no account needed)
1. Click the green **Code** button → **Download ZIP**
2. Unzip to a folder on your Desktop

**Option B — Clone with Git**
```bash
git clone https://github.com/KarolynW/Code-for-MRS.git
cd Code-for-MRS
```

### GitHub Copilot for code review

Copilot lives inside VS Code and is used in this session for **reviewing** finished scripts.

**Setup:**
1. Create a free GitHub account at [github.com](https://github.com)
2. In VS Code: Extensions (Ctrl+Shift+X) → search **GitHub Copilot** → install
3. Also install **GitHub Copilot Chat**
4. Sign in with your GitHub account

**Code review prompt:**
```
Please review this script as if you were a senior Python developer
reviewing work for a junior colleague.

Focus on:
- Are there any bugs or errors in the logic?
- Is the code easy to follow for a beginner?
- Is the error handling complete?
- Is anything missing for a market researcher's needs?

Give specific, actionable feedback. Do not rewrite the whole script.
```

### Basic Git workflow

```bash
git checkout -b improve/documentation   # Create a branch before changing anything
git add 7_claude_api_demo.py            # Stage a changed file
git commit -m "docs: add section comments"  # Save a snapshot
git push                                # Upload to GitHub
git pull                                # Get latest changes
```

---

## Quick reference: which tool for which task?

| Task | Best tool |
|------|-----------|
| Write a new script following CLAUDE.md standards | Claude Code |
| Quick script generation to explore an idea | Codex |
| Create a Word doc, slide deck, or spreadsheet from conversation | Cowork |
| Improve documentation across the whole codebase | Claude Code |
| Fix a specific error | Claude Code or Codex |
| Review a finished script for quality issues | GitHub Copilot |
| Chain tasks without touching a terminal | Cowork |

---

## Common terminal commands

```bash
# ── CLAUDE CODE (desktop app — recommended) ───────────
# Open the Claude desktop app → select Claude Code mode
# → point it at your project folder

# ── CLAUDE CODE (CLI — optional) ─────────────────────
claude                    # Start Claude Code in current folder
claude doctor             # Run diagnostics

# ── OPENAI CODEX (web app — recommended) ──────────────
# Open chatgpt.com/codex in your browser → log in → describe your task

# ── OPENAI CODEX (CLI — optional) ────────────────────
codex                     # Start Codex in current folder

# ── PYTHON ───────────────────────────────────────────
pip install anthropic openai pandas openpyxl python-dotenv
pip install -r requirements.txt
python 7_claude_api_demo.py

# ── GIT ──────────────────────────────────────────────
git clone <url>
git checkout -b my-branch
git status
git add filename.py
git commit -m "docs: improve comments"
git push
git log --oneline
```

---

*This guide was produced for the MRS Advanced AI Course.*  
*Information verified May 2026 against official Anthropic, OpenAI, and GitHub documentation.*  
*Tutor: Karolyn Webb | Repository: https://github.com/KarolynW/Code-for-MRS*
git log --oneline
```

---

*This guide was produced for the MRS Advanced AI Course.*  
*Information verified May 2026 against official Anthropic, OpenAI, and GitHub documentation.*  
*Tutor: Karolyn Webb | Repository: https://github.com/KarolynW/Code-for-MRS*
