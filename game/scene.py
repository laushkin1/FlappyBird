import pygame
import sys
from random import choice

from game.player import Player
from game.load import LoadFile
from game.pipe import Pipe
from game.sound import Sounds
from game.settings import SCALE, SPEED, SCREEN_WIDTH, SCREEN_HEIGHT


class BaseScene():

    score = 0
    pipe_group_stop = pygame.sprite.Group()
    night = False
    
    player = pygame.sprite.GroupSingle()
    
    def __init__(self) -> None:
        self.display = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.gameStateManager = GameStateManager('new_game')
        BaseScene.player.add(Player(choice(['blue', 'red', 'yellow'])))

        self.loadFile = LoadFile()
        self.background_day = self.loadFile.background()
        self.background_night = self.loadFile.background(False)
        self.background_base = self.loadFile.base()
        self.numbers = self.loadFile.numbers()

        self.soundFile = Sounds()
        self.point_sound = self.soundFile.point()
        self.hit_sound = self.soundFile.hit()
        self.die_sound = self.soundFile.die()

        self.base_pos_x = 0
        self.base_pos_y = SCREEN_HEIGHT-(75*SCALE)

        self.speed = SPEED


        self.pipes = None
        self.bird_xy = (33*SCALE, 100*SCALE)
        self.birdimg = self.player.sprite.image

    def set_param(self, display, gameStateManager):
        self.display = display
        self.gameStateManager = gameStateManager

    def run(self):
        pass

    def check_quit_event(self, event):
        if event.type == pygame.QUIT or (
            event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE
        ):
            pygame.quit()
            sys.exit()


    def move_base(self):
        self.base_pos_x -= int(self.speed)
        if self.base_pos_x <= -336*SCALE:
            self.base_pos_x = 0

        self.display.blit(self.background_base, (self.base_pos_x, self.base_pos_y))
        self.display.blit(self.background_base, (self.base_pos_x+(336*SCALE), self.base_pos_y))


    def show_score(self):
        if BaseScene.score < 99:
            if BaseScene.score <= 9:
                self.numbers_rect = self.numbers[0].get_rect(center=(self.display.get_width()/2, 50*SCALE))
                self.display.blit(self.numbers[int(BaseScene.score)], self.numbers_rect)
            else:
                self.numbers_rect = self.numbers[0].get_rect(center=(self.display.get_width()/2-(12*SCALE), 50*SCALE))
                self.display.blit(self.numbers[int(BaseScene.score/10)], self.numbers_rect)
                self.numbers_rect = self.numbers[0].get_rect(center=(self.display.get_width()/2+(12*SCALE), 50*SCALE))
                self.display.blit(self.numbers[int(BaseScene.score-int(BaseScene.score/10)*10)], self.numbers_rect)
        else:
                self.numbers_rect = self.numbers[0].get_rect(center=(self.display.get_width()/2-(12*SCALE), 50*SCALE))
                self.display.blit(self.numbers[9], self.numbers_rect)
                self.numbers_rect = self.numbers[0].get_rect(center=(self.display.get_width()/2+(12*SCALE), 50*SCALE))
                self.display.blit(self.numbers[9], self.numbers_rect)


class NewGame(BaseScene):
    def __init__(self) -> None:
        super().__init__()
        self.message = self.loadFile.message()
        self.speed = int(SPEED/2)

        self.fly_timer = pygame.USEREVENT + 1
        pygame.time.set_timer(self.fly_timer, 1000)
        self.up = True

    def my_events(self):
        for event in pygame.event.get():
            self.check_quit_event(event)
            
            if (event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE) or \
                (event.type == pygame.MOUSEBUTTONDOWN and pygame.mouse.get_pressed()[0]):
                self.run_game = False
                self.new_base_game()
                self.player.sprite.player_jump()
                self.gameStateManager.set_state('main_game')

            if event.type == self.fly_timer:
                self.up = False if self.up else True
                    
    def run(self):
        self.my_events()

        self.display.blit(self.background_day, (0, 0))
        self.player.draw(self.display)
        if self.up: self.player.sprite.rect.y -= 1
        else: self.player.sprite.rect.y += 1
        self.player.sprite.animation()
        self.display.blit(self.message, (52*SCALE, 70*SCALE))
        self.move_base()

    def new_base_game(self):
        BaseScene.score = 0
        BaseScene.night = False


