from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# prompt = """
# You are a senior global shipping planner for a major container line.

# Context:
# - Origin port: Nhava Sheva (JNPT), India
# - Destination port: Rotterdam, Netherlands
# - Number of containers: 250
# - Cargo value per container: $50,000
# - Vessel must depart within: 36 hours

# Tasks:
# 1. Use internet search to check current port disruptions, weather alerts, strikes, conflicts, or delays affecting this route.
# 2. Summarize risks that could impact sailing in the next 7–14 days.
# 3. Propose 2–3 routing or departure strategies.
# 4. Calculate expected delay costs for each strategy.
# 5. Recommend the best strategy.

# IMPORTANT:
# 👉 After giving the final answer, EXPLAIN YOUR REASONING step-by-step.
# 👉 Show your calculations clearly.
# 👉 Separate your explanation under a heading: “Reasoning Process”.
# """


# response = client.responses.create(
#     model="gpt-5-nano",   # must support web search
#     reasoning={"effort": "medium"},

#     tools=[ {"type": "web_search_preview"} ],   # enables live internet search

#     input=[
#         {
#             "role": "user",
#             "content": prompt
#         }
#     ]
# )

# print("=" * 80)
# print("CASE 1: Shipping Route Planning")
# print("=" * 80)
# print(response.output_text)


# Case 2: Logic Puzzle
print("\n" + "=" * 80)
print("CASE 2: Logic Puzzle - Houses and Pets")
print("=" * 80 + "\n")

prompt2 = """
Alice, Bob, and Carol each live in a different house on the same street: red, green, and blue.
The person who lives in the red house owns a cat.
Bob does not live in the green house.
Alice owns a Dog.
The green house is to the immediate left of the red house.
Carol does not own a cat.
Alice lives to the immediate left of Carol.
Dog owner house has no neighbour on left.
Who lives in each house, and what pet do they own?

IMPORTANT:
👉 After giving the final answer, EXPLAIN YOUR REASONING step-by-step.
👉 Show your logical deduction process clearly.
👉 Separate your explanation under a heading: "Reasoning Process".
"""

response2 = client.responses.create(
    model="gpt-5-nano",
    reasoning={"effort": "medium"},
    
    input=[
        {
            "role": "user",
            "content": prompt2
        }
    ]
)

print(response2.output_text)
