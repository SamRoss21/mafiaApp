import copy
from functools import partial
import re
from nicegui import app, ui
from src.data import role, players_setup, roles_setup, game_state, role_definitions
from src.components import night_action_input

night_count = 0

alignment_comparator = """
            (valueA, valueB, nodeA, nodeB, isDescending) => {
                const isBottomA = nodeA.data && nodeA.data.dead;
                const isBottomB = nodeB.data && nodeB.data.dead;
                
                if (isBottomA && isBottomB) return 0;
                if (isBottomA) return isDescending ? -1 : 1;
                if (isBottomB) return isDescending ? 1 : -1;

                const weights = { 'Mafia': 1, '3rd Party': 2, 'Town': 3 };
                const weightA = weights[nodeA.data.alignment] || 0;
                const weightB = weights[nodeB.data.alignment] || 0;
                if (weightA === weightB) return 0;
                return weightA > weightB ? 1 : -1;
            }
            """

@ui.page("/gameplay/{name}")
async def gameplay(name: str):
    """
    Gameplay page. User can record night actions, run the game solver, and
    see the outcomes of each night.
    """
    ui.add_head_html("""
    <link href="https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:opsz,wght,FILL,GRAD@20..48,100..700,0..1,-50..200" rel="stylesheet">
""")
    if len(players_setup.players) > len(roles_setup.roles):
        ui.navigate.to(f"/setup/{name}")
    else:
        rows = []
        columns = [
            {
                "headerName": "Player",
                "field": "player",
                "sortable": False,
                ":cellRenderer": '(params) => params.value ? params.value : ""',
                "pinned": "left",
            },
            {
                "headerName": "Role",
                "field": "role",
                "sortable": True,
                "sort": "asc",
                "sortingOrder": ["asc", "desc"],
                ":comparator": alignment_comparator,
                "pinned": "left",
            },
            {
                "headerName": "Items",
                "field": "items",
                "sortable": False,
                ":cellRenderer": '(params) => params.value ? params.value : ""',
                "pinned": "left",
                'headerComponentParams': {
                    'template': '''
                        <div class="cell-container"><span>Items</span><button class="icon-grid-btn" onclick="window.handleItemClick(event, this)"><span class="material-symbols-outlined">edit</span></button></div>

                    '''
                },
            },
            {
                "headerName": "N0 Action",
                "field": "n0 action",
                "sortable": False,
                ":cellRenderer": '(params) => params.value ? params.value : ""',
                'headerComponentParams': {
                    'template': '''
                        <div class="cell-container"><span>N0 Action</span><div class="flex-container"><button class="icon-grid-btn" night="n0" onclick="window.handleRevertClick(event, this)"><span class="material-symbols-outlined flip-horizontal">refresh</span></button><button class="icon-grid-btn" night="n0" onclick="window.handleNightClick(event, this)"><span class="material-symbols-outlined">play_circle</span></button></div></div>

                    '''
                }
            },
            {
                "headerName": "N0 Result",
                "field": "n0 result",
                "sortable": False,
            },
        ]

        global night_count
        for id, player in game_state.game_state.items():
            if id == "0":
                night_count = len(player.actions) - 1
            icon = "skull" if player.status == "alive" else "medical_services"
            row = {
                "id": f"{id}",
                "player": f'<div class="cell-container"><span>{player.player_name}</span><button class="icon-grid-btn" title="Kill/Revive Player" data-id={id} status="{player.status}" onclick="window.handleKillIconClick(event, this)"><span class="material-symbols-outlined {player.status}-player ">{icon}</span></button></div>',
                "player_name": player.player_name,
                "items":f'<div class="flex gap-2 items-center">{"".join(f'<i title="{item}" class="notranslate item material-symbols-outlined  {player.status}-player">{role_definitions.items[item]["icon"]}</i>' for item in player.current_items)}</div>',
                "role": player.role.role_title(),
                "alignment": player.role.alignment,
                "dead": True if player.status == "dead" else False,
            }

            for night in player.actions.keys():  
                row[f"{night} action"] = (
                    f'<div class="cell-container"><span id="action" class="truncate-text">{player.actions[night]['phrase']}</span><button class="icon-grid-btn" title="Edit Action" data-id={id} night={night} onclick="window.handleEditIconClick(event, this)"><span class="material-symbols-outlined {player.status}-player">edit</span></button></div>'
                )
                row[f"{night} result"] = player.results[night]
            rows.append(row)

        for i in range(1, night_count+1):
            columns.append(
                {
                    "headerName": f"N{i} Action",
                    "field": f"n{i} action",
                    "sortable": False,
                    ":cellRenderer": '(params) => params.value ? params.value : ""',
                    'headerComponentParams': {
                        'template': f'''
                            <div class="cell-container"><span>N{i} Action</span><div class="flex-container"><button class="icon-grid-btn" night="n{i}" onclick="window.handleRevertClick(event, this)"><span class="material-symbols-outlined flip-horizontal">refresh</span></button><button class="icon-grid-btn" night="n{i}" onclick="window.handleNightClick(event, this)"><span class="material-symbols-outlined">play_circle</span></button></div></div>
                        '''
                    }
                }
            )
            columns.append(
                {
                    "headerName": f"N{i} Result",
                    "field": f"n{i} result",
                    "sortable": False,
                }
            )

        # styling to handle row colors for alignment, dead and alive
        ui.add_head_html("""
        <style>
            .row-mafia {
                background-color: #FEE2E2 !important;
            }
            .row-town {
                background-color: #DCFCE7 !important;
            }
            .row-third_party {
                background-color: #F3E8FF !important;
            }
            .dead.row-mafia {
                background-color: #808080 !important;
                color: #FEE2E2
            }
            .dead.row-town {
                background-color: #808080 !important;
                color: #DCFCE7 !important;
            }
            .dead.row-third_party {
                background-color: #808080 !important;
                color: #F3E8FF !important;
            }
            .alive-player{
                color: #000000
            }
            .dead-player{
                color: #ffffff
            }
            .flip-horizontal {
                transform: scaleX(-1);
            }
            .flex-container {
                display: flex;
            }
        </style>
        """)

        # styles to replicate nicegui button appearance in html/css
        # script to handle button click events
        ui.add_head_html("""
        <link rel="stylesheet" href="https://googleapis.com" />
        <style>
            .cell-container {
                display: flex;
                justify-content: space-between;
                align-items: center;
                width: 100%;
                height: 100%;
                min-width: 0;  
            }
            .icon-grid-btn {
                background: transparent;
                color: #000000;
                border: none;
                border-radius: 50%;
                width: 35px;
                height: 35px;
                cursor: pointer;
                display: flex;
                align-items: center;
                justify-content: center;
                transition: background-color 0.2s;
                flex-shrink: 0;
            }
            .icon-grid-btn:hover {
                background-color: rgba(223, 223, 223, 0.69);
                color: #000000;
            }
            .icon-grid-btn .material-symbols-outlined {
                font-size: 20px;
            }
            .item{
                font-size: 25px;
                display: flex;
                height: 35px;
                align-items: center;
                justify-content: center;
                flex-shrink: 0;
                font-weight: 300 !important;
            }
            .truncate-text {
                flex-grow: 1;          
                overflow: hidden;      
                text-overflow: ellipsis;
                white-space: nowrap;    
                margin-right: 8px;      
            }
        </style>
        <script>
            window.handleKillIconClick = function(event, buttonElement) {
                const rowId = buttonElement.getAttribute('data-id');
                const status = buttonElement.getAttribute('status');
                emitEvent('kill_player_click', { id: rowId, status: status });
            }
            window.handleEditIconClick = function(event, buttonElement) {
                const rowId = buttonElement.getAttribute('data-id');
                const night = buttonElement.getAttribute('night');
                emitEvent('edit_night_click', { id: rowId, night: night });
            }
            window.handleNightClick = function(event, buttonElement) {
                const night = buttonElement.getAttribute('night');
                emitEvent('run_night_click', { night: night });
            }
            window.handleRevertClick = function(event, buttonElement) {
                const night = buttonElement.getAttribute('night');
                emitEvent('revert_night_click', { night: night });
            }
            window.handleItemClick = function(event, buttonElement) {
                emitEvent('edit_items_click', {});
            }
        </script>
        """)

        # manually kill the player, or if they're dead revive them
        async def kill_player(e):
            element_id = e.args["id"]
            status = e.args["status"]
            for row in table.options["rowData"]:
                if f"data-id={element_id}" in row["player"]:
                    with table.props.suspend_updates():
                        if status == "alive":
                            row["player"] = (
                                row["player"]
                                .replace("alive", "dead")
                                .replace("skull", "medical_services")
                            )
                            row["items"] = (
                                row["items"]
                                .replace("alive", "dead")
                            )
                            for night in range(night_count+1):
                                row[f"n{night} action"] = row[
                                    f"n{night} action"
                                ].replace("alive", "dead")
                            row["dead"] = True
                            await game_state.game_state[element_id].updateStatus("dead")
                        elif status == "dead":
                            row["player"] = (
                                row["player"]
                                .replace("dead", "alive")
                                .replace("medical_services", "skull")
                            )
                            row["items"] = (
                                row["items"]
                                .replace("dead", "alive")
                            )
                            row["dead"] = False
                            for night in range(night_count+1):
                                row[f"n{night} action"] = row[
                                    f"n{night} action"
                                ].replace("dead", "alive")
                            await game_state.game_state[element_id].updateStatus(
                                "alive"
                            )
                        table.run_grid_method("applyTransaction", {"update": [row]})
                        table.run_grid_method("onSortChanged")

        ui.on("kill_player_click", partial(kill_player))

        # edit night action
        async def edit_night(e):
            element_id = e.args["id"]
            night = e.args["night"]
            player = game_state.game_state[element_id]

            await ui.run_javascript(
                'window._savedScroll = document.querySelector(".ag-body-viewport").scrollTop'
            )

            await night_action_input.edit_action_popup(f"{night}", player)
            
            for row in table.options["rowData"]:
                if f"data-id={element_id} " in row["player"]:
                    row[f"{night} action"] = re.sub(
                        r'(<span id="action"[^>]*>)(.*?)(</span>)',
                        fr"\1{player.actions[f"{night}"]["phrase"]}\3",
                        row[f"{night} action"],
                    )

            table.update()

            await ui.run_javascript(
                'document.querySelector(".ag-body-viewport").scrollTop = window._savedScroll'
            )

            
        ui.on("edit_night_click", edit_night)

        async def add_night(table):
            global night_count
            night_count += 1
            column_count = len(table.options["columnDefs"])

            for row in table.options["rowData"]:
                status = "dead" if row["dead"] else "alive"
                row[f"n{night_count} action"] = (
                    f'<div class="cell-container"><span id="action" class="truncate-text">---</span><button class="icon-grid-btn" data-id={row['id']} night={f'n{night_count}'} onclick="window.handleEditIconClick(event, this)"><span class="material-symbols-outlined {status}-player">edit</span></button></div>'
                )
                row[f"n{night_count} result"] = ""

                await game_state.game_state[row["id"]].updateActions(
                    "---", None, f"n{night_count}"
                )
                await game_state.game_state[row["id"]].updateResults(
                    "---", f"n{night_count}"
                )

            table.options["columnDefs"].append(
                {
                    "headerName": f"N{night_count} Action",
                    "field": f"n{night_count} action",
                    "sortable": False,
                    ":cellRenderer": '(params) => params.value ? params.value : ""',
                    'headerComponentParams': {
                        'template': f'''
                            <div class="cell-container"><span>N{night_count} Action</span><div class="flex-container"><button class="icon-grid-btn" night="n{night_count}" onclick="window.handleRevertClick(event, this)"><span class="material-symbols-outlined flip-horizontal">refresh</span></button><button class="icon-grid-btn" night="n{night_count}" onclick="window.handleNightClick(event, this)"><span class="material-symbols-outlined">play_circle</span></button></div></div>
                        '''
                    }
                }
            )
            table.options["columnDefs"].append(
                {
                    "headerName": f"N{night_count} Result",
                    "field": f"n{night_count} result",
                    "sortable": False,
                }
            )

            table.html_columns.append(column_count)
            table.update()

        async def run_night(e):
            night = e.args["night"]

            #save current state to file before running solver
            #in case you need to revert changes
            await game_state.save_night_state(name, night)

            all_actions = []
            for player in game_state.game_state.values():
                night_command = player.actions[night]['command']
                if night_command:
                    all_actions.append(night_command)

        ui.on("run_night_click", partial(run_night))

        async def revert_night(e):
            night = e.args["night"]
            await game_state.revert_to_night(name, night)
            for row in table.options["rowData"]:
                id = row["id"]
                player = game_state.game_state[id]
                row[f"{night} action"] = re.sub(
                    r'(<span id="action"[^>]*>)(.*?)(</span>)',
                    fr"\1{player.actions[f"{night}"]["phrase"]}\3",
                    row[f"{night} action"],
                )
            table.run_grid_method('redrawRows')
            table.update()

        ui.on("revert_night_click", revert_night)

        async def setup_warning():
             with ui.dialog() as setup_dialog, ui.card().classes("w-150 p-5"):
                with ui.row().classes("w-full items-center flex-nowrap"):
                    ui.icon('sym_r_warning', size='lg').style('display:inline-flex')
                    ui.label("Warning: Returning to setup will reset inputted night actions, do you wish to continue?").classes("text-xl")
                with ui.row().classes('w-full items-end justify-end'):
                    ui.button("Cancel", color=None, on_click=lambda: setup_dialog.close()).props('flat')
                    ui.button("Continue", color=None, on_click= lambda: ui.navigate.to(f"/setup/{name}")).props('flat')
                result = await setup_dialog

        starting_render_columns = [0] + list(range(3, len(columns), 2))
        with ui.column().classes("w-full h-[calc(100vh-2rem)]"):
            with ui.row().classes("items-end"):
                with ui.button(color=None, on_click=lambda: ui.navigate.to(f"/")).props("round flat"):
                    ui.icon("sym_r_home", size="lg")
                ui.label(f"{name}").classes("text-3xl font-bold")
            table = ui.aggrid(
                options={
                    "columnDefs": columns,
                    "rowData": rows,
                    "animateRows": True,
                    ":getRowId": "(params) => params.data.id",
                    "rowClassRules": {
                        "row-mafia": "data.alignment == 'Mafia'",
                        "row-town": "data.alignment == 'Town'",
                        "row-third_party": "data.alignment == '3rd Party'",
                        "dead": "data.dead",
                    },
                    "autoSizeStrategy": {
                        "type": "fitGridWidth",
                        "defaultMinWidth": 200,
                    },
                },
                auto_size_columns=True,
                html_columns = starting_render_columns,
            ).classes("w-full flex-grow")
            with ui.row().classes("w-full justify-between items-center"):
                with ui.button(color=None, on_click=partial(setup_warning)).props('flat'):
                    with ui.row().classes('items-center gap-0'):
                        ui.icon('sym_r_arrow_back')
                        ui.label("Setup").classes("text-xl font-bold")
                with ui.button(color=None, on_click=partial(add_night, table)).tooltip(
                    "Add Night"
                ).props("round flat"):
                    ui.icon("sym_r_add")



        ''' ************** Item Management *******************'''

        def edit_item_popup():

            @ui.refreshable
            def popup_contents():
                for player in game_state.game_state.values():
                    with ui.row().classes('w-full items-center justify-start border-b'):
                        ui.label(player.player_name).classes("text-lg font-bold")
                        item_inventory(player)

            with ui.dialog() as dialog, ui.card().classes("w-60").style(
                "width: auto; max-width: none;"
            ):
                popup_contents()
                with ui.row().classes('w-full items-end justify-end'):
                    ui.button("Close", color=None, on_click=dialog.close).props('flat')

            def open():
                popup_contents.refresh()
                dialog.open()

            return open

        async def handle_item_move(e):
            sender_player = e.sender.player
            target_player = e.target.player

            moved_item = sender_player.current_items[e.old_index]
            await sender_player.removeItem(moved_item)
            await target_player.addItem(moved_item)
            for row in table.options["rowData"]:
                if f"data-id={sender_player.id}" in row["player"]:
                        row['items'] = f'<div class="flex gap-2 items-center">{"".join(f'<i title="{item}" class="notranslate item material-symbols-outlined  {sender_player.status}-player">{role_definitions.items[item]["icon"]}</i>' for item in sender_player.current_items)}</div>'
                if f"data-id={target_player.id}" in row["player"]:
                        row['items'] = f'<div class="flex gap-2 items-center">{"".join(f'<i title="{item}" class="notranslate item material-symbols-outlined  {target_player.status}-player">{role_definitions.items[item]["icon"]}</i>' for item in target_player.current_items)}</div>'
            table.run_grid_method('redrawRows')


        def item_element(item_name):
            ui.icon(role_definitions.items[item_name]['icon']).classes("item material-symbols-outlined").style("filter: drop-shadow(2px 4px 6px rgba(0, 0, 0, 0.3));").props(f'title="{item_name}"')

        def item_inventory(player):
            with ui.card().classes("flex-row items-center h-10").props('flat') as card:
                for item in player.current_items:
                    item_element(item)
            card.make_sortable(group='item_group', on_end=handle_item_move)
            card.player = player
            return card
                
        item_popup = edit_item_popup()
        
        ui.on("edit_items_click", item_popup)

