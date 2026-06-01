import json
from src.data import role_definitions


class Role:
    def __init__(
        self, role_name, targets=None, alignment=None, verbs=None, modifiers=None
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
        self.modifiers = [None] if modifiers is None else modifiers

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
            )
        except json.JSONDecodeError:
            print(f"Skipping malformed JSON line: {json_str}")
            return None

    def updateAlignment(self, alignment):
        self.alignment = alignment

    def updateTargets(self, targets):
        self.targets = targets

    def addVerb(self, verb):
        self.verbs.append(verb)

    def removeVerb(self, verb):
        if verb in self.verbs:
            self.verbs.remove(verb)

    def toString(self):
        role_json = {
            "role_name": self.role_name,
            "targets": self.targets,
            "alignment": self.alignment,
            "verbs": self.verbs,
            "modifiers": self.modifiers,
        }
        return json.dumps(role_json)
