# importing functions
from warrior import Warrior
from mage import Mage
from rogue import Rogue

# Making characters
w = Warrior("Aargon")
m = Mage("Albas")
r = Rogue("Shadow")

# checking status of the characters
w.get_status()
m.get_status()
r.get_status()

print(w.is_enraged())
print(r.backstab(w))

print(m.cast_spell(w))
print(m.cast_spell(w))
print(m.cast_spell(w))
print(m.cast_spell(w))
print(m._mana)
m.cast_spell(w)

