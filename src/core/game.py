import pygame

from src import settings
from src.core.scene_manager import SceneManager
from src.scenes.menu_scene import MenuScene
from src.scenes.game_scene import GameScene
from src.scenes.end_scene import EndScene


def open_window(fullscreen):
    """Окно 960x540, растянутое на весь экран с сохранением пропорций (SCALED). F11 переключает режим."""
    size = (settings.SCREEN_W, settings.SCREEN_H)
    flags = pygame.SCALED | (pygame.FULLSCREEN if fullscreen else 0)
    try:
        return pygame.display.set_mode(size, flags)
    except pygame.error:
        return pygame.display.set_mode(size)


class Game:
    def __init__(self):
        pygame.init()
        self.screen = open_window(getattr(settings, "FULLSCREEN", True))
        pygame.display.set_caption(settings.TITLE)
        self.clock = pygame.time.Clock()
        self.running = True
        self.scenes = SceneManager(self)
        self.scenes.register("menu", MenuScene(self))
        self.scenes.register("game", GameScene(self))
        self.scenes.register("end", EndScene(self))

    def quit(self):
        self.running = False

    def toggle_fullscreen(self):
        try:
            pygame.display.toggle_fullscreen()
        except pygame.error:
            pass

    def step(self, dt):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.quit()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_F11:
                self.toggle_fullscreen()
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
