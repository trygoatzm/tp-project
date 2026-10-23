import pygame
from src.core.scene_manager import Scene
from src.core.state import GameState
from src.entities.player import Player
from src.systems.ai import alive_count, spawn_all, update_all
from src.systems.combat import CombatSystem, read_controls
from src.systems.level_loader import load_levels, load_room
from src.systems.room_view import draw_room
from src.ui.hud import Hud

class GameScene(Scene):
    def on_enter(self, **kwargs):
        levels, _ = load_levels()
        self.state = GameState(levels)
        self.player = Player((0, 0))
        self.combat = CombatSystem()
        self.hud = Hud()
        self.debug = False
        self.reload_room()

    def reload_room(self):
        self.room = load_room(self.state.current_room_id)
        self.player.teleport(self.room.player_spawn)
        self.combat.clear()
        self.enemies = spawn_all(self.room)

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.game.scenes.change("menu")
            elif event.key == pygame.K_F1:
                self.debug = not self.debug

    def update(self, dt):
        move, aim, shooting = read_controls()
        self.combat.add(self.player.update(dt, self.room, move, aim, shooting))
        update_all(dt, self.room, self.enemies, self.player.center)
        events = self.combat.update(dt, self.room, self.player, self.enemies, self.state)
        self.hud.update(dt, self.state.health)

        self.room.set_enemies_alive(alive_count(self.enemies))
        for kind, amount in self.room.collect_pickups(self.player.rect):
            if kind == "heal":
                self.state.heal(amount)

        if "player_dead" in events:
            self.state.register_death()
            self.reload_room()
        elif self.room.exit_reached(self.player.rect):
            if self.state.advance_room() == "game_end":
                self.game.scenes.change("end", deaths=self.state.deaths)
            else:
                self.reload_room()

    def draw(self, surface):
        draw_room(surface, self.room, self.debug)
        actors = [e for e in self.enemies if e.alive] + [self.player]
        for actor in sorted(actors, key=lambda a: a.y):
            actor.draw(surface)
        self.combat.draw(surface)
        self.hud.draw(surface)
