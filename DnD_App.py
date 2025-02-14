import json
import Character
import random
import tkinter as tk
from tkinter import ttk

# import os
    # print(os.getcwd())

class DnD_App:
    def __init__(self, root):
        root = root
        root.title("DnD Game")
        root.geometry("800x600")
        root.configure(bg='firebrick')
        # set minimum window size value
        root.minsize(400, 400)

        self.createGUI()
        # self.main()
        

    plyr = Character.Character(0, '', '', 0, 0, '', '', '', '', '', '', '', '', '')

    def rollDice(self, dice, bonus):
        # print(dice)
        diceArray = dice.split("d")
        leftDice = diceArray[0]
        rightDice = diceArray[1]
        total = 0
        rolls = []
        for i in range(0, int(leftDice)):
            total += random.randint(1, int(rightDice))
            rolls.append(total)
        if bonus != "":
            total += bonus
            return total, rolls
        else:
            return total, rolls

    def createGUI(self):

        plyr = Character.Character.load('p','p','p')
        attribute = plyr['Attributes']
        abilities = attribute['Abilities']
        plyrInventory = plyr['Inventory']
        print(plyr)

        leftFrame = tk.Frame(root, width=200, height=500, bg='light grey')
        leftFrame.pack(padx=10, pady=10, side=tk.LEFT, fill=tk.Y )
        tk.Label(leftFrame, text="D&D App", bg='light grey').pack(padx=50, pady=5)

        notebook = ttk.Notebook(leftFrame)
        notebook.pack(expand=True, fill='both')

        # Character Sheet Tab
        characterTab = tk.Frame(notebook, bg='SteelBlue4')

        AC = plyrInventory['Equipped Armour']['AC']

        stats = [('Level', attribute['Level']), ('Experience', attribute['Experience']), ('Name', attribute['Name']), ('Race', attribute['Race']), ('Class', attribute['Class']),
        ('Health', attribute['Health']), ('AC', AC), ('Strength', abilities['Strength']), ('Dexterity', abilities['Dexterity']),
        ('Constitution', abilities['Constitution']), ('Intelligence', abilities['Intelligence']), ('Wisdom', abilities['Wisdom']),
        ('Charisma', abilities['Charisma'])]

        for i, (stats, value) in  enumerate(stats):
            tk.Label(characterTab, text=stats, bg='light grey').grid(row=i, column=0, padx=10, pady=5, sticky='w')
            tk.Label(characterTab, textvariable=tk.StringVar(value=value), bg='light grey').grid(row=i, column=1, padx=10, pady=5, sticky='w')
            # tk.Entry(characterTab, textvariable=tk.StringVar(value=value), bg='light grey').grid(row=i, column=1, padx=10, pady=5, sticky='w')

        menuTab = tk.Frame(notebook, bg='SteelBlue4')
        options = ('Create Character', 'Load Character', 'Save Character', 'Exit')
        for i, (option) in enumerate(options): 
            tk.Button(menuTab, text=option, bg='light grey').grid(row=i, column=0, padx=10, pady=5, sticky='w')

        # Inventory Tab
        inventoryTab = tk.Frame(notebook, bg='SteelBlue4')
        inventory = [('Equipped Weapon', plyrInventory['Equipped Weapon']['Weapon Name']+' - '+plyrInventory['Equipped Weapon']['Attack Dice']), 
                     ('Equipped Armor', plyrInventory['Equipped Armour']['Armour Name']), 
                     ('Coins', str(plyrInventory['Coins']['Platinum'])+ 'pp, '+str(plyrInventory['Coins']['Gold'])+'gp, '+str(plyrInventory['Coins']['Silver'])+'sp, '+str(plyrInventory['Coins']['Copper'])+'cp'), 
                     ] 
         
        for i, (inventory, value) in enumerate(inventory):
            tk.Label(inventoryTab, text=inventory, bg='light grey').grid(row=i, column=0, padx=10, pady=5, sticky='w')
            tk.Label(inventoryTab, textvariable=tk.StringVar(value=value), bg='light grey').grid(row=i, column=1, padx=10, pady=5, sticky='w')

        # Spells Tab
        spellsTab = tk.Frame(notebook, bg='SteelBlue4')
        spells = [('Level 1', 'Magic Missile'), ('Level 2', 'Healing Hands'), ('Level 3', 'Fireball')]
        for i, (spells, value) in enumerate(spells):
            tk.Label(spellsTab, text=spells, bg='light grey').grid(row=i, column=0, padx=10, pady=5, sticky='w')
            tk.Label(spellsTab, text=value, bg='light grey').grid(row=i, column=1, padx=10, pady=5, sticky='w')
        
        # Dice Tab - not working yet
        diceTab = tk.Frame(notebook, bg='SteelBlue4')
        dice = [('1d4',''),('1d6',''), ('1d8',''), ('1d10',''), ('1d12',''), ('1d20',''), ('1d100','')]
        for i, (dice, bonus) in enumerate(dice):
            tk.Button(diceTab, text=dice, bg='light grey', command=lambda:self.rollDice(dice, bonus)).grid(row=i, column=0, padx=10, pady=5, sticky='w')

        
        menu = [(characterTab, 'Character Sheet'), (inventoryTab,'Inventory'), (spellsTab,'Spells'), (diceTab,'Dice'), (menuTab, 'Menu')] 
        for i, (tabs, title) in enumerate(menu):
            notebook.add(tabs, text=title)

        
        mainFrame = tk.Frame(root, width=600, height=600, bg='light grey')
        mainFrame.pack(padx=10, pady=10, side=tk.RIGHT)


    def createCharacter(self):
        print("Welcome to the D&D Character Creator!")
        name = input("What is your character's name? ")
        level = 1
        race = input("What is your character race? ")
        chrClass = input("What is your character class? ")
        # health =self.rollDice("1d10", "")
        # strength =self.rollDice("3d6", "")
        # dexterity =self.rollDice("3d6", "")
        # constitution =self.rollDice("3d6", "")
        # intelligence =self.rollDice("3d6", "")
        # wisdom =self.rollDice("3d6", "")
        # charisma =self.rollDice("3d6", "")
        plyr = Character.Character(0, 'Player', name, level, 0, race, chrClass,self.rollDice("1d10", "")[0],self.rollDice("3d6", "")[0],self.rollDice("3d6", "")[0],self.rollDice("3d6", "")[0],self.rollDice("3d6", "")[0],self.rollDice("3d6", "")[0],self.rollDice("3d6", "")[0])
        print(plyr)
        if plyr.checkUnique():
            plyr.save()
            print("Character created!")
        else:
            print("Character already exists!")
            print("Would you like to load that player?")
            choice = input("Yes or No?")
            if choice.lower() == "yes":
                plyr == self.loadCharacter(name, race, chrClass)
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
        # print("loadCharacter: ",player)
        # print(player['ID'])
        # print("before if")
        if player:
            # print(player)
            plyr = Character.Character(player['ID'], 'Player', player['Name'], player['Level'], player['Experience'], player['Race'], player['Class'], player['Health'], player['Abilities']['Strength'], player['Abilities']['Dexterity'], player['Abilities']['Constitution'], player['Abilities']['Intelligence'], player['Abilities']['Wisdom'], player['Abilities']['Charisma'])
            # print(plyr)
            return plyr
        else:
            print("Character does not exist.")
            self.main()

    def battle(self, plyr):
        # print("battle: ", plyr)
        mob = Character.Character(0,'Mob', 'Goblin', 1, 0, 'Goblin', 'Warrior', self.rollDice("1d8", "")[0],self.rollDice("3d6", "")[0],self.rollDice("3d6", "")[0],self.rollDice("3d6", "")[0],self.rollDice("3d6", "")[0],self.rollDice("3d6", "")[0],self.rollDice("3d6", "")[0])
        if mob.checkUnique():
            mob = mob.save()
        else:
            mob = self.loadCharacter(mob.Name, mob.Race, mob.Class)
            print('loaded mob: ', mob)
        
        print("A goblin appears!")
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
            print(initiative)
            while mob.Health > 0 or plyr.Health > 0:
                # choice = input("Would you like to attack or run?")
                # if choice == "attack":
                if initiative[0].Health > 0:
                    self.attack(initiative[0],initiative[1]) #attacker, target.
                else:
                    print(f"{initiative[0].Name} died!")
                    break
                if initiative[1].Health > 0:
                    self.attack(initiative[1],initiative[0])
                else:
                    print(f"{initiative[1].Name} died!")
                    break
                # elif choice == "run":
                #     print("You ran away! Coward!")
        elif choice == "run":
            print("You ran away! Coward!")
            
    def attack(self, friend, enemy):
        # print("attack friend: ", friend)
        # print("attack enemy: ", enemy)
        # print(friend)
        weaponDice = self.checkEquipped(friend, "Weapon")
        enemyAC = self.checkEquipped(enemy, "AC")
        toHit, toHitRolls = self.rollDice("1d20", "")
        print(toHit)
        print(weaponDice)
        # print(weaponDice['Attack Dice'])
        if toHit >= enemyAC:
            attack, rolls = self.rollDice(weaponDice["Attack Dice"], "")
            print(attack)
            print(f"{friend.Name} hit {enemy.Name} for {attack} damage!")
            enemy.damage(attack)
        else:
            print(f"{friend.Name} missed!")

    def attackDetails(self, enemy):
        # print('attackdetails',enemy.Role)
        role = enemy.Role
        with open('Characters.json') as f:
            data = json.load(f)
            for enemy in data:
                if enemy[role]['Attributes']['Name'] == enemy.Name:
                    return enemy
                
    def checkEquipped(self, plyr, search):
        # print("checkEquipped", plyr)
        # print(plyr['ID'])
        with open('Characters.json') as f:
            data = json.load(f)
            for i in range(0,len(data)):
                role = data[i]['Role']
                # print(role)
                if data[i][role]['Attributes']['ID'] == plyr.ID:
                    if search == 'Weapon':
                        return data[i][role]['Inventory']['Equipped Weapon']
                    elif search == 'AC':
                        return data[i][role]['Attributes']['AC']

    def story(self, plyr):
        # print("story: ", plyr)
        self.battle(plyr)

    def dev(self):
        plyr = self.loadCharacter("Matthew", "Human", "Rogue")
        print(plyr)
        # levelUp(plyr)
        plyr.level_up("increase ability scores")
        # Character.Character.level_up(plyr, "increase ability scores")
        #   main()

    def levelUp(self, plyr):
        print("Level up")
        level_up_choice = input("Would you like to 'increase ability scores' or choose a 'feat'? ")
        match level_up_choice:
            case "increase ability scores":
                print("in the case")
                print(plyr)
                plyr.level_up("increase ability scores")
            case "feat":
                plyr.level_up("feat")
            case _: 
                print("Invalid choice. Please try again.")
                self.levelUp(plyr)
        # main()

    def main(self):
        
        print("Welcome to the D&D App!")
        choice = input("Would you like to create a new character or load an existing character? ")
        match choice:
            case "create":
                plyr = self.createCharacter()
            case "load":
                plyr = self.loadCharacter("", "", "")
                # load multiple 'players' into a party array?
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
        # print('main: ',plyr)
        self.story(plyr)

if __name__ == "__main__":
    root = tk.Tk()
    app = DnD_App(root)
    root.mainloop()
    
    