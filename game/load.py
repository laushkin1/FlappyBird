import pygame
import os

from game.settings import SCALE

assets_path = os.path.join(os.path.dirname(__file__), "flappy-bird-assets", "sprites")


class LoadFile:
    def background(self, day=True):
        if day:
            return pygame.transform.scale_by(
                pygame.image.load(assets_path + "/background-day.png").convert(), SCALE
            )
        return pygame.transform.scale_by(
            pygame.image.load(assets_path + "/background-night.png").convert(), SCALE
        )

    def base(self):
        return pygame.transform.scale_by(
            pygame.image.load(assets_path + "/base.png").convert(), SCALE
        )

    def pipe(self, rotate=False, red=False):
        if red and rotate:
            return pygame.transform.rotozoom(
                pygame.image.load(assets_path + "/pipe-red.png").convert_alpha(),
                180,
                SCALE,
            )
        if rotate:
            return pygame.transform.rotozoom(
                pygame.image.load(assets_path + "/pipe-green.png").convert_alpha(),
                180,
                SCALE,
            )
        if red:
            return pygame.transform.scale_by(
                pygame.image.load(assets_path + "/pipe-red.png").convert_alpha(), SCALE
            )
        return pygame.transform.scale_by(
            pygame.image.load(assets_path + "/pipe-green.png").convert_alpha(), SCALE
        )

    def birds(self, color="yellow"):
        bird_sprites = []
        bird_sprites.append(
            pygame.transform.scale_by(
                pygame.image.load(
                    assets_path + "/" + color + "bird-downflap.png"
                ).convert_alpha(),
                SCALE,
            )
        )
        bird_sprites.append(
            pygame.transform.scale_by(
                pygame.image.load(
                    assets_path + "/" + color + "bird-midflap.png"
                ).convert_alpha(),
                SCALE,
            )
        )
        bird_sprites.append(
            pygame.transform.scale_by(
                pygame.image.load(
                    assets_path + "/" + color + "bird-upflap.png"
                ).convert_alpha(),
                SCALE,
            )
        )
        return bird_sprites

    def numbers(self):
        numers_list = []
        for i in range(10):
            numers_list.append(
                pygame.transform.scale_by(
                    pygame.image.load(
                        assets_path + "/" + str(i) + ".png"
                    ).convert_alpha(),
                    SCALE,
                )
            )
        return numers_list

    def game_over(self):
        return pygame.transform.scale_by(
            pygame.image.load(assets_path + "/gameover.png").convert_alpha(), SCALE
        )

    def message(self):
        return pygame.transform.scale_by(
            pygame.image.load(assets_path + "/message.png").convert_alpha(), SCALE
        )
