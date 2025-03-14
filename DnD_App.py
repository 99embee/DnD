import json
import Character
import Race
import Class
import random
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import textwrap

class DnD_App:
    def __init__(self, root):
        self.root = root
        self.root.title("DnD Game")
        self.root.configure(bg='firebrick')
        self.root.minsize(800, 600)

        self.createGUI()
        # self.startGUI()

    def rollDice(self, dice, bonus):
        diceArray = dice.split("d")
        leftDice = diceArray[0]
        rightDice = diceArray[1]
        total = 0
        rolls = []
        for i in range(0, int(leftDice)):
            num = random.randint(1, int(rightDice))
            total += num
            rolls.append(num)
        if bonus != "":
            total += bonus
            return total, rolls
        else:
            return total, rolls

    def startGUI(self):
        startFrame = tk.Frame(self.root, width=400, height=400, bg='light grey', bd=2, relief='solid')
        startFrame.pack(padx=20, pady=20)
        lblTitle = tk.Label(startFrame, text="D&D App", bg='SteelBlue4', font=('Helvetica', 16, 'bold'))
        lblTitle.grid(row=0, column=0, padx=10, pady=10, sticky='n')
        btnCreate = tk.Button(startFrame, text="Create Character", bg='SteelBlue4', font=('Helvetica', 12), command=self.designCharacter)
        btnCreate.grid(row=1, column=0, padx=10, pady=10, sticky='n')
        btnLoad = tk.Button(startFrame, text="Load Character", bg='SteelBlue4', font=('Helvetica', 12), command=self.loadCharacter)
        btnLoad.grid(row=2, column=0, padx=10, pady=10, sticky='n')
        btnExit = tk.Button(startFrame, text="Exit", bg='SteelBlue4', font=('Helvetica', 12), command=self.root.quit)
        btnExit.grid(row=3, column=0, padx=10, pady=10, sticky='n')

    def createGUI(self):
        plyr = Character.Character.load('test Barb', 'Human', 'Barbarian')

        if not plyr:
            plyr = self.designCharacter()
            print(plyr)

        attribute = plyr['Attributes']
        abilities = attribute['Abilities']
        plyrInventory = plyr['Inventory']

        leftFrame = tk.Frame(self.root, width=200, height=500, bg='light grey', bd=2, relief='solid')
        leftFrame.pack(padx=20, pady=20, side=tk.LEFT, fill=tk.Y)
        tk.Label(leftFrame, text="D&D App", bg='light grey', font=('Helvetica', 14, 'bold')).pack(padx=50, pady=10)

        notebook = ttk.Notebook(leftFrame)
        notebook.pack(expand=True, fill='both')

        # Character Sheet Tab
        characterTab = tk.Frame(notebook, bg='SteelBlue4', bd=2, relief='solid')

        AC = plyrInventory['Equipped Armour']['AC']

        stats = [('Level', attribute['Level']), ('Experience', attribute['Experience']), ('Name', attribute['Name']), ('Race', attribute['Race']), ('Class', attribute['Class']),
                 ('Health', attribute['Health']), ('AC', AC), ('Strength', abilities['Strength']), ('Dexterity', abilities['Dexterity']),
                 ('Constitution', abilities['Constitution']), ('Intelligence', abilities['Intelligence']), ('Wisdom', abilities['Wisdom']),
                 ('Charisma', abilities['Charisma'])]

        for i, (stat, value) in enumerate(stats):
            tk.Label(characterTab, text=stat, bg='light grey', font=('Helvetica', 12)).grid(row=i, column=0, padx=10, pady=5, sticky='w')
            tk.Label(characterTab, textvariable=tk.StringVar(value=value), bg='light grey', font=('Helvetica', 12)).grid(row=i, column=1, padx=10, pady=5, sticky='w')

        menuTab = tk.Frame(notebook, bg='SteelBlue4', bd=2, relief='solid')
        options = [('Create Character', self.designCharacter), ('Load Character', self.loadCharacter),  ('Exit', self.root.quit)] #('Save Character', self.saveCharacter),
        for i, (option, command) in enumerate(options):
            tk.Button(menuTab, text=option, bg='light grey', font=('Helvetica', 12), command=command).grid(row=i, column=0, padx=10, pady=10, sticky='w')

        # Inventory Tab
        inventoryTab = tk.Frame(notebook, bg='SteelBlue4', bd=2, relief='solid')
        inventory = [('Equipped Weapon', plyrInventory['Equipped Weapon']['Weapon Name'] + ' - ' + plyrInventory['Equipped Weapon']['Attack Dice']),
                     ('Equipped Armor', plyrInventory['Equipped Armour']['Armour Name']),
                     ('Coins', str(plyrInventory['Coins']['Platinum']) + 'pp, ' + str(plyrInventory['Coins']['Gold']) + 'gp, ' + str(plyrInventory['Coins']['Silver']) + 'sp, ' + str(plyrInventory['Coins']['Copper']) + 'cp')]

        for i, (item, value) in enumerate(inventory):
            tk.Label(inventoryTab, text=item, bg='light grey', font=('Helvetica', 12)).grid(row=i, column=0, padx=10, pady=5, sticky='w')
            tk.Label(inventoryTab, textvariable=tk.StringVar(value=value), bg='light grey', font=('Helvetica', 12)).grid(row=i, column=1, padx=10, pady=5, sticky='w')

        # Spells Tab
        spellsTab = tk.Frame(notebook, bg='SteelBlue4', bd=2, relief='solid')
        spells = [('Level 1', 'Magic Missile'), ('Level 2', 'Healing Hands'), ('Level 3', 'Fireball')]
        for i, (spell, value) in enumerate(spells):
            tk.Label(spellsTab, text=spell, bg='light grey', font=('Helvetica', 12)).grid(row=i, column=0, padx=10, pady=5, sticky='w')
            tk.Label(spellsTab, text=value, bg='light grey', font=('Helvetica', 12)).grid(row=i, column=1, padx=10, pady=5, sticky='w')

        # Dice Tab
        diceTab = tk.Frame(notebook, bg='SteelBlue4', bd=2, relief='solid')
        dice = [('1d4', ''), ('1d6', ''), ('1d8', ''), ('1d10', ''), ('1d12', ''), ('1d20', ''), ('1d100', '')]
        for i, (dice, bonus) in enumerate(dice):
            tk.Button(diceTab, text=dice, bg='light grey', font=('Helvetica', 12), command=lambda d=dice, b=bonus: self.rollDice(d, b)).grid(row=i, column=0, padx=10, pady=5, sticky='w')

        menu = [(characterTab, 'Character Sheet'), (inventoryTab, 'Inventory'), (spellsTab, 'Spells'), (diceTab, 'Dice'), (menuTab, 'Menu')]
        for i, (tabs, title) in enumerate(menu):
            notebook.add(tabs, text=title)

        mainFrame = tk.Frame(self.root, width=600, height=600, bg='light grey', bd=2, relief='solid')
        mainFrame.pack(padx=20, pady=20, side=tk.RIGHT)

    def abilityRolls(self, lblAbilityScores, lblTotals, lblRolls, cbxAbilities, appliedRaceBonuses, appliedSubraceBonuses):
        abilities = [('Strength', 10), ('Dexterity', 11), ('Constitution', 12), ('Intelligence', 13), ('Wisdom', 14), ('Charisma', 15)]
        availableAbilities = [ability for ability, _ in abilities]
        selectedAbilities = {}
        diceRolls = {}

        # Reset dice rolls in ability scores
        for ability, pos in abilities:
            racial_bonus = appliedRaceBonuses.get(ability[:3].lower(), 0) + appliedSubraceBonuses.get(ability[:3].lower(), 0)
            lblAbilityScores[pos].config(text=racial_bonus)
            diceRolls[pos] = 0

        for x, (ability, pos) in enumerate(abilities):
            total, rolls = self.rollDice("4d6", "")
            total = total - min(rolls)
            lblTotals[x].config(text=total)
            lblRolls[x].config(text=rolls)
            cbxAbilities[x].set("None")
            diceRolls[pos] = total

            def on_combobox_select(event, x=x, total=total):
                selectedAbility = cbxAbilities[x].get()
                if selectedAbility:
                    if x in selectedAbilities:
                        previousAbility = selectedAbilities[x]
                        if previousAbility != "None":
                            previousPos = next(pos for ability, pos in abilities if ability == previousAbility)
                            current_value = int(lblAbilityScores[previousPos].cget("text"))
                            new_value = current_value - total
                            lblAbilityScores[previousPos].config(text=new_value)
                            if previousAbility not in availableAbilities:
                                availableAbilities.append(previousAbility)
                        del selectedAbilities[x]
                    if selectedAbility != "None":
                        selectedAbilities[x] = selectedAbility
                        pos = next(pos for ability, pos in abilities if ability == selectedAbility)
                        current_value = int(lblAbilityScores[pos].cget("text"))
                        new_value = current_value + total
                        lblAbilityScores[pos].config(text=new_value)
                        availableAbilities.remove(selectedAbility)
                    updateComboboxes()

            cbxAbilities[x].bind("<<ComboboxSelected>>", on_combobox_select)

        def updateComboboxes():
            for i in range(6):
                cbxAbilities['values'] = ["None"] + [ability for ability in availableAbilities if ability not in selectedAbilities.values() or ability == "None"]
        updateComboboxes()

    def designCharacter(self):
        createChar = tk.Toplevel(self.root, bg='firebrick')
        createChar.title("Create a character")
        createChar.geometry("1000x600")

        notebook = ttk.Notebook(createChar)
        notebook.pack(expand=True, fill='both')

        # Name and Class Tab
        nameClassTab = tk.Frame(notebook, bg='SteelBlue4', bd=2, relief='solid')
        notebook.add(nameClassTab, text='Name and Class')

        details = [('What is your character\'s name?', 3), ('What is your character\'s class?', 8)]
        chrDetails = {}
        entryDetails = {}
        for i, (question, pos) in enumerate(details):
            lblDetails = tk.Label(nameClassTab, text=question, bg='SteelBlue4', font=('Helvetica', 12))
            lblDetails.grid(row=i, column=0, padx=10, pady=5, sticky='w')
            entryDetails[pos] = tk.Entry(nameClassTab, bg='SteelBlue4', font=('Helvetica', 12))
            entryDetails[pos].grid(row=i, column=1, padx=10, pady=5, sticky='w')
        
        classVar = tk.StringVar()
        classMenu = ttk.Combobox(nameClassTab, textvariable=classVar, state='readonly', font=('Helvetica', 12))
        classMenu.grid(row=1, column=1, padx=10, pady=5, sticky='w')

        class_classes = Class.load_classes()
        classMenu['values'] = class_classes

        # Background Tab
        backgroundTab = tk.Frame(notebook, bg='SteelBlue4', bd=2, relief='solid')
        notebook.add(backgroundTab, text='Background')

        # Race and Subrace Tab
        raceSubraceTab = tk.Frame(notebook, bg='SteelBlue4', bd=2, relief='solid')
        notebook.add(raceSubraceTab, text='Race and Subrace')

        raceVar = tk.StringVar()
        raceMenu = ttk.Combobox(raceSubraceTab, textvariable=raceVar, state='readonly', font=('Helvetica', 12))
        raceMenu.grid(row=0, column=1, padx=10, pady=5, sticky='w')

        subraceVar = tk.StringVar()
        subraceMenu = ttk.Combobox(raceSubraceTab, textvariable=subraceVar, state='readonly', font=('Helvetica', 12))
        subraceMenu.grid(row=1, column=1, padx=10, pady=5, sticky='w')
        
        race_classes = Race.load_races()
        subrace_classes = Race.load_subraces()

        raceMenu['values'] = race_classes

        def updateSubraces(event):
            race_name = raceVar.get()
            subraces = subrace_classes.get(race_name, [])
            subraceMenu['values'] = subraces
            subraceMenu.set('')  # Clear the current selection

        raceMenu.bind("<<ComboboxSelected>>", updateSubraces)

        # Dice Roll and Abilities Tab
        diceAbilitiesTab = tk.Frame(notebook, bg='SteelBlue4', bd=2, relief='solid')
        notebook.add(diceAbilitiesTab, text='Dice Roll and Abilities')

        abilities = [('Strength', 10), ('Dexterity', 11), ('Constitution', 12), ('Intelligence', 13), ('Wisdom', 14), ('Charisma', 15)]
        lblAbilityScores = {}
        btnBonuses = {}
        for i, (ability, pos) in enumerate(abilities):
            lblAbility = tk.Label(diceAbilitiesTab, text=ability, bg='SteelBlue4', font=('Helvetica', 12))
            lblAbility.grid(row=1, column=i, padx=10, pady=5, sticky='w')
            lblAbilityScores[pos] = tk.Label(diceAbilitiesTab, text=0, bg='SteelBlue4', font=('Helvetica', 12))
            lblAbilityScores[pos].grid(row=2, column=i, padx=10, pady=5, sticky='w')
            btnBonuses[pos] = tk.Button(diceAbilitiesTab, text=0, bg='SteelBlue4', font=('Helvetica', 12))
            btnBonuses[pos].grid(row=3, column=i, padx=10, pady=5, sticky='w')

        tk.Button(diceAbilitiesTab, text='Roll', command=lambda: self.abilityRolls(lblAbilityScores), bg='SteelBlue4', font=('Helvetica', 12)).grid(row=4, column=0, padx=10, pady=5, sticky='w')

        # Equipment Tab
        equipmentTab = tk.Frame(notebook, bg='SteelBlue4', bd=2, relief='solid')
        notebook.add(equipmentTab, text='Equipment')

        tk.Button(createChar, text='Apply', command=lambda: self.createCharacter(chrDetails, entryDetails, raceVar, subraceVar, classVar, lblAbilityScores, createChar), bg='SteelBlue4', font=('Helvetica', 12)).pack(padx=20, pady=20)

        
    def createCharacter(self, chrDetails, entryDetails, raceVar, subraceVar, classVar, lblAbilityScores, createChar):
        chrDetails[3] = entryDetails.get()
        chrDetails[6] = raceVar.get()
        chrDetails[7] = classVar.get()
        chrDetails[8] = subraceVar.get()

        for pos in lblAbilityScores:
            chrDetails[pos] = lblAbilityScores[pos].cget("text")

        if any(value == "" for value in chrDetails.values()):
            messagebox.showerror("Error", "All fields must be filled out.")
            return

        class_data = Class.get_class_data(chrDetails[7])
        character_class = Class.CharacterClassFactory.create_character_class(class_data)

        race_data = Race.get_race_data(chrDetails[6])
        character_race = Race.CharacterRaceFactory.create_character_race(race_data)

        subrace_data = Race.get_subrace_data(chrDetails[6], chrDetails[8])

        plyr = Character.Character(0, 'Player', chrDetails[3], 1, 0, character_race.name, subrace_data['name'], character_class.name, self.rollDice(character_class.hit_die, "")[0], chrDetails[10], chrDetails[11], chrDetails[12], chrDetails[13], chrDetails[14], chrDetails[15])
        if plyr.checkUnique():
            plyr.save()
            createChar.destroy()
            print('success')
        else:
            print("Character already exists.")
            choice = input("Would you like to load that player? Yes or No?")
            if choice.lower() == "yes":
                plyr = self.loadCharacter(chrDetails[3], chrDetails[6], chrDetails[7])
            else:
                self.main()
        return plyr

    def loadCharacter(self, name, race, chrClass):
        if not name and not race and not chrClass:
            print("Welcome to the D&D Character Loader!")
            name = input("What is your character's name?")
            race = input("What is your character's race?")
            chrClass = input("What is your character's class?")

        player = Character.Character.load(name, race, chrClass)
        if player:
            plyr = Character.Character(player['ID'], 'Player', player['Name'], player['Level'], player['Experience'], player['Race'], player['Class'], player['Health'], player['Abilities']['Strength'], player['Abilities']['Dexterity'], player['Abilities']['Constitution'], player['Abilities']['Intelligence'], player['Abilities']['Wisdom'], player['Abilities']['Charisma'])
            return plyr
        else:
            print("Character does not exist.")
            self.main()

    def battle(self, plyr):
        mob = Character.Character(0, 'Mob', 'Goblin', 1, 0, 'Goblin', 'Warrior', self.rollDice("1d8", "")[0], self.rollDice("3d6", "")[0], self.rollDice("3d6", "")[0], self.rollDice("3d6", "")[0], self.rollDice("3d6", "")[0], self.rollDice("3d6", "")[0], self.rollDice("3d6", "")[0])
        if mob.checkUnique():
            mob = mob.save()
        else:
            mob = self.loadCharacter(mob.Name, mob.Race, mob.Class)
            print('loaded mob: ', mob)

        print(f"A {mob.Name} appears!")
        choice = input("Would you like to attack or run?")
        if choice == "attack":
            playerInitiative = self.rollDice("1d20", "")
            mobInitiative = self.rollDice("1d20", "")
            if playerInitiative > mobInitiative:
                initiative = [plyr, mob]
                print(f"{plyr.Name} go first!")
            else:
                initiative = [mob, plyr]
                print(f"The {mob.Name} goes first!")
            while mob.Health > 0 or plyr.Health > 0:
                if initiative[0].Health > 0:
                    self.attack(initiative[0], initiative[1])
                else:
                    print(f"{initiative[0].Name} died!")
                    break
                if initiative[1].Health > 0:
                    self.attack(initiative[1], initiative[0])
                else:
                    print(f"{initiative[1].Name} died!")
                    break
        elif choice == "run":
            print("You ran away! Coward!")

    def attack(self, friend, enemy):
        weaponDice = self.checkEquipped(friend, "Weapon")
        enemyAC = self.checkEquipped(enemy, "AC")
        toHit, toHitRolls = self.rollDice("1d20", "")
        if toHit >= enemyAC:
            attack, rolls = self.rollDice(weaponDice["Attack Dice"], "")
            print(f"{friend.Name} hit {enemy.Name} for {attack} damage!")
            enemy.damage(attack)
        else:
            print(f"{friend.Name} missed!")

    def attackDetails(self, enemy):
        role = enemy.Role
        with open('Characters.json') as f:
            data = json.load(f)
            for enemy in data:
                if enemy[role]['Attributes']['Name'] == enemy.Name:
                    return enemy

    def checkEquipped(self, plyr, search):
        with open('Characters.json') as f:
            data = json.load(f)
            for i in range(0, len(data)):
                role = data[i]['Role']
                if data[i][role]['Attributes']['ID'] == plyr.ID:
                    if search == 'Weapon':
                        return data[i][role]['Inventory']['Equipped Weapon']
                    elif search == 'AC':
                        return data[i][role]['Attributes']['AC']

    def story(self, plyr):
        self.battle(plyr)

    def dev(self):
        plyr = self.loadCharacter("Matthew", "Human", "Rogue")
        plyr.level_up("increase ability scores")

    def levelUp(self, plyr):
        print("Level up")
        level_up_choice = input("Would you like to 'increase ability scores' or choose a 'feat'? ")
        match level_up_choice:
            case "increase ability scores":
                plyr.level_up("increase ability scores")
            case "feat":
                plyr.level_up("feat")
            case _:
                print("Invalid choice. Please try again.")
                self.levelUp(plyr)

    def main(self):
        print("Welcome to the D&D App!")
        choice = input("Would you like to create a new character or load an existing character? ")
        match choice:
            case "create":
                plyr = self.designCharacter()
            case "load":
                plyr = self.loadCharacter("", "", "")
            case "clear":
                with open('Characters.json', 'w') as f:
                    f.write("")
                    self.main()
            case "Level up":
                self.levelUp()
            case "dev":
                self.dev()
            case "exit":
                print("Goodbye!")
                exit()
            case _:
                print("Invalid choice. Please try again.")
                self.main()
        self.story(plyr)

if __name__ == "__main__":
    root = tk.Tk()
    app = DnD_App(root)
    root.mainloop()

