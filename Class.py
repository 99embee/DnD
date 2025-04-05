import json
import os
import re

class CharacterClass:
    def __init__(self, name, hit_die, primary_ability, saving_throws, proficiencies, source, class_features, subclass, subclass_features):
        self.name = name
        self.hit_die = hit_die
        self.primary_ability = primary_ability
        self.saving_throws = saving_throws
        self.proficiencies = [item for sublist in proficiencies for item in (sublist if isinstance(sublist, list) else [sublist])]
        self.source = source
        self.class_features = class_features
        self.subclass = subclass
        self.subclass_features = subclass_features

    def set_subclass(self, subclass_name, subclass_data):
        self.subclass = subclass_name
        self.subclass_features = subclass_data.get('subclassFeatures', {})
        # self.subclass_features = {subclass_name: subclass_data['subclassFeatures'] for subclass_name, subclass_data in subclass.items()}

    def __str__(self):
        return f"{self.name} (Hit Die: {self.hit_die}, Primary Ability: {', '.join(self.primary_ability)}, Saving Throws: {', '.join(self.saving_throws)}, Proficiencies: {str(self.proficiencies)}, Source: {self.source})"

class CharacterClassFactory:
    @staticmethod
    def create_character_class(class_data):
        try:
            class_name = class_data['class_name']
            hit_die = class_data['hit_dice']
            primary_ability = class_data.get('primary_ability', [])
            saving_throws = class_data.get('proficiency', [])
            proficiencies = class_data.get('startingProficiencies', {}).get('armor', []) + \
                            class_data.get('startingProficiencies', {}).get('weapons', []) + \
                            class_data.get('startingProficiencies', {}).get('tools', []) + \
                            class_data.get('startingProficiencies', {}).get('skills', [])
            source = class_data['source']
            class_features = class_data.get('classFeature', [])
            subclass = 'n/a'
            subclass_features = 'n/a'
        except KeyError as e:
            print(f"Missing attribute {e} in class data: {class_data}")
            return None

        return CharacterClass(class_name, hit_die, primary_ability, saving_throws, proficiencies, source, class_features, subclass, subclass_features)

def get_class_data(class_name):
    with open("Classes.json", 'r', encoding='utf-8') as f:
        data = json.load(f)
        return data['class'].get(class_name, None)

def get_subclass_data(class_name, subclass_name):
    with open("Classes.json", 'r', encoding='utf-8') as f:
        data = json.load(f)
        class_data = data['class'].get(class_name, None)
        if class_data:
            return class_data.get('subclasses', {}).get(subclass_name, None)
        return None

def getClassTableGroups(cls):

    headers = ['Level', 'Proficiency Bonus', 'Features']
    rows = {}
    spells = {}
    
    for index, table in enumerate(cls.get('classTableGroups', [])):
        # if cls['name'] == 'Warlock': 
        #     print(cls['name'], ", ",len(cls['classTableGroups']), ", index:",index)

        col_labels = table.get('colLabels', [])
       
        # Use re.sub to replace @filter text in colLabels
        col_labels = [re.sub(r'\{@filter (.*?)\|.*?\}', r'\1', label) for label in col_labels]
        # print(f"Processing class: {cls['name']}")
        if len(headers) >= 3:  # Extend headers only once
            headers.extend(col_labels)

        monkMovement = {1:'0', 2:'+10',3:'+10',4:'+10',5:'+10', 6:'+15',7:'+15',8:'+15',9:'+15', 10:'+20',11:'+20',12:'+20',13:'+20', 14:'+25',15:'+25',16:'+25',17:'+25', 18:'+30',19:'+30',20:'+30'}
        
        if table.get('rows', []):
            for i, row in enumerate(table['rows']):
                level = i + 1
                if level not in rows:
                    rows[level] = []
                for item in row:
                    if isinstance(item, dict):
                        if item.get('type') == 'bonus':
                            rows[level].append(f"+{item['value']}")
                        elif item.get('type') == 'dice':
                            # print(item.get('toRoll'))
                            for dice in item['toRoll']:
                                number = dice['number']
                                faces = dice['faces']
                                # print(f"{number}d{faces}")
                                rows[level].append(f"{number}d{faces}")
                    else:
                        if isinstance(item, str) and '@filter' in item:
                            item = re.sub(r'\{@filter (.*?)\|.*?\}', r'\1', item)
                        
                        if level in rows and len(rows[level]) > 0:
                            index = len(rows[level]) - 1
                            print(f"{cls['name']}:, len(row level): {len(rows[level])} index: {index}")
                            print(f"rows[level]: {rows[level]} item: {item}")
                        else:
                            index = -1
                            print(f"else {index}")
                        if len(rows[level]) <= index + 1:
                            # print(f"rows[level]: {rows[level]} item: {item}")
                            rows[level].append(item)  # Append if the index is out of bounds
                        else:
                            rows[level].insert(index + 1, item)
        

                if cls['name'] == 'Monk':
                    if level in monkMovement:
                        rows[level].insert(2, monkMovement[level])

        if table.get('rowsSpellProgression', []):
            for i, spell_row in enumerate(table.get('rowsSpellProgression', [])):
                level = i + 1
                spells[level] = [0] * (len(col_labels))  # Initialize with zeros
                for j, item in enumerate(spell_row):
                    spells[level][j] = item

    if cls['name'] in ['Sorcerer', 'Warlock']:
        print(cls['name'], ": ",rows)

    # Convert sets to lists
    rows = {level: list(features) for level, features in rows.items()}
    spells = {level: spell_progression for level, spell_progression in spells.items()}

    features = getClassFeatures(cls)
    proficiencyBonuses = ['+2','+2','+2','+2', '+3','+3','+3','+3', '+4','+4','+4','+4', '+5','+5','+5','+5', '+6','+6','+6','+6']

    classTableGroups = {
        'headers': headers,
        'proficiency bonuses': proficiencyBonuses,
        'features': features,
        'rows': rows,
        'spells': spells
    }

    return classTableGroups

