import tkinter as tk
from tkinter import filedialog, messagebox
from warrior import Warrior
from mage import Mage
from rogue import Rogue
from character import Character
from game_battle import GameBattle
from combat_engine import resolve_attack
from tkinter import PhotoImage
from PIL import Image, ImageTk
import os



class GameApp:
    def __init__(self, root):
        self.root = root
        self.player = None
        self.enemy = None
        self.battle = None
        self.show_main_menu()

    def show_main_menu(self):
        self.clear_window()
        MainMenuScreen(self)

    def show_character_select(self):
        self.clear_window()
        CharacterSelectScreen(self)

    def show_battle(self):
        self.clear_window()
        BattleScreen(self)

    def show_end_screen(self, victory):
        self.clear_window()
        EndScreen(self, victory)

    def clear_window(self):
        for widget in self.root.winfo_children():
            widget.destroy()


# ── SCREEN 1: MAIN MENU ───────────────────────────────────────────────────────
class MainMenuScreen:
    def __init__(self, app):
        self.app = app
        self.selected = 0
        self.options = ["NEW GAME", "LOAD GAME", "QUIT"]
        self.option_labels = []
        self.build()

    def build(self):
        self.app.root.configure(bg="#1a0a0a")
        container = tk.Frame(self.app.root, bg="#1a0a0a")
        container.pack(fill="both", expand=True, padx=40, pady=40)

        left = tk.Frame(container, bg="#1a0a0a")
        left.pack(side="left", fill="both", expand=True)

        tk.Label(left, text="────────────────", font=("Courier", 12),
                 bg="#1a0a0a", fg="#c0392b").pack(anchor="w", pady=(60, 0))
        tk.Label(left, text="RPG", font=("Press Start 2P", 42),
                 bg="#1a0a0a", fg="#f0a500").pack(anchor="w")
        tk.Label(left, text="SIMULATOR", font=("Press Start 2P", 22),
                 bg="#1a0a0a", fg="#ffffff").pack(anchor="w")
        tk.Label(left, text="────────────────", font=("Courier", 12),
                 bg="#1a0a0a", fg="#c0392b").pack(anchor="w", pady=(4, 0))
        tk.Label(left, text="A TURN-BASED ADVENTURE", font=("Press Start 2P", 6),
                 bg="#1a0a0a", fg="#aaaacc").pack(anchor="w", pady=(8, 0))
        tk.Label(left, text="v1.0", font=("Press Start 2P", 6),
                 bg="#1a0a0a", fg="#444466").pack(anchor="w", pady=(60, 0))

        right = tk.Frame(container, bg="#1a0a0a")
        right.pack(side="right", fill="both", expand=True)

        tk.Label(right, bg="#1a0a0a", text="", font=("Arial", 40)).pack()
        tk.Label(right, bg="#1a0a0a", text="", font=("Arial", 40)).pack()
        tk.Label(right, text="MAIN MENU", font=("Press Start 2P", 8),
                 bg="#1a0a0a", fg="#444466").pack(anchor="e", pady=(0, 20))

        for i, option in enumerate(self.options):
            row = tk.Frame(right, bg="#1a0a0a")
            row.pack(anchor="e", pady=8)
            cursor = tk.Label(row, text="►", font=("Press Start 2P", 10),
                              bg="#1a0a0a", fg="#f0a500")
            cursor.pack(side="left", padx=(0, 10))
            label = tk.Label(row, text=option, font=("Press Start 2P", 10),
                             bg="#1a0a0a", fg="#ffffff")
            label.pack(side="left")
            self.option_labels.append((cursor, label, row))

        tk.Label(right, text="↑ ↓  NAVIGATE      ENTER  SELECT",
                 font=("Press Start 2P", 5), bg="#1a0a0a",
                 fg="#444466").pack(anchor="e", pady=(40, 0))

        self.update_selection()
        self.app.root.bind("<Up>", self.move_up)
        self.app.root.bind("<Down>", self.move_down)
        self.app.root.bind("<Return>", self.select_option)

    def update_selection(self):
        for i, (cursor, label, row) in enumerate(self.option_labels):
            if i == self.selected:
                cursor.config(fg="#f0a500", bg="#2d1010")
                label.config(fg="#f0a500", bg="#2d1010")
                row.config(bg="#2d1010")
            else:
                cursor.config(fg="#1a0a0a", bg="#1a0a0a")
                label.config(fg="#aaaacc", bg="#1a0a0a")
                row.config(bg="#1a0a0a")

    def move_up(self, event):
        self.selected = (self.selected - 1) % len(self.options)
        self.update_selection()

    def move_down(self, event):
        self.selected = (self.selected + 1) % len(self.options)
        self.update_selection()

    def select_option(self, event):
        self.app.root.unbind("<Up>")
        self.app.root.unbind("<Down>")
        self.app.root.unbind("<Return>")
        if self.selected == 0:
            self.app.show_character_select()
        elif self.selected == 1:
            self.load_game()
        elif self.selected == 2:
            self.app.root.quit()

    def load_game(self):
        filename = filedialog.askopenfilename(
            title="Load Character",
            filetypes=[("JSON Files", "*.json")],
            initialdir="."
        )
        if filename:
            player = Character.load_from_json(filename)
            if player:
                self.app.player = player
                self.app.enemy = Warrior("Dark Knight")
                self.app.battle = GameBattle([self.app.player], [self.app.enemy])
                self.app.show_battle()
            else:
                messagebox.showerror("Load Failed",
                                     "Could not load character from that file.")


