from character import Character
from warrior import Warrior
from mage import Mage
from rogue import Rogue
import random

def calculate_damage(attacker):
    base = attacker._attack_power
    variance = random.uniform(0.8,1.2)
    base *= variance
    if isinstance(attacker, Warrior) and attacker.is_enraged():
        base*=1.5
    return round(base)

def resolve_attack(attacker, defender):
    damage = calculate_damage(attacker)
    print(f"{attacker._name} attacks {defender._name} for {damage} damage!")
    defender.take_damage(damage)

    return {
        "attacker": attacker._name,
        "damage": damage,
        "defender_alive": defender.is_alive
        }



