"""Example Azure OpenAI conversation for customer feedback analysis.

This script connects to an Azure AI Project, posts a piece of customer
feedback, and prints the agent's response.  The example uses Azure's Agents
API, which manages the conversation thread for you.

Before you start
----------------
1. Install the required packages: ``pip install azure-ai-projects azure-identity``.
2. Ensure you have access to an Azure AI Project and the **Agent ID** you want
   to use (replace the placeholder below with your own value).
3. Set the following environment variables so ``DefaultAzureCredential`` can
   authenticate you:
   * ``AZURE_CLIENT_ID``
   * ``AZURE_TENANT_ID``
   * ``AZURE_CLIENT_SECRET`` (or use ``az login`` if you have the Azure CLI
     installed and prefer interactive authentication).

Running in VS Code
------------------
1. Open ``4 Azure API call.py`` in the editor.
2. Update ``AZURE_ENDPOINT`` and ``AGENT_ID`` below to match your Azure setup.
3. Press ``Ctrl+F5`` (``Cmd+F5`` on macOS) to run without debugging.
4. Watch the integrated terminal for the agent's reply.

Tip: Keep your credentials out of the script.  Environment variables or the
Azure CLI are safer than hard-coding secrets.
"""

from typing import Any, Sequence

from azure.ai.projects import AIProjectClient
from azure.ai.agents.models import ListSortOrder
from azure.identity import DefaultAzureCredential


# Replace these with values from your own Azure AI Project portal.
AZURE_ENDPOINT = "https://kw647-5564-resource.services.ai.azure.com/api/projects/kw647-5564"
AGENT_ID = "asst_aWOiJSGXSEJE2MnnCih3GTJZ"


def main() -> None:
    """Send a customer comment to an Azure agent and print the response."""

    # Create a project client. DefaultAzureCredential tries several sign-in
    # methods automatically (service principal, managed identity, CLI login).
    project = AIProjectClient(credential=DefaultAzureCredential(), endpoint=AZURE_ENDPOINT)

    # Retrieve the agent definition.  Agents hold the instructions and tools
    # configured in the Azure portal.
    agent = project.agents.get_agent(AGENT_ID)

    # Start a new thread to keep this conversation's history separate.
    thread = project.agents.threads.create()
    print(f"Created thread, ID: {thread.id}")

    # Post a user message.  Replace this text with your own customer feedback.
    feedback_text = (
        "I really liked the steak but the dessert was too sweet and the service was slow."
    )
    project.agents.messages.create(
        thread_id=thread.id,
        role="user",
        content=feedback_text,
    )

    # Kick off the agent run and wait for it to finish.
    run = project.agents.runs.create_and_process(thread_id=thread.id, agent_id=agent.id)

    if run.status == "failed":
        print(f"Run failed: {run.last_error}")
        return

    # Retrieve the messages in order so the conversation reads naturally.
    messages = project.agents.messages.list(thread_id=thread.id, order=ListSortOrder.ASCENDING)
    for message in messages:
        _print_text_message(message.role, message.text_messages)


def _print_text_message(role: str, text_messages: Sequence[Any]) -> None:
    """Safely print the latest text snippet for a conversation role."""

    if not text_messages:
        return

    latest = text_messages[-1].text.value
    print(f"{role}: {latest}")


if __name__ == "__main__":
    main()
