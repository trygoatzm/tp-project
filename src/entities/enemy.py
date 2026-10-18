import math


def direction(src, dst):
    dx, dy = dst[0] - src[0], dst[1] - src[1]
    d = math.hypot(dx, dy)
    if d < 1e-6:
        return (1.0, 0.0), 0.0
    return (dx / d, dy / d), d


class Enemy:
    SIZE = 24
    STRIKE_TIME = 0.15

    def __init__(self, data, pos):
        self.id = data["id"]
        self.name = data["name"]
        self.kind = data["kind"]
        self.sprite = data["sprite"]
        self.max_hp = data["hp"]
        self.hp = data["hp"]
        self.speed = data["speed"]
        self.contact_damage = data["contact_damage"]
        self.attack = data.get("attack")
        self.x, self.y = float(pos[0]), float(pos[1])
        self.alive = True
        self.hurt_timer = 0.0
        self._projectiles = []
        self.state = "chase"
        self.timer = 0.0
        self.strike_dir = (1.0, 0.0)


    @property
    def rect(self):
        h = self.SIZE / 2
        return (self.x - h, self.y - h, self.SIZE, self.SIZE)

    @property
    def center(self):
        return (self.x, self.y)

    def take_damage(self, n):
        if not self.alive:
            return
        self.hp -= n
        self.hurt_timer = 0.12
        if self.hp <= 0:
            self.hp = 0
            self.alive = False

    def take_projectiles(self):
        out, self._projectiles = self._projectiles, []
        return out

    def attack_hitbox(self):
        if not self.alive or self.state != "strike":
            return None
        r = self.attack["range"]
        side = r + 12
        cx = self.x + self.strike_dir[0] * r / 2
        cy = self.y + self.strike_dir[1] * r / 2
        return ((cx - side / 2, cy - side / 2, side, side), self.attack["damage"])


    def _step_towards(self, dt, room, target, speed):
        (ux, uy), _ = direction(self.center, target)
        h = self.SIZE / 2
        nx, ny = room.slide((self.x - h, self.y - h, self.SIZE, self.SIZE), ux * speed * dt, uy * speed * dt)
        self.x, self.y = nx + h, ny + h


    def update(self, dt, room, target):
        if not self.alive:
            return
        self.hurt_timer = max(0.0, self.hurt_timer - dt)
        a = self.attack
        if self.state == "chase":
            dir_, dist = direction(self.center, target)
            if dist <= a["range"]:
                self.state, self.timer, self.strike_dir = "windup", a["windup"], dir_
            else:
                self._step_towards(dt, room, target, self.speed)
        elif self.state == "windup":
            self.timer -= dt
            if self.timer <= 0:
                self.state, self.timer = "strike", self.STRIKE_TIME
        elif self.state == "strike":
            self.timer -= dt
            if self.timer <= 0:
                self.state, self.timer = "cooldown", a["cooldown"]
        elif self.state == "cooldown":
            self.timer -= dt
            if self.timer <= 0:
                self.state = "chase"

    def draw(self, surface):
        import pygame
        h = self.SIZE
        pos = (self.x - h / 2, self.y - h / 2)
        try:
            from src.systems.assets import get_image
            img = get_image(self.sprite, (h, h))
            surface.blit(img, pos)
        except ImportError:
            pygame.draw.rect(surface, (200, 60, 60), self.rect)
        if self.hurt_timer > 0:
            pygame.draw.rect(surface, (255, 255, 255), self.rect, 2)
        if self.state == "windup":
            pygame.draw.circle(surface, (255, 200, 0), (int(self.x), int(self.y - h)), 4)
