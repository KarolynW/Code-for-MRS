"""Call the OpenAI Responses API with a single prompt.

This script keeps the example intentionally small so you can see the bare
minimum needed to send a message to OpenAI and display the reply.  It is
designed for market researchers who are new to Python and want to understand
the building blocks of an AI call.

Before you run the script
-------------------------
1. Install the OpenAI Python package: `pip install openai`.
2. Create an environment variable called `OPENAI_API_KEY` that holds your API
   key.  In Windows PowerShell you can run
   `setx OPENAI_API_KEY "your-key-here"`.  On macOS/Linux use
   `export OPENAI_API_KEY="your-key-here"` (this lasts for the current
   terminal session).

How to run it from VS Code
--------------------------
1. Open this repository in VS Code and click the file `2 OpenAI Basic Call.py`.
2. Review the prompt text near the bottom and edit it if you want to ask a
   different question.
3. Press ``Ctrl+F5`` (``Cmd+F5`` on macOS) or click **Run > Run Without
   Debugging**.
4. Watch the **Python Terminal** pane for the formatted output from the model.

Tip: If you are unsure whether VS Code can see your API key, open a terminal
inside VS Code and run `echo $env:OPENAI_API_KEY` (PowerShell) or
`echo $OPENAI_API_KEY` (macOS/Linux) to verify.
"""

from openai import OpenAI

# Create an API client.  The library looks up the API key from the
# environment variable mentioned above, so no key needs to be written
# in your code.
client = OpenAI()

# ---------------------------------------------------------------
# 1. Define the conversation we want to send to the model.
# ---------------------------------------------------------------
system_message = "You are a super helpful AI. Keep answers easy to read."
user_question = "Tell me everything about Dogs"

conversation = [
    {
        "role": "system",
        "content": [{"type": "input_text", "text": system_message}],
    },
    {
        "role": "user",
        "content": [{"type": "input_text", "text": user_question}],
    },
]

# ---------------------------------------------------------------
# 2. Send the request to OpenAI.
# ---------------------------------------------------------------
# The fields below control how creative the response is and how long it can be.
response = client.responses.create(
    model="gpt-4o-mini",              # choose an efficient general model
    input=conversation,               # the messages we defined above
    text={"format": {"type": "text"}},
    reasoning={},                     # advanced options left empty
    tools=[],                         # no function-calling in this example
    temperature=0.8,                  # higher = more creative wording
    max_output_tokens=800,            # rough upper bound on word count
    top_p=1,
    store=False,                      # do not store the result in the project
    include=[],                       # no extra metadata required
)

# ---------------------------------------------------------------
# 3. Print a friendly summary for the user.
# ---------------------------------------------------------------
try:
    answer_text = response.output[0].content[0].text
except (AttributeError, IndexError):
    # If the response format changes we fall back to the raw object.
    answer_text = str(response)

print("✅ OpenAI call completed successfully!\n")
print(answer_text)
