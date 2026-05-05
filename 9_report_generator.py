"""Script 9: Executive Summary Report Generator.

This script loads the categorised survey responses produced by Script 8
(``8_categorised_responses.xlsx``), formats them into a structured prompt,
and asks Claude to generate a polished executive summary report.  The report
is saved as a plain-text file ready to share with a client or paste into a
presentation.

Market research use case
------------------------
After categorising and sentiment-scoring hundreds of open-text responses,
a researcher still needs to write the narrative that goes in the report.
Drafting a clear, concise executive summary that reflects the data correctly
takes time — especially under deadline pressure.  This script uses Claude to
generate a first-draft summary that the researcher can then review, refine,
and personalise.  The AI does the heavy lifting; the researcher brings the
judgement, context, and client knowledge.

What you will learn from this script
-------------------------------------
* How to load a DataFrame from Excel and summarise it for a prompt.
* How to build a detailed, structured prompt that produces a professional output.
* How to save the AI's response to a text file for sharing or further editing.
* How the output of one script (Script 8) can feed the input of another
  (Script 9) to create an automated research workflow.

How to install dependencies
----------------------------
Run this once in your terminal::

    pip install anthropic pandas openpyxl python-dotenv

How to run the script
---------------------
1. Run Script 8 first to generate ``8_categorised_responses.xlsx``.
2. Copy ``.env.example`` to ``.env`` and add your Anthropic API key::

       ANTHROPIC_API_KEY=your-anthropic-api-key-here

3. Open ``9_report_generator.py`` in VS Code.
4. Press ``Ctrl+F5`` (``Cmd+F5`` on macOS) to run without debugging.
5. Open ``9_executive_summary.txt`` to read the generated report.

Where to get an API key
-----------------------
Visit https://console.anthropic.com and create a free account.  During the
course, a shared key will be provided.

TEACHING NOTE: Chaining scripts together
-----------------------------------------
Real research workflows often involve several steps: collect data → clean data →
categorise responses → write the report.  By saving intermediate outputs to
files (e.g. an Excel file), each step can be run independently and inspected
before the next step begins.  This makes it easy to spot problems early and
re-run only the step that needs fixing.
"""


import os
import sys

import anthropic
import pandas as pd
from dotenv import load_dotenv


# -----------------------------------------------------------------------
# LOAD THE API KEY
# We store the key in a .env file so it never appears in the script itself.
# -----------------------------------------------------------------------
load_dotenv()

api_key = os.getenv("ANTHROPIC_API_KEY")

if not api_key:
    print("❌  No API key found.")
    print("    Copy .env.example to .env and add your ANTHROPIC_API_KEY.")
    sys.exit(1)


# -----------------------------------------------------------------------
# CONFIGURATION
# Change INPUT_FILE to point at a different Excel file if needed.
# OUTPUT_FILE is where the generated report will be saved.
# -----------------------------------------------------------------------
INPUT_FILE = "8_categorised_responses.xlsx"    # output from Script 8
OUTPUT_FILE = "9_executive_summary.txt"        # where the report will be saved
MODEL = "claude-sonnet-4-6"                    # Sonnet gives higher-quality prose


# -----------------------------------------------------------------------
# PRINT HEADER
# -----------------------------------------------------------------------
print("=" * 60)
print("  MRS Advanced Course — Executive Summary Generator")
print("=" * 60)


# -----------------------------------------------------------------------
# LOAD THE CATEGORISED DATA
# We read the Excel file produced by Script 8.  If it does not exist, we
# print a clear message telling the user which script to run first.
# -----------------------------------------------------------------------
if not os.path.exists(INPUT_FILE):
    print(f"\n❌  Input file not found: {INPUT_FILE}")
    print("    Please run Script 8 (8_open_text_categoriser.py) first to")
    print("    generate the categorised responses file.")
    sys.exit(1)

print(f"\nLoading data from: {INPUT_FILE}")

try:
    df = pd.read_excel(INPUT_FILE)
except Exception as error:
    print(f"❌  Could not open {INPUT_FILE}: {error}")
    sys.exit(1)

# Confirm the file looks like what we expect
required_columns = ["Original Response", "Category", "Sentiment"]
missing_columns = [col for col in required_columns if col not in df.columns]
if missing_columns:
    print(f"❌  The file is missing expected columns: {missing_columns}")
    print("    Make sure you are using the output from Script 8.")
    sys.exit(1)

total_responses = len(df)
print(f"✅  Loaded {total_responses} categorised responses.\n")


# -----------------------------------------------------------------------
# SUMMARISE THE DATA FOR THE PROMPT
# We compute simple counts (category breakdown, sentiment split) and format
# them as readable text.  This gives Claude the facts it needs to write an
# accurate report without having to read every individual response.
# -----------------------------------------------------------------------

# Count how many responses fall into each category
category_counts = df["Category"].value_counts()

# Count positive, neutral, and negative responses
sentiment_counts = df["Sentiment"].value_counts()

# Build a text block listing category counts
category_summary_lines = []
for category, count in category_counts.items():
    percentage = round((count / total_responses) * 100)
    category_summary_lines.append(f"  - {category}: {count} responses ({percentage}%)")

