import pygame

from src.core.scene_manager import Scene
#from src.systems import audio
from src.ui.text import draw_text


class MenuScene(Scene):
    ITEMS = ("Играть", "Выход")

    def on_enter(self, **kwargs):
        self.index = 0
        #audio.play_music("menu.ogg")

    def _rect(self, i):
        return pygame.Rect(360, 260 + i * 70, 240, 50)

    def _choose(self, i):
        if i == 0:
            self.game.scenes.change("game")
        else:
            self.game.quit()

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key in (pygame.K_UP, pygame.K_DOWN, pygame.K_w, pygame.K_s):
                step = 1 if event.key == pygame.K_DOWN else -1
                self.index = (self.index + step) % len(self.ITEMS)
            elif event.key in (pygame.K_RETURN, pygame.K_KP_ENTER):
                self._choose(self.index)
            elif event.key == pygame.K_m:
                #audio.toggle_music()
                pass
        elif event.type == pygame.MOUSEMOTION:
            for i in range(len(self.ITEMS)):
                if self._rect(i).collidepoint(event.pos):
                    self.index = i
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            for i in range(len(self.ITEMS)):
                if self._rect(i).collidepoint(event.pos):
                    self._choose(i)

    def draw(self, surface):
        draw_text(surface, "Диплом любой ценой", (480, 150), 56, center=True)
        for i, name in enumerate(self.ITEMS):
            r = self._rect(i)
            color = (70, 90, 160) if i == self.index else (40, 45, 70)
            pygame.draw.rect(surface, color, r, border_radius=8)
            draw_text(surface, name, r.center, 28, center=True)
        draw_text(surface, "↑/↓ — выбор, Enter — подтвердить, M — музыка",
                  (480, 480), 18, (150, 150, 165), center=True)