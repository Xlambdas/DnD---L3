class BaseRace:
    """Base for all races"""
    def __init__(self, name, base_health=25, agility=0, intelligence=0, strength=0, resistance=0):
        self.name = name
        self.base_health = base_health
        self.agility = agility
        self.intelligence = intelligence
        self.strength = strength
        self.resistance = resistance
        self.bonus = {}

    def descr(self):
        """Return a description of the race"""
        bonus_descr = ", ".join(f"{key}: {value}" for key, value in self.bonus.items())
        return (f"Race: {self.name}, Base Health: {self.base_health}, Agility: {self.agility}, "
                f"Intelligence: {self.intelligence}, Strength: {self.strength}, Abilities: {bonus_descr}")

    # --- | Race-specific methods | ---
    def attack(self, base_attack):
        """Calculate attack bonus based on race abilities"""
        bonus = sum(self.bonus.values())
        return base_attack + bonus

    def range_attack(self):
        """Each race might modify endurance differently"""
        return 0  # Base modifier

    def range_mouv(self):
        """Calculate movement range based on agility"""
        return 1 + self.agility // 2

    def defend(self):
        """Calculate defense bonus based on resistance"""
        return 1 + self.resistance // 2

    # todo
    # def magic_ability(self):
    #     """Calculate magic ability based on intelligence"""
    #     return self.intelligence // 2

class Human(BaseRace):
    def __init__(self):
        super().__init__(name="Human", base_health=30, agility=2, intelligence=2, strength=2, resistance=2)
        self.bonus = {"Versatility": 3}

class Elf(BaseRace):
    def __init__(self):
        super().__init__(name="Elf", base_health=25, agility=4, intelligence=3, strength=1, resistance=1)
        self.bonus = {"Keen Senses": 2}

class Dwarf(BaseRace):
    def __init__(self):
        super().__init__(name="Dwarf", base_health=35, agility=1, intelligence=1, strength=3, resistance=4)
        self.bonus = {"Resilience": 3}

class Orc(BaseRace):
    def __init__(self):
        super().__init__(name="Orc", base_health=40, agility=1, intelligence=0, strength=5, resistance=3)
        self.bonus = {"Brutal Strength": 4}

class Halfling(BaseRace):
    def __init__(self):
        super().__init__(name="Halfling", base_health=20, agility=3, intelligence=2, strength=1, resistance=2)
        self.bonus = {"Luck": 2}

class Gnome(BaseRace):
    def __init__(self):
        super().__init__(name="Gnome", base_health=22, agility=2, intelligence=4, strength=1, resistance=1)
        self.bonus = {"Inventiveness": 3}

class Tiefling(BaseRace):
    def __init__(self):
        super().__init__(name="Tiefling", base_health=25, agility=2, intelligence=3, strength=2, resistance=2)
        self.bonus = {"Infernal Legacy": 3}
