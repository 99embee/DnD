import json
from abc import ABC, abstractmethod
from collections import defaultdict

class Race(ABC):
    def __init__(self, name, speed, size, languages, age=None, darkvision=None, resist=None, immune=None, condition_immune=None, additional_spells=None, entries=None, height_and_weight=None, creature_types=None, trait_tags=None, tool_proficiencies=None, weapon_proficiencies=None, armor_proficiencies=None, subraces=None):
        self.name = name
        self.speed = speed
        self.size = size
        self.languages = languages
        self.age = age
        self.darkvision = darkvision
        self.resist = resist
        self.immune = immune
        self.condition_immune = condition_immune
        self.additional_spells = additional_spells
        self.entries = entries
        self.height_and_weight = height_and_weight
        self.creature_types = creature_types
        self.trait_tags = trait_tags
        self.tool_proficiencies = tool_proficiencies
        self.weapon_proficiencies = weapon_proficiencies
        self.armor_proficiencies = armor_proficiencies
        self.subraces = subraces or []

    @abstractmethod
    def ability_score_increase(self):
        pass

    @abstractmethod
    def special_traits(self):
        pass

    def __str__(self):
        return f"{self.name} (Speed: {self.speed}, Size: {self.size}, Languages: {', '.join(self.languages)})"

def merge_attribute(merged_race, race, attribute):
    if attribute in race:
        if isinstance(race[attribute], list):
            for item in race[attribute]:
                if isinstance(item, dict):
                    merged_race[attribute].extend(item.keys())
                else:
                    merged_race[attribute].append(item)
            merged_race[attribute] = list(set(merged_race[attribute]))
        elif isinstance(race[attribute], dict):
            merged_race[attribute] = list(set(merged_race[attribute] + list(race[attribute].keys())))

def merge_races(races):
    merged_races = defaultdict(lambda: {
        'name': '',
        'speed': 30,
        'size': ['Medium'],
        'languageProficiencies': [],
        'ability': {},
        'traitTags': [],
        'age': None,
        'darkvision': None,
        'resist': [],
        'immune': [],
        'conditionImmune': [],
        'additionalSpells': [],
        'entries': [],
        'heightAndWeight': None,
        'creatureTypes': [],
        'toolProficiencies': [],
        'weaponProficiencies': [],
        'armorProficiencies': []
    })

    for race in races:
        name = race['name']
        merged_race = merged_races[name]
        merged_race['name'] = name

        if 'speed' in race:
            if isinstance(race['speed'], int):
                merged_race['speed'] = max(merged_race['speed'], race['speed'])
            else:
                merged_race['speed'] = max(merged_race['speed'], race['speed'].get('walk', 30))

        # if 'size' in race:
        #     merged_race['size'] = race['size']
        merge_attribute(merged_race, race, 'size')
        merge_attribute(merged_race, race, 'languageProficiencies')

        # Handle ability and skillProficiencies as the same attribute
        if 'ability' in race or 'skillProficiencies' in race:
            abilities = race.get('ability', race.get('skillProficiencies', []))
            for ability in abilities:
                for key, value in ability.items():
                    if key in merged_race['ability']:
                        merged_race['ability'][key] = max(merged_race['ability'][key], value)
                    else:
                        merged_race['ability'][key] = value

        merge_attribute(merged_race, race, 'traitTags')
        merge_attribute(merged_race, race, 'resist')
        merge_attribute(merged_race, race, 'immune')
        merge_attribute(merged_race, race, 'conditionImmune')
        merge_attribute(merged_race, race, 'additionalSpells')
        merge_attribute(merged_race, race, 'entries')
        merge_attribute(merged_race, race, 'creatureTypes')
        merge_attribute(merged_race, race, 'toolProficiencies')
        merge_attribute(merged_race, race, 'weaponProficiencies')
        merge_attribute(merged_race, race, 'armorProficiencies')

        if 'age' in race:
            merged_race['age'] = race['age']

        if 'darkvision' in race:
            merged_race['darkvision'] = race['darkvision']

        if 'heightAndWeight' in race:
            merged_race['heightAndWeight'] = race['heightAndWeight']

    return list(merged_races.values())

def create_race_class(race_data):
    class_name = race_data['name'].replace(" ", "")
    speed = race_data['speed'] if isinstance(race_data['speed'], int) else race_data['speed'].get('walk', 30)
    size = race_data['size'][0]
    languages = race_data.get('languageProficiencies', [])
    age = race_data.get('age')
    darkvision = race_data.get('darkvision')
    resist = race_data.get('resist', [])
    immune = race_data.get('immune', [])
    condition_immune = race_data.get('conditionImmune', [])
    additional_spells = race_data.get('additionalSpells', [])
    entries = race_data.get('entries', [])
    height_and_weight = race_data.get('heightAndWeight')
    creature_types = race_data.get('creatureTypes', [])
    trait_tags = race_data.get('traitTags', [])
    tool_proficiencies = race_data.get('toolProficiencies', [])
    weapon_proficiencies = race_data.get('weaponProficiencies', [])
    armor_proficiencies = race_data.get('armorProficiencies', [])
    subraces = race_data.get('subrace', [])

    def ability_score_increase(self):
        return race_data.get('ability', {})

    def special_traits(self):
        return race_data.get('traitTags', [])

    return type(class_name, (Race,), {
        '__init__': lambda self: Race.__init__(self, class_name, speed, size, languages, age, darkvision, resist, immune, condition_immune, additional_spells, entries, height_and_weight, creature_types, trait_tags, tool_proficiencies, weapon_proficiencies, armor_proficiencies, subraces),
        'ability_score_increase': ability_score_increase,
        'special_traits': special_traits
    })

def load_races_from_json(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
        # races = data.get('race', [])
        races = [race for race in data['race'] if race.get('source') in ['PHB', 'XPHB']]
        merged_races = merge_races(races)
        race_classes = {}
        for race in merged_races:
            race_class = create_race_class(race)
            race_classes[race['name']] = race_class
        return race_classes

# Example usage
if __name__ == "__main__":
    race_classes = load_races_from_json("5eTools data/races.json")

    for race_name, race_class in race_classes.items():
        race_instance = race_class()
        print(race_instance)
        print(race_instance.ability_score_increase())
        print(race_instance.special_traits())
        print("")
