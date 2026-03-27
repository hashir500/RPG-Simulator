from warrior import Warrior
from character import Character

# save a character
w = Warrior("Aragorn")
w.save_to_json("aragorn.json")

# load it back
loaded = Character.load_from_json("aragorn.json")
print(loaded)

# test file not found
bad = Character.load_from_json("missing.json")
print(bad)
