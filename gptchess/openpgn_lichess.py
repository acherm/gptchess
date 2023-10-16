import requests
import sys 

TOKEN_LICHESS="" # prerequisite: create a token in your lichess account

# very specific utility to upload a game to lichess out of a game folder of the database
def mk_lichessURL(game_folder):
    # Define the URL and header
    url = "https://lichess.org/api/import"
    headers = {
        "Authorization": "Bearer {}".format(TOKEN_LICHESS)  
    }

    # Read the file content
    with open("../games/{}/game.pgn".format(game_folder), "r") as file:
        pgn_data = file.read()

    # Prepare the data payload
    data = {
        "pgn": pgn_data
    }

    # Make the POST request
    response = requests.post(url, headers=headers, data=data)

    return response.json()['url']

# first argument is the game_folder path
# eg  python3 openpgn_lichess.py gamea9168c1b-a985-4794-b8cf-f68cdbf2122b
if __name__ == "__main__":
    args = sys.argv
    game_folder = args[1]
    print(mk_lichessURL(game_folder))


