# Code-for-MRS — MRS Advanced AI Course

This repository contains the Python scripts used in the **MRS Advanced AI Course** — a
professional training programme for market researchers learning to use Python and AI APIs
for personal automation.

Every script is a learning artefact.  The code is heavily commented so you can read it
top-to-bottom and understand every decision.  Run the scripts, read the comments, and
adapt them to your own projects.

**Instructor:** Karolyn Webb

---

## Prerequisites

1. Install **Python 3.9 or later** from [python.org](https://www.python.org/downloads/).
2. Install **Visual Studio Code** and the official **Python extension**.
3. (Recommended) Create a virtual environment so packages installed here do not affect
   other projects on your machine.

Open a terminal in VS Code (`` Ctrl+` `` or `` Cmd+` `` on macOS) and run these commands
the first time you set up the repository:

```bash
python -m venv .venv

# Activate the virtual environment:
# Windows PowerShell:
.venv\Scripts\Activate.ps1
# macOS / Linux:
source .venv/bin/activate

# Install all required packages:
pip install -r requirements.txt
```

---

## Setting up your API keys

Scripts 2, 3, 6, 7, 8, and 9 need an API key to call an AI service.  Keys are stored in
a `.env` file in the repository folder — **never** pasted into the scripts themselves.

```bash
# Copy the template:
cp .env.example .env

# Open .env and replace the placeholder values with your real keys.
```

During the course, keys will be provided for you.  To create your own:

- **OpenAI** — [platform.openai.com/api-keys](https://platform.openai.com/api-keys)
- **Anthropic (Claude)** — [console.anthropic.com](https://console.anthropic.com)

---

## Running scripts in VS Code

1. Choose **File → Open Folder…** and select the `Code-for-MRS` folder.
2. In the Explorer sidebar, click the script you want to run.
3. Check that the Python interpreter in the blue status bar points to your virtual
   environment (`.venv`).
4. Click the green **Run Python File** button, or press `Ctrl+F5` (`Cmd+F5` on macOS).
5. Watch the **Python Terminal** panel for output and any prompts.

---

## The scripts

### `1_http_api_demo.py` — Public weather API (no key needed)

A gentle introduction to APIs.  Calls the free Open-Meteo weather service, shows the
raw JSON response, and extracts the current temperature for London.  No API key or
account required — a great first run to confirm your Python environment is working.

### `2_openai_basic_call.py` — Your first OpenAI call

The smallest possible OpenAI example: one system prompt, one question, one answer.
Compare this script with `7_claude_api_demo.py` to see how the OpenAI and Anthropic
APIs follow the same pattern.

### `3_openai_with_system_prompt.py` — Recipe generator with user input

Collects ingredients and cuisine style from the terminal, builds a dynamic prompt, and
returns a full recipe.  Demonstrates how to collect input, customise instructions, and
use parameters like `temperature` to control creativity.

### `6_qualitative_theming.py` — Thematic analysis of survey verbatims

Loads open-ended survey responses from an Excel file, sends each comment to OpenAI,
and receives structured JSON themes in return.  Writes the results to a new Excel file
with two extra columns: the raw JSON and a readable flat version.  Shows a complete
"load → process → export" workflow.

- **Input:** `6_Example_Qualitative.xlsx`
- **Output:** `6_Example_Qualitative_Themed.xlsx`

### `7_claude_api_demo.py` — Your first Claude API call

The Claude equivalent of Script 2, using the same four-step structure so the two APIs
are easy to compare.  The example task is a mini survey analysis: identify themes,
summarise sentiment, and give one recommendation.

### `8_open_text_categoriser.py` — Automated categorisation and sentiment scoring

A practical automation tool.  Takes a list of open-ended survey responses and
automatically assigns each one a category (e.g. *Product Quality*, *Pricing & Value*)
and a sentiment (Positive / Neutral / Negative).  Supports both OpenAI and Claude —
change one variable at the top to switch provider.  Exports results to Excel.

- **Output:** `8_categorised_responses.xlsx`
- **Depends on:** OpenAI key or Anthropic key (set `PROVIDER` at the top of the script)

### `9_report_generator.py` — Executive summary report generator

Loads the Excel output from Script 8, summarises the category and sentiment data, and
asks Claude to write a polished executive summary report.  Saves the report as a
plain-text file ready to review, edit, and share.

This script demonstrates how the output of one script can feed directly into the next,
creating an automated end-to-end research workflow.

- **Input:** `8_categorised_responses.xlsx` (run Script 8 first)
- **Output:** `9_executive_summary.txt`
- **Depends on:** Anthropic key

---

## Legacy scripts (kept for reference)

These two scripts were written for an earlier version of the course that used Azure AI
Foundry.  They are not part of the current course flow but are kept in the repository
for reference.

### `4_azure_agent.py` — Azure AI Agents example

Connects to an Azure AI Project and sends a piece of customer feedback to a pre-built
agent.  Requires Azure credentials configured in `.env`.

### `5_check_ft.py` — Fine-tuning JSONL validator

Checks a `.jsonl` dataset file against Azure's fine-tuning requirements (UTF-8 BOM
encoding, valid JSON structure, required message roles).  Run against
`5_fine_tuning.jsonl` or your own dataset.

---

## Sample data files

| File | Used by | Description |
|---|---|---|
| `6_Example_Qualitative.xlsx` | Script 6 | 10 sample survey responses with open-text comments |
| `6_Example_Qualitative_Themed.xlsx` | — | Pre-generated output for reference |
| `5_fine_tuning.jsonl` | Script 5 | 50 market research Q&A training examples |
| `5_validation_data.jsonl` | Script 5 | 30 validation examples |

---

## Typical workflow

For the main course exercises, run the scripts in this order:

```
1_http_api_demo.py           ← confirm Python + internet are working
2_openai_basic_call.py       ← first OpenAI call
3_openai_with_system_prompt.py ← collect input, build a prompt
6_qualitative_theming.py     ← analyse Excel data with OpenAI
7_claude_api_demo.py         ← same workflow using Claude
8_open_text_categoriser.py   ← categorise + score survey responses
9_report_generator.py        ← generate an executive summary report
```

---

## Troubleshooting

| Problem | What to check |
|---|---|
| `ModuleNotFoundError` | Did you activate the virtual environment before running? Check the interpreter in VS Code's status bar. |
| `401 AuthenticationError` | Your API key is wrong or missing.  Open `.env` and verify the key is correct. |
| `429 RateLimitError` | You have sent too many requests.  Wait 30–60 seconds and try again. |
| Timeout or connection error | Check your internet connection.  Corporate networks sometimes block API calls — try a personal hotspot. |
| Excel file not found | Make sure the data file is in the same folder as the script you are running. |

If you get stuck, read the docstring at the top of the relevant script — it includes
setup steps and common solutions.

---

## Project structure

```
Code-for-MRS/
│
├── 1_http_api_demo.py               ← unauthenticated HTTP API, requests library
├── 2_openai_basic_call.py           ← first OpenAI API call
├── 3_openai_with_system_prompt.py   ← system prompts, user input, parameters
├── 4_azure_agent.py                 ← Azure AI Foundry (legacy — see above)
├── 5_check_ft.py                    ← fine-tuning data validator (legacy)
├── 5_fine_tuning.jsonl              ← 50 example fine-tuning records
├── 5_validation_data.jsonl          ← 30 validation records
├── 6_qualitative_theming.py         ← theme extraction from survey data
├── 6_Example_Qualitative.xlsx       ← sample survey responses
├── 6_Example_Qualitative_Themed.xlsx← pre-generated themed output
├── 7_claude_api_demo.py             ← Claude equivalent of Script 2
├── 8_open_text_categoriser.py       ← categorisation + sentiment, OpenAI or Claude
├── 9_report_generator.py            ← executive summary report generator
│
├── requirements.txt                 ← all Python dependencies
├── .env.example                     ← API key template (copy to .env)
├── CLAUDE.md                        ← instructions for Claude Code
└── USING_AI_CODING_AGENTS.md        ← guide to using Claude Code and Codex
```
