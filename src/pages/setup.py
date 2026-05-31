from nicegui import ui
from src.pages import gameplay

@ui.page('/setup/{name}')
async def setup(name: str):
    """
    Game setup page. User can add players, add roles, and match players
    to roles randomly or manually by arranging or randomizing the player/role 
    orders.
    """
    ui.label(f'Game Setup: {name}')

    ui.button('Start Game', on_click=lambda: ui.navigate.to(f'/gameplay/{name}'))
