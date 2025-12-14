import pyxel
import random

SCREEN_W = 160
SCREEN_H = 120

STATE_TITLE = 0
STATE_PLAYING = 1
STATE_GAMEOVER = 2

class Game:
    def __init__(self):
        pyxel.init(SCREEN_W, SCREEN_H)
        pyxel.mouse(True)

        self.state = STATE_TITLE

        self.player_x = SCREEN_W // 2
        self.player_y = SCREEN_H // 2

        pyxel.images[2].load(0, 0, "o1.png", True)
        self.umplus10 = pyxel.Font("assets/umplus_j10r.bdf")

        self.message = ""
        self.message_timer = 0

        self.rooms = {}
        self.current_room = (1, 1)
        self.inventory = []

        self.create_world()

        pyxel.run(self.update, self.draw)

    # -------------------------------------------------------
    # WORLD SETUP
    # -------------------------------------------------------
    def create_world(self):
        # 3x3 simple rooms
        for rx in range(3):
            for ry in range(3):
                self.rooms[(rx, ry)] = {
                    "color": (rx + ry + 3) % 15,
                    "item": None
                }

        # place 1 item randomly
        arx = random.randint(0, 2)
        ary = random.randint(0, 2)

        self.rooms[(arx, ary)]["item"] = {
            "name": "Ancient Key",
            "x": SCREEN_W // 2,
            "y": SCREEN_H // 2
        }

    # -------------------------------------------------------
    # UPDATE
    # -------------------------------------------------------
    def update(self):
        if self.state == STATE_TITLE:
            self.update_title()
        elif self.state == STATE_PLAYING:
            self.update_playing()
        elif self.state == STATE_GAMEOVER:
            if self.click() or pyxel.btnp(32) or pyxel.btnp(pyxel.KEY_SPACE):
                self.reset_game()

    def update_title(self):
        if self.click() or pyxel.btnp(32) or pyxel.btnp(pyxel.KEY_SPACE):
            self.reset_game()

    def reset_game(self):
        self.state = STATE_PLAYING
        self.message = "Welcome to the adventure!"
        self.message_timer = 120
        self.inventory = []
        self.current_room = (1, 1)
        self.player_x = SCREEN_W // 2
        self.player_y = SCREEN_H // 2
        self.create_world()

    def update_playing(self):
        speed = 1

        # movement
        if pyxel.btn(pyxel.KEY_LEFT):
            self.player_x -= speed
        if pyxel.btn(pyxel.KEY_RIGHT):
            self.player_x += speed
        if pyxel.btn(pyxel.KEY_UP):
            self.player_y -= speed
        if pyxel.btn(pyxel.KEY_DOWN):
            self.player_y += speed

        # bounds
        self.player_x = max(0, min(SCREEN_W - 8, self.player_x))
        self.player_y = max(8, min(SCREEN_H - 8, self.player_y))

        # interaction
        if pyxel.btnp(pyxel.KEY_Z) or pyxel.btnp(90) or pyxel.btnp(32):
            self.try_interact()

        # message timer
        if self.message_timer > 0:
            self.message_timer -= 1
            if self.message_timer == 0:
                self.message = ""

    # -------------------------------------------------------
    # INTERACTION LOGIC
    # -------------------------------------------------------
    def try_interact(self):
        room = self.rooms[self.current_room]
        item = room["item"]

        # item pickup
        if item:
            if abs(self.player_x - item["x"]) < 12 and abs(self.player_y - item["y"]) < 12:
                self.inventory.append(item["name"])
                room["item"] = None
                self.message = f"Picked up {item['name']}!"
                self.message_timer = 120
                return

        # door / win condition
        if "Ancient Key" in self.inventory and self.player_x < 16 and self.player_y < 16:
            self.state = STATE_GAMEOVER
            return

        # nothing
        self.message = "Nothing interesting."
        self.message_timer = 60

    # -------------------------------------------------------
    # DRAW
    # -------------------------------------------------------
    def draw(self):
        if self.state == STATE_TITLE:
            self.draw_title()
        elif self.state == STATE_PLAYING:
            self.draw_playing()
        elif self.state == STATE_GAMEOVER:
            self.draw_gameover()

    def draw_title(self):
        pyxel.cls(1)
        # pyxel.load("my_resource.pyxres")
        # pyxel.blt(0, 0, 0, 0, 0, 160, 120)
        pyxel.blt(0, 0, 2, 0, 0, 160, 120)
        # pyxel.rect(30, 80, 100, 20, 7)
        pyxel.text(95, 87, "タマランドに", (pyxel.frame_count //2) % 32, self.umplus10)
        pyxel.text(95, 100, "ようこそ！", (pyxel.frame_count //2) % 32, self.umplus10)

    def draw_playing(self):
        room = self.rooms[self.current_room]

        pyxel.cls(room["color"])

        # draw item
        item = room["item"]
        if item:
            pyxel.rect(item["x"] - 4, item["y"] - 4, 8, 8, 10)
            pyxel.text(item["x"] - 12, item["y"] - 12, item["name"], 7)

        # player
        pyxel.rect(self.player_x, self.player_y, 8, 8, 1)

        # hud
        pyxel.rect(0, 0, SCREEN_W, 8, 0)
        pyxel.text(4, 1, f"Room {self.current_room}", 7)
        inv = ", ".join(self.inventory) if self.inventory else "Empty"
        pyxel.text(70, 1, f"Inv: {inv}", 7)

        # message box
        if self.message:
            pyxel.rect(0, SCREEN_H - 10, SCREEN_W, 10, 0)
            pyxel.text(4, SCREEN_H - 8, self.message, 7)

    def draw_gameover(self):
        pyxel.cls(0)
        pyxel.text(40, 40, "YOU WIN!", 11)
        pyxel.text(25, 60, "Click or press Enter to restart", 7)

    # -------------------------------------------------------
    # HELPER
    # -------------------------------------------------------
    def click(self):
        return pyxel.btnp(0)


Game()
