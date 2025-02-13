class Character:
    # hp = 0
    def __init__(self, name, race, char_class, level, race_hp, strength, dexterity, constitution, intelligence, wisdom, charisma):
        self.name = name
        self.race = race
        self.char_class = char_class
        self.level = level
        self.hp = race_hp
        self.strength = strength
        self.dexterity = dexterity
        self.constitution = constitution
        self.intelligence = intelligence
        self.wisdom = wisdom
        self.charisma = charisma

    def level_up(self , hp):
        self.level += 1
        self.hp += hp
        

    def take_damage(self, damage):
        self.hp -= damage
        if self.hp < 0:
            self.hp = 0

    def heal(self, amount):
        self.hp += amount
        # Assuming max HP is 10 * level for simplicity
        if self.hp > 10 * self.level:
            self.hp = 10 * self.level

    def __str__(self):
        return (f"Name: {self.name}, Race: {self.race}, Class: {self.char_class}, Level: {self.level}, HP: {self.hp}, "
                f"STR: {self.strength}, DEX: {self.dexterity}, CON: {self.constitution}, INT: {self.intelligence}, "
                f"WIS: {self.wisdom}, CHA: {self.charisma}")
