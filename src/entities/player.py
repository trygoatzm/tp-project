import math

from src import settings
from src.entities.projectile import Projectile

DIRS = ["e", "se", "s", "sw", "w", "nw", "n", "ne"]
FRAME_COUNT = {"idle": 2, "walk": 4, "shoot": 2, "walkshoot": 4}
FRAME_RATE = {"idle": 2, "walk": 8, "walkshoot": 8}
SHOT_FLASH_TIME = 0.1
# Кончик пальца героя относительно центра (x вправо, y вниз), в пикселях игры. Из docs/ART_LOG.md, раздел 3.3.
MUZZLE = {"s": (-5, 8), "se": (3, 7), "e": (5, 5), "ne": (7, 1),
          "n": (6, -1), "nw": (-8, -7), "w": (-5, 5), "sw": (-8, 7)}


def dir8(dx, dy):
    angle = math.degrees(math.atan2(dy, dx)) % 360
    return DIRS[int((angle + 22.5) // 45) % 8]


class Player:
    SIZE = 20
    SHOT_COOLDOWN = 0.40
    SHOT_SPEED = 520
    SHOT_DAMAGE = 1
    SHOT_LIFETIME = 0.8

    def __init__(self, pos):
        self.x, self.y = float(pos[0]), float(pos[1])
        self.aim = (1.0, 0.0)
        self.cooldown = 0.0
        self.invuln = 0.0
        self.facing = "s"
        self.action = "idle"
        self.anim_time = 0.0
        self.shot_flash = 0.0

    @property
    def rect(self):
        h = self.SIZE / 2
        return (self.x - h, self.y - h, self.SIZE, self.SIZE)

    @property
    def center(self):
        return (self.x, self.y)

    @property
    def visible(self):
        return not (self.invuln > 0 and int(self.invuln * 10) % 2 == 0)

    def teleport(self, pos):
        self.x, self.y = float(pos[0]), float(pos[1])
        self.cooldown = 0.0
        self.invuln = 0.0
        self.shot_flash = 0.0

    def update(self, dt, room, move, aim_point, shooting):
        self.cooldown = max(0.0, self.cooldown - dt)
        self.invuln = max(0.0, self.invuln - dt)
        self.shot_flash = max(0.0, self.shot_flash - dt)

        mx, my = move
        moving = bool(mx or my)
        length = math.hypot(mx, my)
        if length > 1:
            mx, my = mx / length, my / length
        if moving:
            h = self.SIZE / 2
            nx, ny = room.slide((self.x - h, self.y - h, self.SIZE, self.SIZE),
                                mx * settings.PLAYER_SPEED * dt, my * settings.PLAYER_SPEED * dt)
            self.x, self.y = nx + h, ny + h

        ax, ay = aim_point[0] - self.x, aim_point[1] - self.y
        d = math.hypot(ax, ay)
        if d > 1e-6:
            self.aim = (ax / d, ay / d)

        if shooting:
            self.facing = dir8(*self.aim)
        elif moving:
            self.facing = dir8(mx, my)
        if shooting and moving:
            action = "walkshoot"
        elif shooting:
            action = "shoot"
        elif moving:
            action = "walk"
        else:
            action = "idle"
        if action != self.action:
            self.action = action
            self.anim_time = 0.0
        else:
            self.anim_time += dt

        shots = []
        if shooting and self.cooldown == 0.0:
            self.cooldown = self.SHOT_COOLDOWN
            self.shot_flash = SHOT_FLASH_TIME
            ux, uy = self.aim
            ox, oy = MUZZLE[self.facing]
            shots.append(Projectile(self.x + ox, self.y + oy,
                                    ux * self.SHOT_SPEED, uy * self.SHOT_SPEED,
                                    damage=self.SHOT_DAMAGE, owner="player",
                                    lifetime=self.SHOT_LIFETIME))
        return shots

    def take_hit(self, amount, state):
        if self.invuln > 0 or not state.is_alive:
            return "ignored"
        died = state.damage(amount)
        self.invuln = settings.INVULN_TIME
        return "dead" if died else "hit"

    def frame_key(self):
        if self.action == "shoot":
            n = 2 if self.shot_flash > 0 else 1
        else:
            n = int(self.anim_time * FRAME_RATE[self.action]) % FRAME_COUNT[self.action] + 1
        return f"player_{self.action}_{self.facing}_{n}"

    def draw(self, surface):
        if not self.visible:
            return
        from src.systems.assets import get_image
        surface.blit(get_image(self.frame_key(), (self.SIZE, self.SIZE)),
                     (self.x - self.SIZE / 2, self.y - self.SIZE / 2))
