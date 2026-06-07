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
    filename = f'{name}_current_game_state.txt'
    global game_state
    game_state = {}
    for index, person in enumerate(players_setup.players):
        player_obj = player.Player(id=index, player_name=person, role=roles_setup.roles[index])
        player_obj.current_items = player_obj.role.items.copy()
        game_state[f'{index}'] = player_obj
        
    await save_game()

#load game state from file
async def load_game(name: str):
    global filepath
    filepath = f'./games/{name}/'
    global filename
    filename = f'{name}_current_game_state.txt'
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
        await init_game(name)
        await load_game(name)

#write game state to file
async def save_game():
    if filepath and filename:
        try:
            with open(filepath+filename, "w") as file:
                for person in game_state.values():
                    file.write(f"{person}\n")
        except FileNotFoundError:
            print('Error: No Game File')

#write game roles to file
async def save_night_state(name, night):
    filepath = f'./games/{name}/'
    file_name = f"{name}_{night}_state.txt"
    try:
        with open(filepath+file_name, "w") as file:
            for person in game_state.values():
                file.write(f"{person}\n")
    except FileNotFoundError:
        print('Error: No Game File')

async def revert_to_night(name, night):
    filepath = f'./games/{name}/'
    file_name = f"{name}_{night}_state.txt"
    try:
        with open(filepath+file_name, "r") as file:
            first_char = file.read(1)
            if not first_char:
                print(f"Error: {night} state has no data")
            else:
                file.seek(0)
                for line in file:
                    clean_json = line.strip()
                    person = player.Player.from_json(clean_json)
                    game_state[f'{person.id}'] = person
                await save_game()
    except FileNotFoundError:
        print(f"Error: {night} state not found")
