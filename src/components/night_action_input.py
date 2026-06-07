import asyncio
from functools import partial
from nicegui import ui
from src.data import game_state, role_definitions

# Dialog for adding roles
async def edit_action_popup(night, player):
    async def update_player_action(night, player, selections):
        phrase = construct_phrase(selections)
        command = construct_command(selections, player)
        await player.updateActions(phrase, command, night)
        action_dialog.close()
        future.set_result(None)

    future = asyncio.get_event_loop().create_future()

    with ui.dialog() as action_dialog, ui.card().classes("w-100 p-5").style(
                    "min-width: 400px; width: auto; max-width: none;"
                ):
        selections = night_action_input(night, player)

        with ui.row().classes('w-full items-end justify-end'):
            ui.button("Close", color=None, on_click=partial(update_player_action, night, player, selections)).props('flat')
        
        action_dialog.close()
        action_dialog.open()

        await future

def construct_phrase(selections):
    phrase = selections["phrase"]
    if 'action' in selections:
        action = selections["action"]
        targets = role_definitions.verbs[action]["targets"]
        if targets > 0:
            phrase = phrase + " " + selections['target1']
        if targets > 1:
            next_word = ""
            match (action):
                case "mail":
                    next_word = " to "
                case "imposter":
                    next_word = " as "
                case "triple_bus_drive":
                    next_word = ", "
                case _:
                    next_word = " and "
            phrase = phrase + next_word + selections['target2']
        if targets > 2:
            phrase = phrase + ' and ' + selections['target3']
    else:
        phrase = 'N/A'
    return phrase

def construct_command(selections, player):
    command = None
    if 'action' in selections:
        action = selections["action"]
        targets = role_definitions.verbs[action]["targets"]
        if targets == 1:
            command = f"{player.player_name}: {action}({selections['target1']})"
        if targets == 2:
            command = f"{player.player_name}: {action}({selections['target1']}, {selections['target2']})"
        if targets == 3:
            command = f"{player.player_name}: {action}({selections['target1']}, {selections['target2']}, {selections['target3']})"
    return command

def night_action_input(night, player):
    role = player.role
    valid_targets = get_valid_targets(player)
    selections = {"phrase":"", "target1":"" ,"target2":"" ,"target3":""}

    def action():
        goon_kill = True if role.alignment == "Mafia" else False
        num_actions = len(role.verbs) + 1 if goon_kill else len(role.verbs)

        if num_actions == 0:
            ui.label("does not have a night action").classes('text-lg')
        elif num_actions == 1:
            action_word = "goon kills" if goon_kill else role_definitions.verbs[role.verbs[0]]['action_word']
            ui.label(f"{action_word}").classes('text-lg')
            selections['phrase'] = action_word
            selections['action'] = 'kill' if goon_kill else role.verbs[0]
        elif num_actions > 1:
            option_phrases = {
                x: role_definitions.verbs[x]["action_word"] for x in role.verbs
            }
            if goon_kill:
                option_phrases["kill"] = "goon kills"
            ui.select(
                options=option_phrases,
                label=None,
                on_change=lambda e: resolve_action_choice(e.value),
            ).classes(
                "items-center justify-center text-lg"
            ).props(
                'dense hide-dropdown-icon outlined popup-content-class="text-lg"'
            ).style(
                "min-width: 80px; max-width: none;"
            )

    def resolve_action_choice(action):
        selections["action"] = action
        selections['phrase'] = role_definitions.verbs[action]['action_word']
        targets.refresh()

    @ui.refreshable
    def targets():
        if "action" in selections:
            action = selections["action"]
            targets = role_definitions.verbs[action]["targets"]
            if targets > 0:
                ui.select(
                    options=valid_targets,
                    label=None,
                    on_change=lambda e: selections.update({"target1": e.value}),
                ).classes("items-center justify-center text-lg").props(
                    'dense hide-dropdown-icon outlined popup-content-class="text-lg"'
                ).style(
                    "min-width: 80px; max-width: none; font-weight: bold;"
                )
            if targets > 1:
                next_word = ""
                match (action):
                    case "mail":
                        next_word = "to"
                    case "imposter":
                        next_word = "as"
                    case "triple_bus_drive":
                        next_word = ","
                    case _:
                        next_word = "and"
                ui.label(next_word).classes('text-lg')
                ui.select(
                    options=valid_targets,
                    label=None,
                    on_change=lambda e: selections.update({"target2": e.value}),
                ).classes(
                    "items-center justify-center text-lg"
                ).props(
                    'dense hide-dropdown-icon outlined stacked popup-content-class="text-lg"'
                ).style(
                    "min-width: 80px; max-width: none; "
                )
            if targets > 2:
                ui.label('and').classes('text-lg')
                ui.select(
                    options=valid_targets,
                    label=None,
                    on_change=lambda e: selections.update({"target3": e.value}),
                ).classes(
                    "items-center justify-center text-lg"
                ).props(
                    'dense hide-dropdown-icon outlined stacked popup-content-class="text-lg"'
                ).style(
                    "min-width: 80px; max-width: none; "
                )

            if action == "kick_out_of_time":
                ui.label("out of time").classes('text-lg')

    with ui.row().classes("w-full items-center justify-start p-5 gap-1"):
        ui.label(player.player_name).classes('text-lg')
        action()
        targets()

    return selections


def get_valid_targets(player):
    all_targets = []
    if "Introverted" in player.role.modifiers:
        all_targets = [player.player_name]
    else:
        all_targets = [x.player_name for x in game_state.game_state.values()]
        if "Extroverted" in player.role.modifiers:
            all_targets.remove(player.player_name)
    return all_targets
