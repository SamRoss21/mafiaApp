import json
from src.data import role_definitions, roles_setup

class Role:
    def __init__(
        self, role_name, targets=None, alignment=None, verbs=None, modifiers=None, sub_roles=None, notes=None, items=None
    ):
        self.role_name = role_name
        self.targets = (
            role_definitions.roles[role_name]["targets"] if targets is None else targets
        )
        self.alignment = (
            role_definitions.roles[role_name]["default_alignment"]
            if alignment is None
            else alignment
        )
        self.verbs = role_definitions.roles[role_name]["verbs"] if verbs is None else verbs
        self.modifiers = [] if modifiers is None else modifiers
        self.sub_roles = {} if sub_roles is None else sub_roles
        self.notes = "" if notes is None else notes
        self.items = [] if items is None else items

    @classmethod
    def from_json(cls, json_str):
        try:
            role_data = json.loads(json_str)
            return cls(
                role_data["role_name"],
                targets=role_data["targets"],
                alignment=role_data["alignment"],
                verbs=role_data["verbs"],
                modifiers=role_data["modifiers"],
                sub_roles=role_data["sub_roles"],
                notes = role_data['notes'],
                items=role_data["items"]
            )
        except json.JSONDecodeError:
            print(f"Skipping malformed JSON line: {json_str}")
            return None

    async def updateAlignment(self, alignment):
        self.alignment = alignment
        await roles_setup.save_roles()

    async def updateTargets(self, targets):
        self.targets = targets
        await roles_setup.save_roles()

    async def addVerb(self, verb):
        if verb not in self.verbs:
            self.verbs.append(verb)
            await roles_setup.save_roles()

    async def removeVerb(self, verb):
        if verb in self.verbs:
            self.verbs.remove(verb)
            await roles_setup.save_roles()

    async def addModifier(self, modifier):
        if modifier not in self.modifiers:
            self.modifiers.append(modifier)
            await roles_setup.save_roles()
    
    async def removeModifier(self, modifier):
        if modifier in self.modifiers:
            self.modifiers.remove(modifier)
            await roles_setup.save_roles()

    async def addSubRole(self, role):
        self.sub_roles[role.role_name]=role
        await roles_setup.save_roles()

    async def removeSubRole(self, role):
        if role.role_name in self.sub_roles.keys():
            self.sub_roles.pop(role.role_name)
            await roles_setup.save_roles()

    async def addItem(self, item):
        if item not in self.items:
            self.items.append(item)
            await roles_setup.save_roles()
    
    async def removeItem(self, item):
        if item in self.items:
            self.items.remove(item)
            await roles_setup.save_roles()

    def role_title(self):
        name_string = ""
        name_string += f"{self.alignment} "
        for modifier in self.modifiers:
            name_string += f"{modifier} "
        name_string += self.role_name
        if self.sub_roles:
            sub_roles = list(self.sub_roles)
            name_string += f" ("
            for sub_role in sub_roles[:-1]:
                name_string += f"{sub_role}, "
            name_string += f"{sub_roles[-1]})"
        if(self.items):
            name_string += " with"
            if len(self.items) == 1:
                name_string += f" {role_definitions.items[self.items[0]]['phrase']}"
            elif len(self.items) > 1:
                for item in self.items[:-1]:
                    name_string += f" {role_definitions.items[item]['phrase']},"
                name_string += f" and {role_definitions.items[self.items[-1]]['phrase']}"
        return name_string

    def __str__(self):
        role_json = {
            "role_name": self.role_name,
            "targets": self.targets,
            "alignment": self.alignment,
            "verbs": self.verbs,
            "modifiers": self.modifiers,
            "sub_roles": self.sub_roles,
            "notes":self.notes,
            "items": self.items
        }
        return json.dumps(role_json, default=str)
