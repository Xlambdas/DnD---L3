class Race:
    def __init__(self, name, speed, abilities):
        self.name = name
        self.speed = speed
        self.abilities = abilities

    def describe(self):
        """
        renvoie une description de la race.
        """
        abilities_desc = ", ".join(f"{key}: {value}" for key, value in self.abilities.items())
        return f"Race: {self.name}, Speed: {self.speed}, Abilities: {abilities_desc}"
        # Example of predefined races stored in a dictionary

    def attack_bonus(self, base_attack):
        """
        Calcule le bonus d'attaque en fonction des capacités de la race.
        """
        bonus = sum(self.abilities.values())
        return base_attack + bonus


predefined_races = {
    "Elf": Race("Elf", 30, {"Dexterity": 2, "Perception": 1}),
    "Dwarf": Race("Dwarf", 25, {"Constitution": 2, "Resilience": 1}),
    "Human": Race("Human", 30, {"Versatility": 1}),
    "Halfling": Race("Halfling", 25, {"Dexterity": 2, "Luck": 1}),
    "Orc": Race("Orc", 30, {"Strength": 2, "Intimidation": 1}),
    "Tiefling": Race("Tiefling", 30, {"Charisma": 2, "Infernal Resistance": 1}),
    "Gnome": Race("Gnome", 25, {"Intelligence": 2, "Craftiness": 1}),
    "Dragonborn": Race("Dragonborn", 30, {"Strength": 2, "Draconic Ancestry": 1}),
}

# Function to retrieve a race by name
def get_race_by_name(name):
    return predefined_races.get(name, None)


print(get_race_by_name("Elf").describe())