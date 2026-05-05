"""Example Azure OpenAI conversation for customer feedback analysis.

This script connects to an Azure AI Project, posts a piece of customer
feedback, and prints the agent's response.  The example uses Azure's Agents
API, which manages the conversation thread for you.

Market research use case
------------------------
Azure AI Agents are pre-configured assistants that a team can share.  You can
give them a persona (e.g. "You are a market research analyst specialising in FMCG
brands"), point them at a specific knowledge base, and query them repeatedly
without rewriting instructions each time.  This script shows the minimum code
needed to send a piece of customer feedback and read the agent's interpretation.

What you will learn from this script
-------------------------------------
* How to authenticate with Azure using environment variables (no secrets in code).
* How to create a conversation thread and send a message to an Azure Agent.
* How to retrieve and print the agent's reply from the thread history.

Before you start
----------------
1. Install the required packages::

       pip install azure-ai-projects azure-identity python-dotenv

2. Copy ``.env.example`` to ``.env`` and fill in your Azure credentials::

       AZURE_ENDPOINT=https://your-resource.services.ai.azure.com/api/projects/your-project
       AZURE_AGENT_ID=asst_your-agent-id

   Then add your authentication details (either ``AZURE_CLIENT_ID``,
   ``AZURE_TENANT_ID``, ``AZURE_CLIENT_SECRET`` for a service principal, or
   simply run ``az login`` in a terminal if you have the Azure CLI installed).

3. Ensure you have access to an Azure AI Project and know the Agent ID from
   the Azure portal.

Running in VS Code
------------------
1. Open ``4_azure_agent.py`` in the editor.
2. Confirm your ``.env`` file has ``AZURE_ENDPOINT`` and ``AZURE_AGENT_ID`` set.
3. Press ``Ctrl+F5`` (``Cmd+F5`` on macOS) to run without debugging.
4. Watch the integrated terminal for the agent's reply.

Note: Scripts 4 and 5 are legacy examples from an earlier version of the
course that used Azure AI Foundry.  They are kept for reference.  The main
course flow now uses Scripts 1–3 and 6–9.
"""

import os
import sys
from typing import Any, Sequence

from azure.ai.projects import AIProjectClient
from azure.ai.agents.models import ListSortOrder
from azure.identity import DefaultAzureCredential
from dotenv import load_dotenv


# -----------------------------------------------------------------------
# LOAD CONFIGURATION FROM .env
# We read the Azure endpoint and agent ID from a .env file so that real
# credentials never appear in the script itself.  Anyone who clones this
# repository cannot accidentally see your private Azure settings.
# -----------------------------------------------------------------------
load_dotenv()

AZURE_ENDPOINT = os.getenv("AZURE_ENDPOINT")
AGENT_ID = os.getenv("AZURE_AGENT_ID")

if not AZURE_ENDPOINT:
    print("❌  AZURE_ENDPOINT is not set.")
    print("    Copy .env.example to .env and fill in your Azure endpoint URL.")
    sys.exit(1)

if not AGENT_ID:
    print("❌  AZURE_AGENT_ID is not set.")
    print("    Copy .env.example to .env and fill in your Agent ID from the Azure portal.")
    sys.exit(1)


def main() -> None:
    """Send a customer comment to an Azure agent and print the response.

    This function orchestrates the full workflow:
    authenticate → load agent → create thread → post message → run → print reply.
    """

    print("=" * 60)
    print("  MRS Advanced Course — Azure Agent Demo")
    print("=" * 60)

    # -----------------------------------------------------------------------
    # AUTHENTICATE WITH AZURE
    # DefaultAzureCredential tries several sign-in methods automatically:
    # environment variables first, then managed identity, then Azure CLI.
    # This keeps the example secure — no secrets are stored in the code.
    # -----------------------------------------------------------------------
    try:
        project = AIProjectClient(
            credential=DefaultAzureCredential(),
            endpoint=AZURE_ENDPOINT,
        )
    except Exception as error:
        print(f"❌  Could not connect to Azure: {error}")
        print("    Check that AZURE_ENDPOINT is correct and your credentials are valid.")
        sys.exit(1)

    # -----------------------------------------------------------------------
    # LOAD THE AGENT
    # An Azure Agent is a pre-configured assistant stored in the portal.
    # We retrieve it by ID so we can send messages and read its replies.
    # -----------------------------------------------------------------------
    try:
        agent = project.agents.get_agent(AGENT_ID)
        print(f"\n✅  Loaded agent: {agent.name}")
    except Exception as error:
        print(f"❌  Could not retrieve agent ID '{AGENT_ID}': {error}")
        print("    Check that AZURE_AGENT_ID is correct and you have access to the project.")
        sys.exit(1)

    # -----------------------------------------------------------------------
    # CREATE A CONVERSATION THREAD
    # Each thread keeps this conversation's history separate.  Every time you
    # run the script you get a fresh thread, so previous experiments never
    # bleed into today's demo.
    # -----------------------------------------------------------------------
    thread = project.agents.threads.create()
    print(f"   Thread created: {thread.id}")

    # -----------------------------------------------------------------------
    # POST THE CUSTOMER FEEDBACK
    # Replace the text below with a real verbatim comment from your dataset.
    # The more realistic the input, the more useful the agent's output will
    # be during live demonstrations.
    # -----------------------------------------------------------------------
    feedback_text = (
        "I really liked the steak but the dessert was too sweet and the service was slow."
    )

    print(f"\n📝  Sending feedback to agent:\n   \"{feedback_text}\"\n")

    project.agents.messages.create(
        thread_id=thread.id,
        role="user",           # "user" means the message comes from us, not the agent
        content=feedback_text,
    )

    # -----------------------------------------------------------------------
    # RUN THE AGENT AND WAIT FOR A RESPONSE
    # create_and_process sends the thread to Azure and blocks until the agent
    # has finished generating a reply.  This is the simplest approach for a
    # workshop demo where we want to wait for the full answer before continuing.
    # -----------------------------------------------------------------------
    run = project.agents.runs.create_and_process(
        thread_id=thread.id,
        agent_id=agent.id,
    )

    if run.status == "failed":
        # When something goes wrong Azure returns a diagnostic message.
        # Printing it helps you adjust credentials or message content.
        print(f"❌  Run failed: {run.last_error}")
        return

    # -----------------------------------------------------------------------
    # READ AND PRINT THE FULL CONVERSATION
    # We retrieve all messages in chronological order so the exchange reads
    # naturally: our prompt first, then the agent's reply.
    # -----------------------------------------------------------------------
    messages = project.agents.messages.list(
        thread_id=thread.id,
        order=ListSortOrder.ASCENDING,    # oldest message first
    )

    print("-" * 40)
    for message in messages:
        _print_text_message(message.role, message.text_messages)
    print("-" * 40)
    print("\n✅  Done!")


def _print_text_message(role: str, text_messages: Sequence[Any]) -> None:
    """Print the latest text snippet for one side of the conversation.

    Azure messages can contain non-text payloads (file attachments, tool
    outputs).  This helper extracts only the plain-text portion so the
    console output stays readable during a demo.

    Args:
        role (str): Either ``"user"`` or ``"assistant"``.
        text_messages (Sequence): The list of text content items returned by
            the Azure SDK for this message.
    """

    if not text_messages:
        # Some messages may only contain non-text payloads; skip those.
        return

    latest = text_messages[-1].text.value
    label = "You" if role == "user" else "Agent"
    print(f"\n{label}: {latest}")


if __name__ == "__main__":
    main()
