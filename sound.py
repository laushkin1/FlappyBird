import pygame

from settings import VOLUME


class Sounds():
    def jump(self):
        s = pygame.mixer.Sound('flappy-bird-assets/audio/wing.wav')
        s.set_volume(VOLUME/100)
        return s

    def point(self):
        s = pygame.mixer.Sound('flappy-bird-assets/audio/point.wav')
        s.set_volume(VOLUME/100)
        return s

    def hit(self):
        s = pygame.mixer.Sound('flappy-bird-assets/audio/hit.wav')
        s.set_volume(VOLUME/100)
        return s

    def die(self):
        s = pygame.mixer.Sound('flappy-bird-assets/audio/die.wav')
        s.set_volume(VOLUME/100)
        return s

