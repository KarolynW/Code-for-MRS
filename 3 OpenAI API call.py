"""Guided recipe generator using the OpenAI Responses API.

This file intentionally walks through every step of a slightly larger API
workflow.  It asks for a list of ingredients and a cuisine style, builds a
prompt, sends it to OpenAI, and prints the resulting recipe.

Why it is useful for market researchers
---------------------------------------
* Shows how to collect input from a stakeholder (the ingredient and cuisine
  prompts).
* Demonstrates where to customise instructions for tone, structure, or brand
  voice.
* Highlights how to guard against common API mistakes with error handling.

Preparing your environment
--------------------------
1. Install Python 3.9 or later and the OpenAI package: ``pip install openai``.
2. Store your OpenAI API key in an environment variable named
   ``OPENAI_API_KEY`` (see the instructions in ``2 OpenAI Basic Call.py``).

Running the script in VS Code
-----------------------------
1. Open the repository folder in VS Code and select ``3 OpenAI API call.py``.
2. Open the built-in terminal (``Ctrl+` `` or ``Cmd+` `` on macOS) if you want
   to see print statements as they run.
3. Choose **Run > Run Without Debugging** or press ``Ctrl+F5`` (``Cmd+F5``).
4. When prompted, type your ingredients and cuisine style directly into the
   terminal panel that appears at the bottom of VS Code.

What to explore next
--------------------
* Try adjusting ``temperature`` or ``max_output_tokens`` to see how it affects
  creativity and length.
* Modify the ``system_prompt`` string to enforce a specific tone of voice or
  output format.
"""

from openai import OpenAI
import sys

# Create the API client (it automatically reads OPENAI_API_KEY from environment)
# The constructor will raise an error if the key cannot be found, which makes it
# easy to diagnose authentication problems before any network call is made.
client = OpenAI()

# Ask the user for some ingredients
# ``input`` pauses the program and waits for text typed into the terminal.  We
# ``strip`` the response to remove accidental trailing spaces so the prompt
# looks neat.
ingredients = input("Enter your ingredients (comma separated): ").strip()
if not ingredients:
    print("No ingredients entered. Exiting.")
    sys.exit(0)

# Ask the user for a style of food or cuisine
# Collecting both pieces of information lets us tailor the recipe to a brief
# similar to what a client might provide in real life.
style = input("Enter the cuisine or style of food (e.g. Italian, Thai, vegan comfort): ").strip()
if not style:
    print("No style entered. Exiting.")
    sys.exit(0)

# Build the system message dynamically.
# This string forms the clear instructions the model will follow.  Notice how
# we interpolate (insert) the user-provided values so the instructions contain
# the latest context without manually rewriting the text each time.
system_prompt = (
    "You must provide a recipe based on the style of food and the ingredients provided by the user. "
    "Include a descriptive title, an ingredients list with quantities, and clear cooking steps.\n\n"
    f"Ingredients: {ingredients}\n"
    f"Style of food: {style}"
)

# Now we make the API call
try:
    response = client.responses.create(
        model="gpt-4o-mini",  # the lightweight GPT-4 model
        input=[  # this is the actual content sent to the model
            {
                "role": "system",        # defines that this text is an instruction, not user chat
                "content": [             # content can include text, images, etc.
                    {
                        "type": "input_text",
                        "text": system_prompt
                    }
                ]
            }
        ],
        text={                         # specify text output formatting
            "format": {"type": "text"}
        },
        reasoning={},                  # optional: used by reasoning models
        tools=[],                      # none needed for this demo
        temperature=0.7,               # controls creativity (0 = factual, 1 = creative)
        max_output_tokens=800,         # roughly limits output length
        top_p=1,
        store=False,                   # don't store this response in project history
        include=[]                     # no need for additional info like web sources
    )

except Exception as e:
    # Catching ``Exception`` keeps the script approachable; the message will
    # explain issues such as network timeouts or invalid parameters.
    print(f"❌ API call failed: {e}")
    sys.exit(1)

# Extract and display the text result
# ``response.output`` mirrors the structure described in the SDK docs.  We use a
# protective ``try`` so the script still prints *something* even if the format
# changes in a later SDK release.
try:
    recipe = response.output[0].content[0].text
except Exception:
    recipe = str(response)

print("\n✅ Recipe generated successfully!\n")
print(recipe)

"""
TEACHING NOTES
--------------
What this demonstrates:
• The API call sends a structured JSON payload to OpenAI’s servers.
• The 'model' field specifies which model to use.
• The 'input' array describes what information is sent.
• The 'output' in the response contains the generated text.
• JSON data moves between systems in a predictable structure.

How to adapt for your own projects:
• Replace the prompt-building section with language suited to your brief.
• Collect inputs from a CSV or survey export instead of manual typing.
• Save the `recipe` variable to a file (e.g., CSV or Excel) for reporting.

Common API errors:
• 401/403 – authentication issue (check your API key)
• 400 – missing or malformed parameter (like forgetting 'input')
• 429 – rate limit exceeded
• 500+ – temporary service problem (retry later)
"""

