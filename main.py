import pygame

from scene import(
    NewGame,
    MainGame,
    GameOver,
    GameStateManager
)

from settings import (
    SCREEN_WIDTH, 
    SCREEN_HEIGHT,
    FPS,
    WINDOW_NAME,
)


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

