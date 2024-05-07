# Debunking the Chessboard: Confronting GPTs Against Chess Engines to Estimate Elo Ratings and Assess Legal Move Abilities

Source code supporting experiments presented in https://blog.mathieuacher.com/GPTsChessEloRatingLegalMoves/ 
I've started with the GPT-3 chess experiment from https://github.com/clevcode/skynet-dev 
and explore the variability space of experiments (GPT variants, number of games, Stockfish skills, temperature, prompt, etc.)

## Install Python dependencies

```pip install openai chess stockfish```

for the analysis part, you'll also need libraries like `pandas` and `matplotlib`

## Install Stockfish

See https://stockfishchess.org/download/
I'm using the Linux `stockfish-ubuntu-x86-64-avx2` binary (version 16). 

## Run Chess experiment

```
export OPENAI_KEY=<your-openai-API-key>
python ./gptchess/gpt-experiments.py 
```

or if you want to run multiple games, you can use a loop like:

```
for i in {1..20}; do python gptchess/gpt-experiments.py; done
```

Edit the source code to change the GPT version, the number of games, the number of moves per game, etc.
Something like this:

```python
chess_config = ChessEngineConfig(
    skill_level=4,
    engine_depth=15,
    engine_time=None,
    random_engine=False
)

gpt_config = GPTConfig(
    model_gpt="gpt-3.5-turbo-instruct",
    temperature=0.0,
    max_tokens=5,
    chat_gpt=False,
    system_role_message=None  
)

play_game(chess_config, gpt_config, base_pgn=BASE_PGN, nmove=1, white_piece=False)
```

The outcome is located in `output` folder and is a subfolder, with the PGN file of the game, the log of the game, and the session with GPT.
You can then analyze the data with the Jupyter notebook `analysis.ipynb`.

### Data and analysis

For convenience, we have released the data used as part of the experiment documented in the blog post. 
It has been saved into the `games.tar.gz` of this repo. 
I'm usually using zenodo, but the size of the data is manageable.  
Decompress the archive to get `games` folder.

``` 
> ls
game30da9c70-31ed-4489-9e93-9ef179661da4  game6a246b94-4511-4b34-908a-6f1fd5b838ac  game98a79424-b219-4764-a4d8-71f524454923  gamec9ba4fa3-b7a9-4953-b8d5-a25db0e10886  gameffa12232-8e93-4440-82d8-a0c8a6023c63
game3179c6e9-935e-4f59-b932-268fd10356fc  game6a34daf4-4820-4eb0-a7ad-6a472d6506a2  game99371010-b5af-48d4-adbc-4fcfda798304  gameca445cfd-0076-4146-ba1b-c263c8cd8707
```

with plenty of folders. Each folder contains:
 * `game.pgn`: the PGN file of the game
 * `metainformation.txt` about configuration of the experiments
 * `log.txt` the log of the game
 * `session.txt` the session with GPT 

`games_db.csv` contains almost all information about all the games, in a structured way. 

`analysis.ipynb` is a Jupyter notebook to analyze the data.

## Update/Misc

 * new experiments based on `Monsieur Phi` suggestion/experiments (X/Twitter thread in french: https://twitter.com/MonsieurPhi/status/1781260337754366265), as a follow-up of his excellent video (in french again!) https://www.youtube.com/watch?v=6D1XIbkm4JE where I was interviewed. The basic idea is to study the impact of the prompt on the GPTs' playing skill, on the very specific position `1. e4 e5 2. Bc4 Nc6 3. Qh5`. I have to wrap-up, but the tldr is that the prompt has indeed a significant impact on the GPTs' playing skill (at least on this position!), and that we can identify intuitive patterns of prompt leading to either g6 or Nf6. See `gptchess/gpt-experiments-prompt-variations.py` and `analysis_prompt_variations.ipyng` and `prompt_variations_phi.csv`. 
 * In parallel, Yosha Iglesias has made a fantastic video: https://www.youtube.com/watch?v=FBx95bdJzh8 further exploring prompt sensitivity and surprising skills of GPT as well as many interesting ideas worth replicating in the large. Fascinating! `analysis_yosha.ipynb` is one ongoing/modest attempt to study the impact of prompt on the GPTs' playing skill (see also `games_yosha.tar.gz` and `games_db_yosha.csv`). Stay tuned for more experiments and analysis! 
 


