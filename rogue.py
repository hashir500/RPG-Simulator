# importing character class & random function
from character import Character
import random

# initizaling rogue class
class Rogue(Character):
    def __init__(self, name):
        super().__init__(name, health=120, max_health=120, attack_power=15, speed=20)

        self._crit_chance = 0.35

    def backstab(self,target):
        if random.random() < self._crit_chance:
            crit_damage = self._attack_power * 2.5
            print(f"Critical hit! Backstab dealt {crit_damage} damage!")
            return crit_damage
        else:
            return self._attack_power
        
    def get_status(self):
        status = super().get_status()
        print(status + f" | Crit Chance: {self._crit_chance*100}%")
            
