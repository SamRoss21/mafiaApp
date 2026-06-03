from src.data import role

roles = []
role_counts = {}
filepath = ""
filename = ""

#load game roles from file
async def load_roles(name: str):
    global filepath
    filepath = f'./games/{name}/'
    global filename
    filename = f'{name}_roles.txt'
    global roles
    global role_counts
    roles = []
    role_counts = {}
    try:
        with open(filepath+filename, "r") as file:
            for line in file:
                clean_json = line.strip()
                new_role = role.Role.from_json(clean_json)
                roles += [new_role] if new_role is not None else []
                role_counts[new_role.role_name] = role_counts.get(new_role.role_name, 0) + 1
    except FileNotFoundError:
        # Create the file because it does not exist
        with open(filepath+filename, "w") as file:
            file.write("")

#create and adds a new role with the provided name
async def add_role(role_name: str):
    global role_counts
    roles.append(role.Role(role_name))
    role_counts[role_name] = role_counts.get(role_name, 0) + 1
    await save_roles()

#remove first instance of a role matching the role name (ignoring metadata)
async def remove_role(role_name: str):
    global role_counts
    for role in roles:
        if(role.role_name == role_name):
            roles.remove(role)
            role_counts[role.role_name] = max(0, (role_counts.get(role.role_name, 1) - 1))
            break
    await save_roles()

#remove first instance of a role matching the total provided json (including metadata)
async def remove_exact_role(role_json: str):
    global role_counts
    for role in roles:
        if(role.__str__() == role_json):
            roles.remove(role)
            role_counts[role.role_name] = max(0, (role_counts.get(role.role_name, 1) - 1))
            break
    await save_roles()

#write game roles to file
async def save_roles():
    if filepath and filename:
        try:
            with open(filepath+filename, "w") as file:
                for role in roles:
                    file.write(f"{role}\n")
        except FileNotFoundError:
            print('Error: No Roles File')
