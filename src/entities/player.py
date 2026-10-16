import math

from src import settings
from src.entities.projectile import Projectile


class Player:
    SIZE = 20
    SHOT_COOLDOWN = 0.30
    SHOT_SPEED = 520
    SHOT_DAMAGE = 1
    HAND = 14

    def __init__(self, pos):
        self.x, self.y = float(pos[0]), float(pos[1])
        self.aim = (1.0, 0.0)
        self.cooldown = 0.0
        self.invuln = 0.0

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

    def update(self, dt, room, move, aim_point, shooting):
        self.cooldown = max(0.0, self.cooldown - dt)
        self.invuln = max(0.0, self.invuln - dt)

        mx, my = move
        length = math.hypot(mx, my)
        if length > 1:
            mx, my = mx / length, my / length
        if mx or my:
            h = self.SIZE / 2
            nx, ny = room.slide((self.x - h, self.y - h, self.SIZE, self.SIZE),
                                mx * settings.PLAYER_SPEED * dt, my * settings.PLAYER_SPEED * dt)
            self.x, self.y = nx + h, ny + h

        ax, ay = aim_point[0] - self.x, aim_point[1] - self.y
        d = math.hypot(ax, ay)
        if d > 1e-6:
            self.aim = (ax / d, ay / d)

        shots = []
        if shooting and self.cooldown == 0.0:
            self.cooldown = self.SHOT_COOLDOWN
            ux, uy = self.aim
            shots.append(Projectile(self.x + ux * self.HAND, self.y + uy * self.HAND,
                                    ux * self.SHOT_SPEED, uy * self.SHOT_SPEED,
                                    damage=self.SHOT_DAMAGE, owner="player"))
        return shots

    def take_hit(self, amount, state):
        if self.invuln > 0 or not state.is_alive:
            return "ignored"
        died = state.damage(amount)
        self.invuln = settings.INVULN_TIME
        return "dead" if died else "hit"

    def draw(self, surface):
        import pygame
        if not self.visible:
            return
        try:
            from src.systems.assets import get_image
            surface.blit(get_image("player_idle", (self.SIZE, self.SIZE)), (self.x - self.SIZE / 2, self.y - self.SIZE / 2))
        except ImportError:
            pygame.draw.rect(surface, (60, 200, 90), self.rect)
        hand = (int(self.x + self.aim[0] * self.HAND), int(self.y + self.aim[1] * self.HAND))
        pygame.draw.circle(surface, (240, 240, 240), hand, 3)
