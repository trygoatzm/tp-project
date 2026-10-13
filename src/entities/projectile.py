import math


def rects_overlap(a, b):
    ax, ay, aw, ah = tuple(a)
    bx, by, bw, bh = tuple(b)
    return ax < bx + bw and bx < ax + aw and ay < by + bh and by < ay + ah


class Projectile:
    def __init__(self, x, y, vx, vy, damage=1, owner="player", radius=4, lifetime=2.0):
        if owner not in ("player", "enemy"):
            raise ValueError("owner должен быть 'player' или 'enemy'")
        self.x, self.y = float(x), float(y)
        self.vx, self.vy = float(vx), float(vy)
        self.damage = damage
        self.owner = owner
        self.radius = radius
        self.lifetime = lifetime
        self.alive = True

    @classmethod
    def aimed(cls, x, y, angle_deg, speed, **kw):
        a = math.radians(angle_deg)
        return cls(x, y, math.cos(a) * speed, math.sin(a) * speed, **kw)

    @property
    def rect(self):
        r = self.radius
        return (self.x - r, self.y - r, 2 * r, 2 * r)

    def update(self, dt, room=None):
        if not self.alive:
            return
        self.x += self.vx * dt
        self.y += self.vy * dt
        self.lifetime -= dt
        if self.lifetime <= 0 or (room is not None and room.blocked(self.rect)):
            self.alive = False

    def draw(self, surface):
        import pygame
        color = (255, 230, 90) if self.owner == "player" else (255, 90, 90)
        pygame.draw.circle(surface, color, (int(self.x), int(self.y)), self.radius)
