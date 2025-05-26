from openai import OpenAI
client = OpenAI()                     # uses OPENAI_API_KEY

prompt = """
Instructions:
- You are a professional chess player.
- You are playing a serious chess game, using PGN notation.
- When it's your turn, you have to play your move using PGN notation.
- For formatting your final decision, use <played_move>...</played_move> tags.

1. e4
"""

resp = client.responses.create(
    model="o3",
    # reasoning={"effort": "low", "summary": "detailed"},
    reasoning={"effort": "low"},
    input=[
        {
        "role": "user",
        "content": prompt
        }
    ],
    # input="1.",                       # user prompt
    # max_tokens=6                      # ≤ 6 tokens is plenty for one SAN move
)
print(resp.output_text.strip())
# print(resp.summary) # → e4
