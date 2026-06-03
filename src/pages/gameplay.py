import copy
from functools import partial

from nicegui import ui
from src.data import role, players_setup, roles_setup, game_state

night_count = 0


@ui.page("/gameplay/{name}")
async def gameplay(name: str):
    """
    Gameplay page. User can record night actions, run the game solver, and
    see the outcomes of each night.
    """

    # TODO: add error validation to setup navigation
    if len(players_setup.players) > len(roles_setup.roles):
        ui.navigate.to(f"/setup/{name}")
    else:
        rows = []
        global night_count
        for id, player in game_state.game_state.items():
            if id == "0":
                night_count = len(player.actions) - 1
            icon = "skull" if player.status == "alive" else "medical_services"
            row = {
                "id": f"{id}",
                "player": f'<div class="cell-container"><span>{player.player_name}</span><button class="icon-grid-btn" data-id={id} status="{player.status}" onclick="window.handleKillIconClick(event, this)"><span class="material-symbols-outlined {player.status}-player">{icon}</span></button></div>',
                "player_name": player.player_name,
                "role": player.role.role_title(),
                "alignment": player.role.alignment,
                "dead": True if player.status == "dead" else False,
            }
            for night in player.actions.keys():
                row[f"{night} action"] = (
                    f'<div class="cell-container"><span>{player.actions[night]}</span><button class="icon-grid-btn" data-id={id} night={night_count} onclick="window.handleEditIconClick(event, this)"><span class="material-symbols-outlined {player.status}-player">edit</span></button></div>'
                )
                row[f"{night} result"] = player.results[night]
            rows.append(row)

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
                "headerName": "N0 Action",
                "field": "n0 action",
                "sortable": False,
                ":cellRenderer": '(params) => params.value ? params.value : ""',
            },
            {
                "headerName": "N0 Result",
                "field": "n0 result",
                "sortable": False,
            },
        ]

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
        </style>
        """)

        # styles to replicate nicegui button appearance in html/css
        # script to handle button click events
        ui.add_head_html("""
        <link href="https://googleapis.com" rel="stylesheet">
        <style>
            .cell-container {
                display: flex;
                justify-content: space-between;
                align-items: center;
                width: 100%;
                height: 100%;
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
            }
            .icon-grid-btn:hover {
                background-color: rgba(223, 223, 223, 0.69);
                color: #000000;
            }
            .icon-grid-btn .material-symbols-outlined {
                font-size: 20px;
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
                            row["dead"] = True
                            for night in range(night_count):
                                row[f"n{night} action"] = row[
                                    f"n{night} action"
                                ].replace("alive", "dead")
                            await game_state.game_state[element_id].updateStatus("dead")
                        elif status == "dead":
                            row["player"] = (
                                row["player"]
                                .replace("dead", "alive")
                                .replace("medical_services", "skull")
                            )
                            row["dead"] = False
                            for night in range(night_count):
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
        def edit_night(e):
            element_id = e.args["id"]
            night = e.args["night"]

        ui.on("edit_night_click", edit_night)

        async def add_night(table):
            global night_count
            night_count += 1
            column_count = len(table.options["columnDefs"])

            for row in table.options["rowData"]:
                status = "dead" if row["dead"] else "alive"
                row[f"n{night_count} action"] = (
                    f'<div class="cell-container"><span>---</span><button class="icon-grid-btn" data-id={row['id']} night={night_count} onclick="window.handleEditIconClick(event, this)"><span class="material-symbols-outlined {status}-player">edit</span></button></div>'
                )
                row[f"n{night_count} result"] = ""

                await game_state.game_state[row["id"]].updateActions(
                    "---", f"n{night_count}"
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

        with ui.column().classes("w-full h-[calc(100vh-2rem)]"):
            ui.label(f"{name}")
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
                auto_size_columns=False,
                html_columns=[0, 2],
            ).classes("w-full flex-grow")
            with ui.row().classes("w-full justify-end"):
                with ui.button(color=None, on_click=partial(add_night, table)).tooltip(
                    "Add Night"
                ).props("round flat"):
                    ui.icon("sym_r_add")
