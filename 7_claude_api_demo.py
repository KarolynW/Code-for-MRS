"""Script 7: Your First Claude API Call.

This script demonstrates how to call the Anthropic Claude API from Python.
It mirrors the pattern from Script 2 (OpenAI), so you can compare the two
APIs side-by-side and see how similar they are — and how easy it is to switch
between providers.

Market research use case
------------------------
A researcher has collected eight open-ended customer satisfaction survey
responses and wants a quick summary: what are the main themes, what is the
overall sentiment, and what is one actionable recommendation?  Normally this
would take 15–20 minutes of careful reading.  Claude does it in seconds.

What you will learn from this script
-------------------------------------
* How to load an API key securely from a ``.env`` file.
* How to build a two-part prompt: a system prompt (the briefing) and a user
  message (the task).
* How to call the Anthropic Claude API and read the response text.
* How to interpret the token usage figures that appear at the end.

How to install dependencies
----------------------------
Run this once in your terminal::

    pip install anthropic python-dotenv

How to run the script
---------------------
1. Copy ``.env.example`` to ``.env`` and add your Anthropic API key::

       ANTHROPIC_API_KEY=your-key-goes-here

2. Open ``7_claude_api_demo.py`` in VS Code.
3. Press ``Ctrl+F5`` (``Cmd+F5`` on macOS) to run without debugging.
4. Watch the terminal for Claude's analysis.

Where to get an API key
-----------------------
Visit https://console.anthropic.com and create a free account.  During the
course, a shared key will be provided for you.

TEACHING NOTE: Comparing OpenAI (Script 2) and Claude (Script 7)
-----------------------------------------------------------------
Both scripts follow the same four-step pattern:
  1. Load API key from .env
  2. Define survey data and build a prompt
  3. Call the API (one line of code!)
  4. Extract the text from the response and print it

The main differences are the library name (``openai`` vs ``anthropic``), the
client method (``responses.create`` vs ``messages.create``), and how the
response text is accessed.  Everything else — the concept of a system prompt,
user messages, tokens, and max tokens — is identical.
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

# -----------------------------------------------------------------------
# MAKE THE API CALL
# We create a client using our API key, then call client.messages.create()
#
# Key parameters to know:
#   model        — which version of Claude to use (Haiku is fast and cheap)
#   max_tokens   — the maximum number of tokens in the response
#   system       — the system prompt (your briefing to the AI)
#   messages     — the conversation, starting with the user's message
#
# TEACHING NOTE: What is a token?
# A token is roughly 0.75 words.  "customer satisfaction" = 3 tokens.
# max_tokens controls both the maximum length of the reply and the cost
# of each API call, because you are charged per token processed.
# -----------------------------------------------------------------------
try:
    response = client.messages.create(
        model="claude-haiku-4-5-20251001",  # Fast, cost-effective model — good for demos
        # model="claude-sonnet-4-6",        # Uncomment for higher-quality analysis
        max_tokens=1024,                    # Cap the response at ~750 words
        system=system_prompt,              # The AI's role and instructions
        messages=[
            {"role": "user", "content": user_message}   # Our survey analysis request
        ]
    )
except anthropic.AuthenticationError:
    print("❌  Your API key was rejected.")
    print("    Check that ANTHROPIC_API_KEY is correct in your .env file.")
    exit()
except anthropic.RateLimitError:
    print("⚠️  You have hit the rate limit. Wait a moment and try again.")
    exit()
except anthropic.APIConnectionError:
    print("❌  Could not connect to the Anthropic API.")
    print("    Check your internet connection and try again.")
    exit()

# At this point, 'response' is a Python object containing Claude's reply,
# usage statistics, and metadata.  We only need the text content.

# -----------------------------------------------------------------------
# EXTRACT AND DISPLAY THE RESPONSE
# response.content is a list of content blocks.  The first block contains
# our answer as a text string.
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
