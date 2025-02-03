from os import pread
import pygame
import sys
from random import randint

from pygame.image import load


# settings.py file
SCREEN_WIDTH = 576
SCREEN_HEIGHT = 1024
FPS = 60
WINDOW_NAME = "Flappy Bird"
#

# load.py file
# import pygame

class LoadFile():
    def __init__(self) -> None:
        ...

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



#

# pipe.py file
# import pygame
# from load import LoadFile

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



#

# player.py file
# import pygame
# import settings # from settings import *
# from load import loadFile

class Player(pygame.sprite.Sprite):
    def __init__(self, color) -> None:
        super().__init__()

        loadFile = LoadFile()
        self.birds = loadFile.birds(color)

        self.bird_indx = 0
        self.angle = 0


        self.new_game()

    def animation(self):
        self.bird_indx += 0.2
        if self.bird_indx >= len(self.birds):
            self.bird_indx = 0
        self.image = self.birds[int(self.bird_indx)]


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

    
    def new_game(self):
        self.gravity = -15
        self.image = self.birds[0]
        self.rect = self.image.get_rect(center = (100, SCREEN_HEIGHT/2))



    def update(self):
        self.animation()
        self.apply_gravity()
#

# file scene.py
# import pygame
# from player import Player
# from load import loadFile
# from pipe import Pipe



colors = ['blue', 'red', 'yellow']
bird_color = colors[randint(0, 2)]
class BaseScene():

    score = 0
    pipe_group_stop = pygame.sprite.Group()
    player_y = 0
    player_angle = 0
    night = False

    def __init__(self) -> None:
        self.display = None
        self.gameStateManager = None

        self.player = pygame.sprite.GroupSingle()
        self.player.add(Player(bird_color))
        

        self.loadFile = LoadFile()
        self.background_day = self.loadFile.background()
        self.background_night = self.loadFile.background(False)
        self.background_base = self.loadFile.base()
        self.numbers = self.loadFile.numbers()

        self.base_pos_x = 0
        self.base_pos_y = SCREEN_HEIGHT-150

        self.speed = 5


        self.pipes = None
        self.bird_xy = (66, 200)
        self.birdimg = self.player.sprite.image

   # def game_over_param(self, pipes, bird_xy, birdimg):
   #     self.pipes = pipes
   #     self.bird_xy = bird_xy
   #     self.birdimg = birdimg

    def set_param(self, display, gameStateManager):
        self.display = display
        self.gameStateManager = gameStateManager


    def run(self):
        pass


    def check_quit_event(self, event):
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()


    def move_base(self):
        self.base_pos_x -= int(self.speed)
        if self.base_pos_x <= -672:
            self.base_pos_x = 0

        self.display.blit(self.background_base, (self.base_pos_x, self.base_pos_y))
        self.display.blit(self.background_base, (self.base_pos_x+672, self.base_pos_y))


    def show_score(self):
        if BaseScene.score < 99:
            if BaseScene.score <= 9:
                self.numbers_rect = self.numbers[0].get_rect(center=(self.display.get_width()/2, 100))
                self.display.blit(self.numbers[int(BaseScene.score)], self.numbers_rect)
            else:
                self.numbers_rect = self.numbers[0].get_rect(center=(self.display.get_width()/2-25, 100))
                self.display.blit(self.numbers[int(BaseScene.score/10)], self.numbers_rect)
                self.numbers_rect = self.numbers[0].get_rect(center=(self.display.get_width()/2+25, 100))
                self.display.blit(self.numbers[int(BaseScene.score-int(BaseScene.score/10)*10)], self.numbers_rect)
        else:
                self.numbers_rect = self.numbers[0].get_rect(center=(self.display.get_width()/2-25, 100))
                self.display.blit(self.numbers[9], self.numbers_rect)
                self.numbers_rect = self.numbers[0].get_rect(center=(self.display.get_width()/2+25, 100))
                self.display.blit(self.numbers[9], self.numbers_rect)






