from nicegui import ui
from src.pages import gameplay
from src.data import players

@ui.page('/setup/{name}')
async def setup(name: str):
    """
    Game setup page. User can add players, add roles, and match players
    to roles randomly or manually by arranging or randomizing the player/role 
    orders.
    """
    ui.label(f'Game Setup: {name}')
            
            
    async def show_player_popup():
        #Dialog for creating a new game
        #triggers popup asking for a name
        with ui.dialog() as player_dialog, ui.card():
            ui.label('Add Players')
            user_input = ui.textarea(value = ",".join(str(item) for item in players.players), placeholder='Insert player names in CSV format')
            with ui.row():
                ui.button('Cancel', on_click=lambda: player_dialog.submit(None))
                ui.button('Save', on_click=lambda: player_dialog.submit(user_input.value))
        result = await player_dialog
        if result != None:
            await players.set_players(result)
        player_dialog.clear()

    ui.button('Add Players', on_click=show_player_popup)

    ui.button('Start Game', on_click=lambda: ui.navigate.to(f'/gameplay/{name}'))
