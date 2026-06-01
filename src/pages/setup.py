from nicegui import ui
from src.pages import gameplay
from src.data import players, roles
from src.components import role_picker
import os

#re-order the list of roles when user drags role names
async def handle_role_reorder(e):
    # e.old_index and e.new_index are available SortableEventArguments
    moved_item = roles.roles.pop(e.old_index)
    roles.roles.insert(e.new_index, moved_item)
    await roles.save_roles()

@ui.refreshable
def role_list():
    ui.add_head_html('''
    <style>
        .role_list > .q-scrollarea__thumb--vertical,
        .role_list > .q-scrollarea__bar--vertical {
            display: none !important;
        }
        .q-scrollarea__content{
            padding: 0px !important;
            justify-content: center
        }
    </style>
''')
    with ui.card().classes('w-64') as card:
        for role in roles.roles:
            bg_color = ''
            match role.alignment:
                case 'Mafia':
                    bg_color = 'bg-red-100'
                case 'Town':
                    bg_color = 'bg-green-100'
                case '3rd Party':
                    bg_color = 'bg-purple-100'
            with ui.row().classes(f'items-center gap-2 {bg_color} w-full rounded-sm'):
                ui.icon('drag_indicator') \
                    .classes('handle cursor-grab active:cursor-grabbing')
                with ui.scroll_area().classes("w-40 h-6 role_list p-0"):
                    ui.label(role.role_name).classes('whitespace-nowrap')
                ui.space()
                with ui.button(color=None).props('round size=xs flat'):
                    ui.icon('sym_r_edit')
    card.make_sortable(handle='.handle', on_end=handle_role_reorder)

@ui.page('/setup/{name}')
async def setup(name: str):
    """
    Game setup page. User can add players, add roles, and match players
    to roles randomly or manually by arranging or randomizing the player/role 
    orders.
    """

    ui.label(f'Game Setup: {name}')
            
    #Dialog for adding player names    
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

    #Dialog for adding roles
    async def show_roles_popup():
        with ui.dialog() as role_dialog, ui.card().classes('w-100'):
            await role_picker.role_picker()
            ui.button('Close', on_click=lambda: role_dialog.submit(None))
        result = await role_dialog

    ui.button('Add Roles', on_click=show_roles_popup)

    #re-order the list of players when user drags player names
    async def handle_player_reorder(e):
        # e.old_index and e.new_index are available SortableEventArguments
        moved_item = players.players.pop(e.old_index)
        players.players.insert(e.new_index, moved_item)
        await players.save_players()



    #reorderable list of player names
    @ui.refreshable
    def player_list():
        with ui.card() as card:
            for player in players.players:
                with ui.row().classes('items-center gap-2 h-6 w-50 border-b border-gray-300'):
                    ui.icon('drag_indicator') \
                        .classes('handle cursor-grab active:cursor-grabbing')
                    ui.label(player)
        card.make_sortable(handle='.handle', on_end= handle_player_reorder)

    

    with ui.row():
        player_list()
        role_list()

    ui.button('Start Game', on_click=lambda: ui.navigate.to(f'/gameplay/{name}'))
