from nicegui import ui
from src.data import role_definitions, role
from src.components import setup_summary
from src.pages import setup
from functools import partial


# update the role's alignment based on checkbox input
async def change_alignment(e, role):
    new_alignment = role.alignment
    if role_definitions.roles[role.role_name]["default_alignment"] == "Town":
        new_alignment = "Town" if e.value is False else "Mafia"
    elif role_definitions.roles[role.role_name]["default_alignment"] == "Mafia":
        new_alignment = "Mafia" if e.value is False else "Town"
    await role.updateAlignment(new_alignment)
    setup.role_item.refresh()
    setup_summary.setup_summary.refresh()

# checkbox for specifying if a town-by-default role should be a mafia role
async def alignment_check(role):
    if role_definitions.roles[role.role_name]["default_alignment"] == "Town":
        if role.alignment == "Town":
            ui.checkbox(
                "Make Mafia Role",
                value=False,
                on_change=partial(change_alignment, role=role),
            )
        elif role.alignment == "Mafia":
            ui.checkbox(
                "Make Mafia Role",
                value=True,
                on_change=partial(change_alignment, role=role),
            )
    elif role_definitions.roles[role.role_name]["default_alignment"] == "Mafia":
        if role.alignment == "Mafia":
            ui.checkbox(
                "Make Town Role",
                value=False,
                on_change=partial(change_alignment, role=role),
            )
        elif role.alignment == "Town":
            ui.checkbox(
                "Make Town Role",
                value=True,
                on_change=partial(change_alignment, role=role),
            )

#update the role's modifiers based on checkbox
async def change_modifier(e, role, modifier):
    if e.value:
        await role.addModifier(modifier)
    else:
        await role.removeModifier(modifier)
    setup.role_item.refresh()

async def modifier_settings(role):
    with ui.expansion("Modifiers").classes("w-full gapless").props("dense"):
        #mafia special case usuper modifier
        if role.alignment == 'Mafia':
            modifier = 'Usurper'
            ui.checkbox(
                modifier,
                value=True if modifier in role.modifiers else False,
                on_change=partial(change_modifier, role=role, modifier=modifier),
            )
        #all other modifiers
        for modifier in role_definitions.modifiers:
            ui.checkbox(
                modifier,
                value=True if modifier in role.modifiers else False,
                on_change=partial(change_modifier, role=role, modifier=modifier),
            )

#update the role's sub-roles based on checkbox
async def change_sub_role(e, role, sub_role):
    if e.value:
        await role.addSubRole(sub_role)
    else:
        await role.removeSubRole(sub_role)
    setup.role_item.refresh()

#select the role abilities for the handyman
async def sub_role_settings(main_role):
    with ui.expansion(f"{main_role.role_name} Actions").classes("w-full gapless").props("dense"):
        #all roles
        for role_name in role_definitions.roles.keys():
            ui.checkbox(
                role_name,
                value=True if role_name in main_role.sub_roles.keys() else False,
                on_change=partial(change_sub_role, role=main_role, sub_role=role.Role(role_name)),
            )

async def change_item(e, role, item):
    if e.value:
        await role.addItem(item)
    else:
        await role.removeItem(item)
    setup.role_item.refresh()

#select the role abilities for the handyman
async def item_settings(role):
    with ui.expansion("Items").classes("w-full gapless").props("dense"):
        #all roles
        for item in role_definitions.items.keys():
            ui.checkbox(
                item,
                value=True if item in role.items else False,
                on_change=partial(change_item, role=role, item=item),
            )

async def role_settings_popup(role):
    with ui.context.client.content:
        with ui.dialog() as role_settings_dialog, ui.card().classes("w-100"):
            role_settings_dialog.props('persistent')
            ui.label(f"{role.role_name} Settings").classes("text-lg font-bold mb-2")
            await alignment_check(role)
            await modifier_settings(role)
            if(role.role_name == 'Handyman' or role.role_name == 'Serial Killer'):
                await sub_role_settings(role)
            await item_settings(role)
            ui.button("Close", color=None, on_click=lambda: (role_settings_dialog.close(), role_settings_dialog.clear()))
        role_settings_dialog.open()