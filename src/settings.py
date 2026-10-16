"""Общие константы. Владелец: архитектор. Тимлид только создаёт заглушку в день 1."""
SCREEN_W = 960
SCREEN_H = 540
FPS = 60
TITLE = "Диплом любой ценой"

"""Общие константы. Владелец: архитектор.
ВАЖНО: имена SCREEN_W, SCREEN_H, FPS, TITLE уже используются каркасом тимлида — не переименовывать.
"""
from pathlib import Path

# --- экран ---
SCREEN_W = 960
SCREEN_H = 540
FPS = 60
TITLE = "Диплом любой ценой"

# --- сетка ---
TILE = 30                      # размер клетки в пикселях; 960/30 = 32 клетки, 540/30 = 18 клеток
ROOM_W_TILES = SCREEN_W // TILE
ROOM_H_TILES = SCREEN_H // TILE

# --- пути (всегда от корня проекта, а не от текущей папки) ---
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
ASSETS_DIR = BASE_DIR / "assets"

# --- игрок ---
PLAYER_MAX_HEALTH = 5          # жизней (сердец)
PLAYER_SPEED = 220             # пикселей в секунду
INVULN_TIME = 1.0              # секунд неуязвимости после удара

# --- диплом ---
RED_DIPLOMA_MAX_DEATHS = 0     # красный диплом, если смертей не больше этого числа
