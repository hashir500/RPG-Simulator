import argparse
from warrior import Warrior
from mage import Mage
from rogue import Rogue
from character import Character
from game_battle import GameBattle
from combat_engine import resolve_attack

parser = argparse.ArgumentParser(description="RPG Battle Simulator")
parser.add_argument("--load", type=str, help="Load a saved character from a JSON file")
args = parser.parse_args()

if args.load:
    player = Character.load_from_json(args.load)
    if player is None:
        print("Failed to load character. Starting fresh.")
        args.load = None

if not args.load:
    print("\nWelcome to RPG Simulator!")
    print("Choose your character:")
    print("(1) Warrior")
    print("(2) Mage")
    print("(3) Rogue")
    
    choice = input("\nEnter choice: ")
    name = input("Enter your character's name: ")
    
    if choice == "1":
        player = Warrior(name)
    elif choice == "2":
        player = Mage(name)
    elif choice == "3":
        player = Rogue(name)
    else:
        print("Invalid choice. Defaulting to Warrior.")
        player = Warrior(name)


print("\nAn enemy approaches...")
enemy = Warrior("Dark Knight")
enemy.get_status()

battle = GameBattle([player], [enemy])
print(f"\nBattle begins! {player._name} vs {enemy._name}")

while not battle.is_battle_over():
    print("\n--- Your Turn ---")
    player.get_status()
    print("\n(1) Attack   (2) Status   (3) Save & Quit")
    action = input("Choose action: ")

    if action == "1":
        resolve_attack(player, enemy)
        if not battle.is_battle_over():
            print("\n--- Enemy Turn ---")
            resolve_attack(enemy, player)
    elif action == "2":
        player.get_status()
        enemy.get_status()
    elif action == "3":
        player.save_to_json(f"{player._name.lower()}.json")
        print("Game saved. Goodbye!")
        exit()
    else:
        print("Invalid choice, try again.")

if player.is_alive:
    print(f"\nVictory! {player._name} has defeated {enemy._name}!")
    player.save_to_json(f"{player._name.lower()}.json")
else:
    print(f"\nDefeat. {player._name} has been defeated by {enemy._name}.")