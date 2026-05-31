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
            
    #Dialog for creating a new game
    #triggers popup asking for a name    
    async def show_player_popup():
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
        player_list.refresh()

    ui.button('Add Players', on_click=show_player_popup)

    #re-order the list of players when user drags player names
    def handle_player_reorder(e):
        # e.old_index and e.new_index are available SortableEventArguments
        moved_item = players.players.pop(e.old_index)
        players.players.insert(e.new_index, moved_item)
        players.save_players()

    #reorderable list of player names
    @ui.refreshable
    def player_list():
        with ui.card() as card:
            for player in players.players:
                with ui.row().classes('items-center gap-2'):
                    ui.icon('drag_indicator') \
                        .classes('handle cursor-grab active:cursor-grabbing')
                    ui.label(player)
        card.make_sortable(handle='.handle', on_end=handle_player_reorder)

    player_list()

    ui.button('Start Game', on_click=lambda: ui.navigate.to(f'/gameplay/{name}'))
