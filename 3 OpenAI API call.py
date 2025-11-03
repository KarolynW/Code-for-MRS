"""
Recipe Generator using OpenAI Responses API
-------------------------------------------

This teaching example:
• Demonstrates how to send and receive data through an API.
• Explains each part of the OpenAI Responses API call.
• Builds a system message dynamically using user input.
• Shows how to parse and display a text result.

Setup:
1) pip install openai
2) Set your OPENAI_API_KEY as an environment variable before running.

Run:
python recipe_demo.py
"""

from openai import OpenAI
import sys

# Create the API client (it automatically reads OPENAI_API_KEY from environment)
client = OpenAI()

# Ask the user for some ingredients
ingredients = input("Enter your ingredients (comma separated): ").strip()
if not ingredients:
    print("No ingredients entered. Exiting.")
    sys.exit(0)

# Ask the user for a style of food or cuisine
style = input("Enter the cuisine or style of food (e.g. Italian, Thai, vegan comfort): ").strip()
if not style:
    print("No style entered. Exiting.")
    sys.exit(0)

# Build the system message dynamically
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
        temperature=0.7,               # controls creativity
        max_output_tokens=800,         # roughly limits output length
        top_p=1,
        store=False,                   # don't store this response in project history
        include=[]                     # no need for additional info like web sources
    )

except Exception as e:
    print(f"❌ API call failed: {e}")
    sys.exit(1)

# Extract and display the text result
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

Common API errors:
• 401/403 – authentication issue (check your API key)
• 400 – missing or malformed parameter (like forgetting 'input')
• 429 – rate limit exceeded
• 500+ – temporary service problem (retry later)
"""

