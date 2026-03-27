# importing character class
from character import Character

# initilizing warrior class
class Mage(Character):
    def __init__(self, name):
        super().__init__(name, health= 100, max_health = 100, attack_power = 25, speed = 7)

        self._mana = 100
        self._mana_cost = 25
    
    def cast_spell(self,target):
        if self._mana >= self._mana_cost:
            self._mana = self._mana - self._mana_cost
            return self._attack_power * 1.5
        else:
            print("Not sufficient mana")
            return 0
        
    def regenerate_mana(self,amount):
        self._mana += amount
        self._mana = min(self._mana,100)
        print(f"{self._name} generated {amount} mana.")

    def get_status(self):
        status = super().get_status()
        print(status + f" | Mana: {self._mana}/100")