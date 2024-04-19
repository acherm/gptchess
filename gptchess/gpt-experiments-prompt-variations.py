#!/usr/bin/env python3

import io
import random
from stockfish import Stockfish

import openai
import chess
import chess.pgn
import os

from dataclasses import dataclass

from parsing_moves_gpt import extract_move_chatgpt

import uuid

openai.organization = "" 
openai.api_key = os.getenv('OPENAI_KEY')


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
        

 
    response = openai.Completion.create(
                model=model_gpt,
                prompt=base_prompt,
                temperature=temperature,
                max_tokens=max_tokens,
            )

    resp = response.choices[0].text # completion 




    san_move = resp.strip().split()[0]
    
    try:
        move = board.push_san(san_move)
    except:
        unknown_san = san_move
        return        

 
    return resp
      
BASE_PGN_HEADERS =  """[Event "FIDE World Championship Match 2024"]
[Site "Los Angeles, USA"]
[Date "2024.12.01"]
[Round "5"]
[White "Carlsen, Magnus"]
[Black "Nepomniachtchi, Ian"]
[Result "1-0"]
[WhiteElo "2885"]
[WhiteTitle "GM"]
[WhiteFideId "1503014"]
[BlackElo "2812"]
[BlackTitle "GM"]
[BlackFideId "4168119"]
[TimeControl "40/7200:20/3600:900+30"]
[UTCDate "2024.11.27"]
[UTCTime "09:01:25"]
[Variant "Standard"]
"""

PGN_POSITION = "1. e4 e5 2. Bc4 Nc6 3. Qh5"




gpt_config = GPTConfig(
    model_gpt="gpt-3.5-turbo-instruct",
    temperature=0.0,
    max_tokens=5,
    chat_gpt=False,
    system_role_message=None  # Since it wasn't provided in the original call
)

# Call the refactored function.


def mk_chess_prompt():
    return BASE_PGN_HEADERS + PGN_POSITION

prompt = mk_chess_prompt()
res = play_game(gpt_config, base_prompt=prompt)
print(res)