class MainGame(BaseScene):
    def __init__(self) -> None:
        super().__init__()

        # Pipe timer
        self.pipe_group = pygame.sprite.Group()
        self.pipe_timer = pygame.USEREVENT + 2
        pygame.time.set_timer(self.pipe_timer, 625*SCALE+625)
        self.checked_pipes = set()

    def my_events(self):
        for event in pygame.event.get():
            self.check_quit_event(event)

            if event.type == self.pipe_timer:
                self.last_pipe = Pipe(int(self.speed))
                self.pipe_group.add(self.last_pipe)
                self.pipe_group.add(Pipe(int(self.speed), rotate=True, xy=(self.last_pipe.x, self.last_pipe.y)))
                BaseScene.pipe_group_stop.add(self.pipe_group)

            if (event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE) or \
                (event.type == pygame.MOUSEBUTTONDOWN and pygame.mouse.get_pressed()[0]):
                self.player.sprite.player_jump()

    def run(self):
        self.my_events()

        self.speed += 0.0005*SCALE

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
            if pipe.rect.x < (50*SCALE) and pipe not in self.checked_pipes:
                if self.check_height():
                    self.checked_pipes.add(pipe)
                    BaseScene.score += 0.5
                    self.point_sound.play()

    def check_height(self):
        if self.player.sprite.rect.bottom <= 0:
            Player.player_y = self.player.sprite.rect.y
            self.hit_sound.play()
            if Player.player_y < 400*SCALE:
                self.die_sound.play()
            self.new_game()
            self.gameStateManager.set_state('game_over')
            return False
        return True

    def collision(self):
        if pygame.sprite.spritecollide(self.player.sprite, self.pipe_group, False) or \
                                                    self.player.sprite.rect.bottom >= 425*SCALE:
            Player.player_y = self.player.sprite.rect.y
            self.hit_sound.play()
            if Player.player_y < 400*SCALE:
                self.die_sound.play()
            self.new_game()
            self.gameStateManager.set_state('game_over')
    
    def new_game(self):
        self.speed = SPEED
        self.pipe_group.empty()
        self.checked_pipes = set()
        self.player.sprite.new_game()


class GameOver(BaseScene):
    def __init__(self) -> None:
        super().__init__()
        self.game_over = self.loadFile.game_over()
        self.speed = 0

    def my_events(self):
        for event in pygame.event.get():
            self.check_quit_event(event)
            if (event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE) or \
                (event.type == pygame.MOUSEBUTTONDOWN and pygame.mouse.get_pressed()[0]):
                self.run_game = False
                self.group_empty()
                self.gameStateManager.set_state('new_game')
   
    def run(self):
        
        self.my_events()

        if BaseScene.night: self.display.blit(self.background_night, (0, 0))
        else: self.display.blit(self.background_day, (0, 0))

        BaseScene.pipe_group_stop.draw(self.display)
        self.move_base()

        img = pygame.transform.rotate(self.player.sprite.image, Player.player_angle)
        if Player.player_y > 410*SCALE:
            Player.player_y = 410*SCALE
        if Player.player_y < 410*SCALE:
            Player.player_y += 8*SCALE
            Player.player_angle -= 5

        self.display.blit(img, (33*SCALE, Player.player_y))

        self.show_score()

        self.display.blit(self.game_over, self.game_over.get_rect(center = (self.display.get_width()/2, 100*SCALE)))

    def group_empty(self):
        BaseScene.player.empty()
        BaseScene.pipe_group_stop.empty()
        BaseScene.player.add(Player(choice(['blue', 'red', 'yellow'])))


class GameStateManager:
    def __init__(self, currentState) -> None:
        self.currentState = currentState

    def get_state(self):
        return self.currentState

    def set_state(self, state):
        self.currentState = state

