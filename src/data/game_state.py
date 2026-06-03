import json
from src.data import player, players_setup, roles_setup

'''Manages the loading and saving of the game state'''

game_state = {}
filepath = ""
filename = ""

#create initial game state
async def init_game(name:str):
    global filepath
    filepath = f'./games/{name}/'
    global filename
    filename = f'{name}_game_state.txt'
    for index, person in enumerate(players_setup.players):
        game_state[f'{index}'] = player.Player(id=index, player_name=person, role=roles_setup.roles[index])
    await save_game()

#load game state from file
async def load_game(name: str):
    global filepath
    filepath = f'./games/{name}/'
    global filename
    filename = f'{name}_game_state.txt'
    global game_state
    game_state = {}
    try:
        with open(filepath+filename, "r") as file:
            first_char = file.read(1)
            if not first_char:
                await init_game(name)
            else:
                file.seek(0)
                for line in file:
                    clean_json = line.strip()
                    person = player.Player.from_json(clean_json)
                    game_state[f'{person.id}'] = person
    except FileNotFoundError:
        # Create the file because it does not exist
        print('Error: No Game State Found')

#write game roles to file
async def save_game():
    if filepath and filename:
        try:
            with open(filepath+filename, "w") as file:
                for person in game_state.values():
                    file.write(f"{person}\n")
        except FileNotFoundError:
            print('Error: No Game File')
