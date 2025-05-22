#!/usr/bin/env python3

import io
import random
from stockfish import Stockfish

import openai
from openai import OpenAI


import chess
import chess.pgn
import os

from dataclasses import dataclass

from parsing_moves_gpt import extract_move_chatgpt

import uuid

client = OpenAI(api_key=os.getenv('OPENAI_KEY'))




@dataclass
class GPTConfig:
    temperature: float = 0
    max_tokens: int = 4
    chat_gpt: bool = False
    system_role_message: str = None
    model_gpt: str = "gpt-3.5-turbo-instruct"

def save_metainformation_experiment(dir_name, gpt_config: GPTConfig, base_pgn):
    with open(os.path.join(dir_name, "metainformation.txt"), "w") as metainformation_file:
        metainformation_file.write(f"model_gpt: {gpt_config.model_gpt}\n")
        metainformation_file.write(f"base_pgn: {base_pgn}\n")
        metainformation_file.write(f"temperature: {gpt_config.temperature}\n")
        metainformation_file.write(f"max_tokens: {gpt_config.max_tokens}\n")
        metainformation_file.write(f"chat_gpt: {gpt_config.chat_gpt}\n")
        metainformation_file.write(f"system_role_message: {gpt_config.system_role_message if gpt_config.system_role_message else 'None'}\n")

 
def play_game(gpt_config: GPTConfig, base_prompt=""):
    
    

    temperature = gpt_config.temperature
    max_tokens = gpt_config.max_tokens
    model_gpt = gpt_config.model_gpt       

 
    response = client.completions.create(model=model_gpt,
    prompt=base_prompt,
    temperature=temperature,
    max_tokens=max_tokens,
    # logprobs=1
    )


    resp = response.choices[0].text # completion 
    move = extract_move_chatgpt(resp)

    # print(response)

 
    return move
      
import random

def mk_chess_prompt(pgn_position, result="1-0", black_name=None, white_name=None, black_elo=None, white_elo=None,
                    include_black_title=True, include_white_title=True):
    # List of possible player names
    names = ["Nepomniachtchi, Ian", "Kramnik, Vladimir", "Kasparov, Gary", "Giraud, Thibaut", "Louapre, David"]

    # Randomly choose names if not specified, ensuring they are not the same
    if not black_name:
        black_name = random.choice(names)
    if not white_name:
        white_name = random.choice([name for name in names if name != black_name])

    # Randomly assign Elo ratings if not specified
    if not black_elo:
        black_elo = random.choice(range(1000, 2901, 100))
    if not white_elo:
        white_elo = random.choice(range(1000, 2901, 100))

    # Optional GM titles
    black_title = "[BlackTitle \"GM\"]" if include_black_title else ""
    white_title = "[WhiteTitle \"GM\"]" if include_white_title else ""
    result_header = ""
    if result != '':
        result_header = f"[Result \"{result}\"]"

    # Construct the PGN header with the configurable options
    pgn_headers = f"""[Event "FIDE World Championship Match 2024"]
[Site "Los Angeles, USA"]
[Date "2024.12.01"]
[Round "5"]
[White "{white_name}"]
[Black "{black_name}"]
{result_header}
[WhiteElo "{white_elo}"]
{white_title}
[BlackElo "{black_elo}"]
{black_title}
[TimeControl "40/7200:20/3600:900+30"]
[UTCDate "2024.11.27"]
[UTCTime "09:01:25"]
[Variant "Standard"]
"""

    return pgn_headers + '\n' + pgn_position





gpt_config = GPTConfig(
    model_gpt="gpt-3.5-turbo-instruct",
    temperature=0.0,
    max_tokens=5,
    chat_gpt=False,
    system_role_message=None  # Since it wasn't provided in the original call
)

