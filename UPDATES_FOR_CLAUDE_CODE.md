# Course Materials Update Task
**For:** Claude Code / Cowork session  
**Prepared by:** Cowork, May 2026  
**Repository:** https://github.com/KarolynW/Code-for-MRS  
**Read CLAUDE.md before starting.**

---

## Summary of all changes required

Three categories of update:
1. Model names — OpenAI GPT-4.x → GPT-5.x equivalents
2. Model names — Claude Opus → Claude Sonnet
3. Codex description — was incorrectly described as a web app; it is a **Windows desktop app** (available from the Microsoft Store), also available on macOS and as a CLI

---

## 1. Python scripts

### 7_claude_api_demo.py

**Change 1 — model name:**
```
OLD:  model="claude-opus-4-7",          # Use a recent Claude model
NEW:  model="claude-sonnet-4-6",        # Use a recent Claude model
```

No other changes needed in this file.

---

### 8_open_text_categoriser.py

**Change 1 — OpenAI model name:**
```
OLD:  model="gpt-4.1-mini",      # Cost-effective model for classification tasks
NEW:  model="gpt-5.4-mini",      # Cost-effective model for classification tasks
```

**Change 2 — Claude model stays as-is:**
```
model="claude-haiku-4-5"   ← leave this unchanged; Haiku 4.5 is correct
```

No other changes needed in this file.

---

## 2. CLAUDE.md

**Change 1 — Claude model in docstring example (around line 94):**
```
OLD:  model="claude-haiku-4-5",             # The model to use — Haiku is fast and cheap
NEW:  (no change — Haiku stays)
```

**Change 2 — Claude quick reference block (around line 405):**
```
OLD:  model="claude-haiku-4-5",             # Fast, cost-effective — good for classification
      # model="claude-opus-4-7",           # More powerful — good for complex analysis
NEW:  model="claude-haiku-4-5",             # Fast, cost-effective — good for classification
      # model="claude-sonnet-4-6",         # More powerful — good for complex analysis
```

**Change 3 — OpenAI quick reference block (around line 429):**
```
OLD:  model="gpt-4.1-mini",           # Cost-effective — good for classification
      # model="gpt-4.1",              # More powerful — good for complex analysis
NEW:  model="gpt-5.4-mini",           # Cost-effective — good for classification
      # model="gpt-5.4",              # More powerful — good for complex analysis
```

---

## 3. USING_AI_CODING_AGENTS.md

This file has several places that incorrectly describe Codex as a web/terminal agent.
It also needs the Claude Opus → Sonnet model update in the comparison table.

### 3a — Summary table at the top of the file

```
OLD:  | **OpenAI Codex** | OpenAI | An AI coding agent available at chatgpt.com/codex — fast and great for quick generation, runs in a cloud sandbox | Generating scripts, exploring alternatives, comparing with Claude Code output |

NEW:  | **OpenAI Codex** | OpenAI | An AI coding agent available as a **Windows desktop app** (Microsoft Store) and macOS app — fast and great for quick generation | Generating scripts, exploring alternatives, comparing with Claude Code output |
```

### 3b — Part 2: OpenAI Codex — "What it is" section

```
OLD:
OpenAI Codex is OpenAI's AI coding agent, powered by **GPT-5.3-Codex** — a model specifically optimised for agentic coding tasks. It is lightweight, fast, and excellent for quick script generation and exploration.

**In this course we use Codex via the web app at [chatgpt.com/codex](https://chatgpt.com/codex)** — log in with your ChatGPT account, describe your task, and Codex writes and runs code in a cloud sandbox. No installation required.

NEW:
OpenAI Codex is OpenAI's AI coding agent, powered by **GPT-5.3-Codex** — a model specifically optimised for agentic coding tasks. It is lightweight, fast, and excellent for quick script generation and exploration.

**In this course we use the Codex Windows desktop app**, available from the Microsoft Store. Sign in with your ChatGPT account, open your project folder, and Codex writes and runs code in a sandboxed environment on your machine. Also available as a macOS app, CLI, and IDE extension.
```

### 3c — Access requirements table

```
OLD:  | **ChatGPT account mode** | A Free, Go, Plus, or Pro ChatGPT account — usage draws from your plan's limits |
NEW:  | **ChatGPT account mode** | A Free, Plus, or Pro ChatGPT account — sign in to the desktop app or CLI with your ChatGPT login |
```

### 3d — Installation section

Replace the entire Installation section:

```
OLD:
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

NEW:
### Getting started (2026)

**Recommended for this course — Windows desktop app:**

1. Open the **Microsoft Store** on Windows and search for **Codex**
2. Install the app and open it
3. Sign in with your ChatGPT account (Plus, Pro, Business, Enterprise, or Edu plan)
4. Point Codex at your project folder — it reads your files and is ready to go

**Also available on macOS:**
Download the macOS app from [openai.com/codex](https://openai.com/codex/).

**CLI method (optional — for those who prefer the terminal):**
```bash
npm install -g @openai/codex
codex
```
See full CLI docs at [developers.openai.com/codex/cli](https://developers.openai.com/codex/cli).

### First run
```

