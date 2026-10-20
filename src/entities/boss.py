import math

from src.entities.enemy import direction
from src.entities.projectile import Projectile


class Boss:
    SIZE = 56
    PROJECTILE_LIFETIME = 4.0
    PROJECTILE_RADIUS = 5
    DEFAULT_WINDUP = 0.5
    FIRST_ATTACK_DELAY = 1.5
    KEEP_DISTANCE = 150

    def __init__(self, data, pos):
        self.id = data["id"]
        self.name = data["name"]
        self.kind = data["kind"]
        self.sprite = data["sprite"]
        self.max_hp = data["hp"]
        self.hp = data["hp"]
        self.speed = data["speed"]
        self.contact_damage = data["contact_damage"]
        self.attacks = data["attacks"]
        self.x, self.y = float(pos[0]), float(pos[1])
        self.alive = True
        self.hurt_timer = 0.0
        self._projectiles = []
        self.state = "rest"
        self.timer = self.FIRST_ATTACK_DELAY
        self.attack_index = 0
        self.current = None
        self.dash_dir = (1.0, 0.0)

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
        if not self.alive or self.state != "dash":
            return None
        return (self.rect, self.current["damage"])

    def _move(self, room, dx, dy):
        h = self.SIZE / 2
        before = (self.x, self.y)
        nx, ny = room.slide((self.x - h, self.y - h, self.SIZE, self.SIZE), dx, dy)
        self.x, self.y = nx + h, ny + h
        return (self.x, self.y) != before

    def _fire_fan(self, target):
        atk = self.current
        (ux, uy), _ = direction(self.center, target)
        center_angle = math.degrees(math.atan2(uy, ux))
        count = max(1, int(atk["projectiles"]))
        spread = atk["spread_deg"]
        for i in range(count):
            offset = 0.0 if count == 1 else spread * (i / (count - 1) - 0.5)
            self._projectiles.append(Projectile.aimed(
                self.x, self.y, center_angle + offset, atk["speed"],
                damage=atk["damage"], owner="enemy",
                radius=self.PROJECTILE_RADIUS, lifetime=self.PROJECTILE_LIFETIME))

    def update(self, dt, room, target):
        if not self.alive:
            return
        self.hurt_timer = max(0.0, self.hurt_timer - dt)

        if self.state == "rest":
            self.timer -= dt
            dir_, dist = direction(self.center, target)
            if dist > self.KEEP_DISTANCE:
                self._move(room, dir_[0] * self.speed * dt, dir_[1] * self.speed * dt)
            if self.timer <= 0:
                self.current = self.attacks[self.attack_index % len(self.attacks)]
                self.attack_index += 1
                self.state = "windup"
                self.timer = self.current.get("windup", self.DEFAULT_WINDUP)
                self.dash_dir = dir_

        elif self.state == "windup":
            self.timer -= dt
            if self.timer <= 0:
                if self.current["type"] == "fan":
                    self._fire_fan(target)
                    self.state = "rest"
                    self.timer = self.current["cooldown"]
                else:
                    self.state = "dash"
                    self.timer = self.current["duration"]

        elif self.state == "dash":
            self.timer -= dt
            speed = self.current["speed"]
            moved = self._move(room, self.dash_dir[0] * speed * dt, self.dash_dir[1] * speed * dt)
            if self.timer <= 0 or not moved:
                self.state = "rest"
                self.timer = self.current["cooldown"]

    def draw(self, surface):
        import pygame
        h = self.SIZE
        pos = (self.x - h / 2, self.y - h / 2)
        try:
            from src.systems.assets import get_image
            surface.blit(get_image(self.sprite, (h, h)), pos)
        except ImportError:
            pygame.draw.rect(surface, (160, 30, 120), self.rect)
        if self.hurt_timer > 0:
            pygame.draw.rect(surface, (255, 255, 255), self.rect, 3)
        if self.state == "windup":
            pygame.draw.rect(surface, (255, 200, 0), self.rect, 3)
        elif self.state == "dash":
            pygame.draw.rect(surface, (255, 70, 70), self.rect, 3)
        bar_w = 120
        bx, by = self.x - bar_w / 2, self.y - h / 2 - 14
        pygame.draw.rect(surface, (40, 40, 40), (bx, by, bar_w, 7))
        pygame.draw.rect(surface, (210, 50, 50), (bx, by, bar_w * self.hp / self.max_hp, 7))
