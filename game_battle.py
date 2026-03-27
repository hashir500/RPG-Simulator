from combat_engine import resolve_attack

class GameBattle:
    def __init__(self,players,enemies):
        self._players = players
        self._enemies = enemies
        self._turn_order = []

    def determine_turn_order(self):
        combined = self._players + self._enemies
        self._turn_order = sorted(combined,key =lambda c: c._speed,reverse=True)

    def is_battle_over(self):
        all_players_dead = not any(c.is_alive for c in self._players)
        all_enemies_dead = not any(c.is_alive for c in self._enemies)
        return all_players_dead or all_enemies_dead
    
    def run_round(self):
        self.determine_turn_order()
        for character in self._turn_order:
            character.tick_status_effects()
            if not character.is_alive:
                continue
            if character in self._players:
                target = next((c for c in self._enemies if c.is_alive), None)
            else:
                target = next((c for c in self._players if c.is_alive), None)
            if target is not None:
                resolve_attack(character, target)
            if self.is_battle_over():
                break