# ── SCREEN 2: CHARACTER SELECT ────────────────────────────────────────────────
class CharacterSelectScreen:
    def __init__(self, app):
        self.app = app
        self.name_entries = []
        self.cards = []
        self.characters = [
            {"class": Warrior, "name": "WARRIOR", "icon": "⚔",
             "desc": "Enters RAGE\nbelow 30% HP",
             "stats": "HP  200\nATK  20\nSPD  10",
             "border": "#c0392b", "bg": "#2d1010"},
            {"class": Mage, "name": "MAGE", "icon": "✦",
             "desc": "Casts spells\nusing mana",
             "stats": "HP  100\nATK  25\nSPD   7",
             "border": "#8e44ad", "bg": "#1e1b2d"},
            {"class": Rogue, "name": "ROGUE", "icon": "◆",
             "desc": "35% chance\nfor CRIT hit",
             "stats": "HP  120\nATK  15\nSPD  20",
             "border": "#27ae60", "bg": "#1b2d1e"},
        ]
        self.build()

    def build(self):
        self.app.root.configure(bg="#1a0a0a")
        tk.Frame(self.app.root, bg="#c0392b", height=6).pack(fill="x")

        title_frame = tk.Frame(self.app.root, bg="#2d1010")
        title_frame.pack(fill="x")
        tk.Label(title_frame, text="PLAYER SELECT", font=("Press Start 2P", 22),
                 bg="#2d1010", fg="#f0a500").pack(side="left", padx=30, pady=15)

        flavour_box = tk.Frame(title_frame, bg="#3d1515", padx=15, pady=10)
        flavour_box.pack(side="right", padx=30, pady=15)
        tk.Label(flavour_box, text="Choose your hero wisely.\nYour fate depends on it...",
                 font=("Press Start 2P", 6), bg="#3d1515",
                 fg="#aaaacc", justify="left").pack()

        tk.Frame(self.app.root, bg="#c0392b", height=3).pack(fill="x")

        cards_frame = tk.Frame(self.app.root, bg="#1a0a0a")
        cards_frame.pack(fill="both", expand=True, pady=30)

        for i, char in enumerate(self.characters):
            card_border = tk.Frame(cards_frame, bg=char["border"], padx=4, pady=4)
            card_border.pack(side="left", padx=25, expand=True)
            self.cards.append(card_border)

            card = tk.Frame(card_border, bg=char["bg"], width=180,
                            height=300, cursor="hand2")
            card.pack()
            card.pack_propagate(False)

            tk.Label(card, text=f"P{i+1}", font=("Press Start 2P", 7),
                     bg=char["border"], fg="#ffffff",
                     padx=6, pady=2).pack(anchor="w", padx=8, pady=(8, 0))
            tk.Label(card, text=char["icon"], font=("Arial", 32),
                     bg=char["bg"], fg=char["border"]).pack(pady=(4, 0))
            tk.Label(card, text=char["name"], font=("Press Start 2P", 9),
                     bg=char["bg"], fg=char["border"]).pack(pady=4)
            tk.Label(card, text="...................", font=("Courier", 8),
                     bg=char["bg"], fg="#444466").pack()
            tk.Label(card, text=char["stats"], font=("Courier", 9),
                     bg=char["bg"], fg="#ffffff", justify="left").pack(pady=6)
            tk.Label(card, text=char["desc"], font=("Press Start 2P", 5),
                     bg=char["bg"], fg="#aaaacc", justify="center").pack(pady=4)

            entry = tk.Entry(card, font=("Press Start 2P", 6), bg="#0d0d0d",
                             fg="#ffffff", insertbackground="white",
                             relief="flat", width=14, justify="center")
            entry.insert(0, "ENTER NAME")
            entry.bind("<FocusIn>", lambda e, en=entry: self.clear_placeholder(en))
            entry.pack(pady=6)
            self.name_entries.append(entry)

            tk.Button(card, text="[ SELECT ]", font=("Press Start 2P", 6),
                      bg=char["border"], fg="#ffffff", relief="flat",
                      cursor="hand2", activebackground="#ffffff",
                      activeforeground=char["border"],
                      command=lambda i=i: self.select_character(i)).pack(pady=6)

        tk.Frame(self.app.root, bg="#c0392b", height=3).pack(fill="x")
        bottom = tk.Frame(self.app.root, bg="#2d1010")
        bottom.pack(fill="x")

        tk.Button(bottom, text="[ ← BACK ]", font=("Press Start 2P", 6),
                  bg="#2d1010", fg="#aaaacc", relief="flat", cursor="hand2",
                  command=self.app.show_main_menu).pack(side="left", padx=20, pady=10)

        self.flicker_label = tk.Label(bottom, text="[ SELECT YOUR CLASS TO BEGIN ]",
                                      font=("Press Start 2P", 6),
                                      bg="#2d1010", fg="#f0a500")
        self.flicker_label.pack(side="right", padx=20, pady=10)
        self.flicker()

    def clear_placeholder(self, entry):
        if entry.get() == "ENTER NAME":
            entry.delete(0, tk.END)

    def flicker(self):
        try:
            current = self.flicker_label.cget("fg")
            next_color = "#2d1010" if current == "#f0a500" else "#f0a500"
            self.flicker_label.config(fg=next_color)
            self.app.root.after(600, self.flicker)
        except Exception:
            return

    def select_character(self, index):
        char = self.characters[index]
        name = self.name_entries[index].get().strip()
        if not name or name == "ENTER NAME":
            messagebox.showwarning("No Name",
                                   "Please enter your character's name first.")
            return
        self.app.player = char["class"](name)
        self.app.enemy = Warrior("Dark Knight")
        self.app.battle = GameBattle([self.app.player], [self.app.enemy])
        self.app.show_battle()


