class BaseClasse:
    """Base class for all character classes"""
    def __init__(self, name, strength=0, endurance=0, intelligence=0, agility=0):
        self.class_name = name
        self.strength = strength
        self.endurance = endurance
        self.intelligence = intelligence
        self.agility = agility
        self.bonus = {}

    def descr(self):
        """Returns a description of the class."""
        bonus_desc = ", ".join(f"{key}: {value}" for key, value in self.bonus.items())
        return (f"Class: {self.class_name}, Strength: {self.strength}, Endurance: {self.endurance}, "
                f"Intelligence: {self.intelligence}, Agility: {self.agility}, Bonus: {bonus_desc}")

    def range_mouv(self):
        """Each class might have different movement abilities"""
        return 1 + self.agility // 2

    def range_attack(self):
        """Basic attack range"""
        return self.intelligence // 2

    def attack(self):
        """Basic attack method"""
        return self.strength + self.bonus.get('attack', 0)

    def defend(self):
        """Basic defend method"""
        return self.endurance + self.bonus.get('defense', 0)


class Warrior(BaseClasse):
    def __init__(self):
        super().__init__("Warrior", strength=10, endurance=8, intelligence=2, agility=4)
        self.bonus = {"attack": 2, "defense": 2}


class Mage(BaseClasse):
    def __init__(self):
        super().__init__("Mage", strength=2, endurance=4, intelligence=10, agility=4)
        self.bonus = {"attack": 3, "defense": 1}


class Rogue(BaseClasse):
    def __init__(self):
        super().__init__("Rogue", strength=6, endurance=4, intelligence=4, agility=10)
        self.bonus = {"attack": 1, "defense": 1}


class Paladin(BaseClasse):
    def __init__(self):
        super().__init__("Paladin", strength=8, endurance=10, intelligence=4, agility=2)
        self.bonus = {"attack": 2, "defense": 3}


class Druid(BaseClasse):
    def __init__(self):
        super().__init__("Druid", strength=4, endurance=6, intelligence=8, agility=4)
        self.bonus = {"attack": 2, "defense": 2}


class Bard(BaseClasse):
    def __init__(self):
        super().__init__("Bard", strength=4, endurance=4, intelligence=6, agility=6)
        self.bonus = {"attack": 1, "defense": 1}


class Sorcerer(BaseClasse):
    def __init__(self):
        super().__init__("Sorcerer", strength=3, endurance=3, intelligence=10, agility=4)
        self.bonus = {"attack": 3, "defense": 1}


class Warlock(BaseClasse):
    def __init__(self):
        super().__init__("Warlock", strength=4, endurance=4, intelligence=8, agility=4)
        self.bonus = {"attack": 2, "defense": 1}

