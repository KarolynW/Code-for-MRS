"""Script 6: Qualitative Thematic Analysis Tool.

This script reads open-ended survey comments from an Excel file, sends each
comment to OpenAI, and receives a structured list of themes in return.  The
enriched results are saved back to a new Excel file with two additional columns:
one containing the raw JSON themes, and one with a plain text version for easy
reading in a spreadsheet.

Market research use case
------------------------
Thematic analysis of qualitative verbatims (open-ended responses) is one of the
most time-consuming tasks in market research.  A researcher might spend several
hours reading hundreds of comments and grouping them into meaningful themes.
This script does a first-pass in seconds.  The researcher then reviews and
refines the AI's suggestions — using their judgement for interpretation — rather
than starting from scratch.

What you will learn from this script
-------------------------------------
* How to load data from an Excel file using ``pandas``.
* How to loop through rows and send each one to an AI model.
* How to ask the model to respond in JSON format so the output is structured.
* How to add new columns to a DataFrame and write the results back to Excel.
* Why rate-limiting (brief pauses between calls) matters in real deployments.

How to install dependencies
----------------------------
Run this once in your terminal before running the script::

    pip install openai pandas openpyxl python-dotenv

How to run the script
---------------------
1. Copy ``.env.example`` to ``.env`` and add your OpenAI API key::

       OPENAI_API_KEY=your-openai-api-key-here

2. Make sure ``6_Example_Qualitative.xlsx`` is in the same folder.
3. Open ``6_qualitative_theming.py`` in VS Code.
4. Press ``Ctrl+F5`` (``Cmd+F5`` on macOS) to run without debugging.
5. When it finishes, open ``6_Example_Qualitative_Themed.xlsx`` to see the results.

Where to get an API key
-----------------------
Visit https://platform.openai.com/api-keys and create a new secret key.
Add it to your ``.env`` file (never paste it directly into the script).

TEACHING NOTE: Why use JSON output?
-------------------------------------
When we ask the AI to return themes as a list, we could get them as plain text
— but that is hard to process automatically.  By asking for JSON, we get data
in a predictable structure that Python can parse and insert directly into a
spreadsheet column.  This is a fundamental pattern in AI automation: use
structured output when you need to do something with the result.
"""


import os
import sys
import json
import time

import pandas as pd
from openai import OpenAI
from dotenv import load_dotenv


# -----------------------------------------------------------------------
# LOAD API KEY
# We load OPENAI_API_KEY from a .env file so it never appears in the script.
# -----------------------------------------------------------------------
load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    print("❌  OPENAI_API_KEY not found.")
    print("    Copy .env.example to .env and add your OpenAI API key.")
    sys.exit(1)


# -----------------------------------------------------------------------
# COLOUR CODES
# ANSI escape sequences for coloured terminal output.  These make it much
# easier to follow progress at a glance when the script is running.
# Note: colours display correctly in most terminals (macOS Terminal,
# Windows Terminal, VS Code integrated terminal).
# -----------------------------------------------------------------------
C_RESET = "\033[0m"      # return to default colour
C_BLUE = "\033[94m"      # section headings
C_GREEN = "\033[92m"     # success messages
C_YELLOW = "\033[93m"    # warnings
C_RED = "\033[91m"       # error messages
C_CYAN = "\033[96m"      # progress / in-progress messages


# -----------------------------------------------------------------------
# CONFIGURATION
# Change these constants to point at your own files or to use a different
# model.  The rest of the script does not need to change.
# -----------------------------------------------------------------------
INPUT_XLSX = "6_Example_Qualitative.xlsx"          # source data
OUTPUT_XLSX = "6_Example_Qualitative_Themed.xlsx"  # results file
MODEL = "gpt-4o-mini"          # cost-effective model; good for classification tasks
RATE_LIMIT_DELAY = 0.3         # seconds to pause between API calls


# -----------------------------------------------------------------------
# CREATE THE API CLIENT
# The client reads OPENAI_API_KEY from the environment variable we loaded
# above.  Keeping the key in .env means it is never visible in the code.
# -----------------------------------------------------------------------
client = OpenAI(api_key=api_key)


