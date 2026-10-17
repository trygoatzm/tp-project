"""Игровой экран. Заглушка тимлида; наполняют остальные роли."""
import pygame
from src.core.scene_manager import Scene
from src.entities.player import Player
from src.systems.combat import CombatSystem, read_controls

class GameScene(Scene):
    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.game.scenes.change("menu")
            elif event.key == pygame.K_e:
                self.game.scenes.change("end", deaths=0)
    def on_enter(self):
        self.player = Player(self.room.player_spawn) 
        self.combat = CombatSystem()
    def update(self, dt):
        move, aim, shooting = read_controls()
        self.combat.add(self.player.update(dt, self.room, move, aim, shooting))
        events = self.combat.update(dt, self.room, self.player, self.enemies, self.state)
        
        if "player_dead" in events:
            self.state.register_death()
            self.reload_room()

    def draw(self, surface):
        font = pygame.font.Font(None, 48)
        surface.blit(font.render("GAME: Esc - menu, E - end", True, (255, 255, 255)), (40, 40))
    def reload_room(self):
        pass