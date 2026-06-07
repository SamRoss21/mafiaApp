import json
from src.data import role_definitions, roles_setup, role, game_state

class Player:
    def __init__(self, id, player_name, role, actions=None, results=None, status=None, current_items=None):
        self.id = id
        self.player_name = player_name
        self.role = role
        self.actions = {'n0':{'phrase':'---','command':None}} if actions is None else actions
        self.results = {'n0':'---'} if results is None else results
        self.status = 'alive' if status is None else status
        self.current_items = [] if current_items is None else current_items

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
                current_items=player_data["current_items"],
            )
        except json.JSONDecodeError:
            print(f"Skipping malformed JSON line: {json_str}")
            return None

    async def updateStatus(self, status):
        self.status = status
        await game_state.save_game()

    #give player an item
    async def addItem(self, item):
        if item not in self.current_items:
            self.current_items.append(item)
            await game_state.save_game()
    
    #remove item from player
    async def removeItem(self, item):
        if item in self.current_items:
            self.current_items.remove(item)
            await game_state.save_game()

    async def updateActions(self, action_phrase, action_command, night):
        self.actions[night] = {'phrase':action_phrase, "command":action_command}
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

    def __str__(self):
        role_json = {
            "id":self.id,
            "player_name": self.player_name,
            "role": self.role,
            "actions": self.actions,
            "results": self.results,
            "status": self.status,
            "current_items": self.current_items
        }
        return json.dumps(role_json, default=str)
