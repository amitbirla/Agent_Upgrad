from openai import OpenAI
import json

from dotenv import load_dotenv

load_dotenv()
client = OpenAI()


response = client.responses.create(
    model="gpt-4o-mini",
    input="Tell me Upgrad inception story in 100 words.",
    instructions="Respond in a funny way and in Captain Jack Sparrow Style.",
    temperature=1,
    max_output_tokens=200,
    
)

print("Response from LLM with tool integration:", response.output_text)


# response = client.responses.create(
#     model="gpt-4o-mini",
#     input="65364*23563",
#     instructions="Be concise and factual.",
#     temperature=1,
#      tools=[
#         {"type": "code_interpreter", "container": {"type": "auto"}}
#     ],
    
#     max_output_tokens=200,
    
# )

# print("Response from LLM with tool integration:", response.output_text)


