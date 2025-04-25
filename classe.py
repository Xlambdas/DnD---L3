class BaseClasse:
    """Base class for all character classes"""
    def __init__(self, name):
        self.class_name = name
        self.strength = 20  # Default value
        self.endurance = 20  # Default value
        self.bonus = {}  # Default empty bonus

    def describe(self):
        """Returns a description of the class."""
        bonus_desc = ", ".join(f"{key}: {value}" for key, value in self.bonus.items())
        return f"Class: {self.class_name}, Strength: {self.strength}, Endurance: {self.endurance}, Bonus: {bonus_desc}"

    def attack(self):
        """Basic attack method"""
        return f"{self.class_name} attacks with a strength of {self.strength}!"

    def defend(self):
        """Basic defend method"""
        return f"{self.class_name} defends with an endurance of {self.endurance}."

    def get_endurance(self):
        """Return the endurance value for movement calculations"""
        return self.endurance

    def special_ability(self):
        """Each class has a special ability"""
        return f"{self.class_name} uses a special ability!"

# Specific class implementations
class Warrior(BaseClasse):
    def __init__(self):
        super().__init__("Warrior")
        # Additional warrior-specific attributes
        self.weapon_mastery = True

    def special_ability(self):
        return f"{self.class_name} uses Heroic Strike!"

class Mage(BaseClasse):
    def __init__(self):
        super().__init__("Mage")
        # Additional mage-specific attributes
        self.spell_mastery = True

    def special_ability(self):
        return f"{self.class_name} casts Arcane Explosion!"

    def attack(self):
        """Mages attack with magic"""
        return f"{self.class_name} casts a spell with intelligence of {self.bonus.get('intelligence', 0)}!"

class Rogue(BaseClasse):
    def __init__(self):
        super().__init__("Rogue")
        # Additional rogue-specific attributes
        self.stealth_mastery = True

    def special_ability(self):
        return f"{self.class_name} uses Shadowstrike!"