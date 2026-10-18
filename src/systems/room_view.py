import pygame
from src import settings
from src.systems.assets import get_image

WALL_COLOR = (90, 90, 100)
DOOR_CLOSED = (170, 60, 60)
DOOR_OPEN = (60, 170, 90)
HEAL_COLOR = (80, 220, 120)


def draw_room(surface, room):
    surface.blit(get_image(room.background, room.size_px), (0, 0))
    for w in room.walls:
        pygame.draw.rect(surface, WALL_COLOR, w)
    if room.door is not None:
        pygame.draw.rect(surface, DOOR_OPEN if room.door_open else DOOR_CLOSED, room.door)
    r = settings.TILE // 3
    for kind, (cx, cy), _ in room.pickups:
        pygame.draw.circle(surface, HEAL_COLOR, (cx, cy), r)