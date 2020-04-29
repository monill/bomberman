import character
import pygame
import random


class Enemy(character.Character):

    def __init__(self, name, image_name, point):
        character.Character.__init__(self, name, "enemies/" + image_name, point)
        self.instance_of = "enemy"

    def next_move(self):
        ary = [pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT]
        return self.movement(ary[int(random.randrange(0, 4))])
