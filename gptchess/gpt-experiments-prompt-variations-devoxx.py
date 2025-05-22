#!/usr/bin/env python3
import os, itertools, random, pandas as pd
from dataclasses import dataclass
from openai import OpenAI
from parsing_moves_gpt import extract_move_chatgpt

# --------------------------------------------------------------------------- #
#  OpenAI client
# --------------------------------------------------------------------------- #
client = OpenAI(api_key=os.getenv("OPENAI_KEY"))

# --------------------------------------------------------------------------- #
#  Minimal PGN prompt with only the two ELO headers
# --------------------------------------------------------------------------- #
def mk_chess_prompt_elo_only(white_elo: int, black_elo: int) -> str:
    pgn_headers = f"""[WhiteElo "{white_elo}"]
[BlackElo "{black_elo}"]"""
    moves_so_far = "1. e4 d6 2. Bb5+"
    return f"{pgn_headers}\n\n{moves_so_far}"

# --------------------------------------------------------------------------- #
#  Single call to GPT that returns the first move in SAN
# --------------------------------------------------------------------------- #
def play_game(prompt: str, temperature: float, max_tokens: int, model: str = "gpt-3.5-turbo-instruct") -> str:
    resp = client.completions.create(
        model=model,
        prompt=prompt,
        temperature=temperature,
        max_tokens=max_tokens,
    )
    return extract_move_chatgpt(resp.choices[0].text)

# --------------------------------------------------------------------------- #
#  Experimental grid
# --------------------------------------------------------------------------- #
elos          = [1000, 1400, 1800, 2200, 2600, 2900]
temperatures  = [round(x, 1) for x in (0.0, 0.2, 0.4, 0.6, 0.8, 1.0)]
max_token_set = [5, 10]

rows = []

for white_elo, black_elo, T, max_tok in itertools.product(elos, elos, temperatures, max_token_set):
    prompt = mk_chess_prompt_elo_only(white_elo, black_elo)
    move   = play_game(prompt, temperature=T, max_tokens=max_tok)
    rows.append({
        "WhiteElo":   white_elo,
        "BlackElo":   black_elo,
        "Temperature": T,
        "MaxTokens":   max_tok,
        "Move":        move,
    })
    print(f"{white_elo}-{black_elo} | T={T} | max_tok={max_tok} → {move}")

# --------------------------------------------------------------------------- #
#  Save as CSV
# --------------------------------------------------------------------------- #
df = pd.DataFrame(rows)
df.to_csv("elo_only_with_gpt_params.csv", index=False)
print("Saved → elo_only_with_gpt_params.csv")
