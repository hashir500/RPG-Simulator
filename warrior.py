# importing character class
from character import Character

# initilizing warrior class
class Warrior(Character):
    def __init__(self, name):
        super().__init__(name, health=200, max_health=200, attack_power=20, speed=10)

        self._rage_threshold = 0.30

    def is_enraged(self):
        return self._health / self._max_health <self._rage_threshold
          
    
    def attack(self,target):
        if self.is_enraged():
            return self._attack_power * 1.5
        else:
            return self._attack_power
    
    def get_status(self):
        status = super().get_status()
        if self.is_enraged():
            print(status + "ENRAGED")
        else:
            print(status)