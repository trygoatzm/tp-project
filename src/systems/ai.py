"""Создание врагов из JSON и общие функции. Владелец: роль 5.
game_scene: enemies = spawn_all(room); room.set_enemies_alive(alive_count(enemies)).
"""
import json
from pathlib import Path

from src import settings
from src.entities.enemy import Enemy


def create_enemy(enemy_id, pos, data_dir=None):
    base = Path(data_dir) if data_dir else settings.DATA_DIR
    with open(base / "enemies" / f"{enemy_id}.json", encoding="utf-8") as f:
        data = json.load(f)
    if data["kind"] == "boss":
        from src.entities.boss import Boss  # boss.py появится позже (дни 7-8)
        return Boss(data, pos)
    return Enemy(data, pos)


def spawn_all(room, data_dir=None):
    """Список врагов по спавнам комнаты (room.enemy_spawns = [(id, (x, y)), ...])."""
    return [create_enemy(eid, pos, data_dir) for eid, pos in room.enemy_spawns]


def alive_count(enemies):
    return sum(1 for e in enemies if e.alive)


def update_all(dt, room, enemies, target):
    for e in enemies:
        e.update(dt, room, target)


def draw_all(surface, enemies):
    for e in enemies:
        if e.alive:
            e.draw(surface)