### 3e — Comparison table (How Codex differs from Claude Code)

```
OLD:  | Model | Claude Sonnet / Opus | GPT-5.3-Codex |
NEW:  | Model | Claude Sonnet | GPT-5.3-Codex |
```

Also update the Auth row if it mentions a web app:
```
OLD:  | Auth | Anthropic account or API key | ChatGPT account or OpenAI API key |
NEW:  (no change needed)
```

### 3f — Common terminal commands section at the bottom

```
OLD:
# ── OPENAI CODEX (web app — recommended) ──────────────
# Open chatgpt.com/codex in your browser → log in → describe your task

# ── OPENAI CODEX (CLI — optional) ────────────────────
codex                     # Start Codex in current folder

NEW:
# ── OPENAI CODEX (desktop app — recommended) ──────────
# Open the Codex Windows app (Microsoft Store) → sign in → open your project folder

# ── OPENAI CODEX (CLI — optional) ────────────────────
codex                     # Start Codex in current folder
```

---

## 4. Course_Agenda_Updated.docx

Open and edit this Word document. Find and replace:

```
OLD:  What OpenAI Codex is and how to use it via the web app (chatgpt.com/codex)
NEW:  What OpenAI Codex is and how to use it via the Windows desktop app (Microsoft Store)
```

Use the docx skill to unpack, edit the XML, and repack. The text is in `word/document.xml`.

---

## 5. Course_Delivery_Checklist.docx

This document was generated by a JavaScript script. The simplest approach is to edit the
source script (`make_checklist.js` in the outputs folder if available) and regenerate,
OR unpack and edit the XML directly.

Find and replace these strings throughout the document:

```
OLD:  Open a browser tab to chatgpt.com/codex and log in with your ChatGPT account
NEW:  Open the Codex Windows desktop app (installed from the Microsoft Store)

OLD:  Confirm you can see the Codex interface and it is ready to accept a task
NEW:  Confirm Codex opens correctly and shows your project files

OLD:  chatgpt.com/codex — ChatGPT Codex (logged in and ready)
NEW:  Codex Windows app (open and signed in via Microsoft Store install)

OLD:  chatgpt.com/codex in your browser (already logged in)
(any other references to chatgpt.com/codex as a browser/web destination)
NEW:  the Codex Windows desktop app
```

Also find the Demo 2 section and update:
```
OLD:  chatgpt.com/codex: switch to the browser tab, give it the same task
NEW:  Codex desktop app: switch to the Codex app window, give it the same task
```

---

## 6. MRS_Advanced_AI_Course_Deck_WITH_NOTES.pptx — Speaker notes

Two slides need their speaker notes updated. Use the pptx skill (unpack → edit notesSlide XML → pack).

### Slide 23 — notesSlide23.xml

The notes currently say "go to chatgpt.com/codex — you log in with your ChatGPT account."

Replace the Codex paragraph with:
```
CHATGPT CODEX (WINDOWS DESKTOP APP): 'Codex is a desktop app available from the Microsoft Store — search for Codex, install it, and sign in with your ChatGPT account. It runs in a sandboxed environment on your own machine. Also available on macOS and as a CLI.'
```

### Slide 27 — notesSlide27.xml

The notes currently reference switching to "chatgpt.com/codex browser tab."

Replace with:
```
6. Switch to the Codex desktop app window. Give it the same task — compare the two approaches side by side.
```

---

## Verification checklist

After making all changes, run these checks:

```bash
# No old GPT-4 model references should remain in active scripts/docs
grep -rni "gpt-4\." . --include="*.py" --include="*.md"
# Expected: nothing (or only legacy script references in 4_azure.py / 5_check_ft.py)

# No opus references should remain in active scripts/docs
grep -rni "claude-opus-4-7\|claude-opus-4-5" . --include="*.py" --include="*.md"
# Expected: nothing

# No web/browser Codex references should remain
grep -rni "chatgpt.com/codex\|web app.*codex\|codex.*web app" . --include="*.py" --include="*.md"
# Expected: nothing (URL may appear only as an informational link, not as the primary access route)

# Confirm correct new model names are present
grep -rni "claude-sonnet-4-6\|gpt-5\.4-mini\|gpt-5\.4" . --include="*.py" --include="*.md"
# Expected: hits in 7_claude_api_demo.py, 8_open_text_categoriser.py, CLAUDE.md, USING_AI_CODING_AGENTS.md
```

---

## Model reference summary (for any new scripts you write)

| Use case | Provider | Model string |
|---|---|---|
| Fast, cheap classification | Claude | `claude-haiku-4-5` |
| General purpose, balanced | Claude | `claude-sonnet-4-6` |
| Complex reasoning / analysis | Claude | `claude-opus-4-7` |
| Fast, cheap classification | OpenAI | `gpt-5.4-mini` |
| General purpose, balanced | OpenAI | `gpt-5.4` |
| Most capable | OpenAI | `gpt-5.5` |

---

*Task prepared by Cowork session, May 2026.*  
*All changes verified against Anthropic and OpenAI official documentation.*
