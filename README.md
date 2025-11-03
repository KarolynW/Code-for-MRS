# Code-for-MRS Example Scripts

This repository contains four small Python programs that demonstrate how market
researchers can interact with different AI services.  Each script has been
heavily commented so that you can read it top-to-bottom and understand the full
process.  The sections below provide a quick overview plus step-by-step
instructions for running everything in [Visual Studio Code](https://code.visualstudio.com/).

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

pip install -r requirements.txt  # If you create this file for your team
```

> **Tip:** If you do not have a `requirements.txt` file, simply install the
> packages noted in each script (`requests`, `openai`, `azure-ai-projects`, and
> `azure-identity`).

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
