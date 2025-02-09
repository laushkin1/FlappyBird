import pygame
from random import randint

from game.load import LoadFile
from game.settings import SCALE, SCREEN_WIDTH

class Pipe(pygame.sprite.Sprite):
    def __init__(self, speed, rotate=False, xy=None, night=False) -> None:
        super().__init__()
        self.speed = speed
        self.rotate = rotate

        load = LoadFile()

        if night:
            self.pipe = load.pipe(rotate=self.rotate, red=True)
        else:
            self.pipe = load.pipe(rotate=self.rotate)

        if xy is None:
            self.x = randint(SCREEN_WIDTH, SCREEN_WIDTH+(50*SCALE))
            self.y = randint(50, 250) * SCALE
        else:
            self.x, self.y = xy

        self.image = self.pipe
        if rotate:
            self.rect = self.image.get_rect(midbottom = (self.x, self.y))
        else:
            self.rect = self.image.get_rect(midtop = (self.x, self.y+(110*SCALE)))


    def destroy(self):
        if self.rect.x <= -50*SCALE:
            self.kill()

    def update(self):
        self.rect.x -= self.speed
        self.destroy()

