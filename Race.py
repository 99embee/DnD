from abc import ABC, abstractmethod

class Race(ABC):
    def __init__(self, name, speed, size, languages):
        self.name = name
        self.speed = speed
        self.size = size
        self.languages = languages

    @abstractmethod
    def ability_score_increase(self):
        pass

    @abstractmethod
    def special_traits(self):
        pass

    def __str__(self):
        return f"{self.name} (Speed: {self.speed}, Size: {self.size}, Languages: {', '.join(self.languages)})"

class Human(Race):
    def __init__(self):
        super().__init__(name="Human", speed=30, size="Medium", languages=["Common"])

    def ability_score_increase(self):
        return {"Strength": 1, "Dexterity": 1, "Constitution": 1, "Intelligence": 1, "Wisdom": 1, "Charisma": 1}

    def special_traits(self):
        return ["Extra Language"]

class Elf(Race):
    def __init__(self):
        super().__init__(name="Elf", speed=30, size="Medium", languages=["Common", "Elvish"])

    def ability_score_increase(self):
        return {"Dexterity": 2}

    def special_traits(self):
        return ["Darkvision", "Keen Senses", "Fey Ancestry", "Trance"]

class Dwarf(Race):
    def __init__(self):
        super().__init__(name="Dwarf", speed=25, size="Medium", languages=["Common", "Dwarvish"])

    def ability_score_increase(self):
        return {"Constitution": 2}

    def special_traits(self):
        return ["Darkvision", "Dwarven Resilience", "Stonecunning"]