# ── SCREEN 3: BATTLE ─────────────────────────────────────────────────────────
class BattleScreen:
    def __init__(self, app):
        self.app = app
        self.log_messages = []
        self.torch_states = []
        self.images = {}
        self.load_sprites()    
        self.build()           
        self.update_torches()


    def load_sprites(self):
        import os
        sprite_map = {
            "warrior":     "assets/knight.png",
            "mage":        "assets/wizard.png",
            "rogue":       "assets/rogue.png",
            "dark_knight": "assets/dark_knight.png",
        }
        for key, path in sprite_map.items():
            if os.path.exists(path):
                img = Image.open(path).convert("RGBA")
                frame_height = img.height
                frame_width = frame_height
                img = img.crop((0, 0, frame_width, frame_height))
                img = img.resize((90, 110), Image.NEAREST)
                self.images[key] = ImageTk.PhotoImage(img)
            else:
                self.images[key] = None


    def build(self):
        self.app.root.configure(bg="#1a0a0a")

        # top bar
        top_bar = tk.Frame(self.app.root, bg="#0d0d0d", height=70)
        top_bar.pack(fill="x")
        top_bar.pack_propagate(False)

        player_frame = tk.Frame(top_bar, bg="#0d0d0d")
        player_frame.pack(side="left", padx=20, pady=10)
        tk.Label(player_frame, text=self.app.player._name.upper(),
                 font=("Press Start 2P", 8), bg="#0d0d0d",
                 fg="#f0a500").pack(anchor="w")

        self.player_hp_frame = tk.Frame(player_frame, bg="#333333",
                                        width=200, height=14)
        self.player_hp_frame.pack(anchor="w", pady=3)
        self.player_hp_frame.pack_propagate(False)
        self.player_hp_bar = tk.Frame(self.player_hp_frame, bg="#27ae60", height=14)
        self.player_hp_bar.place(x=0, y=0, relheight=1, width=200)
        self.player_hp_label = tk.Label(
            player_frame,
            text=f"HP: {self.app.player._health}/{self.app.player._max_health}",
            font=("Press Start 2P", 6), bg="#0d0d0d", fg="#aaaacc")
        self.player_hp_label.pack(anchor="w")

        tk.Label(top_bar, text="VS", font=("Press Start 2P", 12),
                 bg="#0d0d0d", fg="#c0392b").pack(side="left", expand=True)

        enemy_frame = tk.Frame(top_bar, bg="#0d0d0d")
        enemy_frame.pack(side="right", padx=20, pady=10)
        tk.Label(enemy_frame, text=self.app.enemy._name.upper(),
                 font=("Press Start 2P", 8), bg="#0d0d0d",
                 fg="#c0392b").pack(anchor="e")

        self.enemy_hp_frame = tk.Frame(enemy_frame, bg="#333333",
                                       width=200, height=14)
        self.enemy_hp_frame.pack(anchor="e", pady=3)
        self.enemy_hp_frame.pack_propagate(False)
        self.enemy_hp_bar = tk.Frame(self.enemy_hp_frame, bg="#27ae60", height=14)
        self.enemy_hp_bar.place(x=0, y=0, relheight=1, width=200)
        self.enemy_hp_label = tk.Label(
            enemy_frame,
            text=f"HP: {self.app.enemy._health}/{self.app.enemy._max_health}",
            font=("Press Start 2P", 6), bg="#0d0d0d", fg="#aaaacc")
        self.enemy_hp_label.pack(anchor="e")

        tk.Frame(self.app.root, bg="#c0392b", height=3).pack(fill="x")

        self.arena = tk.Canvas(self.app.root, bg="#2a2a3e",
                               height=220, highlightthickness=0)
        self.arena.pack(fill="x")
        self.app.root.update_idletasks()
        self.draw_arena()

        tk.Frame(self.app.root, bg="#c0392b", height=3).pack(fill="x")

        log_frame = tk.Frame(self.app.root, bg="#0d0d0d")
        log_frame.pack(fill="x")
        tk.Label(log_frame, text="  ► BATTLE LOG", font=("Press Start 2P", 6),
                 bg="#0d0d0d", fg="#444466").pack(anchor="w", padx=10, pady=(6, 0))
        tk.Frame(log_frame, bg="#333333", height=1).pack(fill="x", padx=10)

        self.log_labels = []
        for i in range(3):
            lbl = tk.Label(log_frame, text="", font=("Press Start 2P", 6),
                           bg="#0d0d0d", fg="#aaaacc", anchor="w", padx=10)
            lbl.pack(fill="x", pady=2)
            self.log_labels.append(lbl)

        tk.Frame(self.app.root, bg="#333333", height=1).pack(fill="x")

        btn_frame = tk.Frame(self.app.root, bg="#1a0a0a")
        btn_frame.pack(fill="x", pady=12)

        buttons = [
            ("⚔  ATTACK", "#c0392b", self.action_attack),
            ("✦  SPELL",  "#8e44ad", self.action_spell),
            ("◆  STATUS", "#27ae60", self.action_status),
            ("▣  SAVE",   "#b8860b", self.action_save),
        ]
        for text, color, cmd in buttons:
            tk.Button(btn_frame, text=text, font=("Press Start 2P", 7),
                      bg=color, fg="#ffffff", relief="flat", cursor="hand2",
                      padx=14, pady=8, activebackground="#ffffff",
                      activeforeground=color, command=cmd).pack(
                side="left", padx=10, expand=True)

    def draw_arena(self):
        self.arena.update_idletasks()
        w = self.arena.winfo_width() or 800
        h = 220
        tile = 32

        for x in range(0, w, tile):
            for y in range(0, h, tile):
                shade = "#2a2a3e" if (x // tile + y // tile) % 2 == 0 else "#252535"
                self.arena.create_rectangle(x, y, x + tile, y + tile,
                                            fill=shade, outline="#1a1a2e", width=1)

        for x in range(0, w, tile):
            self.arena.create_rectangle(x, 0, x + tile, tile,
                                        fill="#3a3a4e", outline="#1a1a2e", width=1)
            self.arena.create_rectangle(x + 4, 4, x + tile - 4, tile - 4,
                                        fill="#353548", outline="", width=0)

        torch_positions = [w // 4, w // 2, 3 * w // 4]
        self.torch_states = []
        for tx in torch_positions:
            self.arena.create_rectangle(tx - 4, 6, tx + 4, 20,
                                        fill="#8B4513", outline="")
            flame = self.arena.create_oval(tx - 6, 0, tx + 6, 14,
                                           fill="#f0a500", outline="")
            self.torch_states.append(flame)

        px, py = w // 4, h // 2 + 10
        self.player_plate = self.draw_player_sprite(px, py)

        ex, ey = 3 * w // 4, h // 2 + 10
        self.enemy_plate = self.draw_enemy_sprite(ex, ey)

        self.arena.create_text(px, py + 65,
                               text=self.app.player._name[:8].upper(),
                               font=("Press Start 2P", 6), fill="#f0a500")
        self.arena.create_text(ex, ey + 65,
                               text=self.app.enemy._name[:8].upper(),
                               font=("Press Start 2P", 6), fill="#c0392b")

    def draw_player_sprite(self, cx, cy):
        if isinstance(self.app.player, Warrior):
            key = "warrior"
            outline_color = "#f0a500"
        elif isinstance(self.app.player, Mage):
            key = "mage"
            outline_color = "#8e44ad"
        elif isinstance(self.app.player, Rogue):
            key = "rogue"
            outline_color = "#27ae60"
        else:
            key = "warrior"
            outline_color = "#f0a500"

        plate = self.arena.create_rectangle(
            cx - 50, cy - 58, cx + 50, cy + 58,
            fill="#1e1e2e", outline=outline_color, width=2)

        if self.images.get(key):
            self.arena.create_image(cx, cy, image=self.images[key],
                                    anchor="center")
        else:
            self.arena.create_text(cx, cy, text="?",
                                   font=("Press Start 2P", 24),
                                   fill=outline_color)
        return plate

    def draw_enemy_sprite(self, cx, cy):
        plate = self.arena.create_rectangle(
            cx - 50, cy - 58, cx + 50, cy + 58,
            fill="#1e1e2e", outline="#c0392b", width=2)

        if self.images.get("dark_knight"):
            self.arena.create_image(cx, cy, image=self.images["dark_knight"],
                                    anchor="center")
        else:
            self.arena.create_text(cx, cy, text="☠",
                                   font=("Arial", 32),
                                   fill="#c0392b")
        return plate

    def update_torches(self):
        import random
        colors = ["#f0a500", "#e8940a", "#ffbc00", "#ff8c00"]
        for flame in self.torch_states:
            try:
                self.arena.itemconfig(flame, fill=random.choice(colors))
            except Exception:
                return
        self.app.root.after(150, self.update_torches)

    def add_log(self, message):
        self.log_messages.insert(0, message)
        self.log_messages = self.log_messages[:3]
        colors = ["#f0a500", "#aaaacc", "#666688"]
        for i, lbl in enumerate(self.log_labels):
            if i < len(self.log_messages):
                lbl.config(text=f"  {self.log_messages[i]}", fg=colors[i])
            else:
                lbl.config(text="")

    def refresh_hp_bars(self):
        p = self.app.player
        p_ratio = p._health / p._max_health
        p_width = int(200 * p_ratio)
        p_color = "#27ae60" if p_ratio > 0.5 else \
                  "#f0a500" if p_ratio > 0.25 else "#c0392b"
        self.player_hp_bar.place(width=p_width)
        self.player_hp_bar.config(bg=p_color)
        self.player_hp_label.config(
            text=f"HP: {p._health}/{p._max_health}")

        e = self.app.enemy
        e_ratio = e._health / e._max_health
        e_width = int(200 * e_ratio)
        e_color = "#27ae60" if e_ratio > 0.5 else \
                  "#f0a500" if e_ratio > 0.25 else "#c0392b"
        self.enemy_hp_bar.place(width=e_width)
        self.enemy_hp_bar.config(bg=e_color)
        self.enemy_hp_label.config(
            text=f"HP: {e._health}/{e._max_health}")

    def flash_plate(self, plate, original_color):
        self.arena.itemconfig(plate, fill="#c0392b")
        self.app.root.after(
            200, lambda: self.arena.itemconfig(plate, fill=original_color))

    def capture_log(self, attacker, defender):
        import io, sys
        buffer = io.StringIO()
        sys.stdout = buffer
        result = resolve_attack(attacker, defender)
        sys.stdout = sys.__stdout__
        output = buffer.getvalue().strip().split("\n")
        for line in output:
            if line.strip():
                self.add_log(line.strip())
        return result

    def action_attack(self):
        if self.app.battle.is_battle_over():
            return
        self.capture_log(self.app.player, self.app.enemy)
        self.flash_plate(self.enemy_plate, "#1e1e2e")
        self.refresh_hp_bars()
        if self.app.battle.is_battle_over():
            self.app.root.after(800, lambda: self.app.show_end_screen(True))
            return
        self.app.root.after(600, self.enemy_turn)

    def enemy_turn(self):
        self.capture_log(self.app.enemy, self.app.player)
        self.flash_plate(self.player_plate, "#1e1e2e")
        self.refresh_hp_bars()
        if self.app.battle.is_battle_over():
            self.app.root.after(800, lambda: self.app.show_end_screen(False))

    def action_spell(self):
        if not isinstance(self.app.player, Mage):
            self.add_log("Only a Mage can cast spells!")
            return
        if self.app.battle.is_battle_over():
            return
        import io, sys
        buffer = io.StringIO()
        sys.stdout = buffer
        damage = self.app.player.cast_spell(self.app.enemy)
        sys.stdout = sys.__stdout__
        output = buffer.getvalue().strip().split("\n")
        for line in output:
            if line.strip():
                self.add_log(line.strip())
        if damage and damage > 0:
            self.app.enemy.take_damage(damage)
            self.add_log(
                f"{self.app.player._name} cast spell for {damage} dmg!")
            self.flash_plate(self.enemy_plate, "#1e1e2e")
            self.refresh_hp_bars()
            if self.app.battle.is_battle_over():
                self.app.root.after(800, lambda: self.app.show_end_screen(True))
                return
        self.app.root.after(600, self.enemy_turn)

    def action_status(self):
        p, e = self.app.player, self.app.enemy
        self.add_log(f"{p._name}: HP {p._health}/{p._max_health}")
        self.add_log(f"{e._name}: HP {e._health}/{e._max_health}")

    def action_save(self):
        self.app.player.save_to_json(f"{self.app.player._name.lower()}.json")
        self.add_log(f"{self.app.player._name} saved successfully.")

# ── SCREEN 4: END SCREEN ─────────────────────────────────────────────────────
class EndScreen:
    def __init__(self, app, victory):
        self.app = app
        self.victory = victory
        self.build()

    def build(self):
        self.app.root.configure(bg="#1a0a0a")
        title = "VICTORY!" if self.victory else "DEFEATED..."
        color = "#f0a500" if self.victory else "#c0392b"
        subtitle = "You conquered the Dark Knight!" \
                   if self.victory else "The darkness has claimed you..."

        tk.Label(self.app.root, text=title, font=("Press Start 2P", 30),
                 bg="#1a0a0a", fg=color).pack(pady=60)
        tk.Label(self.app.root, text=subtitle, font=("Press Start 2P", 8),
                 bg="#1a0a0a", fg="#aaaacc").pack(pady=10)
        tk.Frame(self.app.root, bg=color, height=3).pack(
            fill="x", padx=80, pady=30)

        btn_frame = tk.Frame(self.app.root, bg="#1a0a0a")
        btn_frame.pack(pady=20)

        tk.Button(btn_frame, text="[ PLAY AGAIN ]",
                  font=("Press Start 2P", 8), bg="#f0a500", fg="#1a0a0a",
                  relief="flat", cursor="hand2", padx=14, pady=8,
                  command=self.app.show_main_menu).pack(side="left", padx=20)
        tk.Button(btn_frame, text="[ QUIT ]",
                  font=("Press Start 2P", 8), bg="#c0392b", fg="#ffffff",
                  relief="flat", cursor="hand2", padx=14, pady=8,
                  command=self.app.root.quit).pack(side="left", padx=20)