def getClassFeatures(cls):
    details = []
    groupedFeature = {}
    expectedLevels = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20]
    for feature in cls.get('classFeatures', []):
        if isinstance(feature, dict):
            item = feature.get('classFeature', '')
            # print("before split ",item)
            item = item.split('|')
            # print("after split ",item)
        else:
            item = feature.split('|')

        # item = feature.split('|')
        details.append(item)
        # print(details)
    for data in details:
        feature = data[0]
        level = int(data[3])
        # print(f"level {level}")
        if level not in groupedFeature:
            groupedFeature[level] = set()
        groupedFeature[level].add(feature)
        
    # Ensure all expected levels are present in groupedFeature
    for level in expectedLevels:
        if level not in groupedFeature:
            groupedFeature[level] = {"---"}  # Add a default value for missing levels

    # Convert sets to lists
    groupedFeature = {level: list(features) for level, features in groupedFeature.items()}
    groupedFeature = dict(sorted(groupedFeature.items()))

    return groupedFeature

def load_classes_from_json(directory):
    details = {} 
    details['class'] = {}
    
    for filename in os.listdir(directory):
        if filename.startswith("class-") and filename.endswith(".json"):
            with open(os.path.join(directory, filename), 'r', encoding='utf-8') as f:
                data = json.load(f)
                for cls in data.get('class', []):
                    if cls['source'] in ['PHB','TCE'] and 'Sidekick' not in cls['name']:
                        className = cls['name']
                        details['class'][className] = {
                            'class_name': cls['name'],
                            'source': cls['source'],
                            'page': cls['page'],
                            'hit_dice': f"{cls['hd']['number']}d{cls['hd']['faces']}",
                            'proficiency': cls['proficiency'],
                            'startingProficiencies': cls['startingProficiencies'],
                            'startingEquipment': cls['startingEquipment'],
                            'multiclassing': cls['multiclassing'],
                            'classTableGroups': getClassTableGroups(cls),
                            # 'classTableGroups': cls.get('classTableGroups'),
                            # 'defaultClassFeatures': getClassFeatures(cls),
                            # 'defaultClassFeatures': cls['classFeatures'],
                            'classFeature': [],
                            'subclasses': {}
                        }

                        for clsfeature in data.get('classFeature', []):
                            if details['class'][className]['class_name'] == clsfeature['className']:
                                feature_details = {
                                    'name': clsfeature['name'],
                                    'source': clsfeature['source'],
                                    'page': clsfeature['page'],
                                    'level': clsfeature['level'],
                                    'features': clsfeature['entries']
                                }
                                details['class'][className]['classFeature'].append(feature_details)

                        for subclass in data.get('subclass', []):
                            if subclass['classSource'] in ['PHB','TCE']:
                                subclassName = subclass['name']
                                details['class'][className]['subclasses'][subclassName] = {
                                    'subclassName': subclass['name'],
                                    'shortSubclassName': subclass['shortName'],
                                    'source': subclass['source'],
                                    'page': subclass['page'],
                                    'subclassFeatures': [],
                                    'spellcastingAbility': subclass.get('spellcastingAbility', 'n/a'),
                                    'additionalSpells': subclass.get('additionalSpells', 'n/a')
                                }

                                for feature in data.get('subclassFeature', []):
                                    if details['class'][className]['subclasses'][subclassName]['shortSubclassName'] == feature['subclassShortName']:
                                        feature_details = {
                                            'name': feature['name'],
                                            'source': feature['source'],
                                            'page': feature.get('page', 'n/a'),
                                            'level': feature['level'],
                                            'feature': feature.get('entries')
                                        }
                                        details['class'][className]['subclasses'][subclassName]['subclassFeatures'].append(feature_details)

    write_classes_to_json(details, "Classes.json")
    return details

def write_classes_to_json(class_details, filename):
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(class_details, f, ensure_ascii=False, indent=4)

def load_classes():
    with open("Classes.json", 'r', encoding='utf-8') as f:
        data = json.load(f)
        keys = [key for key in data['class']]
        return keys

if __name__ == "__main__":
    directory = "5eTools data/class"
    character_classes = load_classes_from_json(directory)
    # write_classes_to_json(character_classes, "Classes.json")

