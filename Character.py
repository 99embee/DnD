import json

class Character:
    def __init__(self, ID, Role, Name, Level, Experience, Race, Subrace, Class, Subclass, Health, Strength, Dexterity, Constitution, Intelligence, Wisdom, Charisma):
        self.ID = ID
        self.Role = Role
        self.Name = Name
        self.Level = Level
        self.Experience = Experience
        self.Race = Race
        self.Subrace = Subrace
        self.Class = Class
        self.Subclass = Subclass
        self.Health = Health
        self.Strength = Strength
        self.Dexterity = Dexterity
        self.Constitution = Constitution
        self.Intelligence = Intelligence
        self.Wisdom = Wisdom
        self.Charisma = Charisma
        self.modifiers = self.calculate_modifiers()

    def calculate_modifiers(self):
        modifiers = {}
        abilities = {
            'Strength': self.Strength,
            'Dexterity': self.Dexterity,
            'Constitution': self.Constitution,
            'Intelligence': self.Intelligence,
            'Wisdom': self.Wisdom,
            'Charisma': self.Charisma
        }
        for ability, score in abilities.items():
            if score > 10 and score % 2 == 0:
                modifiers[ability] = (score - 10) // 2
            elif score < 10 and score % 2 == 0:
                modifiers[ability] = (score - 10) // 2
            else:
                modifiers[ability] = (score - 10) // 2
        return modifiers

    def checkUnique(self):
        # print(self)
        try:
            with open('Characters.json', 'r', encoding='utf-8') as f:
                data = json.load(f)
                for i in range(0, len(data)):
                    if 'Role' in data[i]:
                        role = data[i]['Role']
                        if data[i][role]['Attributes']['Name'] == self.Name and data[i][role]['Attributes']['Race'] == self.Race and data[i][role]['Attributes']['Class'] == self.Class:
                            return False
                    else:
                        print(f"Error: 'Role' key not found in data[{i}]")
                return True
        except (FileNotFoundError, json.JSONDecodeError):
            return True

    def save(self):
        try:
            with open('Characters.json', 'r', encoding='utf-8') as f:
                data = json.load(f)
                role = data[-1]['Role']
                self.id = data[-1][role]['Attributes']['ID'] + 1
        except (FileNotFoundError, json.JSONDecodeError):
            data = []
            self.id = 1

        player = {'Ref' : str(self.id) + '-'+self.Name, 'Role': self.Role, self.Role: 
                    { 'Attributes':
                        {'ID' : self.id, 'Name' : self.Name, 'Level' : self.Level, 'Experience': self.Experience, 'Race' : self.Race,
                         'Subrace' : self.Subrace, 'Class' : self.Class, 'Subclass' : self.Subclass, 'Health' : self.Health, 
                        'Abilities':{'Strength' : self.Strength,
                                     'Dexterity' : self.Dexterity, 'Constitution' : self.Constitution, 
                                     'Intelligence' : self.Intelligence, 'Wisdom' : self.Wisdom, 'Charisma' : self.Charisma}},
                        'Modifiers' : self.modifiers,
                        'Extra' : {'Alignment' : '', 'Background' : '', 'Personality' : '', 'Ideals' : '', 'Bonds' : '', 'Flaws' : ''},
                        'Details' : {'Feats' : [], 'Spells' : {'Cantrips' : {}, 
                                                               '1st Level': {'1st Spell Slots': {}, '1st lvl Spells': {}},
                                                               '2nd Level': {'2nd Spell Slots': {}, '2nd lvl Spells': {}}, 
                                                               '3rd Level': {'3rd Spell Slots': {}, '3rd lvl Spells': {}}, 
                                                               '4th Level': {'4th Spell Slots': {}, '4th lvl Spells': {}}, 
                                                               '5th Level': {'5th Spell Slots': {}, '5th lvl Spells': {}}, 
                                                               '6th Level': {'6th Spell Slots': {}, '6th lvl Spells': {}}, 
                                                               '7th Level': {'7th Spell Slots': {}, '7th lvl Spells': {}}, 
                                                               '8th Level': {'8th Spell Slots': {}, '8th lvl Spells': {}}, 
                                                               '9th Level': {'9th Spell Slots': {}, '9th lvl Spells': {}}},
                                      'Skills' : {'Skills' : []}, 'Languages' : {'Languages' : []}
                        },
                        'Inventory' : 
                        {'Coins': 
                            {'Platinum': 0, 'Gold' : 0, 'Silver': 0, 'Copper': 0},
                        'Equipped Weapon': {},'Weapons' : [], 'Equipped Armour' : {}, 'Armour' : [], 'Items' : [] }
                    }
                 }
                  
        data.append(player)
        with open('Characters.json', 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

        # print(player)
        return player

    def load(Name, Race, Class):
        with open('Characters.json') as f:
            data = json.load(f)
            for i in range(0, len(data)):
                role = data[i]['Role']
                if data[i][role]['Attributes']['Name'] == Name and data[i][role]['Attributes']['Race'] == Race and data[i][role]['Attributes']['Class'] == Class:
                    player = data[i][role]
                    # print(player)
                    return player
            else:
                return False
        
    def __str__(self):
        return f'Character ID:{self.ID} - {self.Name} is a level {self.Level} {self.Race} {self.Class} with {self.Health} health, {self.Strength} strength, {self.Dexterity} dexterity, {self.Constitution} constitution, {self.Intelligence} intelligence, {self.Wisdom} wisdom, and {self.Charisma} charisma.'

    feats = [{'Sentinel', "A successful OA reduce creature's speed to 0 for this turn and possibility to make an OA even if the ennemy take Disengage."},
            {'Great Weapon Master', 'Extra attack after a melee critical hit and you can choose to take -5 to attack roll to add +10 to damage with an heavy weapon.'},
            {'Sharpshooter', 'Extra attack after a ranged critical hit and you can choose to take -5 to attack roll to add +10 to damage with a ranged weapon.'},
            {'Mage Slayer', 'Advantage on saving throw against spell and opportunity attack against a creature casting a spell.'},
            {'Lucky', 'You can reroll 1, 2 or 3 on a d20 roll.'}]

    def level_up(self, choice):
        print('first line')
        print(f'{self.Name} leveled up!')
        self.Level += 1
        if self.Level == 3 and self.Subclass is None:
            self.Subclass = input('Choose your subclass: ')
        if choice == 'increase ability scores':
            print('You can increase one ability score by 2 or two ability scores by 1.')
            cost = 2
            while cost > 0:
                ability = input('Which ability would you like to increase? ').lower()
                try:
                    increase = int(input('Would you like to increase that ability by 1 or 2? '))
                    if increase not in [1, 2]:
                            raise ValueError('Invalid increase amount')
                except ValueError as e:
                    print(e)
                    continue

                if ability == 'strength':
                    self.Strength += increase
                elif ability == 'dexterity' :
                    self.Dexterity += increase
                elif ability == 'constitution' :
                    self.Constitution += increase
                elif ability == 'intelligence':
                    self.Intelligence += increase
                elif ability == 'wisdom':
                    self.Wisdom += increase
                elif ability == 'charisma':
                    self.Charisma += increase
                else:
                    print('Invalid ability. Please try again.')
                    continue

                cost -= increase

        elif choice == 'feat':
            
            for title, desc in Character.feats:
                print(f'{title}: {desc} \n')
            feat = input('Which feat would you like to take? ')
            self.feat.append(feat)

    def heal(self, amount):
        self.Health += amount
    
    def damage(self, amount):
        self.Health -= amount
