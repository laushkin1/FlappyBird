import pygame
from random import randint

from load import LoadFile
from settings import SCREEN_WIDTH

class Pipe(pygame.sprite.Sprite):
    def __init__(self, speed, rotate=False, xy=None) -> None:
        super().__init__()
        self.speed = speed
        self.rotate = rotate

        load = LoadFile()

        if self.speed > 10:
            self.pipe = load.pipe(rotate=self.rotate, red=True)
        else:
            self.pipe = load.pipe(rotate=self.rotate)

        if xy is None:
            self.x = randint(SCREEN_WIDTH, SCREEN_WIDTH+100)
            self.y = randint(100, 500)
        else:
            self.x, self.y = xy

        self.image = self.pipe
        if rotate:
            self.rect = self.image.get_rect(midbottom = (self.x, self.y))
        else:
            self.rect = self.image.get_rect(midtop = (self.x, self.y+300))


    def destroy(self):
        if self.rect.x <= -100:
            self.kill()

    def update(self):
        self.rect.x -= self.speed
        self.destroy()

