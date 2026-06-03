import json
from src.data import role_definitions, roles_setup, role, game_state

class Player:
    def __init__(self, id, player_name, role, actions=None, results=None, status=None):
        self.id = id
        self.player_name = player_name
        self.role = role
        self.actions = {'n0':'---'} if actions is None else actions
        self.results = {'n0':'---'} if results is None else results
        self.status = 'alive' if status is None else status

    @classmethod
    def from_json(cls, json_str):
        try:
            player_data = json.loads(json_str)
            return cls(
                player_data['id'],
                player_data["player_name"],
                role=role.Role.from_json(player_data["role"]),
                actions=player_data["actions"],
                results=player_data["results"],
                status=player_data["status"],
            )
        except json.JSONDecodeError:
            print(f"Skipping malformed JSON line: {json_str}")
            return None

    async def updateStatus(self, status):
        self.status = status
        await game_state.save_game()

    async def addItem(self, item):
        if item not in self.role.items:
            self.role.items.append(item)
            await game_state.save_game()
    
    async def removeItem(self, item):
        if item in self.role.items:
            self.role.items.remove(item)
            await game_state.save_game()

    async def updateActions(self, action, night):
        self.actions[night] = action
        await game_state.save_game()

    async def updateResults(self, result, night):
        self.results[night] = result
        await game_state.save_game()

    async def addSubRole(self, role):
        self.role.sub_roles[role.role_name]=role
        await game_state.save_game()

    async def removeSubRole(self, role):
        if role.role_name in self.role.sub_roles.keys():
            self.role.sub_roles[role.role_name].notes = 'expended'
            await game_state.save_game()

    async def addItem(self, item):
        if item not in self.items:
            self.items.append(item)
            await roles_setup.save_roles()
    
    async def removeItem(self, item):
        if item in self.items:
            self.items.remove(item)
            await roles_setup.save_roles()

    def __str__(self):
        role_json = {
            "id":self.id,
            "player_name": self.player_name,
            "role": self.role,
            "actions": self.actions,
            "results": self.results,
            "status": self.status,
        }
        return json.dumps(role_json, default=str)
