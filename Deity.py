import json

class Deity:
    def __init__(self, name, alignment, domains, source, page):
        self.name = name
        self.alignment = alignment
        self.domains = domains
        self.source = source
        self.page = page

    def __str__(self):
        return f"{self.name} (Alignment: {self.alignment}, Domains: {self.domains}, Source: {self.source}, Page: {self.page})"

def load_from_json(filename):
    details = {}
    details['deity'] = {}
    with open(filename, 'r', encoding='utf-8') as f:
        data = json.load(f)
        for item in data.get('deity', []):
            name = item['name']
            details['deity'][name] = {
                'name': item['name'],
                'source': item.get('source', 'Unknown'),
                'page': item.get('page', 0),
                'title': item.get('title', 'Unknown'),
                'pantheon': item.get('pantheon', 'Unknown'),
                'alignment': item.get('alignment', 'Unknown'),
                'planet': item.get('plane', 'Unknown'),
                'worshippers': item.get('worshippers', []),
                'category': item.get('category', 'Unknown'),
                'domains': item.get('domains', []),
                'province': item.get('province', []),
                'symbol': item.get('symbol', 'Unknown'),
                'entries': item.get('entries', []),
            }

    write_to_json(details, "deities.json")
    return details

def write_to_json(details, filename):
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(details, f, ensure_ascii=False, indent=4)

def load_deities():
    with open("deities.json", 'r', encoding='utf-8') as f:
        data = json.load(f)
        keys = [key for key in data['deity']]
        return keys
    
def get_deity(name):
    data = load_deities()
    if name in data['deity']:
        return data['deity'][name]
    else:
        return None

if __name__ == "__main__":
    details = load_from_json("5eTools data/deities.json")
    # print(details)
    # print(load_deities())
    