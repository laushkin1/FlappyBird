import pygame
from random import randint


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

    def birds(self, blue=False, red=False):
        if blue:
            bird_sprites = []
            bird_sprites.append(pygame.transform.scale2x(pygame.image.load('flappy-bird-assets/sprites/bluebird-downflap.png')))
            bird_sprites.append(pygame.transform.scale2x(pygame.image.load('flappy-bird-assets/sprites/bluebird-midflap.png')))
            bird_sprites.append(pygame.transform.scale2x(pygame.image.load('flappy-bird-assets/sprites/bluebird-upflap.png')))
            return bird_sprites
        if red:
            bird_sprites = []
            bird_sprites.append(pygame.transform.scale2x(pygame.image.load('flappy-bird-assets/sprites/redbird-downflap.png')))
            bird_sprites.append(pygame.transform.scale2x(pygame.image.load('flappy-bird-assets/sprites/redbird-midflap.png')))
            bird_sprites.append(pygame.transform.scale2x(pygame.image.load('flappy-bird-assets/sprites/redbird-upflap.png')))
            return bird_sprites

        bird_sprites = []
        bird_sprites.append(pygame.transform.scale2x(pygame.image.load('flappy-bird-assets/sprites/yellowbird-downflap.png')))
        bird_sprites.append(pygame.transform.scale2x(pygame.image.load('flappy-bird-assets/sprites/yellowbird-midflap.png')))
        bird_sprites.append(pygame.transform.scale2x(pygame.image.load('flappy-bird-assets/sprites/yellowbird-upflap.png')))
        return bird_sprites


    def numbers(self):
        numers_list = []
        for i in range(10):
            numers_list.append(pygame.transform.scale2x(pygame.image.load('flappy-bird-assets/sprites/' + str(i) + '.png')))

        return numers_list



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
    def __init__(self) -> None:
        super().__init__()

        self.gravity = 0

        loadFile = LoadFile()
        self.birds = loadFile.birds()
        self.bird_indx = 0


        self.image = self.birds[self.bird_indx]
        self.rect = self.image.get_rect(center = (100, SCREEN_HEIGHT/2))

    def animation(self):
        self.bird_indx += 0.2
        if self.bird_indx >= len(self.birds):
            self.bird_indx = 0
        self.image = self.birds[int(self.bird_indx)]


    def apply_gravity(self) -> None:
        self.gravity += 1
        self.player_rotate(self.gravity*1.5)
        self.rect.y += self.gravity


    def player_input(self) -> None:
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            self.gravity = -15


    def player_rotate(self, angle) -> None:
        self.image = pygame.transform.rotate(self.image, -angle)

    
    def new_game(self):
        self.gravity = 0
        self.image = self.birds[0]
        self.rect = self.image.get_rect(center = (100, SCREEN_HEIGHT/2))


    def update(self):
        self.animation()
        self.apply_gravity()
        self.player_input()
#



display = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))


class Game():
    def __init__(self, display) -> None:
        self.display = display
        self.run_game = True
        self.clock = pygame.time.Clock() 

        # Files
        self.loadFile = LoadFile()
        self.background_day = self.loadFile.background()
        self.background_night = self.loadFile.background(False)
        self.background_base = self.loadFile.base()
        

        self.base_pos_x = 0
        self.base_pos_y = SCREEN_HEIGHT-150
        
        self.speed = 5
        self.score = 0
        self.checked_pipes = set()  

        self.pipe_group = pygame.sprite.Group()
        self.pipe_timer = pygame.USEREVENT + 1
        self.pipe_timer_interval = 1500
        pygame.time.set_timer(self.pipe_timer, self.pipe_timer_interval)

        # Player
        self.player = pygame.sprite.GroupSingle()
        self.player.add(Player())



    def run(self):
        pygame.init()
        while self.run_game:
            self.speed += 0.001
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.run_game = False

                if event.type == self.pipe_timer:
                    self.last_pipe = Pipe(int(self.speed))
                    self.pipe_group.add(self.last_pipe)
                    self.pipe_group.add(Pipe(int(self.speed), rotate=True, xy=(self.last_pipe.x, self.last_pipe.y)))

                    # if self.pipe_timer_interval < 2000:
                    #     self.pipe_timer_interval += 50
                    #     pygame.time.set_timer(self.pipe_timer, self.pipe_timer_interval)

            # Game Here

            self.display.fill('white')
            # Background
            if self.speed > 10:
                self.display.blit(self.background_night, (0, 0))
            else:
                self.display.blit(self.background_day, (0, 0))

            # Player
            self.player.draw(self.display)
            self.player.update()

            # Pipes
            self.pipe_group.draw(self.display)
            self.pipe_group.update()

            # Base
            self.move_base()

            # Score
            self.show_score()

            # collision
            self.collision()
        
            print(pygame.mouse.get_pos())
            pygame.display.update()
            self.clock.tick(FPS)

            # # # # # # # 

        pygame.quit()


    def move_base(self):
        self.base_pos_x -= int(self.speed)
        if self.base_pos_x <= -672:
            self.base_pos_x = 0

        self.display.blit(self.background_base, (self.base_pos_x, self.base_pos_y))
        self.display.blit(self.background_base, (self.base_pos_x+672, self.base_pos_y))


    def show_score(self):
        for pipe in self.pipe_group:
            if pipe.rect.x < 100 and pipe not in self.checked_pipes:
                self.score += 0.5
                self.checked_pipes.add(pipe)

                
        self.numbers = self.loadFile.numbers()
        if self.score < 99:
            if self.score <= 9:
                self.numbers_rect = self.numbers[0].get_rect(center=(self.display.get_width()/2, 100))
                self.display.blit(self.numbers[int(self.score)], self.numbers_rect)
            else:
                self.numbers_rect = self.numbers[0].get_rect(center=(self.display.get_width()/2-25, 100))
                self.display.blit(self.numbers[int(self.score/10)], self.numbers_rect)
                self.numbers_rect = self.numbers[0].get_rect(center=(self.display.get_width()/2+25, 100))
                self.display.blit(self.numbers[int(self.score-int(self.score/10)*10)], self.numbers_rect)
        else:
                self.numbers_rect = self.numbers[0].get_rect(center=(self.display.get_width()/2-25, 100))
                self.display.blit(self.numbers[9], self.numbers_rect)
                self.numbers_rect = self.numbers[0].get_rect(center=(self.display.get_width()/2+25, 100))
                self.display.blit(self.numbers[9], self.numbers_rect)


    
    def collision(self):
        if pygame.sprite.spritecollide(self.player.sprite, self.pipe_group, False) or \
                self.player.sprite.rect.bottom >= 880:
            self.speed = 5
            self.pipe_group.empty()
            self.player.sprite.new_game()
            self.score = 0
            self.checked_pipes = set()




if __name__ == "__main__":
    game = Game(display)
    game.run()

