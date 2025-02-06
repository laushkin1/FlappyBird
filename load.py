import pygame

class LoadFile():
    def background(self, day = True):
        if day:
            return pygame.transform.scale2x(pygame.image.load('flappy-bird-assets/sprites/background-day.png').convert())
        return pygame.transform.scale2x(pygame.image.load('flappy-bird-assets/sprites/background-night.png').convert())

    def base(self):
        return pygame.transform.scale2x(pygame.image.load('flappy-bird-assets/sprites/base.png').convert())

    def pipe(self, rotate=False, red = False):
        if red and rotate:
            return pygame.transform.rotozoom(pygame.image.load('flappy-bird-assets/sprites/pipe-red.png').convert_alpha(), 180, 2)
        if rotate:
            return pygame.transform.rotozoom(pygame.image.load('flappy-bird-assets/sprites/pipe-green.png').convert_alpha(), 180, 2)
        if red:
            return pygame.transform.scale2x(pygame.image.load('flappy-bird-assets/sprites/pipe-red.png').convert_alpha())
        return pygame.transform.scale2x(pygame.image.load('flappy-bird-assets/sprites/pipe-green.png').convert_alpha())

    def birds(self, color='yellow'):
        bird_sprites = []
        bird_sprites.append(pygame.transform.scale2x(pygame.image.load('flappy-bird-assets/sprites/' + color + 'bird-downflap.png')))
        bird_sprites.append(pygame.transform.scale2x(pygame.image.load('flappy-bird-assets/sprites/' + color + 'bird-midflap.png')))
        bird_sprites.append(pygame.transform.scale2x(pygame.image.load('flappy-bird-assets/sprites/' + color + 'bird-upflap.png')))
        return bird_sprites

    def numbers(self):
        numers_list = []
        for i in range(10):
            numers_list.append(pygame.transform.scale2x(pygame.image.load('flappy-bird-assets/sprites/' + str(i) + '.png')))
        return numers_list

    def game_over(self):
        return pygame.transform.scale2x(pygame.image.load('flappy-bird-assets/sprites/gameover.png'))

    def message(self):
        return pygame.transform.scale2x(pygame.image.load('flappy-bird-assets/sprites/message.png'))

