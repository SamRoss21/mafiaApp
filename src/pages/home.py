from nicegui import ui
from src.pages import setup

@ui.page("/")
async def home_page():
    """
    App start page. Shows each created game and lets 
    the user create a new game.
    """
    ui.label('Welcome to CSE Mafia!')

    with ui.dialog() as dialog, ui.card():
        ui.label('Create New Game')
        user_input = ui.input(placeholder='Game Name')
        with ui.row():
            ui.button('Cancel', on_click=lambda: dialog.close())
            ui.button('Create', on_click=lambda: dialog.submit(user_input.value))
            

    async def show_popup():
        result = await dialog
        if dialog != None:
            ui.navigate.to(f'/setup/{result}')
        ui.notify(f'You clicked: {result}')

    ui.button('New Game', on_click=show_popup)
