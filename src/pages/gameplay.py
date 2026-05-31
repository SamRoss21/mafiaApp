from nicegui import ui

@ui.page('/gameplay/{name}')
async def gameplay(name: str):
    """
    Gameplay page. User can record night actions, run the game solver, and 
    see the outcomes of each night.
    """
    ui.label(f'{name}')
