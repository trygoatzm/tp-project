import pygame

from src.ui.text import draw_text

HEART_FULL = (220, 50, 70)
HEART_EMPTY = (70, 40, 50)
BAR_BG = (60, 20, 20)
BAR_FG = (200, 40, 40)
BAR_BORDER = (230, 230, 240)
HINT = (255, 230, 120)
SHADOW = (0, 0, 0)


def _heart(surface, color, x, y, size=11):
    r = size // 2 + 1
    pygame.draw.circle(surface, color, (x - r + 1, y - 2), r)
    pygame.draw.circle(surface, color, (x + r - 1, y - 2), r)
    pygame.draw.polygon(surface, color, [(x - size, y), (x + size, y), (x, y + size)])


def _text_shadow(surface, text, pos, size, color, center=False):
    draw_text(surface, text, (pos[0] + 2, pos[1] + 2), size, SHADOW, center=center)
    draw_text(surface, text, pos, size, color, center=center)


def draw_hud(surface, state, enemies):
    for i in range(state.max_health):
        color = HEART_FULL if i < state.health else HEART_EMPTY
        _heart(surface, color, 40 + i * 30, 40)

    _text_shadow(surface, f"Смертей: {state.deaths}", (28, 62), 20, (255, 255, 255))

    for e in enemies:
        if e.alive and e.kind == "boss":
            w, h = 400, 14
            x, y = 480 - w // 2, 44
            ratio = max(0.0, min(1.0, e.hp / e.max_hp)) if e.max_hp else 0.0
            pygame.draw.rect(surface, BAR_BG, (x, y, w, h))
            pygame.draw.rect(surface, BAR_FG, (x, y, int(w * ratio), h))
            pygame.draw.rect(surface, BAR_BORDER, (x, y, w, h), 2)
            _text_shadow(surface, e.name, (480, 28), 20, (255, 255, 255), center=True)
            break


def draw_hint(surface, text):
    _text_shadow(surface, text, (480, 500), 22, HINT, center=True)
