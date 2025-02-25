from abc import ABC, abstractmethod
import json
import os

class CharacterClass(ABC):
    def __init__(self, name, hit_die, primary_ability, saving_throws, proficiencies, fluff=None):
        self.name = name
        self.hit_die = hit_die
        self.primary_ability = primary_ability
        self.saving_throws = saving_throws
        self.proficiencies = proficiencies
        self.fluff = fluff

    @abstractmethod
    def class_features(self):
        pass

    def __str__(self):
        return f"{self.name} (Hit Die: {self.hit_die}, Primary Ability: {self.primary_ability}, Saving Throws: {', '.join(self.saving_throws)}, Proficiencies: {', '.join(self.proficiencies)})"

def load_classes_from_json(directory):
    classes = {}
    for filename in os.listdir(directory):
        if filename.startswith("class-") and filename.endswith(".json"):
            with open(os.path.join(directory, filename), 'r', encoding='utf-8') as f:
                data = json.load(f)
                for cls in data.get('class', []):
                    classes[f"{cls['name']}|{cls['source']}"] = cls
    return classes

def load_fluff_from_json(directory):
    fluff = {}
    for filename in os.listdir(directory):
        if filename.startswith("fluff-class-") and filename.endswith(".json"):
            with open(os.path.join(directory, filename), 'r', encoding='utf-8') as f:
                data = json.load(f)
                for cls in data.get('classFluff', []):
                    fluff[f"{cls['name']}|{cls['source']}"] = cls
    return fluff

def merge_class_and_fluff(classes, fluff):
    for class_name, class_data in classes.items():
        if class_name in fluff:
            class_data['fluff'] = fluff[class_name]
    return classes

def create_character_class(class_data):
    class_name = class_data['name'].replace(" ", "")
    hit_die = class_data['hd']
    primary_ability = class_data['primaryAbility'] #if isinstance(class_data['primaryAbility'], list) else class_data['primaryAbility']
    saving_throws = class_data['proficiency']
    proficiencies = class_data['startingProficiencies']
    fluff = class_data.get('fluff', None)

    def class_features(self):
        return class_data.get('classFeatures', [])

    return type(class_name, (CharacterClass,), {
        '__init__': lambda self: CharacterClass.__init__(self, class_name, hit_die, primary_ability, saving_throws, proficiencies, fluff),
        'class_features': class_features
    })

def create_character_subclass(subclass_data, parent_class):
    subclass_name = subclass_data['name'].replace(" ", "")
    parent_class_name = parent_class.__name__

    def subclass_features(self):
        return subclass_data.get('subclassFeatures', [])

    return type(subclass_name, (parent_class,), {
        '__init__': lambda self: parent_class.__init__(self, parent_class_name, parent_class.hit_die, parent_class.primary_ability, parent_class.saving_throws, parent_class.proficiencies, parent_class.fluff),
        'subclass_features': subclass_features
    })

def load_and_create_classes(directory):
    classes = load_classes_from_json(directory)
    fluff = load_fluff_from_json(directory)
    merged_classes = merge_class_and_fluff(classes, fluff)

    character_classes = {}
    for class_name, class_data in merged_classes.items():
        character_class = create_character_class(class_data)
        character_classes[class_name] = character_class

        for subclass_data in class_data.get('subclass', []):
            character_subclass = create_character_subclass(subclass_data, character_class)
            character_classes[f"{subclass_data['name']}|{subclass_data['source']}"] = character_subclass

    return character_classes

# Example usage
if __name__ == "__main__":
    directory = "5eTools data/class"
    character_classes = load_and_create_classes(directory)

    for class_name, character_class in character_classes.items():
        print(character_class())
