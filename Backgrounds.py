import json

class Backgrounds:
    def __init__(self, name, skills, languages, starting_equipment, source, page):
        self.name = name
        skills = skills
        languages = languages
        starting_equipment = starting_equipment
        self.source = source
        self.page = page
    
    def __str__(self):
        return f"{self.name} (Skills: {self.skills}, Languages: {self.languages}, Starting Equipment: {self.starting_equipment}, Source: {self.source}, Page: {self.page})"

def load_from_json(filename):
    details = {}
    details['background'] = {}
    with open(filename, 'r', encoding='utf-8') as f:
        data = json.load(f)
        for item in data.get('background', []):
            name = item['name']
            if item['source'] not in ['XPHB']:
                details['background'][name] = {
                    'name': item['name'],
                    'source': item.get('source', 'Unknown'),
                    'page': item.get('page', 0),
                    'skill proficiencies': item.get('skillProficiencies', []),
                    'languages': item.get('languageProficiencies', []),
                    'starting equipment': item.get('startingEquipment', []),
                    'entries': item.get('entries', [])
                    
                }

    write_to_json(details, "Backgrounds.json")
    return details

def write_to_json(details, filename):
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(details, f, ensure_ascii=False, indent=4)

def load_backgrounds():
    with open("Backgrounds.json", 'r', encoding='utf-8') as f:
        data = json.load(f)
        keys = [key for key in data['background']]
        return keys
    
    
def get_background(name):
    data = load_backgrounds()
    if name in data['background']:
        return data['background'][name]
    else:
        return None

if __name__ == "__main__":
    details = load_from_json("5eTools data/backgrounds.json")
    # print(details)
    # print(load_backgrounds())
    