category_summary = "\n".join(category_summary_lines)

# Build a text block listing sentiment counts
sentiment_summary_lines = []
for sentiment, count in sentiment_counts.items():
    percentage = round((count / total_responses) * 100)
    sentiment_summary_lines.append(f"  - {sentiment}: {count} responses ({percentage}%)")

sentiment_summary = "\n".join(sentiment_summary_lines)

# Collect a short selection of verbatim quotes (up to 6) to ground the report
# in real customer language.  We take two from each sentiment group if possible.
sample_quotes = []
for sentiment in ["Positive", "Negative", "Neutral"]:
    subset = df[df["Sentiment"] == sentiment]["Original Response"].head(2).tolist()
    sample_quotes.extend(subset)

quotes_text = "\n".join(f'  "{q}"' for q in sample_quotes[:6])

# At this point we have all the facts Claude needs to write the report.
print("📊  Data summary:")
print(f"    Total responses:   {total_responses}")
print(f"    Categories found:  {len(category_counts)}")
print(f"    Sentiment split:   {dict(sentiment_counts)}")


# -----------------------------------------------------------------------
# BUILD THE PROMPT
# A detailed, structured prompt produces a more useful report.  We give
# Claude the data summary as facts and ask it to write specific sections.
# -----------------------------------------------------------------------
system_prompt = """You are an expert market research analyst writing for a professional audience.
Your task is to produce a concise, well-structured executive summary report based on the
survey data provided.  Write in clear, confident British English.  Do not use jargon.
Use bullet points for lists.  Every claim must be grounded in the data provided."""

user_message = f"""Please write an executive summary report for the following survey data.

--- SURVEY DATA SUMMARY ---

Total responses analysed: {total_responses}

Category breakdown:
{category_summary}

Sentiment breakdown:
{sentiment_summary}

Sample verbatim responses:
{quotes_text}

--- END OF DATA ---

Please structure your report with the following sections:
1. Overview — one paragraph summarising what was researched and how many responses were analysed.
2. Key Findings — three to five bullet points highlighting the most important patterns in the data.
3. Sentiment Analysis — a short paragraph interpreting the sentiment split and what it means for the client.
4. Recommendations — two or three specific, actionable recommendations based on the findings.
5. Next Steps — one paragraph suggesting what further research would be valuable.

Keep the total length to around 400–500 words.  The report should be ready to present to a client."""


# -----------------------------------------------------------------------
# MAKE THE API CALL
# We use claude-sonnet-4-6 here because writing a polished narrative report
# benefits from a more capable model than a classification task.
# -----------------------------------------------------------------------
print("\nSending data to Claude for report generation...")
print("(This may take a few seconds — Claude is writing the report.)\n")

client = anthropic.Anthropic(api_key=api_key)

try:
    response = client.messages.create(
        model=MODEL,                          # Sonnet — good quality prose
        # model="claude-haiku-4-5-20251001",  # Uncomment for faster, cheaper output
        max_tokens=1024,                      # enough for a 400–500 word report
        system=system_prompt,                 # the analyst role and writing style
        messages=[
            {"role": "user", "content": user_message}    # the data and instructions
        ]
    )
except anthropic.AuthenticationError:
    print("❌  Your API key was rejected.")
    print("    Check that ANTHROPIC_API_KEY is correct in your .env file.")
    sys.exit(1)
except anthropic.RateLimitError:
    print("⚠️  You have hit the rate limit. Wait a moment and try again.")
    sys.exit(1)
except anthropic.APIConnectionError:
    print("❌  Could not connect to the Anthropic API.")
    print("    Check your internet connection and try again.")
    sys.exit(1)

# At this point 'response' contains Claude's report as a text string.

# -----------------------------------------------------------------------
# EXTRACT THE REPORT TEXT
# response.content is a list of content blocks; the first contains the text.
# -----------------------------------------------------------------------
report_text = response.content[0].text


# -----------------------------------------------------------------------
# SAVE THE REPORT TO A TEXT FILE
# We write the report to a plain-text file so it can be opened in any
# editor, emailed to a client, or pasted into a Word document.
# -----------------------------------------------------------------------
try:
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write("EXECUTIVE SUMMARY REPORT\n")
        f.write("=" * 60 + "\n")
        f.write(f"Generated from: {INPUT_FILE}\n")
        f.write(f"Total responses: {total_responses}\n")
        f.write("=" * 60 + "\n\n")
        f.write(report_text)
        f.write("\n")
except OSError as error:
    print(f"❌  Could not save the report: {error}")
    sys.exit(1)


# -----------------------------------------------------------------------
# PRINT SUCCESS AND A PREVIEW
# -----------------------------------------------------------------------
print("Claude's Executive Summary:")
print("-" * 40)
print(report_text)
print("-" * 40)

print(f"\n✅  Report saved to: {OUTPUT_FILE}")
print(f"\n📊  Token usage:")
print(f"    Input tokens  (your data and prompt): {response.usage.input_tokens}")
print(f"    Output tokens (Claude's report):       {response.usage.output_tokens}")
print("\n✅  Done! Open the text file to review and edit the report.")
