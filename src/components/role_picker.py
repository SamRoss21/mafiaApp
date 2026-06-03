from nicegui import ui
from src.data import role_definitions, roles_setup
from src.components import setup_summary
from src.pages import setup
from functools import partial

#add role to role list
async def increase_role(role_name):
    await roles_setup.add_role(role_name)
    setup.role_list.refresh()
    role_count.refresh()
    setup_summary.setup_summary.refresh()

#remove role from role list
async def decrease_role(role_name):
    await roles_setup.remove_role(role_name)
    setup.role_list.refresh()
    role_count.refresh()
    setup_summary.setup_summary.refresh()

#widget displaying current count for the given role name
@ui.refreshable
def role_count(role_name):
    ui.label(roles_setup.role_counts.get(role_name, 0))

#widget for increasing/decreasing the count of a given role
@ui.refreshable
async def role_entry(role_name):
    with ui.row().classes('items-center w-70 pb-1'):
        ui.label(role_name).classes('text-grey-7 pl-4')
        ui.space()
        with ui.button(color=None, on_click=partial(decrease_role, role_name)).props('round size=xs flat'):
            ui.icon('sym_r_remove')
        role_count(role_name)
        with ui.button(color=None, on_click= partial(increase_role, role_name)).props('round size=xs flat'):
            ui.icon('sym_r_add')

#function for grouping the role categories from role_definitions
#returns roles with a given alignment and subcategory
def get_roles_of_type(alignment, category):
    filtered_roles = []
    for role_name in role_definitions.roles.keys():
        if(role_definitions.roles[role_name]['default_alignment']==alignment and role_definitions.roles[role_name]['category']==category):
            filtered_roles.append(role_name)
    return filtered_roles

#widget for selecting roles to put in the game
async def role_picker():
    ui.add_css('''
    .gapless .nicegui-expansion-content {
        padding-top: 0px !important;
        padding-bottom: 0px !important;
        gap: 0 !important;
    }
''')
    ui.add_head_html('''
    <style>
        /* Styles ONLY the top-level expansion header */
        .top-level-expansion > .q-expansion-item__container > .q-item {
            font-weight: bold;  
        }
    </style>
''')
    # Main container with styling
    ui.label('Select Roles').classes('text-lg font-bold mb-2')
    
    # Mafia Roles
    with ui.expansion('Mafia Roles').classes('w-full gapless top-level-expansion bg-red-100').props('dense'):
        
        # Leaders
        with ui.expansion('Leaders').classes('w-full gapless').props('dense'):
            for role_name in get_roles_of_type('Mafia', 'Leaders'):
                await role_entry(role_name)
        
        # Sneaky
        with ui.expansion('Sneaky').classes('w-full gapless').props('dense'):
            for role_name in get_roles_of_type('Mafia', 'Sneaky'):
                await role_entry(role_name)

        # Killers
        with ui.expansion('Killers').classes('w-full gapless').props('dense'):
            for role_name in get_roles_of_type('Mafia', 'Killers'):
                await role_entry(role_name)

        # Mischief
        with ui.expansion('Mischief').classes('w-full gapless').props('dense'):
            for role_name in get_roles_of_type('Mafia', 'Mischief'):
                await role_entry(role_name)

        # Misc
        with ui.expansion('Misc').classes('w-full gapless').props('dense'):
            for role_name in get_roles_of_type('Mafia', 'Misc'):
                await role_entry(role_name)

    # Town Roles
    with ui.expansion('Town Roles').classes('w-full gapless top-level-expansion bg-green-100').props('dense'):

        # Information
        with ui.expansion('Information').classes('w-full gapless').props('dense'):
            for role_name in get_roles_of_type('Town', 'Information'):
                await role_entry(role_name)
        
        # Life & Death
        with ui.expansion('Life & Death').classes('w-full gapless').props('dense'):
            for role_name in get_roles_of_type('Town', 'Life & Death'):
                await role_entry(role_name)

        # Mischief
        with ui.expansion('Mischief').classes('w-full gapless').props('dense'):
            for role_name in get_roles_of_type('Town', 'Mischief'):
                await role_entry(role_name)

        # Flexible
        with ui.expansion('Flexible').classes('w-full gapless').props('dense'):
            for role_name in get_roles_of_type('Town', 'Flexible'):
                await role_entry(role_name)

        # Stationary
        with ui.expansion('Stationary').classes('w-full gapless').props('dense'):
            for role_name in get_roles_of_type('Town', 'Stationary'):
                await role_entry(role_name)

    # 3rd Party Roles
    with ui.expansion('3rd Party Roles').classes('w-full gapless top-level-expansion bg-purple-100').props('dense'):
        for role_name in get_roles_of_type('3rd Party', 'None'):
                await role_entry(role_name)
            