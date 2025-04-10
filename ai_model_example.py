from transformers import pipeline
import json

# Load the JSON file
with open("5eTools data", "r", encoding="utf-8") as file:
    data = json.load(file)

# Example: Extract storylines or NPC data
storylines = []
for entry in data.get("5eTools data/adventure", []):  # Adjust the key based on the JSON structure
    storylines.append(entry.get("data", ""))

# Load a text generation pipeline
generator = pipeline("text-generation", model="gpt2")

# # Generate a storyline
# prompt = "You are a Dungeon Master. Create a starting storyline for a D&D game set in a epic fantasy world."
# storyline = generator(
#     prompt,
#     max_length=150,
#     num_return_sequences=6,
#     temperature=0.7,
#     top_k=50
# )
# for i, story in enumerate(storyline):
#     print(f"Storyline {i + 1}: {story['generated_text']}")