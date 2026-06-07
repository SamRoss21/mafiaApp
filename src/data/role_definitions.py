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
        "verbs": ["investigate", "doctor", "block", "kill"],
        "targets": 1,
        "default_alignment": "Town",
        "category": "Flexible",
    },
    "Rando": {
        "verbs": ["investigate", "doctor", "block", "kill"],
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
    "Inventor": {
        "verbs": [],
        "targets": -1,
        "default_alignment": "Town",
        "category": "Flexible",
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
    "Enthralling Book": {"phrase":"an Enthralling Book", "icon":"book_2"},
    "Crystal Ball": {"phrase":"a Crystal Ball", "icon":'tips_and_updates'},
    "TNT": {"phrase":"TNT", "icon":"destruction"},
    "Glitter Bomb": {"phrase":"a Glitter Bomb", "icon":"air_freshener"},
    "Hot Potato": {"phrase":"a Hot Potato", "icon":"onsen"},
    "Zombie Bombie": {"phrase":"a Zombie Bombie", "icon":"bomb"},
    "Night Stone": {"phrase":"a Night Stone", "icon":"diamond"},
    "Day Stone": {"phrase":"a Day Stone", "icon":"diamond_shine"},
    "Gun": {"phrase":"a Gun", "icon":"barcode_reader"},
    "Knife": {"phrase":"a Knife", "icon":"colorize"},
    "Dead Man’s Switch": {"phrase":"a Dead Man’s Switch", "icon":"switch"},
    "Energy Drink": {"phrase":"an Energy Drink", "icon":"water_bottle"},
    "Tequila": {"phrase":"Tequila", "icon":"liquor"},
    "Narcissus’s Mirror": {"phrase":"Narcissus’s Mirror", "icon":"self_care"},
    "Elixir of Immortality": {"phrase":"an Elixir of Immortality", "icon":"experiment"},
}

verbs = {
    "block": {"action_word":"blocks", "targets":1},
    "jailkeep" : {"action_word":"jailkeeps", "targets":1},
    "loki_bus_drive": {"action_word":"Loki bus drives", "targets":2},
    "bus_drive": {"action_word":"bus drives", "targets":2},
    "triple_bus_drive": {"action_word":"triple bus drives", "targets":3},
    "trolley_drive": {"action_word":"trolley drives", "targets":2},
    "mail": {"action_word":"mails", "targets":2},
    "kick_out_of_time": {"action_word":"kicks", "targets":1},
    "speed_up": {"action_word":"speeds up", "targets":1}, 
    "slow_down": {"action_word":"slows down", "targets":1},
    "doctor": {"action_word":"protects", "targets":1},
    "bodyguard": {"action_word":"bodyguards", "targets":1},
    "elite_bodyguard": {"action_word":"elite Bodyguards", "targets":1},
    "frame": {"action_word":"frames", "targets":1},
    "imposter": {"action_word":"imposters", "targets":2},
    "double": {"action_word":"doubles", "targets":1},
    "hide": {"action_word":"hides behind", "targets":1},
    "kill": {"action_word":"kills", "targets":1},
    "poison": {"action_word":"poisons", "targets":1},
    "ninja_kill": {"action_word":"ninja kills", "targets":1},
    "janitor": {"action_word":"janitors", "targets":1},
    "CPR": {"action_word":"CPRs", "targets":1},
    "hitman": {"action_word":"hitman kills", "targets":1},
    "investigate": {"action_word":"investigates", "targets":1},
    "role_investigate": {"action_word":"role investigates", "targets":1},
    "track": {"action_word":"tracks", "targets":1},
    "watch": {"action_word":"watches", "targets":1},
    "forensic_investigate": {"action_word":"forensic investigates", "targets":1},
    "surveil": {"action_word":"surveils", "targets":1},
    "journal": {"action_word":"journals", "targets":1}
}
