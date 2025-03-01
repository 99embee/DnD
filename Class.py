import json
import os

class CharacterClass:
    def __init__(self, name, hit_die, primary_ability, saving_throws, proficiencies, source, class_features, subclasses, subclass_features):
        self.name = name
        self.hit_die = hit_die
        self.primary_ability = primary_ability
        self.saving_throws = saving_throws
        self.proficiencies = proficiencies
        self.source = source
        self.class_features = class_features
        self.subclasses = subclasses
        self.subclass_features = subclass_features

    def __str__(self):
        return f"{self.name} (Hit Die: {self.hit_die}, Primary Ability: {', '.join(self.primary_ability)}, Saving Throws: {', '.join(self.saving_throws)}, Proficiencies: {', '.join(self.proficiencies)}, Source: {self.source})"

class CharacterClassFactory:
    @staticmethod
    def create_character_class(class_data): #, subclass_data
        try:
            class_name = class_data['name']
            hit_die = f"{class_data['hd']['number']}d{class_data['hd']['faces']}"
            primary_ability = [key for ability in class_data.get('primaryAbility', []) for key in ability.keys()] if isinstance(class_data.get('primaryAbility'), list) else list(class_data.get('primaryAbility', {}).keys())
            saving_throws = class_data.get('proficiency', [])
            proficiencies = class_data.get('startingProficiencies', {})
            source = class_data['source']
            class_features = class_data.get('classFeatures', [])
            
            
        except KeyError as e:
            # print(f"Missing attribute {e} in class data: {class_data}")
            return None

        return CharacterClass(class_name, hit_die, primary_ability, saving_throws, proficiencies, source, class_features) #, subclasses, subclass_details


def load_data_from_json(directory):
    details = {} 
    details['class'] = {}
    
    for filename in os.listdir(directory):
        if filename.startswith("class-") and filename.endswith(".json"):
            with open(os.path.join(directory, filename), 'r', encoding='utf-8') as f:
                data = json.load(f)
                print(filename)
                for cls in data.get('class', []):
                    cls['name']
                    if cls['source'] in ['PHB','TCE'] and 'Sidekick' not in cls['name']   :
                        className = cls['name']
                        details['class'][className] = {}
                        details['class'][className]['class_name'] = cls['name']
                        details['class'][className]['source'] = cls['source']  
                        details['class'][className]['page'] = cls['page']  
                        details['class'][className]['hit_dice'] = f"{cls['hd']['number']}d{cls['hd']['faces']}"
                        details['class'][className]['proficiency'] = cls['proficiency']
                        details['class'][className]['startingProficiencies'] = cls['startingProficiencies']
                        details['class'][className]['startingEquipment'] = cls['startingEquipment']
                        details['class'][className]['multiclassing'] = cls['multiclassing']
                        details['class'][className]['classTableGroups'] = cls.get('classTableGroups')
                        details['class'][className]['defaultClassFeatures'] = cls['classFeatures']
                        details['class'][className]['classFeature'] = []
                        details['class'][className]['subclasses'] = {}

                        for clsfeature in data.get('classFeature', []):
                            className = cls['name']
                            if details['class'][className]['class_name'] == clsfeature['className']:
                                if 'classFeature' not in details['class'][className]:
                                    details['class'][className]['classFeature'] = []
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
                                                'page': feature.get('page', 'n/a'),  # Use get method to avoid KeyError
                                                'level': feature['level'],
                                                'feature': feature.get('entries')
                                            }
                                            details['class'][className]['subclasses'][subclassName]['subclassFeatures'].append(feature_details)

    # print(details)
    return details

def write_classes_to_json(class_details, filename):
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(class_details, f, ensure_ascii=False, indent=4)

if __name__ == "__main__":
    directory = "5eTools data/class"
    character_classes = load_data_from_json(directory)
    write_classes_to_json(character_classes, "Classes.json")
    