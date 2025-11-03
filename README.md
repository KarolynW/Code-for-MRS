# Code-for-MRS Example Scripts

This repository contains six small Python programs that demonstrate how market
researchers can interact with different AI services and datasets.
Each script has been heavily commented so that you can read it top-to-bottom and
understand the full process.  The sections below provide a quick overview plus
step-by-step instructions for running everything in [Visual Studio Code](https://code.visualstudio.com/).

This README was produced by Codex.

## Prerequisites

1. Install **Python 3.9 or later** from [python.org](https://www.python.org/downloads/).
2. Install **Visual Studio Code** and the official **Python extension**.
3. (Optional) Create a virtual environment for the repository so packages you
   install here do not affect other projects.

Open a terminal in VS Code (``Ctrl+` `` or ``Cmd+` `` on macOS) and run the
following commands the first time you set up the examples:

```bash
python -m venv .venv
# Activate the environment before installing packages
# Windows PowerShell:
.venv\Scripts\Activate.ps1
# macOS/Linux:
source .venv/bin/activate

pip install -r requirements.txt
```

The provided `requirements.txt` installs every library used across the scripts,
including `requests`, `openai`, `pandas`, and the Azure SDK packages.  Install
them once at the start and you will be able to run any example without hunting
for extra dependencies.

## Running the examples in VS Code

1. Choose **File → Open Folder…** and select the cloned `Code-for-MRS` folder.
2. In the Explorer sidebar click the script you want to run.
3. Ensure the Python interpreter in the blue status bar points to your virtual
   environment (or the Python version you installed).
4. Click the green **Run Python File** button or press ``Ctrl+F5`` (``Cmd+F5`` on
   macOS) to run without debugging.
5. Watch the **Python Terminal** panel for prompts and output.

The individual sections below highlight what each script covers.

### 1. `1 API Call.py` – Public weather API

* Shows how to call an unauthenticated HTTP API with the `requests` library.
* Demonstrates how query parameters change the results you receive.
* Prints both the raw JSON data and selected fields for easy reading.

### 2. `2 OpenAI Basic Call.py` – Minimal OpenAI request

* Teaches the structure of an OpenAI Responses API call (system + user
  messages).
* Includes guidance on storing your `OPENAI_API_KEY` securely.
* Extracts the text answer from the response object and prints it nicely.

### 3. `3 OpenAI API call.py` – Guided recipe generator

* Collects input from the console and builds a detailed system prompt.
* Explains how to alter model parameters (`temperature`, `max_output_tokens`).
* Contains teaching notes on adapting the pattern for your own briefs.

### 4. `4 Azure API call.py` – Azure AI Agents example

* Walks through authenticating with Azure using `DefaultAzureCredential`.
* Starts a new agent thread, posts a user message, and prints the reply.
* Includes placeholders for your Azure endpoint and agent ID.

### 5. `5 Check FT.py` – Fine-tuning JSONL validator

* Opens a `.jsonl` file and verifies Azure fine-tuning requirements.
* Confirms UTF-8 with BOM encoding and checks each example for `system`, `user`,
  and `assistant` messages.
* Summarises valid examples and flags structural issues before you upload your
  dataset.

### 6. `6 GPT Thematic Analysis.py` – Simple thematic analysis tool

* Loads the sample qualitative responses in `6 Example Qualitative.xlsx`.
* Calls the OpenAI Responses API to extract concise themes for every comment.
* Writes the enriched results to `6 Example Qualitative Themed.xlsx` with both
  JSON and flattened theme columns so the findings are easy to review.

## Sample datasets

Two `.jsonl` files (`5 fine tuning.jsonl` and `5 validation data.jsonl`) provide
ready-made examples for experimenting with Azure fine-tuning workflows.  Use
`5 Check FT.py` to inspect your own datasets or these examples before uploading
them to the service.

## Troubleshooting checklist

* **Module not found:** Ensure you installed the required package into the
  correct Python environment.  Check the interpreter selection in VS Code.
* **Authentication errors:** Confirm that the relevant environment variables
  (`OPENAI_API_KEY`, `AZURE_CLIENT_ID`, etc.) are available in the integrated
  terminal.  You can use `echo $VARIABLE_NAME` to verify.
* **Timeouts or connection issues:** Double-check that you are online and not
  blocked by a corporate firewall.

If you get stuck, read the docstring at the top of each script—they include the
most common setup steps and configuration tips.
