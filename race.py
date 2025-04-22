
class BaseRace:
    """Base for all races"""
    def __init__(self, name):
        self.name = name
        self.base_health = 25  # Default value
        self.bonus = {}

    def describe(self):
        """Return a description of the race"""
        bonus_descr = ", ".join(f"{key}: {value}" for key, value in self.bonus.items())
        return f"Race: {self.name}, Base Health: {self.base_health}, Abilities: {bonus_descr}"

    # --- | gestion de la race | ---
    def attack_bonus(self, base_attack):
        """Calculate attack bonus based on race abilities"""
        bonus = sum(self.bonus.values())
        return base_attack + bonus

    def get_endurance(self):
        """Each race might modify endurance differently"""
        return 0  # Base modifier


# --- | Specific race classes | ---
class Elf(BaseRace):
    def __init__(self):
        super().__init__("Elf")
        # Additional elf-specific attributes
        self.night_vision = True

    def get_endurance(self):
        """Elves are more agile but have less endurance"""
        return -2

class Dwarf(BaseRace):
    def __init__(self):
        super().__init__("Dwarf")
        # Additional dwarf-specific attributes
        self.stone_resistance = True
        
    def get_endurance(self):
        """Dwarves have better endurance"""
        return +3

class Human(BaseRace):
    def __init__(self):
        super().__init__("Human")
        # Additional human-specific attributes
        self.adaptability = True
        
    def get_endurance(self):
        """Humans have average endurance"""
        return +1