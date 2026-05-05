"""Script 2: Your First OpenAI API Call.

This script keeps the example intentionally small so you can see the bare
minimum needed to send a message to OpenAI and display the reply.  It is
designed for market researchers who are new to Python and want to understand
the building blocks of an AI call.

Compare this script with Script 7 (``7_claude_api_demo.py``) to see how
the OpenAI and Anthropic APIs follow the same four-step pattern.

Market research use case
------------------------
Before using AI for real research tasks, it helps to run a simple "hello world"
call to confirm everything is wired up correctly.  This script is that first
call — a single question, a single answer, nothing more.

What you will learn from this script
-------------------------------------
* How to load an API key securely from a ``.env`` file.
* How to write a system prompt and a user message.
* How to call the OpenAI Responses API and read the reply.

How to install dependencies
----------------------------
Run this once in your terminal::

    pip install openai python-dotenv

How to run the script
---------------------
1. Copy ``.env.example`` to ``.env`` and add your OpenAI API key::

       OPENAI_API_KEY=your-openai-api-key-here

2. Open ``2_openai_basic_call.py`` in VS Code.
3. Press ``Ctrl+F5`` (``Cmd+F5`` on macOS) to run without debugging.
4. Watch the terminal for OpenAI's answer.

Where to get an API key
-----------------------
Visit https://platform.openai.com/api-keys and create a new secret key.
Add it to your ``.env`` file (never paste it into the script itself).

TEACHING NOTE: System prompts and user messages
------------------------------------------------
Every AI conversation has two parts:
  - The **system prompt** tells the AI how to behave — its role, its tone,
    any constraints.  Think of it as the briefing you give a member of staff.
  - The **user message** is the actual question or task you want answered.

Separating these two parts makes it easy to reuse the same instructions
(system prompt) while changing just the question (user message).
"""


import os
import sys

from openai import OpenAI
from dotenv import load_dotenv


# -----------------------------------------------------------------------
# LOAD THE API KEY
# We store the API key in a .env file so it never appears in the script.
# load_dotenv() reads that file and makes the key available to os.getenv().
# -----------------------------------------------------------------------
load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")

if not api_key:
    print("❌  No API key found.")
    print("    Copy .env.example to .env and add your OPENAI_API_KEY.")
    sys.exit(1)


# -----------------------------------------------------------------------
# DEFINE THE QUESTION
# A "system prompt" gives the AI its role and instructions.
# The "user message" is the actual question we want answered.
# Try changing the user_message to something relevant to your work.
# -----------------------------------------------------------------------
system_prompt = "You are a helpful AI assistant. Keep your answers clear and easy to read."
user_message = "Tell me everything about Dogs"

print("=" * 60)
print("  MRS Advanced Course — OpenAI API Demo")
print("=" * 60)
print(f"\nQuestion: {user_message}\n")
print("Sending request to OpenAI...\n")


# -----------------------------------------------------------------------
# CREATE THE API CLIENT AND MAKE THE CALL
# The client is initialised with our API key.
#
# Key parameters to know:
#   model            — which version of GPT to use (gpt-4o-mini is fast and cheap)
#   instructions     — the system prompt (the AI's briefing / role)
#   input            — the user's question or task
#   temperature      — creativity level (0 = factual and precise, 1 = creative)
#   max_output_tokens — maximum length of the response (roughly 0.75 words per token)
#
# TEACHING NOTE: What is a token?
# A token is roughly 0.75 words.  "market research" = 3 tokens.
# max_output_tokens controls both the response length and the cost per call.
# -----------------------------------------------------------------------
client = OpenAI(api_key=api_key)

try:
    response = client.responses.create(
        model="gpt-4o-mini",           # cost-effective model — good for demos
        instructions=system_prompt,    # the AI's role and instructions
        input=user_message,            # our question
        temperature=0.8,               # slightly creative — good for open questions
        max_output_tokens=800,         # cap the response at roughly 600 words
    )
except Exception as error:
    print(f"❌  API call failed: {error}")
    print("    Common causes: invalid API key, no internet connection, or rate limit.")
    sys.exit(1)

# At this point, 'response' is a Python object containing OpenAI's reply and
# usage statistics.  We access the text via the output_text shortcut.

# -----------------------------------------------------------------------
# EXTRACT AND DISPLAY THE RESPONSE
# response.output_text is a convenience property that returns the model's
# reply as a plain string — no need to navigate nested lists.
# -----------------------------------------------------------------------
answer_text = response.output_text

print("OpenAI's Answer:")
print("-" * 40)
print(answer_text)
print("-" * 40)
print("\n✅  Done! You have successfully called the OpenAI API.")
