import tkinter as tk
# from tkinter.ttk import *

from Dice import Dice

class DnDApp:
    def __init__(self, root):
        self.root = root
        self.root.title("DnD Game")
        
        self.D4 = Dice(4)
        self.D6 = Dice(6)
        self.D8 = Dice(8)
        self.D10 = Dice(10)
        self.D20 = Dice(20)
        self.create_widgets()

    def create_dice(self, dice):
        diceArray = dice.split("d")
        rightDice = Dice(int(diceArray[1]))
        leftDice = int(diceArray[0])
        damage, damageRolls = rightDice.roll(leftDice)
        print(damage, damageRolls)
        return damage, damageRolls

    def create_widgets(self):
        # self.d4_edit = tk.Entry(self.root)
        # self.d4_edit.pack(pady=5)
        # self.d4_button = tk.Button(self.root, text="Roll D4", command=lambda:self.roll_dice(self.D4, int(self.d4_edit.get())))
        # self.d4_button.pack(pady=5)
        # self.d4_label = tk.Label(self.root, text="")
        # self.d4_label.pack(pady=5)

        # self.d6_edit = tk.Entry(self.root)
        # self.d6_edit.pack(pady=5)
        # self.d6_button = tk.Button(self.root, text="Roll D6", command=lambda:self.roll_dice(self.D6, int(self.d6_edit.get() )))
        # self.d6_button.pack(pady=5)
        # self.d6_label = tk.Label(self.root, text="")
        # self.d6_label.pack(pady=5)

        # self.d8_edit = tk.Entry(self.root)
        # self.d8_edit.pack(pady=5)
        # self.d8_button = tk.Button(self.root, text="Roll D8", command=lambda:self.roll_dice(self.D8, int(self.d8_edit.get() )))
        # self.d8_button.pack(pady=5)
        # self.d8_label = tk.Label(self.root, text="")
        # self.d8_label.pack(pady=5)

        # self.d10_edit = tk.Entry(self.root)
        # self.d10_edit.pack(pady=5)
        # self.d10_button = tk.Button(self.root, text="Roll D10", command=lambda:self.roll_dice(self.D10, int(self.d10_edit.get())) )
        # self.d10_button.pack(pady=5)
        # self.d10_label = tk.Label(self.root, text="")
        # self.d10_label.pack(pady=5)

        # self.d20_edit = tk.Entry(self.root)
        # self.d20_edit.pack(pady=5)
        # self.d20_button = tk.Button(self.root, text="Roll D20", command=lambda:self.roll_dice(self.D20,  int(self.d20_edit.get()) ))
        # self.d20_button.pack(pady=5)
        # self.d20_label = tk.Label(self.root, text="")
        # self.d20_label.pack(pady=5)
        

        
        weapons = [("Sword", "1d6"), ("Dagger", "1d4"), ("Axe", "1d8"), ("Mace", "1d10"), ("Greatsword", "2d6"), ("Greataxe", "1d12"), ("Greatclub", "1d8")] 
        # print(weapons)

       
        selected_dice = tk.StringVar(value=weapons[0][1])


        for (weapon, dice) in weapons:
            tk.Radiobutton(self.root, text=weapon, variable=selected_dice, value=dice).pack(anchor=tk.W)
        self.attack_btn = tk.Button(self.root, text="Attack", command=lambda:self.attack(self.D20, selected_dice.get(), True, False))
        self.attack_btn.pack(pady=5)
        self.attack_lbl = tk.Label(self.root, text="")
        self.attack_lbl.pack(pady=5)

        self.test_lbl = tk.Label(self.root, text="")
        self.test_lbl.pack(pady=5)

        # self.map_button = tk.Button(self.root, text="Show Map", command=self.show_map)
        # self.map_button.pack(pady=10)
        self.character_create_button = tk.Button(self.root, text="Create Character", command=self.create_character)
        self.character_create_button.pack(pady=10)

    def create_character(self):
        new_window = tk.Toplevel(self.root)
        new_window.title("Create Character")

        name_label = tk.Label(new_window, text="Name:")
        name_label.pack(pady=5)
        name_entry = tk.Entry(new_window)
        name_entry.pack(pady=5)

        race_label = tk.Label(new_window, text="Race:")
        race_label.pack(pady=5)
        race_entry = tk.Entry(new_window)
        race_entry.pack(pady=5)

        class_label = tk.Label(new_window, text="Class:")
        class_label.pack(pady=5)
        class_entry = tk.Entry(new_window)
        class_entry.pack(pady=5)

        ability_label = tk.Label(new_window, text="Ability Scores:")
        ability_label.pack(pady=5)
        ability_frame = tk.Frame(new_window)
        ability_frame.pack(pady=5)


        create_button = tk.Button(new_window, text="Create", command=lambda: self.save_character(new_window, name_entry.get(), race_entry.get(), class_entry.get()))
        create_button.pack(pady=10)
    def save_character(self, window, name, race, char_class):
        # Here you can add the logic to save the character
        print(f"Character Created: {name}, {race}, {char_class}")
        messagebox.showinfo("Character Created", f"Character Created: {name}, {race}, {char_class}")
        window.destroy()

    def attack(self, dice, attackDice, advantage, disadvantage):
        if advantage|disadvantage:
            result, rolls = dice.roll(2)
            if advantage:
                print(rolls)
                print(max(rolls))
                result = max(rolls)
                print(result)
            else:
                result = min(int(rolls))
        else:
            result, rolls = dice.roll(1)
        result = int(result)
        if result == 20:
            self.attack_lbl.config(text=f"Critical Hit: {rolls if len(rolls) != 1 else ""} {result}") 
        elif result == 1:
            self.attack_lbl.config(text=f"Critical Miss: {rolls if len(rolls) != 1 else ""} {result}") 
        else:
            self.attack_lbl.config(text=f"To Hit: {advantage}, {rolls if len(rolls) != 1 else ""} {result}") 

        # print(attackDice)
        damage, damageRolls = self.create_dice(attackDice)
        self.damage_lbl = tk.Label(self.root, text=f"Damage dealt: {damageRolls if len(damageRolls) != 1 else ""} {damage}").pack(pady=5)       
        

    # def roll_dice(self, dice, times):  
    #     result, rolls = dice.roll(times)
    #     if dice == self.D4:
    #         self.d4_label.config(text=f"Result: {rolls} = {result}")
    #     elif dice == self.D6:
    #         self.d6_label.config(text=f"Result: {rolls} = {result}")
    #     elif dice == self.D8:
    #         self.d8_label.config(text=f"Result: {rolls} = {result}")
    #     elif dice == self.D10:
    #         self.d10_label.config(text=f"Result: {rolls} = {result}")
    #     elif dice == self.D20:
    #         self.d20_label.config(text=f"Result: {rolls} = {result}")

if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("400x400")
 
    # set minimum window size value
    root.minsize(400, 400)

    app = DnDApp(root)

    root.mainloop()