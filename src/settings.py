SCREEN_W = 960
SCREEN_H = 540
FPS = 60
TITLE = "Диплом любой ценой"

from pathlib import Path

SCREEN_W = 960
SCREEN_H = 540
FPS = 60
TITLE = "Диплом любой ценой"

TILE = 30
ROOM_W_TILES = SCREEN_W // TILE
ROOM_H_TILES = SCREEN_H // TILE

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
ASSETS_DIR = BASE_DIR / "assets"

PLAYER_MAX_HEALTH = 5
PLAYER_SPEED = 220
INVULN_TIME = 1.0

RED_DIPLOMA_MAX_DEATHS = 0
