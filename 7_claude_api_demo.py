"""
Script 7: Your First Claude API Call
=====================================
This script demonstrates how to call the Anthropic Claude API from Python.
It mirrors the pattern from Script 2 (OpenAI), so you can see how similar
both APIs are — and how easy it is to switch between them.

Market research use case: Ask Claude to summarise a set of survey responses.

How to run this script:
-----------------------
1. Install the library:   pip install anthropic
2. Set your API key:      Create a file called .env and add the line:
                          ANTHROPIC_API_KEY=your-key-goes-here
3. Run the script:        Press Ctrl+F5 in VS Code, or run in the terminal

Note: During the course, an API key will be provided for you. If you want
to create your own free account, visit: https://console.anthropic.com
"""

# -----------------------------------------------------------------------
# IMPORTS
# We need two libraries:
#   anthropic  - the official Anthropic Python SDK
#   dotenv     - to safely load our API key from a .env file
# -----------------------------------------------------------------------
import anthropic
from dotenv import load_dotenv
import os

# -----------------------------------------------------------------------
# LOAD THE API KEY
# It is important never to paste your API key directly into a script.
# Instead, we store it in a separate .env file and load it here.
# If the .env file is missing, the script will tell you what to do.
# -----------------------------------------------------------------------
load_dotenv()

api_key = os.getenv("ANTHROPIC_API_KEY")

if not api_key:
    print("❌  No API key found.")
    print("    Create a file called .env in the same folder as this script.")
    print("    Inside it, add this line:")
    print("    ANTHROPIC_API_KEY=your-key-goes-here")
    exit()

# -----------------------------------------------------------------------
# SOME EXAMPLE SURVEY RESPONSES
# These are fictional open-text responses from a customer satisfaction survey.
# In a real project, you would load these from a CSV or Excel file.
# -----------------------------------------------------------------------
survey_responses = [
    "The onboarding process was confusing and took much longer than expected.",
    "Really enjoyed the product — it's intuitive and saved me a lot of time.",
    "Customer support was slow to respond but eventually resolved my issue.",
    "Great value for money. Would definitely recommend to colleagues.",
    "The interface feels dated and is hard to navigate on mobile devices.",
    "Excellent training resources. I felt confident using the product from day one.",
    "Pricing is too high compared to competitors offering similar features.",
    "The integration with our existing tools worked seamlessly — very impressed.",
]

print("=" * 60)
print("  MRS Advanced Course — Claude API Demo")
print("=" * 60)
print(f"\nWe have {len(survey_responses)} survey responses to analyse.\n")

# -----------------------------------------------------------------------
# BUILD THE PROMPT
# A prompt has two parts:
#   system  — instructions that tell the AI what role to play
#   user    — the actual task or question you want answered
#
# Think of the system prompt as a brief you'd give to a researcher
# before handing them a stack of responses to read.
# -----------------------------------------------------------------------
system_prompt = """You are an expert market research analyst with experience
in qualitative data analysis. Your role is to identify key themes in
customer feedback and present your findings clearly and concisely.
Always present your analysis in plain English, suitable for sharing
with a non-technical client."""

# We join all responses into one block of text for the user message
responses_text = "\n".join(f"- {r}" for r in survey_responses)

user_message = f"""Please analyse the following customer survey responses
and provide:

1. The top 3 themes that emerge from the feedback
2. A brief summary (2-3 sentences) of the overall sentiment
3. One actionable recommendation for the client

Survey responses:
{responses_text}"""

# -----------------------------------------------------------------------
# MAKE THE API CALL
# We create a client using our API key, then call client.messages.create()
#
# Key parameters to know:
#   model        — which version of Claude to use
#   max_tokens   — the maximum length of the response
#   system       — the system prompt (your briefing to the AI)
#   messages     — the conversation, starting with the user's message
# -----------------------------------------------------------------------
print("Sending request to Claude...\n")

client = anthropic.Anthropic(api_key=api_key)

response = client.messages.create(
    model="claude-opus-4-5",          # Use a recent Claude model
    max_tokens=1024,                   # Limit the response length
    system=system_prompt,
    messages=[
        {"role": "user", "content": user_message}
    ]
)

# -----------------------------------------------------------------------
# EXTRACT AND DISPLAY THE RESPONSE
# The response object contains a lot of information. We just want the text.
# response.content is a list; the first item contains our answer.
# -----------------------------------------------------------------------
result_text = response.content[0].text

print("Claude's Analysis:")
print("-" * 40)
print(result_text)
print("-" * 40)

# -----------------------------------------------------------------------
# SHOW USAGE INFORMATION
# This tells you how many tokens were used, which affects cost.
# Tokens are roughly equivalent to words (1 token ≈ 0.75 words).
# -----------------------------------------------------------------------
print(f"\n📊 Token usage:")
print(f"   Input tokens  (your prompt):  {response.usage.input_tokens}")
print(f"   Output tokens (Claude's reply): {response.usage.output_tokens}")
print(f"\n✅  Done! You've successfully called the Claude API.")
