from functools import partial
from nicegui import ui
from src.pages import setup
from src.data import players_setup, roles_setup, game_state
import os
from pathlib import Path


def get_games():
    games_folder_path = Path("./games/")
    folder_names = [x.name for x in games_folder_path.iterdir() if x.is_dir()]
    return folder_names


@ui.page("/")
async def home_page():
    """
    App start page. Shows each created game and lets
    the user create a new game.
    """

    # loads the data files for the provided game name, or creates
    # them if they do not exist.
    async def load_game(name: str):
        game_folder = f"./games/{name}"
        if not os.path.exists(game_folder):
            os.mkdir(game_folder)
        await players_setup.load_players(name)
        await roles_setup.load_roles(name)
        #if blank game go to setup, otherwise gameplay
        if not players_setup.players and not roles_setup.roles:
            ui.navigate.to(f"/setup/{name}")
        else:
            await game_state.load_game(name)
            ui.navigate.to(f"/gameplay/{name}")
        

    async def show_popup():
        result = await create_dialog
        if result != None:
            await load_game(result)

    # Dialog for creating a new game
    # prompts user to input a game name
    #if they put a name that already exists they will just open the existing game
    with ui.dialog() as create_dialog, ui.card():
        ui.label("Create New Game")
        user_input = ui.input(placeholder="Game Name")
        with ui.row():
            ui.button("Cancel", on_click=lambda: create_dialog.close())
            create_btn = ui.button(
                "Create", on_click=lambda: create_dialog.submit(user_input.value)
            )
            # prevents creating new game without being named first
            create_btn.bind_enabled_from(
                user_input, "value", backward=lambda val: bool(val and val.strip())
            )

    #card grid representing each existing game
    with ui.column().classes("w-full justify-center items-center"):
        ui.label("Welcome to CSE Mafia!").classes("pt-10 text-3xl font-bold mb-2")
        with ui.scroll_area().classes("w-full h-200 justify-center items-center"):
            with ui.row().classes("w-full justify-center items-center"):
                with ui.column().classes("w-2/3 h-full justify-center items-center"):
                    with ui.row().classes("w-full justify-center items-center"):
                        with ui.card().classes("h-40 w-40 justify-center items-center"):
                            with ui.button(
                                color=None, on_click=partial(show_popup)
                            ).classes("w-full h-full").props("flat"):
                                with ui.column().classes("justify-center items-center"):
                                    ui.icon("sym_r_add").props("size=xl")
                                    ui.label("New Game")
                        for game in get_games():
                            with ui.card().classes(
                                "h-40 w-40 justify-center items-center"
                            ):
                                ui.button(
                                    game, color=None, on_click=partial(load_game, game)
                                ).classes("w-full h-full text-xl").props("flat")
