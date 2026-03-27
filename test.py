from warrior import Warrior
from mage import Mage
from rogue import Rogue
from combat_engine import resolve_attack

w = Warrior("Aragorn")
m = Mage("Albas")
r = Rogue("Shadow")

# test 1 — warrior attacks mage
print("--- Warrior attacks Mage ---")
result = resolve_attack(w, m)
print(result)
m.get_status()

# test 2 — mage attacks warrior
print("--- Mage attacks Warrior ---")
result = resolve_attack(m, w)
print(result)
w.get_status()

# test 3 — rogue attacks mage
print("--- Rogue attacks Mage ---")
result = resolve_attack(r, m)
print(result)
m.get_status()

# test 4 — drain mage health to 0 and check defeat message
print("--- Defeat test ---")
resolve_attack(w, m)
resolve_attack(w, m)
resolve_attack(w, m)
resolve_attack(w, m)
resolve_attack(w, m)
m.get_status()

# test 5 — check defender_alive is False when defeated
print("--- is_alive check ---")
print(m.is_alive)