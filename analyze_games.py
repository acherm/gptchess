import os
import csv
import re

GAMES_DIR = 'games_o3'
OUTPUT_CSV = 'games_analysis.csv'

CSV_COLUMNS = [
    'subfolder',
    'gpt_model',
    'reasoning_effort',
    'number of moves played',
    'illegal move',
    'illegal_move_detail',
    'result of the game',
    'comments'
]

def parse_metainformation(path):
    gpt_model = None
    reasoning_effort = 'low'
    with open(path, 'r') as f:
        for line in f:
            if line.startswith('model_gpt:'):
                gpt_model = line.split(':', 1)[1].strip()
            elif line.startswith('reasoning_effort:'):
                reasoning_effort = line.split(':', 1)[1].strip()
    return gpt_model, reasoning_effort

def parse_pgn(path):
    result = None
    illegal_move = 'no'
    illegal_move_detail = ''
    moves = ''
    with open(path, 'r') as f:
        lines = f.readlines()
    for line in lines:
        if line.startswith('[Result '):
            result = line.split('"')[1]
        if line.startswith('[UnknownSAN '):
            illegal_move = 'yes'
            # Extract the illegal move detail from the header
            match = re.match(r'\[UnknownSAN\s+"([^"]+)"\]', line.strip())
            if match:
                illegal_move_detail = match.group(1)
            else:
                # Fallback: try to extract after the space
                illegal_move_detail = line.split(' ', 1)[1].strip('[]"\n')
        if not line.startswith('[') and line.strip():
            moves += ' ' + line.strip()
    # Count moves: each move number (e.g., 1., 2., ...) is a full move (white+black)
    move_numbers = re.findall(r'\b\d+\.', moves)
    # Count individual moves (not just full moves)
    move_tokens = re.findall(r'\b[a-hRNBQKO0-9][^\s]*', moves)
    # Remove move numbers and results from tokens
    move_tokens = [tok for tok in move_tokens if not re.match(r'\d+\.', tok) and tok not in ['1-0', '0-1', '1/2-1/2', '*']]
    number_of_moves = len(move_tokens)
    # Determine result
    if illegal_move == 'yes':
        result_of_game = 'defeat (illegal move)'
    elif result == '*':
        result_of_game = 'ongoing'
    elif result:
        result_of_game = result
    else:
        result_of_game = 'unknown'
    return number_of_moves, illegal_move, illegal_move_detail, result_of_game

def main():
    rows = []
    for subfolder in os.listdir(GAMES_DIR):
        subpath = os.path.join(GAMES_DIR, subfolder)
        if not os.path.isdir(subpath):
            continue
        meta_path = os.path.join(subpath, 'metainformation.txt')
        pgn_path = os.path.join(subpath, 'game.pgn')
        if not (os.path.exists(meta_path) and os.path.exists(pgn_path)):
            continue
        gpt_model, reasoning_effort = parse_metainformation(meta_path)
        number_of_moves, illegal_move, illegal_move_detail, result_of_game = parse_pgn(pgn_path)
        row = [
            subfolder,
            gpt_model or '',
            reasoning_effort,
            number_of_moves,
            illegal_move,
            illegal_move_detail,
            result_of_game,
            ''  # comments
        ]
        rows.append(row)
    with open(OUTPUT_CSV, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(CSV_COLUMNS)
        writer.writerows(rows)
    print(f'Analysis complete. Output written to {OUTPUT_CSV}')

if __name__ == '__main__':
    main() 