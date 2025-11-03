from openai import OpenAI
client = OpenAI()

response = client.responses.create(
  model="gpt-4o-mini",
  input=[
    {
      "role": "system",
      "content": [
        {
          "type": "input_text",
          "text": "You are a super helpful AI"
        }
      ]
    },
    {
      "role": "user",
      "content": [
        {
          "type": "input_text",
          "text": "Tell me everything about Dogs"
        }
      ]
    }
  ],
  text={
    "format": {
      "type": "text"
    }
  },
  reasoning={},
  tools=[],
  temperature=1,
  max_output_tokens=2048,
  top_p=1,
  store=True,
  include=["web_search_call.action.sources"]
)

print(response)