def analyse_comment_to_themes(comment: str) -> dict:
    """Send one verbatim comment to OpenAI and return a dictionary of themes.

    Constructs a system prompt that instructs the model to return themes as
    a JSON object.  Handles API errors and JSON parse errors gracefully,
    returning a fallback dictionary so the main loop can always continue.

    Args:
        comment (str): The raw survey verbatim to analyse.

    Returns:
        dict: A dictionary with a single key ``"themes"`` containing a list
            of short theme strings, e.g. ``{"themes": ["Value for money",
            "Poor packaging"]}``.  On error the list will contain a single
            descriptive error string so the output file always has a value.

    Example:
        >>> result = analyse_comment_to_themes("The packaging was easy to open.")
        >>> result["themes"]
        ['Easy packaging', 'Positive experience']
    """

    system_prompt = (
        "You are a market research assistant. "
        "Extract 2 to 5 short, high-level themes from the consumer comment below. "
        "Use British English and concise wording. "
        "Return ONLY valid JSON in this exact schema:\n"
        "{\n"
        '  \"themes\": [\"<theme1>\", \"<theme2>\", \"...\"]\n'
        "}\n"
        "Do not add explanations or any extra text. Keep each theme under 4 words."
    )

    user_text = f"Comment:\n{comment}"

    # Send request to API
    # We wrap the network call in ``try`` so beginners see a friendly message if
    # their API key is missing or the internet connection drops mid-run.
    try:
        print(f"{C_CYAN}   ↳ Sending to model...{C_RESET}")
        resp = client.responses.create(
            model=MODEL,
            input=[
                {"role": "system", "content": [{"type": "input_text", "text": system_prompt}]},
                {"role": "user", "content": [{"type": "input_text", "text": user_text}]},
            ],
            text={"format": {"type": "json_object"}},
            temperature=0.2,
            max_output_tokens=200,
            store=False,
        )
    except Exception as e:
        print(f"{C_RED}   ⚠ API call failed: {e}{C_RESET}")
        return {"themes": [f"api_error: {str(e)}"]}

    # Try to extract and parse JSON
    # The Responses API returns a structured object.  We carefully unwrap the
    # nested lists and fall back to ``str(resp)`` if anything unexpected happens.
    try:
        content = resp.output[0].content[0].text
    except Exception:
        content = str(resp)

    try:
        data = json.loads(content)
        if isinstance(data, dict) and "themes" in data:
            data["themes"] = [str(t).strip() for t in data["themes"] if str(t).strip()]
            if not data["themes"]:
                data["themes"] = ["no_themes_extracted"]
            print(f"{C_GREEN}   ✓ Themes extracted: {', '.join(data['themes'])}{C_RESET}")
            return data
        else:
            print(f"{C_YELLOW}   ⚠ Unexpected JSON structure returned{C_RESET}")
            return {"themes": ["parse_error_or_wrong_schema"]}
    except json.JSONDecodeError:
        print(f"{C_YELLOW}   ⚠ Could not decode JSON{C_RESET}")
        return {"themes": ["json_decode_error"]}


def main():
    """Orchestrate the full thematic analysis workflow.

    Loads the input Excel file, sends each comment row to OpenAI, collects
    the JSON themes, adds them as two new columns, and writes the enriched
    DataFrame to a new Excel file.
    """

    print(f"{C_BLUE}=== Qualitative Thematic Analysis ==={C_RESET}")

    # Step 1: Load Excel file
    # By checking for the file before opening it we can display a clear message
    # if the user forgets to copy their own dataset into the project folder.
    if not os.path.exists(INPUT_XLSX):
        print(f"{C_RED}❌ Input file not found: {INPUT_XLSX}{C_RESET}")
        sys.exit(1)

    print(f"{C_CYAN}Loading data from {INPUT_XLSX}...{C_RESET}")
    df = pd.read_excel(INPUT_XLSX)
    print(f"{C_GREEN}✓ Loaded {len(df)} rows successfully.{C_RESET}")

    required_cols = ["Key", "Favourite Flavour", "Least Favourite Flavour", "Would Purchase Again (Yes/No)", "Comments"]
    missing = [c for c in required_cols if c not in df.columns]
    if missing:
        print(f"{C_RED}Missing expected columns: {missing}{C_RESET}")
        sys.exit(1)

    # Step 2: Loop through comments
    print(f"{C_BLUE}\n--- Analysing comments ---{C_RESET}")
    themes_json_list = []

    for i, row in df.iterrows():
        comment = str(row.get("Comments", "")).strip()
        print(f"{C_CYAN}Processing Row {i+1}/{len(df)}{C_RESET}")

        if not comment:
            print(f"{C_YELLOW}   ⚠ Empty comment – skipping{C_RESET}")
            themes_json_list.append(json.dumps({"themes": ["no_comment"]}))
            continue

        result = analyse_comment_to_themes(comment)
        themes_json_list.append(json.dumps(result, ensure_ascii=False))
        # Pause between requests so we stay within OpenAI's rate limits and keep
        # demos polite when run from shared networks.
        time.sleep(RATE_LIMIT_DELAY)

    # Step 3: Add themes back to DataFrame
    df["Themes (JSON)"] = themes_json_list

    def flatten_themes(js):
        try:
            data = json.loads(js)
            return "; ".join(data.get("themes", []))
        except Exception:
            return ""
    # ``apply`` lets us create a human-readable column alongside the raw JSON so
    # the output spreadsheet is easy to skim in stakeholder presentations.
    df["Themes (flat)"] = df["Themes (JSON)"].apply(flatten_themes)

    # Step 4: Save results
    print(f"{C_CYAN}\nSaving results to {OUTPUT_XLSX}...{C_RESET}")
    df.to_excel(OUTPUT_XLSX, index=False)
    print(f"{C_GREEN}✅ Done! File saved successfully.{C_RESET}")

    print(f"{C_BLUE}\nAll comments analysed and themed. Great job!{C_RESET}")


if __name__ == "__main__":
    main()

