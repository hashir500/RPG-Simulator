from dataclasses import dataclass


@dataclass
class StatusEffect:
    name: str
    damage_per_turn: int
    duration: int

    def apply(self, target):
        target.take_damage(self.damage_per_turn)
        self.duration -= 1
        if self.duration > 0:
            print(f"{target._name} is {self.name}! Takes {self.damage_per_turn} damage. ({self.duration} turns remaining)")
        else:
            print(f"{target._name}'s {self.name} effect has worn off!")
