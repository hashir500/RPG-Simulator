
# base class
class Character:
    # attributes for character
    def __init__(self,name,health=150,max_health=150,attack_power=10,speed=5):
        self._name = name
        self._health = health
        self._max_health = max_health
        self._attack_power = attack_power
        self._speed = speed
        self._status_effects = []

    def __str__(self):
        return f" {self._name}\n HP: {self._health}/{self._max_health}\n Attack: {self._attack_power}\n Speed: {self._speed}"
    
    def __repr__(self):
         return f"Character( name= {self._name} hp= {self._health} max_hp= {self._max_health} attack= {self._attack_power} speed= {self._speed})"
    
    @property
    def health(self):
        return self._health
    
    def set_health(self, value):
        if not isinstance(value, (int, float)):
            raise TypeError("Value is not an integer or float")
        elif value < 0:
            raise ValueError("Value is negative")
        else:
            self._health = min(value, self._max_health)
    
    @property
    def name(self):
        return self._name

    @property
    def is_alive(self):
        return self._health > 0
          
    
    def get_status(self):
        return(f"{self._name} (Health: {self._health}/{self._max_health})")
    
    def take_damage(self,damage):
        self._health -= damage
        self._health = max(0, self._health)
        print(f"{self._name} took {damage} damage! Health is now {self._health}.")
        if self._health == 0:
            print(f"{self._name} has been defeated")

    def attack(self, target):
        target.take_damage(self._attack_power)

    def apply_status(self, effect):
        self._status_effects.append(effect)
        print(f"{self._name} is now {effect.name}!")


    def tick_status_effects(self):
        for effect in self._status_effects:
            effect.apply(self)
        self._status_effects = [e for e in self._status_effects if e.duration > 0]


