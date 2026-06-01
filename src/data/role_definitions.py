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

# Note - Mafia goon kills are not included here among verb options
roles = {
    "Roleblocker": {
        "verbs": ["block"],
        "targets": 1,
        "default_alignment": "Mafia",
        "category": "Mischief",
    },
    "Jailkeeper": {
        "verbs": ["jailkeep"],
        "targets": 1,
        "default_alignment": "Town",
        "category": "Mischief",
    },
    "Loki Bus Driver": {
        "verbs": ["loki_bus_drive"],
        "targets": 2,
        "default_alignment": "Mafia",
        "category": "Mischief",
    },
    "Bus Driver": {
        "verbs": ["bus_drive"],
        "targets": 2,
        "default_alignment": "Town",
        "category": "Mischief",
    },
    "Trolley Driver": {
        "verbs": ["trolley_drive"],
        "targets": 2,
        "default_alignment": "Town",
        "category": "Mischief",
    },
    "Mailman": {
        "verbs": ["mail"],
        "targets": 2,
        "default_alignment": "Town",
        "category": "Mischief",
    },
    "Time Traveller": {
        "verbs": ["kick_out_of_time", "speed_up", "slow_down"],
        "targets": 1,
        "default_alignment": "Mafia",
        "category": "Mischief",
    },
    "Doctor": {
        "verbs": ["doctor"],
        "targets": 1,
        "default_alignment": "Town",
        "category": "Life & Death",
    },
    "Bodyguard": {
        "verbs": ["bodyguard"],
        "targets": 1,
        "default_alignment": "Town",
        "category": "Life & Death",
    },
    "Elite Bodyguard": {
        "verbs": ["elite_bodyguard"],
        "targets": 1,
        "default_alignment": "Town",
        "category": "Life & Death",
    },
    "Framer": {
        "verbs": ["frame"],
        "targets": 1,
        "default_alignment": "Mafia",
        "category": "Mischief",
    },
    "Imposter": {
        "verbs": ["imposter"],
        "targets": 2,
        "default_alignment": "Mafia",
        "category": "Mischief",
    },
    "Doubler": {
        "verbs": ["double"],
        "targets": 1,
        "default_alignment": "Town",
        "category": "Flexible",
    },
    "Hider": {
        "verbs": ["hide"],
        "targets": 1,
        "default_alignment": "Town",
        "category": "Life & Death",
    },
    "Poisoner": {
        "verbs": ["poison"],
        "targets": 1,
        "default_alignment": "Mafia",
        "category": "Sneaky",
    },
    "Ninja": {
        "verbs": ["ninja_kill"],
        "targets": 1,
        "default_alignment": "Mafia",
        "category": "Sneaky",
    },
    "Janitor": {
        "verbs": ["janitor"],
        "targets": 1,
        "default_alignment": "Mafia",
        "category": "Killers",
    },
    "CPR Doctor": {
        "verbs": ["CPR"],
        "targets": 1,
        "default_alignment": "Town",
        "category": "Life & Death",
    },
    "Hitman": {
        "verbs": ["hitman"],
        "targets": 1,
        "default_alignment": "Mafia",
        "category": "Killers",
    },
    "Private Investigator": {
        "verbs": ["investigate"],
        "targets": 1,
        "default_alignment": "Town",
        "category": "Information",
    },
    "Role Investigator": {
        "verbs": ["role_investigate"],
        "targets": 1,
        "default_alignment": "Town",
        "category": "Information",
    },
    "Tracker": {
        "verbs": ["track"],
        "targets": 1,
        "default_alignment": "Town",
        "category": "Information",
    },
    "Watcher": {
        "verbs": ["watch"],
        "targets": 1,
        "default_alignment": "Town",
        "category": "Information",
    },
    "Forensic Investigator": {
        "verbs": ["forensic_investigate"],
        "targets": 1,
        "default_alignment": "Town",
        "category": "Information",
    },
    "Surveillance Officer": {
        "verbs": ["surveil"],
        "targets": 1,
        "default_alignment": "Town",
        "category": "Information",
    },
    "Journalist": {
        "verbs": ["journal"],
        "targets": 1,
        "default_alignment": "Town",
        "category": "Information",
    },
    "Godfather": {
        "verbs": [],
        "targets": 1,
        "default_alignment": "Mafia",
        "category": "Leaders",
    },
    "Monarch": {
        "verbs": ["bus_drive"],
        "targets": 1,
        "default_alignment": "Mafia",
        "category": "Leaders",
    },
    "Warlord": {
        "verbs": [],
        "targets": 1,
        "default_alignment": "Mafia",
        "category": "Leaders",
    },
    "Lone Wolf": {
        "verbs": [],  # will be assigned by mod
        "targets": 1,
        "default_alignment": "Mafia",
        "category": "Misc",
    },
    "Survivor": {
        "verbs": [],
        "targets": 0,
        "default_alignment": "3rd Party",
        "category": "None",
    },
    "Serial Killer": {
        "verbs": ["kill"],
        "targets": 1,
        "default_alignment": "3rd Party",
        "category": "None",
    },
    "Sheriff": {
        "verbs": [],
        "targets": 0,
        "default_alignment": "Town",
        "category": "Information",
    },
    "Vigilante": {
        "verbs": ["kill"],
        "targets": 1,
        "default_alignment": "Town",
        "category": "Life & Death",
    },
    "Jack of All Trades": {
        "verbs": ["investigate", "protect", "roleblock", "kill"],
        "targets": 1,
        "default_alignment": "Town",
        "category": "Flexible",
    },
    "Rando": {
        "verbs": ["investigate", "protect", "roleblock", "kill"],
        "targets": 1,
        "default_alignment": "Town",
        "category": "Flexible",
    },
    "Handyman": {
        "verbs": [],
        "targets": -1,
        "default_alignment": "Town",
        "category": "Flexible",
    },
    "Bomb": {
        "verbs": [],
        "targets": 0,
        "default_alignment": "Town",
        "category": "Stationary",
    },
    "Governor": {
        "verbs": [],
        "targets": 0,
        "default_alignment": "Town",
        "category": "Stationary",
    },
    "Mason": {
        "verbs": [],
        "targets": 0,
        "default_alignment": "Town",
        "category": "Stationary",
    },
    "Paranoid Gun Owner": {
        "verbs": [],
        "targets": 0,
        "default_alignment": "Town",
        "category": "Stationary",
    },
}

