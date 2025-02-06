import pygame

from load import LoadFile
from sound import Sounds
from settings import SCREEN_HEIGHT

class Player(pygame.sprite.Sprite):
    player_y = SCREEN_HEIGHT/2
    player_angle = 0
    def __init__(self, color) -> None:
        super().__init__()

        loadFile = LoadFile()
        self.birds = loadFile.birds(color)
        soundFile = Sounds()
        self.jump_sound = soundFile.jump()

        self.bird_indx = 0
        self.angle = 0

        self.gravity = -15
        self.image = self.birds[self.bird_indx]
        self.rect = self.image.get_rect(center = (100, SCREEN_HEIGHT/2))

    def animation(self):
        self.bird_indx += 0.2
        if self.bird_indx >= len(self.birds):
            self.bird_indx = 0
        self.image = self.birds[int(self.bird_indx)]

    def player_jump(self) -> None:
        self.jump_sound.play()
        self.gravity = -15

    def apply_gravity(self) -> None:
        self.gravity += 1
        if self.gravity <= 36:
            self.player_rotate(self.gravity*2.5)
        else: 
            self.player_rotate(90)
        self.rect.y += self.gravity

    def player_rotate(self, angle) -> None:
        self.angle = -angle
        self.image = pygame.transform.rotate(self.image, -angle)
        Player.player_angle = -angle
    
    def new_game(self):
        self.gravity = -15
        self.image = self.birds[0]
        self.rect = self.image.get_rect(center = (100, SCREEN_HEIGHT/2))

    def update(self):
        self.animation()
        self.apply_gravity()

