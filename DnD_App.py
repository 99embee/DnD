import json
import Character
import Backgrounds
import Deity
import Race
import Class
import random
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import re
import pandas as pd
# from transformers import pipeline
from transformers import AutoTokenizer, AutoModelForCausalLM

class DnD_App:
    def __init__(self, root):
        self.root = root
        self.root.title("DnD Game")
        self.root.configure(bg='firebrick')
        self.root.minsize(800, 600)
        
        self.party = []
        self.mobs = []

        # Load GPT-NeoX model
        # tokenizer = AutoTokenizer.from_pretrained("EleutherAI/gpt-neox-20b")
        # model = AutoModelForCausalLM.from_pretrained("EleutherAI/gpt-neox-20b")

        # print("test")
        # Load GPT-J model
        # self.tokenizer = AutoTokenizer.from_pretrained("EleutherAI/gpt-j-6B")
        # self.model = AutoModelForCausalLM.from_pretrained("EleutherAI/gpt-j-6B")

        self.tokenizer = AutoTokenizer.from_pretrained("gpt2")
        self.model = AutoModelForCausalLM.from_pretrained("gpt2")

        # self.dm_ai = pipeline("text-generation", model="gpt2")  # Replace "gpt2" with your desired model
        self.promptDefault = "You are a Dungeons and Dragons Dungeon Master. The setting is an epic fantasy world. Narrate the following event: "
        print("test")
        self.startFrame = None  # Store a reference to the start frame
        self.startGUI()

    def generate_story(self, prompt, max_length=200):
        inputs = self.tokenizer(prompt, return_tensors="pt")
        outputs = self.model.generate(inputs["input_ids"], max_length=max_length, temperature=0.7, top_p=0.9)
        return self.tokenizer.decode(outputs[0], skip_special_tokens=True)
   

    def generate_dm_response(self, prompt, max_length=150):
        """
        Generate a response from the AI Dungeon Master.
        """
        response = self.dm_ai(
            prompt, 
            max_length=max_length, 
            truncation=True, 
            num_return_sequences=1, 
            temperature=0.7, # Adjust the creativity of the response
            top_p=0.9,  # Use nucleus sampling
            top_k=40    # Consider only the top ## tokens
        )
        print(response)
        print("\n")

        generated_text = response[0]['generated_text']
        print(generated_text)
        # Remove the prompt from the generated text
        if generated_text.startswith(prompt):
            generated_text = generated_text[len(prompt):].strip()

        # Remove repeated sentences
        sentences = generated_text.split('. ')
        unique_sentences = []
        for sentence in sentences:
            if sentence not in unique_sentences:
                unique_sentences.append(sentence)
        concise_text = '. '.join(unique_sentences).strip()

        return concise_text

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
        self.startFrame = tk.Frame(self.root, width=400, height=400, bg='light grey', bd=2, relief='solid')
        self.startFrame.pack(padx=20, pady=20)
        lblTitle = tk.Label(self.startFrame, text="D&D App", bg='SteelBlue4', font=('Helvetica', 16, 'bold'))
        lblTitle.grid(row=0, column=0, padx=10, pady=10, sticky='n')
        btnCreate = tk.Button(self.startFrame, text="Create Character", bg='SteelBlue4', font=('Helvetica', 12), command=lambda: self.designCharacter())
        btnCreate.grid(row=1, column=0, padx=10, pady=10, sticky='n')
        btnLoad = tk.Button(self.startFrame, text="Load Character", bg='SteelBlue4', font=('Helvetica', 12), command=lambda: self.loadCharacter('','','', ''))
        btnLoad.grid(row=2, column=0, padx=10, pady=10, sticky='n')
        btnExit = tk.Button(self.startFrame, text="Exit", bg='SteelBlue4', font=('Helvetica', 12), command=self.root.quit)
        btnExit.grid(row=3, column=0, padx=10, pady=10, sticky='n')
        
        btnDev = tk.Button(self.startFrame, text="Dev Load", bg='SteelBlue4', font=('Helvetica', 12), command=lambda: self.loadCharacter('test Barb', 'Human', 'Barbarian', 'Player'))
        btnDev.grid(row=4, column=0, padx=10, pady=10, sticky='n')

    def createGUI(self, plyr):
        # print(plyr)
            
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

        stats = [('Level', attribute['Level']), ('Experience', attribute['Experience']), ('Name', attribute['Name']),
                 ('Race', attribute['Race']), ('Subrace', attribute['Subrace']), ('Class', attribute['Class']),
                 ('Subclass', attribute['Subclass']), ('Health', attribute['Health']), ('AC', AC), 
                 ('Strength', abilities['Strength']), ('Dexterity', abilities['Dexterity']), 
                 ('Constitution', abilities['Constitution']), ('Intelligence', abilities['Intelligence']), 
                 ('Wisdom', abilities['Wisdom']), ('Charisma', abilities['Charisma'])]

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

        self.txtOutput = tk.Text(mainFrame, wrap=tk.WORD, bg='light grey', font=('Helvetica', 8, 'bold'))
        self.txtOutput.grid(padx=10, pady=10, row=0, column=0, sticky='nsew')
        self.txtOutput.insert(tk.END,f"Welcome, {attribute['Name']}! \n\nYour character is ready to play.\n\nHave fun! \n")
        
        inputFrame = tk.Frame(mainFrame, bg='red', relief='solid')
        inputFrame.grid(padx=10, pady=10, sticky='ew', row=1, column=0)
        # inputFrame.grid_rowconfigure(0, weight=1)
        # inputFrame.grid_columnconfigure(0, weight=1)

        self.txtInput = tk.Text(inputFrame, wrap=tk.WORD, bg='light blue', font=('Helvetica', 8, 'bold'))
        self.txtInput.grid( padx=5, pady=5, sticky='ew', row=0, column=0)

        btnInput = tk.Button(inputFrame, text="Send", bg='SteelBlue4', font=('Helvetica', 8), command=lambda: self.IOText(self.txtInput.get('1.0',tk.END), "black"))
        btnInput.grid(padx=5, pady=5, sticky='ew', row=0, column=1)
        mainFrame.grid_rowconfigure(0, weight=1)

        # scrollbar = ttk.Scrollbar(mainFrame, orient=tk.VERTICAL, command=self.txtOutput.yview)
        # scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        # self.txtOutput.configure(yscrollcommand=scrollbar.set)
        self.txtOutput.config(state=tk.DISABLED)

    def IOText(self, text, colour):
        self.txtOutput.config(state=tk.NORMAL)
        self.txtOutput.insert(tk.END,"\n"+ text + "\n", colour)
        self.txtOutput.see(tk.END)
        self.txtOutput.config(state=tk.DISABLED)
        self.txtInput.delete('1.0',tk.END)  # Clear the input field

        self.txtOutput.tag_configure("blue", foreground="blue")  # Configure the tag for blue text
        self.txtOutput.tag_configure("red", foreground="red")  # Configure the tag for red text
        self.txtOutput.tag_configure("green", foreground="green")  # Configure the tag for green text
        self.txtOutput.tag_configure("yellow", foreground="yellow")  # Configure the tag for yellow text
        self.txtOutput.tag_configure("purple", foreground="purple")  # Configure the tag for purple text
        self.txtOutput.tag_configure("orange", foreground="orange")  # Configure the tag for orange text
        self.txtOutput.tag_configure("black", foreground="black")  # Configure the tag for black text
        self.txtOutput.tag_configure("white", foreground="white")  # Configure the tag for white text
        
        self.reader(text)
    
    def reader(self, word):
        word = word.strip().lower()
        if word == 'fight':
            print("fight")
            self.battle()

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
            cbxAbilities[x].config(state="readonly")
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
        chrDetails = {}
        chosenAbilities = []
        notebook = ttk.Notebook(createChar)
        notebook.grid(row=1, column=0, padx=10, pady=5, sticky='nsew', columnspan=8)

        # Class Tab
        nameClassTab = tk.Frame(notebook, bg='SteelBlue4', bd=2, relief='solid')
        notebook.add(nameClassTab, text='Class')

        # details = [('What is your character\'s name?', 3), ('What is your character\'s class?', 8)]
        entryDetails = {}
        
        lblDetails = tk.Label(createChar, text='What is your character\'s name?', bg='SteelBlue4', font=('Helvetica', 12))
        lblDetails.grid(row=0, column=0, padx=10, pady=5, sticky='w')    
        entryDetails[3] = tk.Entry(createChar, bg='SteelBlue4', font=('Helvetica', 12))
        entryDetails[3].grid(row=0, column=1, padx=10, pady=5, sticky='w')
        
        lblDetails = tk.Label(nameClassTab, text='What is your character\'s class?', bg='SteelBlue4', font=('Helvetica', 12))
        lblDetails.grid(row=1, column=0, padx=10, pady=5, sticky='w')  
        entryDetails[8] = tk.Entry(nameClassTab, bg='SteelBlue4', font=('Helvetica', 12))
        entryDetails[8].grid(row=1, column=1, padx=10, pady=5, sticky='w')

        classVar = tk.StringVar()
        classMenu = ttk.Combobox(nameClassTab, textvariable=classVar, state='readonly', font=('Helvetica', 12))
        classMenu.grid(row=1, column=1, padx=10, pady=5, sticky='w')

        class_classes = Class.load_classes()
        classMenu['values'] = class_classes

        classNotebook = ttk.Notebook(nameClassTab)
        classNotebook.grid(row=4, column=0, padx=10, columnspan=2, pady=5, sticky='w')

        lblClassTitle = tk.Label(nameClassTab, text='Class', bg='SteelBlue4', font=('Helvetica', 12))
        lblClassTitle.grid(row=3, column=0, padx=10, pady=5, sticky='w')

        classDetails = tk.Frame(classNotebook, bg='SteelBlue4', bd=2, relief='solid')
        classDetails.grid(row=3, column=0, columnspan=2, padx=20, pady=20, sticky='nsew')
        classTable = tk.Frame(classNotebook, bg='SteelBlue4', bd=2, relief='solid')
        classTable.grid(row=3, column=0, columnspan=2, padx=20, pady=20, sticky='nsew')
        classNotebook.add(classDetails, text='Class Details')
        classNotebook.add(classTable, text='Class Table')
        
        def displayClassDetails(event):
            class_name = classVar.get()
            class_data = Class.get_class_data(class_name)
            lblClassTitle.config(text=class_name)

            # Clear previous content in the classDetails frame
            for widget in classDetails.winfo_children():
                widget.destroy()

            # Clear previous content in the classTable frame
            for widget in classTable.winfo_children():
                widget.destroy()

            def decode_items(data):
                decoded_items = []
                if isinstance(data, list):
                    # If data is a list, process each item
                    for item in data:
                        if isinstance(item, dict):
                            # If the item is a dictionary, extract relevant fields
                            if "full" in item:
                                decoded_items.append(item["full"])  # Use the 'full' field if available
                            elif "proficiency" in item:
                                decoded_items.append(item["proficiency"])  # Use the 'proficiency' field as fallback
                            
                        elif isinstance(item, str):
                            # Check if the string matches the @item pattern
                            if re.match(r'\{@item .*?\}', item):
                                # Decode @item pattern
                                item = re.sub(r'\{@item (.*?)\|.*?\}', r'\1', item)
                            # Add the plain string or decoded item to the list
                            decoded_items.append(item)
                elif isinstance(data, dict):
                    # If data is a dict, process its values
                    for key, item in data.items():
                        if isinstance(item, dict):
                            # Handle nested dictionaries
                            if "full" in item:
                                decoded_items.append(item["full"])
                            elif "proficiency" in item:
                                decoded_items.append(item["proficiency"])
                        elif isinstance(item, str):
                            # Check if the string matches the @item pattern
                            if re.match(r'\{@item .*?\}', item):
                                # Decode @item pattern
                                item = re.sub(r'\{@item (.*?)\|.*?\}', r'\1', item)
                            # Add the plain string or decoded item to the list
                            decoded_items.append(item)
                return decoded_items

            def format_list(items, max_items_per_line=4):
                """
                Format a list of items into a string with a new line after a certain number of items.
                """
                formatted_lines = []
                for i in range(0, len(items), max_items_per_line):
                    formatted_lines.append(", ".join(items[i:i + max_items_per_line]))
                return "\n".join(formatted_lines)

            starting_proficiencies = class_data.get('startingProficiencies', {})
            # print(class_data)
            lblClassHitDice = tk.Label(classDetails, text=f"Hit Dice: {class_data['hit_dice']}", bg='SteelBlue4', font=('Helvetica', 12))
            lblClassHitDice.grid(row=1, column=0, padx=10, pady=5, sticky='w')
            lblClassProficiency = tk.Label(classDetails, text=f"Proficiency: {', '.join(class_data['proficiency'])}", bg='SteelBlue4', font=('Helvetica', 12))
            lblClassProficiency.grid(row=2, column=0, padx=10, pady=5, sticky='w')

            if starting_proficiencies.get('armor'):
                starting_armour = class_data['startingProficiencies']['armor']
                decoded_armour = decode_items(starting_armour)
                lblClassStartArmour = tk.Label(classDetails, text=f"Starting Armour: {', '.join(decoded_armour)}", bg='SteelBlue4', font=('Helvetica', 12))
                lblClassStartArmour.grid(row=3, column=0, padx=10, pady=5, sticky='w')
            if starting_proficiencies.get('tools'):
                starting_tools = class_data['startingProficiencies']['tools'][0]
                print(starting_tools)
                starting_tools = re.sub(r'\{@item (.*?)\|.*?\}', r'\1', starting_tools)
                # decoded_tools = decode_items(starting_tools)
                lblClassStartTools = tk.Label(classDetails, text=f"Starting Tools: {starting_tools}", bg='SteelBlue4', font=('Helvetica', 12))
                lblClassStartTools.grid(row=3, column=0, padx=10, pady=5, sticky='w')
            

            starting_weapons = class_data['startingProficiencies']['weapons']
            decoded_weapons = decode_items(starting_weapons)
            lblClassStartWeapons = tk.Label(classDetails, text=f"Starting Weapons: {', '.join(decoded_weapons)}", bg='SteelBlue4', font=('Helvetica', 12))
            lblClassStartWeapons.grid(row=4, column=0, padx=10, pady=5, sticky='w')
            for item in starting_proficiencies.get('skills', []):
                # print(item)
                if 'choose' in item:
                    skills = item['choose']['from']
                    skills = format_list(skills)
                    count = item['choose']['count']
                    skill_proficiencies = f"Choose {count} from:\n {skills}"
                else:
                    skill_proficiencies = item
            lblClassStartSkills = tk.Label(classDetails, text=f"Starting Skills: {skill_proficiencies}", bg='SteelBlue4', font=('Helvetica', 12))
            lblClassStartSkills.grid(row=5, column=0, padx=10, pady=5, sticky='w')
            
            # Process starting equipment
            starting_equipment = class_data['startingEquipment']['default']
            processed_equipment = []
            for item in starting_equipment:
                item = re.sub(r'\{@item (.*?)\|.*?\}', r'\1', item)  # Replace {@item ...} with the item name
                item = re.sub(r'\{@filter (.*?)\|.*?\}', r'\1', item)  # Replace {@filter ...} with the filter description
                processed_equipment.append(item)
            goldAlt = re.sub(r'\{@dice (.*?)\|.*?\}', r'\1',  class_data['startingEquipment']['goldAlternative']) # Replace {@dice ...} with the dice roll
            processed_equipment.append(f"Alternatively, you can use {goldAlt} gold to purchase your own equipment.")
            lblClassStartingEquipment = tk.Label(classDetails, text=f"Starting Equipment:\n{'\n'.join(processed_equipment)}", bg='SteelBlue4', font=('Helvetica', 12))
            lblClassStartingEquipment.grid(row=6, column=0, padx=10, pady=5, sticky='w')

            # Process class table
            data = class_data.get('classTableGroups', [])
            # print(data)
            headers = data.get('headers', [])
            profBons = data.get('proficiency bonuses', [])
            features = data.get('features',[])
            rows = data.get('rows', [])
            spells = data.get('spells',[])

            if spells:
                max_spell_count = max(len(spell_list) for spell_list in spells.values())  # Find the maximum length of the lists
                spellHeaders = [f"{i}th" if i > 3 else f"{i}{['st', 'nd', 'rd'][i-1]}" for i in range(1, max_spell_count + 1)]
                headers.extend(spellHeaders)

            # Initialize the details dictionary
            details = {header: [] for header in headers}

            classHeaders = headers[3:]

            for value in profBons:
                details['Proficiency Bonus'].append(value)

            if rows:
                for level in rows.keys():
                    details['Level'].append(level)
                    rowData = rows[level]
                    for column, value in zip(classHeaders, rowData):
                        details[column].append(value)
            else:
                for level in features.keys():
                    details['Level'].append(level)

            for values in features.values():
                details['Features'].append(values)

            def get_ordinal_suffix(n):
                if 11 <= n % 100 <= 13:
                    return 'th'
                if n % 10 == 1:
                    return 'st'
                if n % 10 == 2:
                    return 'nd'
                if n % 10 == 3:
                    return 'rd'
                return 'th'

            if spells:
                # print(spells)
                for values in spells.values():
                    for spLevel,value in enumerate(values):
                        spLevel = spLevel+1
                        spLevel_with_suffix = f"{spLevel}{get_ordinal_suffix(spLevel)}"  # Add the ordinal suffix
                        if spLevel_with_suffix in spellHeaders:  # Check if it matches a spell header
                            details[spLevel_with_suffix].append(value)

            # print()
            print(details)
            # print

            df= pd.DataFrame(details)

            # Clear any existing content in the classTable frame
            for widget in classTable.winfo_children():
                widget.destroy()

            # Create a Treeview widget
            # visible_columns = df.columns[:5]  # Display only the first 5 columns
            tree = ttk.Treeview(classTable, columns=list(df.columns), show="headings", height=20)

            # Add column headers
            if spells:
                wdth = 45
            else:
                wdth = 120

            for col in df.columns:
                tree.heading(col, text=col)
                tree.column(col, anchor="center", width=wdth)  # Limit to MAX_COLUMN_WIDTH

            # Add rows to the Treeview
            for index, row in df.iterrows():
                tree.insert("", "end", values=list(row))

            # Add vertical scrollbar
            v_scrollbar = ttk.Scrollbar(classTable, orient="vertical", command=tree.yview)
            tree.configure(yscrollcommand=v_scrollbar.set)
            v_scrollbar.pack(side="right", fill="y")

            # Add horizontal scrollbar
            h_scrollbar = ttk.Scrollbar(classTable, orient="horizontal", command=tree.xview)
            tree.configure(xscrollcommand=h_scrollbar.set)
            h_scrollbar.pack(side="bottom", fill="x")

            # Pack the Treeview
            tree.pack(fill="y", expand=True)

        # Background Tab
        backgroundTab = tk.Frame(notebook, bg='SteelBlue4', bd=2, relief='solid')
        notebook.add(backgroundTab, text='Background')

        details = ['What is your character\'s background?','What deity do you follow?', 'What is your character\'s alignment?']
        for i, question in enumerate(details):
            lblDetails = tk.Label(backgroundTab, text=question, bg='SteelBlue4', font=('Helvetica', 12))
            lblDetails.grid(row=i, column=0, padx=10, pady=5, sticky='w')

        backgroundVar = tk.StringVar()
        backgroundMenu = ttk.Combobox(backgroundTab, textvariable=backgroundVar, state='readonly', font=('Helvetica', 12))
        backgroundMenu.grid(row=0, column=1, padx=10, pady=5, sticky='w')
        backgrounds = Backgrounds.load_backgrounds()
        print(backgrounds)
        backgroundMenu['values'] = backgrounds
        # backgroundMenu.bind("<<ComboboxSelected>>", displayClassDetails)
        # backgroundMenu.set('')  # Clear the current selection

        deityVar = tk.StringVar()
        deityMenu = ttk.Combobox(backgroundTab, textvariable=deityVar, state='readonly', font=('Helvetica', 12))
        deityMenu.grid(row=1, column=1, padx=10, pady=5, sticky='w')
        deities = Deity.load_deities()
        deityMenu['values'] = deities


        alignmentVar = tk.StringVar()
        alignmentMenu = ttk.Combobox(backgroundTab, textvariable=alignmentVar, state='readonly', font=('Helvetica', 12))
        alignmentMenu.grid(row=2, column=1, padx=10, pady=5, sticky='w')
        alignments = ['Lawful Good', 'Neutral Good', 'Chaotic Good', 'Lawful Neutral', 'True Neutral', 'Chaotic Neutral', 'Lawful Evil', 'Neutral Evil', 'Chaotic Evil']
        alignmentMenu['values'] = alignments
        # alignmentMenu.set('')  # Clear the current selection


        # Race and Subrace Tab
        raceSubraceTab = tk.Frame(notebook, bg='SteelBlue4', bd=2, relief='solid')
        notebook.add(raceSubraceTab, text='Race and Subrace')
        details = [('What is your character\'s race?', 6), ('What is your character\'s subrace?', 7)]
        for i, (question, pos) in enumerate(details):
            lblDetails = tk.Label(raceSubraceTab, text=question, bg='SteelBlue4', font=('Helvetica', 12))
            lblDetails.grid(row=i, column=0, padx=10, pady=5, sticky='w')

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

        def applyRacialBonuses():
            race_name = raceVar.get()
            race_data = Race.get_race_data(race_name)
            raceBonuses = race_data.get('ability', [])

            for pos, value in chosenAbilities:
                current_value = int(lblAbilityScores[pos].cget("text"))
                lblAbilityScores[pos].config(text=str(current_value - value))
                btnBonuses[pos].config(text=0)

            # Remove previous race bonuses
            for ability, value in appliedRaceBonuses.items():
                for i, (ability_name, pos) in enumerate(abilities):
                    if ability_name[:3].lower() == ability:
                        current_value = int(lblAbilityScores[pos].cget("text"))
                        lblAbilityScores[pos].config(text=str(current_value - value))
                        btnBonuses[pos].config(text=0)

            appliedRaceBonuses.clear()

            # Remove previous subrace bonuses
            for ability, value in appliedSubraceBonuses.items():
                for i, (ability_name, pos) in enumerate(abilities):
                    if ability_name[:3].lower() == ability:
                        current_value = int(lblAbilityScores[pos].cget("text"))
                        lblAbilityScores[pos].config(text=str(current_value - value))
                        btnBonuses[pos].config(text=0)

            appliedSubraceBonuses.clear()

            # Apply new race bonuses
            for bonus in raceBonuses:
                if 'choose' in bonus:
                    choose_data = bonus['choose']
                    from_abilities = choose_data['from']
                    count = choose_data['count']
                    setButtonCommands(from_abilities, count)
                else:
                    for ability, value in bonus.items():
                        for i, (ability_name, pos) in enumerate(abilities):
                            if ability_name[:3].lower() == ability:
                                current_value = int(lblAbilityScores[pos].cget("text"))
                                lblAbilityScores[pos].config(text=str(current_value + value))
                                btnBonuses[pos].config(text=value, command=None)  # Disable button if not 'choose'
                                appliedRaceBonuses[ability] = value
                                break

        def applySubracialBonuses():
            # displayRaceDetails(None, 'subrace')
            race_name = raceVar.get()
            subrace_name = subraceVar.get()
            subrace_data = Race.get_subrace_data(race_name, subrace_name)
            subraceBonuses = subrace_data.get('ability', [])

            if chosenAbilities:
                for pos, value in chosenAbilities:
                    current_value = int(lblAbilityScores[pos].cget("text"))
                    lblAbilityScores[pos].config(text=str(current_value - value))

            # Remove previous subrace bonuses
            for ability, value in appliedSubraceBonuses.items():
                for i, (ability_name, pos) in enumerate(abilities):
                    if ability_name[:3].lower() == ability:
                        current_value = int(lblAbilityScores[pos].cget("text"))
                        lblAbilityScores[pos].config(text=str(current_value - value))
                        btnBonuses[pos].config(text=0)

            appliedSubraceBonuses.clear()

            # Apply new subrace bonuses
            for bonus in subraceBonuses:
                if 'choose' in bonus:
                    choose_data = bonus['choose']
                    from_abilities = choose_data['from']
                    count = choose_data['count']
                    setButtonCommands(from_abilities, count)
                else:
                    for ability, value in bonus.items():
                        for i, (ability_name, pos) in enumerate(abilities):
                            if ability_name[:3].lower() == ability:
                                current_value = int(lblAbilityScores[pos].cget("text"))
                                lblAbilityScores[pos].config(text=str(current_value + value))
                                btnBonuses[pos].config(text=value, command=None)  # Disable button if not 'choose'
                                appliedSubraceBonuses[ability] = value
                                break

        def onRaceSelected(event):
            applyRacialBonuses()
            updateSubraces(event)
            # displayRaceDetails(event, 'race')

        raceMenu.bind("<<ComboboxSelected>>", onRaceSelected)
        classMenu.bind("<<ComboboxSelected>>", displayClassDetails)
        subraceMenu.bind("<<ComboboxSelected>>", lambda event: applySubracialBonuses())

        # Dice Roll and Abilities Tab
        diceAbilitiesTab = tk.Frame(notebook, bg='SteelBlue4', bd=2, relief='solid')
        notebook.add(diceAbilitiesTab, text='Abilities')

        abilities = [('Strength', 10), ('Dexterity', 11), ('Constitution', 12), ('Intelligence', 13), ('Wisdom', 14), ('Charisma', 15)]
        lblAbilityScores = {}
        appliedRaceBonuses = {}
        appliedSubraceBonuses = {}
        btnBonuses = {}
        for i, (ability, pos) in enumerate(abilities):
            lblAbility = tk.Label(diceAbilitiesTab, text=ability, bg='SteelBlue4', font=('Helvetica', 12))
            lblAbility.grid(row=1, column=i, padx=1, pady=1, sticky='')
            lblAbilityScores[pos] = tk.Label(diceAbilitiesTab, text=0, bg='SteelBlue4', font=('Helvetica', 12))
            lblAbilityScores[pos].grid(row=2, column=i, padx=1, pady=1, sticky='')
            btnBonuses[pos] = tk.Button(diceAbilitiesTab, text=0, bg='SteelBlue4', font=('Helvetica', 12))
            btnBonuses[pos].grid(row=3, column=i, padx=1, pady=1, sticky='')

        lblTotals = {}
        lblRolls = {}
        cbxAbilities = {}
        availableAbilities = ["None"] + [ability for ability, _ in abilities]
        selectedAbilities = {}
        max_width = max(len(ability) for ability, _ in abilities)

        for x, (ability, pos) in enumerate(abilities):
            lblTotals[x] = tk.Label(diceAbilitiesTab, text=0, bg='SteelBlue4', font=('Helvetica', 12))
            lblTotals[x].grid(row=4, column=x, padx=10, pady=5, sticky='')
            lblRolls[x] = tk.Label(diceAbilitiesTab, text=0, bg='SteelBlue4', font=('Helvetica', 12))
            lblRolls[x].grid(row=5, column=x, padx=10, pady=5, sticky='')
            cbxAbilities[x] = ttk.Combobox(diceAbilitiesTab, state='disabled', values=availableAbilities, width=max_width, font=('Helvetica', 12))
            cbxAbilities[x].grid(row=6, column=x, padx=1, pady=1,  sticky='')

            def on_combobox_select(event, x=x):
                selectedAbility = cbxAbilities[x].get()
                if selectedAbility:
                    if x in selectedAbilities:
                        previousAbility = selectedAbilities[x]
                        if previousAbility != "None":
                            previousPos = next(pos for ability, pos in abilities if ability == previousAbility)
                            lblAbilityScores[previousPos].config(text=0)
                            availableAbilities.append(previousAbility)
                        del selectedAbilities[x]
                    if selectedAbility != "None":
                        selectedAbilities[x] = selectedAbility
                        pos = next(pos for ability, pos in abilities if ability == selectedAbility)
                        lblAbilityScores[pos].config(text=lblTotals[x].cget("text"))
                        availableAbilities.remove(selectedAbility)
                    updateComboboxes()

            cbxAbilities[x].bind("<<ComboboxSelected>>", on_combobox_select)

        def updateComboboxes():
            for i in range(6):
                cbxAbilities[i]['values'] = ["None"] + [ability for ability in availableAbilities if ability not in selectedAbilities.values() or ability == "None"]

        def setButtonCommands(from_abilities, count):
            chosenAbilities.clear()
            count_holder = [count]

            def allocateAbilityPoint(pos):
                if count_holder[0] > 0 and pos not in [pos for pos, _ in chosenAbilities]:
                    current_value = int(lblAbilityScores[pos].cget("text"))
                    lblAbilityScores[pos].config(text=str(current_value + 1))
                    current_bonus = int(btnBonuses[pos].cget("text"))
                    btnBonuses[pos].config(text=str(current_bonus - 1))
                    count_holder[0] -= 1
                    chosenAbilities.append((pos, 1))
                    if count_holder[0] == 0:
                        for i, (ability, pos) in enumerate(abilities):
                            if ability[:3].lower() in from_abilities:
                                btnBonuses[pos].config(text=0, command=None)
                            else:
                                btnBonuses[pos].config(command=None)

            for i, (ability, pos) in enumerate(abilities):
                if ability[:3].lower() in from_abilities:
                    btnBonuses[pos].config(text="+1", command=lambda pos=pos: allocateAbilityPoint(pos))
                else:
                    btnBonuses[pos].config(command=None)
        
        tk.Button(diceAbilitiesTab, text='Roll', command=lambda: self.abilityRolls(lblAbilityScores, lblTotals, lblRolls, cbxAbilities, appliedRaceBonuses, appliedSubraceBonuses), bg='SteelBlue4', font=('Helvetica', 12)).grid(row=11, column=0, padx=10, pady=5, sticky='w')

        # Equipment Tab
        equipmentTab = tk.Frame(notebook, bg='SteelBlue4', bd=2, relief='solid')
        notebook.add(equipmentTab, text='Equipment')

        tk.Button(createChar, text='Apply', command=lambda: self.createCharacter(chrDetails, entryDetails, raceVar, subraceVar, classVar, lblAbilityScores, createChar), bg='SteelBlue4', font=('Helvetica', 12)).pack(padx=20, pady=20)

    def createCharacter(self, chrDetails, entryDetails, raceVar, subraceVar, classVar, lblAbilityScores, createChar):
        chrDetails[3] = entryDetails[3].get()
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
            self.createGUI(plyr)  # Call createGUI with the created player object
        else:
            print("Character already exists.")
            choice = input("Would you like to load that player? Yes or No?")
            if choice.lower() == "yes":
                plyr = self.loadCharacter(chrDetails[3], chrDetails[6], chrDetails[7])
                self.createGUI(plyr)  # Call createGUI with the loaded player object
            else:
                self.startGUI()
        return plyr

    def loadCharacter(self, name, race, class_name, role):
        loadChar = tk.Toplevel(self.root, bg='firebrick')
        loadChar.title("Load your character")

        
        def searchCharacter(name, race, char_class, role):
            
            if race == "":
                name = entryDetails[3].get()
                race = entryDetails[6].get()
                char_class = entryDetails[7].get()
            
            player = Character.Character.load(name, race, char_class)
            
            if player:
                # print(player)
                player = {
                    'Attributes': {
                        'ID': player['Attributes']['ID'],
                        'Name': player['Attributes']['Name'],
                        'Level': player['Attributes']['Level'],
                        'Experience': player['Attributes']['Experience'],
                        'Race': player['Attributes']['Race'],
                        'Subrace': player['Attributes']['Subrace'],
                        'Class': player['Attributes']['Class'],
                        'Subclass': player['Attributes']['Subclass'],
                        'Health': player['Attributes']['Health'],
                        'Abilities': {
                            'Strength': player['Attributes']['Abilities']['Strength'],
                            'Dexterity': player['Attributes']['Abilities']['Dexterity'],
                            'Constitution': player['Attributes']['Abilities']['Constitution'],
                            'Intelligence': player['Attributes']['Abilities']['Intelligence'],
                            'Wisdom': player['Attributes']['Abilities']['Wisdom'],
                            'Charisma': player['Attributes']['Abilities']['Charisma']
                        },
                        'Modifiers': player['Attributes']['Modifiers']
                    },
                    'Extra': player['Extra'],
                    'Details': player['Details'],
                    'Inventory': player['Inventory']
                }
                if role == 'Mob':
                    # print("Mob loaded: ", player)
                    loadChar.destroy()
                    return player
                else:
                    self.plyr = player
                    loadChar.destroy()
                    self.startFrame.destroy()  # Destroy the start frame
                    self.createGUI(self.plyr)
            else:
                messagebox.showerror("Error", "Character does not exist.")
                loadChar.destroy()
                self.startGUI()
        
        if not name:
        
            details = [('What is your character\'s name?', 3), ('What is your character\'s race?', 6), ('What is your character\'s class?', 7)]
            
            entryDetails = {}
            for i, (question, pos) in enumerate(details):
                lblDetails = tk.Label(loadChar, text=question, bg='SteelBlue4', font=('Helvetica', 12))
                lblDetails.grid(row=i, column=0, padx=10, pady=5, sticky='w')
                if pos == 3:
                    entryDetails[pos] = tk.Entry(loadChar, bg='SteelBlue4', font=('Helvetica', 12))
                    entryDetails[pos].grid(row=i, column=1, padx=10, pady=5, sticky='w')
                else:
                    entryDetails[pos] = ttk.Combobox(loadChar, state='readonly', font=('Helvetica', 12))
                    entryDetails[pos].grid(row=i, column=1, padx=10, pady=5, sticky='w')

            race_classes = Race.load_races()
            class_classes = Class.load_classes()

            entryDetails[6]['values'] = race_classes
            entryDetails[7]['values'] = class_classes

            tk.Button(loadChar, text='Search', command=lambda: searchCharacter('','','', ''), bg='SteelBlue4', font=('Helvetica', 12)).grid(row=len(details), column=0, columnspan=2, padx=10, pady=10, sticky='w')

        else:
            return searchCharacter(name, race, class_name, role)  
    
    def battle(self):
        print("battle start")
        mob = Character.Character(0, 'Mob', 'Goblin', 1, 0, 'Goblin', '', 'Warrior', '', self.rollDice("1d8", "")[0], self.rollDice("3d6", "")[0], self.rollDice("3d6", "")[0], self.rollDice("3d6", "")[0], self.rollDice("3d6", "")[0], self.rollDice("3d6", "")[0], self.rollDice("3d6", "")[0])
        # template --- Character.Character(0, 'Player', chrDetails[3], 1, 0, character_race.name, subrace_data['name'], character_class.name, self.rollDice(character_class.hit_die, "")[0], chrDetails[10], chrDetails[11], chrDetails[12], chrDetails[13], chrDetails[14], chrDetails[15])
        if mob.checkUnique():
            mob = mob.save()
        else:
            print(mob.Name,", ", mob.Race,", ", mob.Class,)
            mob = self.loadCharacter(mob.Name, mob.Race, mob.Class, 'Mob')
            # print('loaded mob: ', mob)    
            # print(mob['Attributes']['Name'])
        self.mobs.append(mob)
        # print("list of mobs: ", self.mobs)

        for mob in self.mobs:
            mob_name = mob['Attributes']['Name']
            mob_class = mob['Attributes']['Class']
            # mob_health = mob['Attributes']['Health']
            mob_race = mob['Attributes']['Race']
            mob_inventory = mob['Inventory']
            mob_weapon = mob_inventory.get('Equipped Weapon', {}).get('Weapon Name', 'no weapon')
            mob_armour = mob_inventory.get('Equipped Armour', {}).get('Armour Name', 'no armor')

        prompt = (
            f"{self.promptDefault} A goblin appeared. describe the scene and the mob's demeanor."
            # f"{self.promptDefault} A {mob_race} {mob_class} named {mob_name} appears. Describe the cave and the mob's demeanor. "
            # f"It is equipped with {mob_weapon} and {mob_armour}. "
            # "Describe the scene and the mob's demeanor."
        )
        print(prompt)
        # narration = self.generate_dm_response(prompt)
        narration = self.generate_story(prompt)
        
        print(narration)
        self.IOText(narration, "black")

        # print(f"A {mob.Name} appears!")
        # choice = input("Would you like to attack or run?")
        # if choice == "attack":
        #     playerInitiative = self.rollDice("1d20", "")
        #     mobInitiative = self.rollDice("1d20", "")
        #     if playerInitiative > mobInitiative:
        #         initiative = [plyr, mob]
        #         print(f"{plyr.Name} go first!")
        #     else:
        #         initiative = [mob, plyr]
        #         print(f"The {mob.Name} goes first!")
        #     while mob.Health > 0 or plyr.Health > 0:
        #         if initiative[0].Health > 0:
        #             self.attack(initiative[0], initiative[1])
        #         else:
        #             print(f"{initiative[0].Name} died!")
        #             break
        #         if initiative[1].Health > 0:
        #             self.attack(initiative[1], initiative[0])
        #         else:
        #             print(f"{initiative[1].Name} died!")
        #             break
        # elif choice == "run":
        #     print("You ran away! Coward!")

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

if __name__ == "__main__":
    root = tk.Tk()
    app = DnD_App(root)
    root.mainloop()

