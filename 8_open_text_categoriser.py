"""
Script 8: Open-Text Categoriser for Market Research
=====================================================
A practical automation for market researchers.

This script takes a list of open-ended survey responses and automatically:
  1. Assigns each response to a category (e.g. Product, Support, Pricing)
  2. Gives each response a sentiment score (Positive / Neutral / Negative)
  3. Exports the results to a clean Excel file for further analysis

This is the kind of task that might take a researcher hours to do manually.
With this script, it runs in seconds.

You can use EITHER the OpenAI API or the Claude API — the script supports both.
Change the PROVIDER variable below to switch between them.

Requirements:
-------------
    pip install anthropic openai pandas openpyxl python-dotenv

API keys:
---------
    Add to your .env file:
        OPENAI_API_KEY=your-openai-key
        ANTHROPIC_API_KEY=your-anthropic-key

    During the course, keys will be provided. To get your own:
        OpenAI:     https://platform.openai.com
        Anthropic:  https://console.anthropic.com
"""

import os
import json
import pandas as pd
from dotenv import load_dotenv

# -----------------------------------------------------------------------
# CONFIGURATION — change these to suit your project
# -----------------------------------------------------------------------

# Choose which AI provider to use: "openai" or "claude"
PROVIDER = "claude"

# The categories you want responses sorted into
# Edit this list to match your research topic
CATEGORIES = [
    "Product Quality",
    "Customer Support",
    "Pricing & Value",
    "Ease of Use",
    "Onboarding & Training",
    "Other",
]

# -----------------------------------------------------------------------
# SAMPLE DATA
# Replace this with your real data — ideally loaded from a CSV or Excel file.
# See the commented-out section at the bottom for how to load from a file.
# -----------------------------------------------------------------------
responses = [
    {"id": 1, "response": "The onboarding process was confusing and took much longer than expected."},
    {"id": 2, "response": "Really enjoyed the product — it's intuitive and saved me a lot of time."},
    {"id": 3, "response": "Customer support was slow to respond but eventually resolved my issue."},
    {"id": 4, "response": "Great value for money. Would definitely recommend to colleagues."},
    {"id": 5, "response": "The interface feels dated and is hard to navigate on mobile devices."},
    {"id": 6, "response": "Excellent training resources. I felt confident using the product from day one."},
    {"id": 7, "response": "Pricing is too high compared to competitors offering similar features."},
    {"id": 8, "response": "The integration with our existing tools worked seamlessly — very impressed."},
    {"id": 9, "response": "Had to contact support three times before getting a helpful answer."},
    {"id": 10, "response": "Would be great if there was a free trial before committing to a subscription."},
]

# -----------------------------------------------------------------------
# LOAD API KEYS
# -----------------------------------------------------------------------
load_dotenv()

# -----------------------------------------------------------------------
# HELPER FUNCTION: Call the AI API
# This function works with both OpenAI and Claude.
# It sends one response at a time and asks the AI to categorise it.
# -----------------------------------------------------------------------
def categorise_response(response_text: str, provider: str) -> dict:
    """
    Send a single survey response to an AI model and get back:
      - category: one of the categories defined above
      - sentiment: Positive, Neutral, or Negative
      - reason: a brief explanation of the categorisation

    Returns a dictionary with these three fields.
    """

    # Build the prompt
    categories_list = ", ".join(CATEGORIES)
    system_prompt = f"""You are a market research analyst categorising open-ended survey responses.

For each response you receive, return a JSON object with exactly these fields:
  - category: one of [{categories_list}]
  - sentiment: one of [Positive, Neutral, Negative]
  - reason: a single sentence explaining your categorisation

Return ONLY valid JSON. Do not include any explanation or extra text."""

    user_message = f'Categorise this survey response: "{response_text}"'

    # ---- OpenAI ----
    if provider == "openai":
        from openai import OpenAI
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OPENAI_API_KEY not found in .env file")
        client = OpenAI(api_key=api_key)
        result = client.responses.create(
            model="gpt-5.4-mini",      # Cost-effective model for classification tasks
            instructions=system_prompt,
            input=user_message,
        )
        raw_text = result.output_text

    # ---- Claude ----
    elif provider == "claude":
        import anthropic
        api_key = os.getenv("ANTHROPIC_API_KEY")
        if not api_key:
            raise ValueError("ANTHROPIC_API_KEY not found in .env file")
        client = anthropic.Anthropic(api_key=api_key)
        result = client.messages.create(
            model="claude-haiku-4-5-20251001",  # Fast, cost-effective model for classification
            max_tokens=256,
            system=system_prompt,
            messages=[{"role": "user", "content": user_message}],
        )
        raw_text = result.content[0].text

    else:
        raise ValueError(f"Unknown provider: {provider}. Use 'openai' or 'claude'.")

    # Parse the JSON response from the AI
    # Sometimes the AI wraps JSON in markdown code fences — we strip those
    cleaned = raw_text.strip().strip("```json").strip("```").strip()
    parsed = json.loads(cleaned)
    return parsed


# -----------------------------------------------------------------------
# MAIN SCRIPT
# -----------------------------------------------------------------------
if __name__ == "__main__":

    print("=" * 60)
    print("  Open-Text Categoriser")
    print(f"  Provider: {PROVIDER.upper()}")
    print("=" * 60)
    print(f"\nProcessing {len(responses)} responses...\n")

    results = []

    for item in responses:
        response_id = item["id"]
        response_text = item["response"]

        print(f"  [{response_id}/{len(responses)}] Processing: {response_text[:50]}...")

        try:
            categorisation = categorise_response(response_text, PROVIDER)

            results.append({
                "ID": response_id,
                "Original Response": response_text,
                "Category": categorisation.get("category", "Unknown"),
                "Sentiment": categorisation.get("sentiment", "Unknown"),
                "Reason": categorisation.get("reason", ""),
            })

        except Exception as e:
            print(f"    ⚠️  Error processing response {response_id}: {e}")
            results.append({
                "ID": response_id,
                "Original Response": response_text,
                "Category": "ERROR",
                "Sentiment": "ERROR",
                "Reason": str(e),
            })

    # -----------------------------------------------------------------------
    # EXPORT TO EXCEL
    # -----------------------------------------------------------------------
    df = pd.DataFrame(results)

    output_file = "8_categorised_responses.xlsx"
    df.to_excel(output_file, index=False)

    print(f"\n✅  Done! Results saved to: {output_file}")
    print(f"\n📊  Summary:")
    print(df["Category"].value_counts().to_string())
    print(f"\n😊  Sentiment breakdown:")
    print(df["Sentiment"].value_counts().to_string())

    # -----------------------------------------------------------------------
    # SHOW A PREVIEW
    # -----------------------------------------------------------------------
    print(f"\n📋  First few results:")
    print(df[["ID", "Category", "Sentiment"]].to_string(index=False))


# -----------------------------------------------------------------------
# HOW TO LOAD DATA FROM A REAL FILE
# -----------------------------------------------------------------------
# If you have a CSV file of responses, replace the 'responses' list above
# with something like this:
#
#   import pandas as pd
#   df = pd.read_csv("my_survey_data.csv")
#   responses = [
#       {"id": i + 1, "response": row["open_text_column"]}
#       for i, row in df.iterrows()
#   ]
#
# For an Excel file:
#   df = pd.read_excel("my_survey_data.xlsx")
#   responses = [
#       {"id": i + 1, "response": row["open_text_column"]}
#       for i, row in df.iterrows()
#   ]