modifiers = [
    "Bulletproof",
    "Commuting",
    "Double-Voting",
    "No-Voting",
    "Nega-Voting",
    "Gambling",
    "Graverobbing",
    "Introverted",
    "Extroverted",
    "Over-eager",
    "Paranoid",
    "Suspicious",
    "Black Hole",
    "Fate-Bonded",
    "Insomniac",
    "Beloved",
]

items = {
    "Enthralling Book": "an Enthralling Book",
    "Crystal Ball": "a Crystal Ball",
    "TNT": "TNT",
    "Glitter Bomb": "a Glitter Bomb",
    "Hot Potato": "a Hot Potato",
    "Zombie Bombie": "a Zombie Bombie",
    "Night Stone": "a Night Stone",
    "Day Stone": "a Day Stone",
    "Gun": "a Gun",
    "Knife": "a Knife",
    "Dead Man’s Switch": "a Dead Man’s Switch",
    "Energy Drink": "an Energy Drink",
    "Tequila": "Tequila",
    "Narcissus’s Mirror": "Narcissus’s Mirror",
    "Elixir of Immortality": "an Elixir of Immortality",
}

# TODO: replace with call to mafia-bot
verbs = [
    "block",
    "jailkeep",
    "loki_bus_drive",
    "bus_drive",
    "batch_bus_drive",
    "trolley_drive",
    "mail",
    "kick_out_of_time",
    "doctor",
    "bodyguard",
    "elite_bodyguard",
    "frame",
    "imposter",
    "double",
    "hide",
    "kill",
    "poison",
    "ninja_kill",
    "janitor",
    "CPR",
    "hitman",
    "investigate",
    "role_investigate",
    "track",
    "watch",
    "forensic_investigate",
    "surveil",
    "journal",
]