class MainGame(BaseScene):
    def __init__(self) -> None:
        super().__init__()

        # Pipe timer
        self.pipe_group = pygame.sprite.Group()
        self.pipe_timer = pygame.USEREVENT + 1
        self.pipe_timer_interval = 1500
        pygame.time.set_timer(self.pipe_timer, self.pipe_timer_interval)
        self.checked_pipes = set()  



    def my_events(self):
        for event in pygame.event.get():
            self.check_quit_event(event)

            if event.type == self.pipe_timer:
                self.last_pipe = Pipe(int(self.speed))
                self.pipe_group.add(self.last_pipe)
                self.pipe_group.add(Pipe(int(self.speed), rotate=True, xy=(self.last_pipe.x, self.last_pipe.y)))
                BaseScene.pipe_group_stop.add(self.pipe_group)

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.player.sprite.gravity = -15

            if event.type == pygame.MOUSEBUTTONDOWN:
                self.player.sprite.gravity = -15

    
    def run(self):

        self.my_events()

        self.speed += 0.001

        if self.speed > 10:
            BaseScene.night = True
            self.display.blit(self.background_night, (0, 0))
        else:
            self.display.blit(self.background_day, (0, 0))
        

        self.pipe_group.draw(self.display)
        self.pipe_group.update()

        self.move_base()

        self.player.draw(self.display)
        self.player.update()

        self.change_score()
        self.show_score()

        self.collision()

    def change_score(self):
        for pipe in self.pipe_group:
            if pipe.rect.x < 100 and pipe not in self.checked_pipes:
                BaseScene.score += 0.5
                self.checked_pipes.add(pipe)

                if self.player.sprite.rect.bottom <= 0:
                    self.new_game()
                    self.gameStateManager.set_state('game_over')
                    BaseScene.score = 0





    def collision(self):
        if pygame.sprite.spritecollide(self.player.sprite, self.pipe_group, False) or \
                                                    self.player.sprite.rect.bottom >= 850:
            
            BaseScene.player_y += self.player.sprite.rect.y
            self.new_game()
            self.gameStateManager.set_state('game_over')

    
    def new_game(self):
        self.speed = 5
        self.pipe_group.empty()
        self.checked_pipes = set()
        BaseScene.player_angle = self.player.sprite.angle
        self.player.sprite.new_game()



class GameOver(BaseScene):
    def __init__(self) -> None:
        super().__init__()
        self.game_over = self.loadFile.game_over()

    def my_events(self):
        for event in pygame.event.get():
            self.check_quit_event(event)

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.run_game = False
                    self.gameStateManager.set_state('new_game')

            if event.type == pygame.MOUSEBUTTONDOWN:
                self.run_game = False
                self.gameStateManager.set_state('new_game')

   
    def run(self):
        self.my_events()

        self.speed = 0


        if BaseScene.night:
            self.display.blit(self.background_night, (0, 0))
        else:
            self.display.blit(self.background_day, (0, 0))

        BaseScene.pipe_group_stop.draw(self.display)
        self.move_base()
        img = pygame.transform.rotate(self.player.sprite.image, BaseScene.player_angle)
        if BaseScene.player_y > 820:
            BaseScene.player_y = 820
        if BaseScene.player_y < 820:
            BaseScene.player_y += 15
            BaseScene.player_angle -= 5
            # if BaseScene.player_angle * -1 < 90:
            #     BaseScene.player_angle -= 5
            # else:
            #     BaseScene.player_angle = -90
        self.display.blit(img, (66, BaseScene.player_y))
        

        self.show_score()

        self.display.blit(self.game_over, self.game_over.get_rect(center = (self.display.get_width()/2, 200)))




class NewGame(BaseScene):
    def __init__(self) -> None:
        super().__init__()
        self.message = self.loadFile.message()

        self.fly_timer = pygame.USEREVENT + 2
        pygame.time.set_timer(self.fly_timer, 1000)
        self.up = True

    def my_events(self):
        for event in pygame.event.get():
            self.check_quit_event(event)

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.run_game = False
                    self.player.sprite.gravity = -15
                    BaseScene.score = 0
                    BaseScene.pipe_group_stop.empty()
                    BaseScene.player_y = 0
                    BaseScene.player_angle = 0
                    BaseScene.night = False
                    self.gameStateManager.set_state('main_game')

            if event.type == pygame.MOUSEBUTTONDOWN:
                self.run_game = False
                self.player.sprite.gravity = -15
                self.player.sprite.rect.y = 488
                BaseScene.score = 0
                BaseScene.pipe_group_stop.empty()
                BaseScene.player_y = 0
                BaseScene.player_angle = 0
                BaseScene.night = False
                self.gameStateManager.set_state('main_game')

            if event.type == self.fly_timer:
                self.up = False if self.up else True
                    

 

    def run(self):
        self.my_events()

        self.display.blit(self.background_day, (0, 0))
        self.player.draw(self.display)
        if self.up:
            self.player.sprite.rect.y -= 1
        else:
            self.player.sprite.rect.y += 1
        self.player.sprite.animation()
        self.display.blit(self.message, (105, 140))
        self.move_base()



class GameStateManager:
    def __init__(self, currentState) -> None:
        self.currentState = currentState

    def get_state(self):
        return self.currentState

    def set_state(self, state):
        self.currentState = state
 

#






class Game():
    pygame.init()
    pygame.display.set_caption(WINDOW_NAME)
    display = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    def __init__(self) -> None:
        self.clock = pygame.time.Clock() 
        self.display = Game.display
        
        self.gameStateManager = GameStateManager('new_game')

        self.new_game = NewGame()
        self.main_game = MainGame()
        self.game_over = GameOver()


        self.states = {
                'new_game': self.new_game,
                'main_game': self.main_game,
                'game_over': self.game_over
                }

        for scene in self.states:
            self.states[scene].set_param(self.display, self.gameStateManager)

    def run(self):
        while True:
            self.states[self.gameStateManager.get_state()].run()


            pygame.display.update()
            self.clock.tick(FPS)



if __name__ == "__main__":
    game = Game()
    game.run()

