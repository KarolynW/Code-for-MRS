"""
Crisp Comments -> Simple Theme JSON (Teaching Version with Colours)
===================================================================

Purpose:
--------
• Reads qualitative comments from an Excel file.
• Sends each comment to OpenAI for thematic analysis.
• Receives concise themes in JSON format.
• Adds new columns and writes a new Excel file.

Visual Features:
----------------
• Coloured print statements show progress.
• Each stage (loading, analysing, saving) is clearly labelled.

Run:
    python theme_comments_coloured.py
"""

import os
import sys
import json
import time

import pandas as pd
from openai import OpenAI

# --- COLOUR CODES -------------------------------------------------------------
# ANSI escape codes for coloured terminal output
C_RESET = "\033[0m"      # reset colour
C_BLUE = "\033[94m"      # info / action
C_GREEN = "\033[92m"     # success
C_YELLOW = "\033[93m"    # warning
C_RED = "\033[91m"       # error
C_CYAN = "\033[96m"      # progress
# -----------------------------------------------------------------------------

# --- CONFIGURATION ------------------------------------------------------------
INPUT_XLSX = "6 Example Qualitative.xlsx"
OUTPUT_XLSX = "6 Example Qualitative Themed.xlsx"
MODEL = "gpt-4o-mini-2024-07-18"
RATE_LIMIT_DELAY = 0.3  # short pause to avoid hitting request-per-minute limits
# -----------------------------------------------------------------------------

# Create a reusable OpenAI client.  The SDK looks for ``OPENAI_API_KEY`` in the
# environment, keeping credentials out of the script.
client = OpenAI()


def analyse_comment_to_themes(comment: str) -> dict:
    """Send one comment to OpenAI and return simple JSON themes."""

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
    """Main analysis process."""

    print(f"{C_BLUE}=== Crisp Thematic Analysis ==={C_RESET}")

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

