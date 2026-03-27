from dataclasses import dataclass, asdict


@dataclass
class CharacterData:
    name: str
    health: int
    max_health: int 
    attack_power: int 
    speed: int