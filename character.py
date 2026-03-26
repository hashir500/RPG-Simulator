# base class
class Character:
    # attributes for character
    def __init__(self,name,health=150,max_health=150,attack_power=10,speed=5):
        self._name = name
        self._health = health
        self._max_health = max_health
        self._attack_power = attack_power
        self._speed = speed

    def __str__(self):
        return f" {self._name}\n HP: {self._health}/{self._max_health}\n Attack: {self._attack_power}\n Speed: {self._speed}"
    
    def __repr__(self):
         return f"Character( name= {self._name} hp= {self._health} max_hp= {self._max_health} attack= {self._attack_power} speed= {self._speed})"
    
    @property
    def is_alive(self):
        return self._health > 0
          
    
    def get_status(self):
        return(f"{self._name} (Health: {self._health}/{self._max_health})")




