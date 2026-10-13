"""Главный цикл"""
import pygame

from src import settings
from src.core.scene_manager import SceneManager
from src.scenes.menu_scene import MenuScene
from src.scenes.game_scene import GameScene
from src.scenes.end_scene import EndScene


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((settings.SCREEN_W, settings.SCREEN_H))
        pygame.display.set_caption(settings.TITLE)
        self.clock = pygame.time.Clock()
        self.running = True
        self.scenes = SceneManager(self)
        self.scenes.register("menu", MenuScene(self))
        self.scenes.register("game", GameScene(self))
        self.scenes.register("end", EndScene(self))

    def quit(self):
        self.running = False

    def step(self, dt):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.quit()
            elif self.scenes.current:
                self.scenes.current.handle_event(event)
        if self.scenes.current:
            self.scenes.current.update(dt)
            self.screen.fill((20, 20, 30))
            self.scenes.current.draw(self.screen)
        pygame.display.flip()

    def run(self):
        while self.running:
            dt = self.clock.tick(settings.FPS) / 1000.0
            self.step(dt)
        pygame.quit()