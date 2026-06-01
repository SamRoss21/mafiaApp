import csv

players = []
filepath = ""
filename = ""

async def load_players(name: str):
    global filepath
    filepath = f'./games/{name}/'
    global filename
    filename = f'{name}_players.csv'
    try:
        with open(filepath+filename, "r") as file:
            content = csv.reader(file)
            global players 
            players = next(content, [])
    except FileNotFoundError:
        # Create the file because it does not exist
        with open(filepath+filename, "w") as file:
            file.write("")

async def set_players(players_csv: str):
    print(players_csv)
    players_csv = "" if players_csv is None else players_csv;
    global players
    players = players_csv.split(',')

    if filepath and filename:
        try:
            with open(filepath+filename, "w") as file:
                file.write(players_csv)
        except FileNotFoundError:
            print('Error: No Player File')

async def save_players():
    if filepath and filename:
        try:
            with open(filepath+filename, "w") as file:
                file.write(",".join(str(item) for item in players))
        except FileNotFoundError:
            print('Error: No Player File')