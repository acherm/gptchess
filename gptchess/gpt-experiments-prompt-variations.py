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

# TODO: The 'openai.organization' option isn't read in the client API. You will need to pass it when you instantiate the client, e.g. 'OpenAI(organization="")'
# openai.organization = "" 


def setup_directory():
    OUTPUT_DIR = "games/"
    dir_name = OUTPUT_DIR + "game" + str(uuid.uuid4())
    os.makedirs(dir_name, exist_ok=True)
    return dir_name

def log_msg(dir_name, message):
    with open(os.path.join(dir_name, "log.txt"), "a") as log_file:
        log_file.write(message + "\n")

def record_session(dir_name, prompt, response, system_role_message = None):
    with open(os.path.join(dir_name, "session.txt"), "a") as session_file:
        if system_role_message is not None:
            session_file.write("SYSTEM: " + system_role_message + "\n")
        session_file.write("PROMPT: " + prompt + "\n")      
        session_file.write("RESPONSE: " + response + "\n\n")


@dataclass
class GPTConfig:
    temperature: float = 0
    max_tokens: int = 4
    chat_gpt: bool = False
    system_role_message: str = None
    model_gpt: str = "gpt-3.5-turbo-instruct"

 
def play_game(gpt_config: GPTConfig, base_prompt=""):
    
    

    temperature = gpt_config.temperature
    max_tokens = gpt_config.max_tokens
    model_gpt = gpt_config.model_gpt

    

    

    board = chess.Board()
    
    unknown_san = None # can be the case that GPT plays an unknown SAN (invalid move)
        

 
    response = client.completions.create(model=model_gpt,
    prompt=base_prompt,
    temperature=temperature,
    max_tokens=max_tokens)


    resp = response.choices[0].text # completion 
    move = extract_move_chatgpt(resp)

 
    return move
      
import random

def mk_chess_prompt(result="1-0", black_name=None, white_name=None, black_elo=None, white_elo=None,
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

    # Construct the PGN header with the configurable options
    pgn_headers = f"""[Event "FIDE World Championship Match 2024"]
[Site "Los Angeles, USA"]
[Date "2024.12.01"]
[Round "5"]
[White "{white_name}"]
[Black "{black_name}"]
[Result "{result}"]
[WhiteElo "{white_elo}"]
{white_title}
[BlackElo "{black_elo}"]
{black_title}
[TimeControl "40/7200:20/3600:900+30"]
[UTCDate "2024.11.27"]
[UTCTime "09:01:25"]
[Variant "Standard"]
"""

    pgn_position = "1. e4 e5 2. Bc4 Nc6 3. Qh5"
    return pgn_headers + '\n' + pgn_position





gpt_config = GPTConfig(
    model_gpt="gpt-3.5-turbo-instruct",
    temperature=0.0,
    max_tokens=5,
    chat_gpt=False,
    system_role_message=None  # Since it wasn't provided in the original call
)

# Call the refactored function.


# Example usage
prompt = mk_chess_prompt(result="0-1", black_name="Kasparov, Gary", white_name="Kramnik, Vladimir")
print(prompt)
res = play_game(gpt_config, base_prompt=prompt)
print(res)

prompt2 = mk_chess_prompt(result="1-0", black_name="XXX", white_name="YYY", black_elo=1000, white_elo=1000, include_black_title=False, include_white_title=False)
print(prompt2)
res2 = play_game(gpt_config, base_prompt=prompt2)
print(res2)

import pandas as pd
import itertools
import random

# Define possible values for each parameter
results = ["1-0", "1/2-1/2", "0-1"]
# results = ["1-0", "0-1"]
names = ["Nepomniachtchi, Ian", "Kramnik, Vladimir", "Giraud, Thibaut", "Louapre, David", "XXX"] # ["Nepomniachtchi, Ian", "Kramnik, Vladimir", "Kasparov, Gary", "Giraud, Thibaut", "Louapre, David"]
elos = [1000, 1400, 1700, 1800, 2000, 2900]
# include_title = [True, False]
include_title = [False]

# Create DataFrame
df = pd.DataFrame(columns=["Result", "WhiteName", "BlackName", "WhiteElo", "BlackElo", "IncludeWhiteTitle", "IncludeBlackTitle", "Move"])

data = []  # List to collect all row data


# Generate configurations and populate the list
# black elo = white elo to simplify 
for result, white_elo, include_white_title, include_black_title in itertools.product(
    results, elos, include_title, include_title):
    for white_name in names:
        for black_name in [name for name in names if name != white_name]:
            prompt = mk_chess_prompt(result=result, black_name=black_name, white_name=white_name,
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
            print("new data", data)

# Convert list of dictionaries to DataFrame
df = pd.DataFrame(data)


# Explicitly convert boolean columns if needed
df['IncludeWhiteTitle'] = df['IncludeWhiteTitle'].astype(bool)
df['IncludeBlackTitle'] = df['IncludeBlackTitle'].astype(bool)

print(df.head())

df.to_csv("prompt_variations_phi.csv", index=False)











