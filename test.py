
from warrior import Warrior
from mage import Mage
from rogue import Rogue
from status_effects import StatusEffect

print("--- Status Effect Test ---")
poison = StatusEffect(name="poisoned", damage_per_turn=8, duration=3)

m2 = Mage("Zara")
m2.apply_status(poison)

print("--- Tick 1 ---")
m2.tick_status_effects()
m2.get_status()

print("--- Tick 2 ---")
m2.tick_status_effects()
m2.get_status()

print("--- Tick 3 ---")
m2.tick_status_effects()
m2.get_status()

print("--- Tick 4 (effect should be gone) ---")
m2.tick_status_effects()
m2.get_status()