# Call the refactored function.
# pgn_position = "1. e4 e5 2. Bc4 Nc6 3. Qh5"
# pgn_position = "1. e4 d5 2. exd5 c6 3. dxc6 Nf6 4. cxb7 Bxb7 5. Nf3 e5 6. Nxe5 Bd6 7. Bb5+ Nbd7 8. Nxd7 Nxd7 9. Qe2+ Kf8 10. O-O Qh4 11. h3 Ne5 12. " # Hard!
# pgn_position = "1. d4 c6 2. Nf3 Nf6 3. c4 d5 4. e3 e6 5. Nc3 dxc4 6. Bxc4 b5 7. Bd3 b4 8. Ne4 Nxe4 9. Bxe4 Ba6 10. Qa4 Bb5 11. Qc2 Nd7 12. " # Bd2...
# pgn_position = "1. e4 d5 2. exd5 Nf6 3. d4 Qxd5 4. Nc3 Qe6+ 5. Be2 Qd7 6. Nf3 c6 7. Ne5 Qd8 8. Bc4 Nd5 9. Qf3 f6 10. Qh5+ g6 11. Nxg6 Bg4 12. Qxg4 hxg6 13. Qxg6+ Kd7 14. Nxd5 cxd5 15. "
# pgn_position = "1. Nf3 e6 2. d3 d5 3. Nfd2 " # Black
# pgn_position = "1. e4 d6 2. d4 Nf6 3. Nc3 Nfd7 4. " 
# pgn_position = "1. Nf3 d5 2. d4 Nf6 3. e3 e6 4. Nbd2 c5 5. Be2 Nc6 6. c3 Bd6 7. O-O O-O 8. Bd3 e5 9. e4 cxd4 10. exd5 Nxd5 11. Be4 Nf6 12. cxd4 exd4 13. Bxc6 bxc6 14. Nc4 c5 15. Nxd6 Qxd6 16. h3 Bb7 17. Qb3 Rab8 18. Re1 Bxf3 19. Qxf3 Rfe8 20. Bg5 Nd5 21. Bh4 Rxe1+ 22. Rxe1 Qd7 23. b3 h6 24. Re5 Nc3 25. Qg3 Re8 26. Qg4 Qxg4 27. Rxe8+ Kh7 28. hxg4 d3 29. Rd8 g5 30. Bg3 Ne2+ 31. Kf1 Nxg3+ 32. fxg3 c4 33. Ke1 c3 34. Kd1 d2 35. Rd7 Kg6 36. Rd3 c2+ 37. Kxc2 d1=Q+ 38. Kxd1 "
# pgn_position = "1. e4 d5 2. exd5 e5 3. dxe6 Qe7 4. "
# pgn_position = "1. Nf3 d5 2. d3 Nf6 3. Nfd2 e5 4. Nb3 Nc6 5. N3d2"
# pgn_position = "1. e4 Nc6 2. d4 e6 3. Nc3 Nce7 4. Nf3 Ng6 5. Be2 N6e7 6."
# pgn_position = "1. e4 Nc6 2. d4 e6 3. Nc3 Nce7 4. Nf3 Ng6 5. Be2 N6e7 6. O-O Ng6 7. Re1 N8e7 8."
# pgn_position = "1. e4 Nc6 2. d4 e6 3. Nc3 Nce7 4. Nf3 Ng6 5. Be2 N6e7 6. O-O Ng6 7. Re1 N8e7 8. Bf1 Nc6 9. d5 Nce7 10."
# pgn_position = "1. e4 Nc6 2. d4 e6 3. Nc3 Nce7 4. Nf3 Ng6 5. Be2 N6e7 6. O-O Ng6 7. Re1 N8e7 8. Bf1 Nc6 9. d5 Nce7 10. dxe6 fxe6 11."
# pgn_position = "1. e4 d5 2. exd5 e5 3. dxe6 Qe7 4."
# pgn_position = "1. e4 d5 2. exd5 e5 3. dxe6 Qe7 4. Nf3 Nd7 5."
# pgn_position = "1. e4 d5 2. exd5 e5 3. dxe6 Qe7 4. Nf3 Bd7 5."
# pgn_position = "1. e4 d5 2. exd5 e5 3. dxe6 Qe7 4. Nf3 Qb4 5."
# pgn_position = "1. e4 d5 2. exd5 e5 3. dxe6 Qe7 4. Nf3 a5 5."
# pgn_position = "1. e4 d5 2. exd5 e5 3. dxe6 Qe7 4. Nf3 a5 5. d4 Ra6 6."
# pgn_position = "1. e4 d5 2. exd5 e5 3. dxe6 Qe7 4. Nf3 a5 5. d4 Ra6 6. Bxa6 Nd7 7."
# pgn_position = "1. e4 d5 2. exd5 e6 3. dxe6 Qe7 4. Nf3 a5 5. d4 Ra6 6. Bxa6 Nd7 7."
# pgn_position = "1. e4 d5 2. exd5 e6 3. dxe6 Qe7 4. Nf3 Nd7 5."
# pgn_position = "1. e4 d5 2. exd5 e6 3. dxe6 Qe7 4. d4 a5 5. Be2 Ra6 6. Bxa6 Nd7 7."
# pgn_position = "1. e4 d5 2. exd5 a5 3. Nf3 e6 4. dxe6 Qe7 5. Bc4 Ra6 6. Bxa6 Nd7 7."
# pgn_position = "1. e4 d5 2. exd5 a5 3. Nc3 e5 4.  dxe6 Qe7 5. Bc4 Ra6 6. Bxa6 Nd7 7."
# pgn_position = "1. e4 d5 2. exd5 e6 3. dxe6 Qe7 4. Nf3 a5 5. d4 Ra6 6. Bxa6 Nd7 7."
# pgn_position = "1. e4 d5 2. exd5 e5 3. dxe6 Qe7 4."
# pgn_position = "1. e4 d5 2. exd5 e6 3."
# pgn_position = "1. e4 d5 2. exd5 e5 3. dxe6 Qe7 4. Nf3 a5 5. d4 Ra6 6. Bxa6 Nd7 7."
pgn_position = "1. e4 d5 2. exd5 e5 3. dxe6 Qe7 4. Nf3 a5 5. d4 Ra6 6. Bxa6 Nd7 7."
# pgn_position = "1. e4 d5 2. exd5 e5 3. dxe6 Qe7 4. Nf3 Nf6 5."
# pgn_position = "1."
prompt = mk_chess_prompt(pgn_position, result="1-0", white_name="Carlsen, Magnus", black_name="Nepomniachtchi, Ian", white_elo=2885, black_elo=2812)
print(prompt)
print("**********" * 5)
res = play_game(gpt_config, base_prompt=prompt)
print(res)

