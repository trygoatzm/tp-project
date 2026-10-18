import pygame
from src.core.scene_manager import Scene


class MenuScene(Scene):
    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                self.game.scenes.change("game")
            elif event.key == pygame.K_ESCAPE:
                self.game.quit()

    def draw(self, surface):
        font = pygame.font.Font(None, 48)
        surface.blit(font.render("MENU: Enter - play, Esc - exit", True, (255, 255, 255)), (40, 40))
