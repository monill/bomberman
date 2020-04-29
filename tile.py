import config
import pygame


class Tile(pygame.sprite.Sprite):

    def __init__(self, type):
        pygame.sprite.Sprite.__init__(self)
        self.c = config.Config()
        self.type = type

        self.bomb = None
        self.powerup = None

        self.set_power_up()
        self.set_attributes()

    def set_power_up(self):
        if self.type == self.c.BOMB_UP:
            self.powerup = self.c.BOMB_UP
            self.type = self.c.BRICK
        elif self.type == self.c.POWER_UP:
            self.powerup = self.c.POWER_UP
            self.type = self.c.BRICK

    def is_power_up(self):
        return self.type == self.c.POWER_UP or self.type == self.c.BOMB_UP
        # return self.type != self.c.GROUND & self.type != self.c.BRICK & self.type != self.c.WALL

    def set_attributes(self):
        if self.type == self.c.GROUND:
            self.passable = True
        elif self.type == self.c.BRICK:
            self.passable = False
            self.destroyable = True
        elif self.type == self.c.WALL:
            self.passable = False
            self.destroyable = False
        elif self.type == self.c.BOMB_UP or self.type == self.c.POWER_UP:
            self.passable = True
            self.destroyable = True

        self.image = pygame.image.load(self.c.IMAGE_PATH + "tiles/" + str(self.type) + ".png").convert()

    def destroy(self):
        if self.powerup != None:
            self.type = self.powerup
            self.powerup = None
        else:
            self.type = self.c.GROUND
        self.set_attributes()

    # RFCT
    def can_bomb_pass(self):
        if self.type == self.c.BOMB_UP or self.type == self.c.POWER_UP:
            return False
        return self.passable & (self.bomb == None)

    def can_pass(self):
        return self.passable & (self.bomb == None)

    def get_background(self):
        if self.bomb != None:
            return self.bomb.image
        return self.image

    def get_image(self):
        if self.bomb != None:
            return self.bomb.image
        return self.image

    def __str__(self):
        return str(self.type)
