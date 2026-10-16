"""Состояние игры. Владелец: архитектор.
Не зависит от pygame и от файлов — поэтому тестируется без окна.
"""
from src import settings


class GameState:
    """Единственный источник правды: здоровье, прогресс, смерти.

    levels — список уровней; каждый уровень — список id комнат по порядку.
    Пример: [["l1_entrance", "l1_battle", "l1_boss"], ["l2_entrance", ...]]
    """

    def __init__(self, levels):
        if not levels or any(not rooms for rooms in levels):
            raise ValueError("levels должен содержать хотя бы одну комнату в каждом уровне")
        self.levels = levels
        self.reset()

    # ---------- сброс ----------
    def reset(self):
        self.max_health = settings.PLAYER_MAX_HEALTH
        self.health = self.max_health
        self.level_index = 0
        self.room_index = 0
        self.deaths = 0

    # ---------- чтение ----------
    @property
    def current_room_id(self):
        return self.levels[self.level_index][self.room_index]

    @property
    def is_alive(self):
        return self.health > 0

    @property
    def red_diploma(self):
        return self.deaths <= settings.RED_DIPLOMA_MAX_DEATHS

    # ---------- здоровье ----------
    def damage(self, amount=1):
        """Отнять здоровье. Возвращает True, если герой умер от этого удара."""
        if amount < 0:
            raise ValueError("amount должен быть >= 0")
        if self.health <= 0:
            return False
        self.health = max(0, self.health - amount)
        return self.health == 0

    def heal(self, amount=1):
        if amount < 0:
            raise ValueError("amount должен быть >= 0")
        self.health = min(self.max_health, self.health + amount)

    # ---------- смерть ----------
    def register_death(self):
        """Вызывать ОДИН раз при смерти: +1 к счётчику, здоровье полное.
        Прогресс не трогаем: перезапускается текущая комната."""
        self.deaths += 1
        self.health = self.max_health

    # ---------- прогресс ----------
    def advance_room(self):
        """Перейти дальше. Возвращает 'room' | 'level' | 'game_end'."""
        if self.room_index + 1 < len(self.levels[self.level_index]):
            self.room_index += 1
            return "room"
        if self.level_index + 1 < len(self.levels):
            self.level_index += 1
            self.room_index = 0
            return "level"
        return "game_end"
