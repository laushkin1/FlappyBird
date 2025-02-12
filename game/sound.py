import pygame
import os

from game.settings import VOLUME

assets_path = os.path.join(os.path.dirname(__file__), "flappy-bird-assets", "audio")


class Sounds:
    def jump(self):
        s = pygame.mixer.Sound(assets_path + "/wing.wav")
        s.set_volume(VOLUME / 100)
        return s

    def point(self):
        s = pygame.mixer.Sound(assets_path + "/point.wav")
        s.set_volume(VOLUME / 100)
        return s

    def hit(self):
        s = pygame.mixer.Sound(assets_path + "/hit.wav")
        s.set_volume(VOLUME / 100)
        return s

    def die(self):
        s = pygame.mixer.Sound(assets_path + "/die.wav")
        s.set_volume(VOLUME / 100)
        return s
