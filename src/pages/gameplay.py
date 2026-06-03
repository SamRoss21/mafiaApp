import copy

from nicegui import ui
from src.data import players, roles, role

global night_count

def add_night(table):
    global night_count
    night_count += 1
    table.options["columnDefs"].append(
        {
            "headerName": f"N{night_count} Action",
            "field": f"n{night_count} action",
            "sortable": False,
        }
    )
    table.options["columnDefs"].append(
        {
            "headerName": f"N{night_count} Result",
            "field": f"n{night_count} result",
            "sortable": False,
        }
    )

    for row in table.options["rowData"]:
        row[f"n{night_count} action"] = ""
        row[f"n{night_count} result"] = ""

    table.update()


@ui.page("/gameplay/{name}")
async def gameplay(name: str):
    """
    Gameplay page. User can record night actions, run the game solver, and
    see the outcomes of each night.
    """
    # TODO: add error validation to setup navigation
    if len(players.players) > len(roles.roles):
        ui.navigate.to(f"/setup/{name}")
    else:
        global night_count
        night_count = 0
        rows = []
        for index, player in enumerate(players.players):
            player_role = roles.roles[index]
            rows.append(
                {
                    "id":f'{index}',
                    "player": f'<div class="cell-container"><span>{player}</span><button class="icon-grid-btn" data-id={index} status="alive" onclick="window.handleGridIconClick(event, this)"><span class="material-symbols-outlined alive-player">skull</span></button></div>',
                    "role": player_role.role_title(),
                    "n0 action": "",
                    "n0 result": "",
                    "alignment": player_role.alignment,
                    "dead": False,
                }
            )

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
            },
            {
                "headerName": "Role",
                "field": "role",
                "sortable": True,
                "sort": "asc",
                'sortingOrder': ['asc', 'desc'],
                ":comparator": alignment_comparator,
            },
            {
                "headerName": "N0 Action",
                "field": "n0 action",
                "sortable": False,
            },
            {
                "headerName": "N0 Result",
                "field": "n0 result",
                "sortable": False,
            },
        ]

        #styling to handle row colors for alignment, dead and alive
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

        #styles to replicate nicegui button appearance in html/css
        #script to handle button click events
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
            window.handleGridIconClick = function(event, buttonElement) {
                const rowId = buttonElement.getAttribute('data-id');
                const status = buttonElement.getAttribute('status');
                if(status == 'alive'){
                    emitEvent('kill_player_click', { id: parseInt(rowId, 10) });
                } else {
                    emitEvent('revive_player_click', { id: parseInt(rowId, 10) });
                }
            }
        </script>
        """)
         
        def kill_player(e):
            element_id = e.args['id']
            for row in table.options['rowData']:
                if f'data-id={element_id}' in row['player']:
                    with table.props.suspend_updates():
                        row['player'] = row['player'].replace('alive', 'dead').replace('skull', 'medical_services')
                        row['dead'] = True

                    table.run_grid_method('applyTransaction', {'update': [row]})
                    table.run_grid_method('onSortChanged')


        def revive_player(e):
            element_id = e.args['id']
            for row in table.options['rowData']:
                if f'data-id={element_id}' in row['player']:
                    with table.props.suspend_updates():
                        row['player'] = row['player'].replace('dead', 'alive').replace('medical_services','skull')
                        row['dead'] = False
                    table.run_grid_method('applyTransaction', {'update': [row]})
                    table.run_grid_method('onSortChanged')


        # def handle_cell_change(e):
        #     print("***")
        #     # Retrieve the updated row data from the event
        #     updated_row = e.args['data']
            
        #     # Run a grid transaction to quietly update the row client-side
        #     table.run_grid_method('applyTransaction', {'update': [updated_row]})
            
        #     # Force the grid to act as if the sort was changed to reorder the rows
        #     table.run_grid_method('onSortChanged')

        ui.on('kill_player_click', kill_player)
        ui.on('revive_player_click', revive_player)
        

        with ui.column().classes("w-full h-[calc(100vh-2rem)]"):
            ui.label(f"{name}")
            table = ui.aggrid(
                options={
                    "columnDefs": columns,
                    "rowData": rows,
                    'animateRows': True,
                    'deltaRowDataMode': True,
                    ':getRowId': '(params) => params.data.id',
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
                html_columns=[0]
            ).classes("w-full flex-grow")
            with ui.row().classes("w-full justify-end"):
                with ui.button(color=None, on_click=lambda: add_night(table)).tooltip(
                    "Add Night"
                ).props("round flat"):
                    ui.icon("sym_r_add")

