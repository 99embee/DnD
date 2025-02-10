import tkinter as tk
from tkinter import messagebox
import random

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

        self.weapon_check = tk.Checkbutton(self.root, text="Sword", variable=self.D6, onvalue=self.D6)
        self.weapon_check.pack(pady=5)
        self.attack_btn = tk.Button(self.root, text="Attack", command=lambda:self.attack(self.D20, self.weapon_check.cget("variable"), True, False))
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

        create_button = tk.Button(new_window, text="Create", command=lambda: self.save_character(new_window, name_entry.get(), race_entry.get(), class_entry.get()))
        create_button.pack(pady=10)
    def save_character(self, window, name, race, char_class):
        # Here you can add the logic to save the character
        print(f"Character Created: {name}, {race}, {char_class}")
        messagebox.showinfo("Character Created", f"Character Created: {name}, {race}, {char_class}")
        window.destroy()

    def attack(self, dice, attackDice, advantage, disadvantage=False):
        if advantage|disadvantage:
            result, rolls = dice.roll(2)
            # rolls = rolls.split(",")
            if advantage:
                if rolls[0] > rolls[1]:
                    result = rolls[0]
                else:
                    result = rolls[1]
            else:
                if rolls[0] < rolls[1]:
                    result = rolls[0]
                else:
                    result = rolls[1]
        else:
            result, rolls = dice.roll(1)
        result = int(result)
        # self.test_lbl.config(text=f"result: {rolls if len(rolls) != 1 else ""} {result}")
        if result == 20:
            self.attack_lbl.config(text=f"Critical Hit: {rolls if len(rolls) != 1 else ""} {result}") 
        elif result == 1:
            self.attack_lbl.config(text=f"Critical Miss: {rolls if len(rolls) != 1 else ""} {result}") 
        else:
            self.attack_lbl.config(text=f"To Hit: {advantage}, {rolls if len(rolls) != 1 else ""} {result}") 
        

    def roll_dice(self, dice, times):  
        result, rolls = dice.roll(times)
        if dice == self.D4:
            self.d4_label.config(text=f"Result: {rolls} = {result}")
        elif dice == self.D6:
            self.d6_label.config(text=f"Result: {rolls} = {result}")
        elif dice == self.D8:
            self.d8_label.config(text=f"Result: {rolls} = {result}")
        elif dice == self.D10:
            self.d10_label.config(text=f"Result: {rolls} = {result}")
        elif dice == self.D20:
            self.d20_label.config(text=f"Result: {rolls} = {result}")

    def show_map(self):
        messagebox.showinfo("Map", "Interactive map will be displayed here.")

if __name__ == "__main__":
    root = tk.Tk()
    app = DnDApp(root)
    root.mainloop()