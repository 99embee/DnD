import json
import os

class CharacterRace:
    def __init__(self, name, subraces, size, age, speed, ability, languages, features, source, page):
        self.name = name
        self.subraces = subraces
        self.size = size
        self.age = age
        self.speed = speed
        self.ability = ability
        self.languages = languages
        self.features = features
        self.source = source
        self.page = page

    def __str__(self):
        return f"{self.name} (Subraces: {self.subraces}, Size: {self.size}, Age: {self.age}, Speed: {self.speed}, Ability: {self.ability}, Languages: {', '.join(self.languages)}, Features: {self.features}, Source: {self.source}, Page: {self.page})"

class CharacterRaceFactory:
    @staticmethod
    def create_character_race(race_data):
        try:
            name = race_data['name']
            size = race_data.get('size', 'Medium')
            age = race_data.get('age', 'Unknown')
            speed = race_data.get('speed', 30)
            ability = race_data.get('ability', {})
            languages = race_data.get('languages', [])
            features = race_data.get('entries', [])
            source = race_data.get('source', 'Unknown')
            page = race_data.get('page', 0)
            subraces = race_data.get('subraces', {})
        except KeyError as e:
            print(f"Missing attribute {e} in race data: {race_data}")
            return None

        return CharacterRace(name, subraces, size, age, speed, ability, languages, features, source, page)

def get_race_data(race_name):
    with open("Races.json", 'r', encoding='utf-8') as f:
        data = json.load(f)
        return data['race'][race_name]
    
def get_subrace_data(race_name, subrace_name):
    with open("Races.json", 'r', encoding='utf-8') as f:
        data = json.load(f)
        return data['race'][race_name]['subraces'][subrace_name]

def load_races_from_json(filename):
    details = {}
    details['race'] = {}
    with open(filename, 'r', encoding='utf-8') as f:
        data = json.load(f)
        for race in data.get('race', []):
            raceName = race['name']
            if race['source'] in ['PHB', 'DMG']:
                details['race'][raceName] = {
                    'name': race['name'],
                    'source': race.get('source', 'Unknown'),
                    'page': race.get('page', 0),
                    'size': race.get('size', 'Medium'),
                    'age': race.get('age', 'Unknown'),
                    'speed': race.get('speed', 30),
                    'ability': race.get('ability', {}),
                    'languages': race.get('languages', []),
                    'features': race.get('entries', []),
                    'traitTags': race.get('traitTags', []),
                    'subraces': {}
                }

        for subrace in data.get('subrace', []):
            if subrace['raceSource'] in ['PHB', 'DMG'] and subrace['raceName'] in details['race']:
                raceName = subrace['raceName']
                subraceName = subrace.get('name', 'Unknown Subrace')
                details['race'][raceName]['subraces'][subraceName] = {
                    'name': subraceName,
                    'source': subrace['source'],
                    'page': subrace['page'],
                    'ability': subrace.get('ability', {}),
                    'skillProficiencies': subrace.get('skillProficiencies', {}),
                    'toolProficiencies': subrace.get('toolProficiencies', {}),
                    'traitTags': subrace.get('traitTags', {}),
                    'features': subrace.get('entries', []),
                }

                if '_versions' in subrace:
                    for version in subrace['_versions']:
                        if '_abstract' in version:
                            base_name = version['_abstract']['name']
                            for implementation in version['_implementations']:
                                colour = implementation['_variables']['color']
                                colour_name = base_name.replace("{{color}}", colour)
                                details['race'][raceName]['subraces'][colour_name] = {
                                    'name': colour_name,
                                    'size': race.get('size', 'Medium'),
                                    'age': race.get('age', 'Unknown'),
                                    'speed': race.get('speed', 30),
                                    'ability': [{k: v for ability in race.get('ability', []) for k, v in ability.items()}],
                                    'languages': race.get('languages', []),
                                    'features': race.get('entries', []),
                                    'traitTags': race.get('traitTags', []),
                                    'source': race.get('source', 'Unknown'),
                                    'page': race.get('page', 0),
                                    'resist': implementation.get('resist', []),
                                    'breathWeapon': {
                                        'damageType': implementation['_variables']['damageType'],
                                        'area': implementation['_variables']['area'],
                                        'savingThrow': implementation['_variables']['savingThrow']
                                    }
                                }

    write_races_to_json(details, "Races.json")
    return details

def write_races_to_json(race_details, filename):
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(race_details, f, ensure_ascii=False, indent=4)

def load_races():
    with open("Races.json", 'r', encoding='utf-8') as f:
        data = json.load(f)
        keys = [key for key in data['race']]
        return keys

def load_subraces():
    with open( "Races.json", 'r', encoding='utf-8') as f:
        data = json.load(f)
        subrace_dict = {}
        for race in data['race']:
            subraces = data['race'][race]['subraces']
            subrace_dict[race] = [subraces[subrace]['name'] for subrace in subraces]
        return subrace_dict

if __name__ == "__main__":
    races = load_races_from_json("5eTools data/races.json")
    print(races)
