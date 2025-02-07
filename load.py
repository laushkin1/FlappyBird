import pygame

from settings import SCALE

class LoadFile():
    def background(self, day = True):
        if day:
            return pygame.transform.scale_by(pygame.image.load('flappy-bird-assets/sprites/background-day.png').convert(), SCALE)
        return pygame.transform.scale_by(pygame.image.load('flappy-bird-assets/sprites/background-night.png').convert(), SCALE)

    def base(self):
        return pygame.transform.scale_by(pygame.image.load('flappy-bird-assets/sprites/base.png').convert(), SCALE)

    def pipe(self, rotate=False, red = False):
        if red and rotate:
            return pygame.transform.rotozoom(pygame.image.load('flappy-bird-assets/sprites/pipe-red.png').convert_alpha(), 180, SCALE)
        if rotate:
            return pygame.transform.rotozoom(pygame.image.load('flappy-bird-assets/sprites/pipe-green.png').convert_alpha(), 180, SCALE)
        if red:
            return pygame.transform.scale_by(pygame.image.load('flappy-bird-assets/sprites/pipe-red.png').convert_alpha(), SCALE)
        return pygame.transform.scale_by(pygame.image.load('flappy-bird-assets/sprites/pipe-green.png').convert_alpha(), SCALE)

    def birds(self, color='yellow'):
        bird_sprites = []
        bird_sprites.append(pygame.transform.scale_by(pygame.image.load('flappy-bird-assets/sprites/' + color + 'bird-downflap.png').convert_alpha(), SCALE))
        bird_sprites.append(pygame.transform.scale_by(pygame.image.load('flappy-bird-assets/sprites/' + color + 'bird-midflap.png').convert_alpha(), SCALE))
        bird_sprites.append(pygame.transform.scale_by(pygame.image.load('flappy-bird-assets/sprites/' + color + 'bird-upflap.png').convert_alpha(), SCALE))
        return bird_sprites

    def numbers(self):
        numers_list = []
        for i in range(10):
            numers_list.append(pygame.transform.scale_by(pygame.image.load('flappy-bird-assets/sprites/' + str(i) + '.png').convert_alpha(), SCALE))
        return numers_list

    def game_over(self):
        return pygame.transform.scale_by(pygame.image.load('flappy-bird-assets/sprites/gameover.png').convert_alpha(), SCALE)

    def message(self):
        return pygame.transform.scale_by(pygame.image.load('flappy-bird-assets/sprites/message.png').convert_alpha(), SCALE)

