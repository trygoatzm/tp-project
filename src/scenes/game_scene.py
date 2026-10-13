"""Игровой экран. Заглушка тимлида; наполняют остальные роли."""
import pygame
from src.core.scene_manager import Scene


class GameScene(Scene):
    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.game.scenes.change("menu")
            elif event.key == pygame.K_e:
                self.game.scenes.change("end", deaths=0)

    def draw(self, surface):
        font = pygame.font.Font(None, 48)
        surface.blit(font.render("GAME: Esc - menu, E - end", True, (255, 255, 255)), (40, 40))