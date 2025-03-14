import json
import os

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
                            'classTableGroups': cls.get('classTableGroups'),
                            'defaultClassFeatures': cls['classFeatures'],
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

