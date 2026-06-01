from nicegui import ui
from src.pages import setup
from src.data import players, roles
import os

@ui.page("/")
async def home_page():
    """
    App start page. Shows each created game and lets 
    the user create a new game.
    """
    ui.label('Welcome to CSE Mafia!')
    
    #loads the data files for the provided game name, or creates 
    #them if they do not exist.
    async def load_game(name:str):
        game_folder = f'./games/{name}'
        if not os.path.exists(game_folder):
            os.mkdir(game_folder)
        await players.load_players(name)
        await roles.load_roles(name)
    #Button for creating a new game
    #triggers popup asking for a name
    with ui.dialog() as create_dialog, ui.card():
        ui.label('Create New Game')
        user_input = ui.input(placeholder='Game Name')
        with ui.row():
            ui.button('Cancel', on_click=lambda: create_dialog.close())
            create_btn = ui.button('Create', on_click=lambda: create_dialog.submit(user_input.value))
            #prevents creating new game without being named first
            create_btn.bind_enabled_from(user_input, 'value', backward=lambda val: bool(val and val.strip()))
            
    async def show_popup():
        result = await create_dialog
        if result != None:
            await load_game(result)
            ui.navigate.to(f'/setup/{result}')
            

    ui.button('New Game', on_click=show_popup)
