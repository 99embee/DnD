import json
import Character
import random
import os

# print(os.getcwd())

plyr = Character.Character('', '', 0, 0, '', '', '', '', '', '', '', '', '')

def rollDice( dice, bonus):
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

def createCharacter():
    print("Welcome to the D&D Character Creator!")
    name = input("What is your character's name? ")
    level = 1
    race = input("What is your character race? ")
    chrClass = input("What is your character class? ")
    # health = rollDice("1d10", "")
    # strength = rollDice("3d6", "")
    # dexterity = rollDice("3d6", "")
    # constitution = rollDice("3d6", "")
    # intelligence = rollDice("3d6", "")
    # wisdom = rollDice("3d6", "")
    # charisma = rollDice("3d6", "")
    plyr = Character.Character('Player', name, level, 0, race, chrClass, rollDice("1d10", "")[0], rollDice("3d6", "")[0], rollDice("3d6", "")[0], rollDice("3d6", "")[0], rollDice("3d6", "")[0], rollDice("3d6", "")[0], rollDice("3d6", "")[0])
    print(plyr)
    if plyr.checkUnique():
        plyr.save()
        print("Character created!")
    else:
        print("Character already exists!")
        print("Would you like to load that player?")
        choice = input("Yes or No?")
        if choice.lower() == "yes":
            plyr ==loadCharacter(name, race, chrClass)
        else:
            main()
    return plyr
    

def loadCharacter(name, race, chrClass):
    if not name and not race and not chrClass:
        print("Welcome to the D&D Character Loader!")
        name = input("What is your character's name?")
        race = input("What is your character's race?")
        chrClass = input("What is your character's class?")

    player = Character.Character.load(name, race, chrClass)
    print("before if")
    if player:
        # print(player)
        plyr = Character.Character('Player', player['Name'], player['Level'], player['Experience'], player['Race'], player['Class'], player['Health'], player['Abilities']['Strength'], player['Abilities']['Dexterity'], player['Abilities']['Constitution'], player['Abilities']['Intelligence'], player['Abilities']['Wisdom'], player['Abilities']['Charisma'])
        # print(plyr)
        return plyr
    else:
        print("Character does not exist.")
        main()

def battle(plyr):
    # print("battle", plyr)
    mob = Character.Character('Mob', 'Goblin', 1, 0, 'Goblin', 'Warrior', rollDice("1d8", "")[0], rollDice("3d6", "")[0], rollDice("3d6", "")[0], rollDice("3d6", "")[0], rollDice("3d6", "")[0], rollDice("3d6", "")[0], rollDice("3d6", ""))
    mob.save()
    print("A goblin appears!")
    choice = input("Would you like to attack or run?")
    if choice == "attack":
        playerInitiative = rollDice("1d20", "")
        mobInitiative = rollDice("1d20", "")
        if playerInitiative > mobInitiative:
            initiative = {plyr, mob}
            print("You go first!")       
            # print(plyr.Health)
        else:
            initiative = {mob, plyr}
            print(f"The {mob.Name} goes first!")
            # print(plyr.Health)
        print(initiative)
        print(initiative[0])
        print(initiative[1].Name)
        while mob.Health > 0 or plyr.Health > 0:
            # choice = input("Would you like to attack or run?")
            # if choice == "attack":
            if initiative[0].Health > 0:
                attack(initiative[1])
            else:
                print(f"{initiative[1].Name} died!")
                break
            if initiative[1].Health > 0:
                attack(initiative[0])
            else:
                print(f"{initiative[0].Name} died!")
                break
            # elif choice == "run":
            #     print("You ran away! Coward!")
    elif choice == "run":
        print("You ran away! Coward!")
        
def attack(enemy):
    mobDetails(enemy)
    weaponDice = checkEquipped()
    toHit = rollDice("1d20", "")
    if toHit >= 10:
        attack, rolls = rollDice(weaponDice, "")
        print(f"You hit {enemy.Name} for {attack[0]} damage!")
    else:
        print("You missed!")

def mobDetails(enemy):
    with open('Characters.json') as f:
        data = json.load(f)
        for player in data:
            if player['Mob']['Attributes']['Name'] == enemy.Name:
                return player['Mob']

def checkEquipped():
    with open('Characters.json') as f:
        data = json.load(f)
        for player in data:
            if player['Player']['Attributes']['ID'] == plyr.id:
                return player['Player']['Inventory']['Equipped Weapon']

def story(plyr):
    # print("story", plyr)
    battle(plyr)

def dev():
    plyr = loadCharacter("Matthew", "Human", "Rogue")
    print(plyr)
    # levelUp(plyr)
    plyr.level_up("increase ability scores")
    # Character.Character.level_up(plyr, "increase ability scores")
#   main()

def levelUp(plyr):
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
            levelUp(plyr)
    # main()

def main():
    
    print("Welcome to the D&D App!")
    choice = input("Would you like to create a new character or load an existing character? ")
    match choice:
        case "create":
            createCharacter()
        case "load":
            plyr = loadCharacter("", "", "")
            # load multiple 'players' into a party array?
        case "clear":
            with open('Characters.json', 'w') as f:
                f.write("")
                main()
        case "Level up":
            levelUp()
        case "dev":
            dev()
        case "exit":
            print("Goodbye!")
            exit()
        case _:
            print("Invalid choice. Please try again.")
            main()
        
    story(plyr)

if __name__ == "__main__":
    main()
    