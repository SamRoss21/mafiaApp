from nicegui import ui
from src.data import roles, role, players

@ui.refreshable
def setup_summary():
    town_count = 0
    mafia_count = 0
    third_party_count = 0
    total_count = len(roles.roles)
    for role in roles.roles:
        match role.alignment:
            case "Town":
                town_count += 1
            case "Mafia":
                mafia_count += 1
            case "3rd Party":
                third_party_count += 1

    with ui.card().classes('w-50'):
        with ui.column():
            ui.label(f'{len(players.players)} Players').classes('text-bold')
            ui.label(f'{total_count} Roles').classes('text-bold')
            ui.label(f'{mafia_count} Mafia ({((mafia_count / total_count * 100) if total_count != 0 else 0):.0f}%)').classes('pl-2')
            ui.label(f'{town_count} Town ({((town_count / total_count * 100) if total_count != 0 else 0):.0f}%)').classes('pl-2')
            ui.label(f'{third_party_count} 3rd Party ({((third_party_count / total_count * 100) if total_count != 0 else 0):.0f}%)').classes('pl-2')