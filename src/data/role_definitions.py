"""Missing Roles:
- Incarnation of Fury
- Gunsmith
- Cable Car Operator
- the Cult
- Bus Cult
- The Demon
- Body Snatcher
- The Sith
- Tripple Bus Driver
- Logic Gate
- Master of None
- Inventor
- Copycat

"""

#Note - Mafia goon kills are not included here among verb options
roles = {
    "Roleblocker": {
        "verbs": ["block"], 
        "targets": 1,
        "default_alignment":"Mafia",
        "category":"Mischief"
        },
    "Jailkeeper": {
        "verbs": ["jailkeep"], 
        "targets": 1,
        "default_alignment":"Town",
        "category":"Mischief"
        },
    "Loki Bus Driver": {
        "verbs": ["loki_bus_drive"], 
        "targets": 2,
        "default_alignment":"Mafia",
        "category":"Mischief"
        },
    "Bus Driver": {
        "verbs": ["bus_drive"], 
        "targets": 2,
        "default_alignment":"Town",
        "category":"Mischief"
        },
    "Trolley Driver": {
        "verbs": ["trolley_drive"], 
        "targets": 2,
        "default_alignment":"Town",
        "category":"Mischief"
        },
    "Mailman": {
        "verbs": ["mail"], 
        "targets": 2,
        "default_alignment":"Town",
        "category":"Mischief"
        },
    "Time Traveller": {
        "verbs": ["kick_out_of_time", "speed_up", "slow_down"], 
        "targets": 1,
        "default_alignment":"Mafia",
        "category":"Mischief"
        },
    "Doctor": {
        "verbs": ["doctor"], 
        "targets": 1,
        "default_alignment":"Town",
        "category":"Life & Death"
        },
    "Bodyguard": {
        "verbs": ["bodyguard"], 
        "targets": 1,
        "default_alignment":"Town",
        "category":"Life & Death"
        },
    "Elite Bodyguard": {
        "verbs": ["elite_bodyguard"], 
        "targets": 1,
        "default_alignment":"Town",
        "category":"Life & Death"
        },
    "Framer": {
        "verbs": ["frame"], 
        "targets": 1,
        "default_alignment":"Mafia",
        "category":"Mischief"
        },
    "Imposter": {
        "verbs": ["imposter"], 
        "targets": 2,
        "default_alignment":"Mafia",
        "category":"Mischief"
        },
    "Doubler": {
        "verbs": ["double"], 
        "targets": 1,
        "default_alignment":"Town",
        "category":"Flexible"
        },
    "Hider": {
        "verbs": ["hide"], 
        "targets": 1,
        "default_alignment":"Town",
        "category":"Life & Death"
        },
    "Poisoner": {
        "verbs": ["poison"], 
        "targets": 1,
        "default_alignment":"Mafia",
        "category":"Sneaky"
        },
    "Ninja": {
        "verbs": ["ninja_kill"], 
        "targets": 1,
        "default_alignment":"Mafia",
        "category":"Sneaky"
        },
    "Janitor": {
        "verbs": ["janitor"], 
        "targets": 1,
        "default_alignment":"Mafia",
        "category":"Killers"
        },
    "CPR Doctor": {
        "verbs": ["CPR"], 
        "targets": 1,
        "default_alignment":"Town",
        "category":"Life & Death"
        },
    "Hitman": {
        "verbs": ["hitman"], 
        "targets": 1,
        "default_alignment":"Mafia",
        "category":"Killers"
        },
    "Private Investigator": {
        "verbs": ["investigate"], 
        "targets": 1,
        "default_alignment":"Town",
        "category":"Information"
        },
    "Role Investigator": {
        "verbs": ["role_investigate"], 
        "targets": 1,
        "default_alignment":"Town",
        "category":"Information"
        },
    "Tracker": {
        "verbs": ["track"], 
        "targets": 1,
        "default_alignment":"Town",
        "category":"Information"
        },
    "Watcher": {
        "verbs": ["watch"], 
        "targets": 1,
        "default_alignment":"Town",
        "category":"Information"
        },
    "Forensic Investigator": {
        "verbs": ["forensic_investigate"], 
        "targets": 1,
        "default_alignment":"Town",
        "category":"Information"
        },
    "Surveillance Officer": {
        "verbs": ["surveil"], 
        "targets": 1,
        "default_alignment":"Town",
        "category":"Information"
        },
    "Journalist": {
        "verbs": ["journal"], 
        "targets": 1,
        "default_alignment":"Town",
        "category":"Information"
        },
    "Godfather": {
        "verbs": [], 
        "targets": 1,
        "default_alignment":"Mafia",
        "category":"Leaders"
        },
    "Monarch": {
        "verbs": ["bus_drive"], 
        "targets": 1,
        "default_alignment":"Mafia",
        "category":"Leaders"
        },
    "Warlord": {
        "verbs": [], 
        "targets": 1,
        "default_alignment":"Mafia",
        "category":"Leaders"
        },
    "Lone Wolf": {
        "verbs": [], #will be assigned by mod
        "targets": 1,
        "default_alignment":"Mafia",
        "category":"Misc"
        },
    "Survivor": {
        "verbs": [], 
        "targets": 0,
        "default_alignment":"3rd Party",
        "category":"None"
        },
    "Serial Killer": {
        "verbs": ["kill"], 
        "targets": 1,
        "default_alignment":"3rd Party",
        "category":"None"
        },
    "Sheriff": {
        "verbs": [], 
        "targets": 0,
        "default_alignment":"Town",
        "category":"Information"
        },
    "Vigilante": {
        "verbs": ['kill'], 
        "targets": 1,
        "default_alignment":"Town",
        "category":"Life & Death"
        },
    "Jack of All Trades": {
        "verbs": ['investigate', 'protect', 'roleblock', 'kill'], 
        "targets": 1,
        "default_alignment":"Town",
        "category":"Flexible"
        },
    "Rando": {
        "verbs": ['investigate', 'protect', 'roleblock', 'kill'], 
        "targets": 1,
        "default_alignment":"Town",
        "category":"Flexible"
        },
    "Handyman": {
        "verbs": [], 
        "targets": -1,
        "default_alignment":"Town",
        "category":"Flexible"
        },
    "Bomb": {
        "verbs": [], 
        "targets": 0,
        "default_alignment":"Town",
        "category":"Stationary"
        },
    "Governor": {
        "verbs": [], 
        "targets": 0,
        "default_alignment":"Town",
        "category":"Stationary"
        },
    "Mason": {
        "verbs": [], 
        "targets": 0,
        "default_alignment":"Town",
        "category":"Stationary"
        },
    "Paranoid Gun Owner": {
        "verbs": [], 
        "targets": 0,
        "default_alignment":"Town",
        "category":"Stationary"
        },
    
}
