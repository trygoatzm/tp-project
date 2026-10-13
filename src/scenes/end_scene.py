"""Финальный экран. Заглушка тимлида: диплом красный при 0 смертей, иначе синий."""
import pygame
from src.core.scene_manager import Scene


class EndScene(Scene):
    def on_enter(self, deaths=0, **kwargs):
        self.deaths = deaths

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
            self.game.scenes.change("menu")

    def draw(self, surface):
        color = (200, 30, 30) if self.deaths == 0 else (30, 60, 200)
        pygame.draw.rect(surface, color, (280, 150, 400, 240))
        font = pygame.font.Font(None, 40)
        surface.blit(font.render(f"Deaths: {self.deaths}. Enter - menu", True, (255, 255, 255)), (40, 40))