# prompt2 = mk_chess_prompt(result="1-0", black_name="XXX", white_name="YYY", black_elo=1000, white_elo=1000, include_black_title=False, include_white_title=False)
# print(prompt2)
# res2 = play_game(gpt_config, base_prompt=prompt2)
# print(res2)

import pandas as pd
import itertools
import random

# Define possible values for each parameter
# results = ["1-0", "1/2-1/2", "0-1"]
results = ["1-0", "0-1", "1/2-1/2", ""]
# results = ["1-0"]
# results = ["1-0", "0-1"]
# names = ["Nepomniachtchi, Ian", "Kramnik, Vladimir", "Kasparov, Garry", "Giraud, Thibaut", "Louapre, David", "XXX"] # FIXME: Garry, not Gary!
names = ["Carlsen, Magnus", "Nepomniachtchi, Ian", "Kramnik, Vladimir"] # , "Giraud, Thibaut", "Louapre, David", "XXX"]
# elos = [1000, 1400, 1700, 1800, 1900, 2000, 2900]
elos = [1400, 2900]
# include_title = [True, False]
include_title = [True, False]

# Create DataFrame
df = pd.DataFrame(columns=["Result", "WhiteName", "BlackName", "WhiteElo", "BlackElo", "IncludeWhiteTitle", "IncludeBlackTitle", "Move"])

data = []  # List to collect all row data


# Generate configurations and populate the list
# black elo = white elo to simplify 
for result, white_elo, include_white_title, include_black_title in itertools.product(
    results, elos, include_title, include_title):
    for white_name in names:
        for black_name in [name for name in names if name != white_name]:
            prompt = mk_chess_prompt(pgn_position, result=result, black_name=black_name, white_name=white_name,
                                     black_elo=white_elo, white_elo=white_elo,
                                     include_black_title=include_black_title, include_white_title=include_white_title)
            config = {
                "Result": result,
                "WhiteName": white_name,
                "BlackName": black_name,
                "WhiteElo": white_elo,
                "BlackElo": white_elo,
                "IncludeWhiteTitle": include_white_title,
                "IncludeBlackTitle": include_black_title,
                "Move": play_game(gpt_config, base_prompt=prompt)  # Using the generated prompt in play_game
            }
            data.append(config)
            print("new data",config)

# Convert list of dictionaries to DataFrame
df = pd.DataFrame(data)


# Explicitly convert boolean columns if needed
df['IncludeWhiteTitle'] = df['IncludeWhiteTitle'].astype(bool)
df['IncludeBlackTitle'] = df['IncludeBlackTitle'].astype(bool)

print(df.head())

folder_name = "positions_prompt_variations"

# get a unique identifier
hash_pgn = folder_name + "/" + str(uuid.uuid4())

# create a directory with hash_pgn as the name
os.mkdir(hash_pgn)

# save the CSV file in the directory
df.to_csv(f"{hash_pgn}/prompt_variations_results.csv", index=False)

save_metainformation_experiment(hash_pgn, gpt_config, pgn_position)

print("Saved to", hash_pgn)

# save the 











