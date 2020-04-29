import config
import pygame


class Character(pygame.sprite.Sprite):
    lives = 1
    speed = 1

    def __init__(self, name, image_name, point):
        pygame.sprite.Sprite.__init__(self)
        self.c = config.Config()
        self.name = name
        self.image_name = image_name
        self.s_position = point
        self.reset(True)

    def reset(self, bool):
        self.get_image('down')
        self.position = self.image.get_rect()
        self.move(self.s_position)

    def get_image(self, direction):
        image_path = self.c.IMAGE_PATH + self.image_name + direction + ".png"
        self.image = pygame.image.load(image_path).convert()

    def update(self, *args):
        print("=D")

    def movement(self, key):
        c = config.Config()

        if key == pygame.K_UP:
            self.get_image('up')
            return [0, -1 * c.TILE_SIZE]
        elif key == pygame.K_DOWN:
            self.get_image('down')
            return [0, c.TILE_SIZE]
        elif key == pygame.K_LEFT:
            self.get_image('left')
            return [-1 * c.TILE_SIZE, 0]
        elif key == pygame.K_RIGHT:
            self.get_image('right')
            return [c.TILE_SIZE, 0]

    def move(self, point):
        self.old = self.position
        self.position = self.position.move(point)
