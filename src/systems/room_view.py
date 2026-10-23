import pygame
from src import settings
from src.systems.assets import get_image

WALL_COLOR = (90, 90, 100)
DOOR_OPEN = (60, 170, 90)
DOOR_CLOSED = (170, 60, 60)
CLOSED_DOOR_ALPHA = 150
HEAL_COLOR = (80, 220, 120)
NPC_SIZE = 30


def draw_room(surface, room, debug=False):
    """Фон, закрытая дверь, лечилки и NPC. Стены нарисованы на фоне; серые прямоугольники только в режиме отладки."""
    surface.blit(get_image(room.background, room.size_px), (0, 0))
    if debug:
        for w in room.walls:
            pygame.draw.rect(surface, WALL_COLOR, w, 1)
        if room.door is not None:
            pygame.draw.rect(surface, DOOR_OPEN if room.door_open else DOOR_CLOSED, room.door, 2)
    elif room.door is not None and not room.door_open:
        x, y, w, h = room.door
        cover = pygame.Surface((w, h), pygame.SRCALPHA)
        cover.fill((*DOOR_CLOSED, CLOSED_DOOR_ALPHA))
        surface.blit(cover, (x, y))
    r = settings.TILE // 3
    for kind, (cx, cy), _ in room.pickups:
        pygame.draw.circle(surface, HEAL_COLOR, (cx, cy), r)
    for npc_id, (cx, cy), _ in room.npcs:
        image = get_image(f"npc_{npc_id}", (NPC_SIZE, NPC_SIZE))
        surface.blit(image, (cx - NPC_SIZE // 2, cy - NPC_SIZE // 2))
