import bomb
import character
import config


# RFCT NEEDED
class Player(character.Character):
    lives = 3
    score = 0
    current_bomb = 1
    max_bombs = 1
    power = 1  # Bomb player
    speed = 1  # Player movemnt speed

    def __init__(self, name, image_name, id, point):
        character.Character.__init__(self, name, "players/" + image_name, point)
        self.c = config.Config()
        self.id = id
        self.instance_of = "player"

    # Reset all stats if death is true
    def reset(self, death):
        character.Character.reset(self, True)
        if death:
            self.current_bomb = self.max_bombs = 1
            self.power = 1
            self.speed = 1

    def deploy_bomb(self):
        if self.current_bomb > 0:
            self.current_bomb -= 1
            return bomb.Bomb(self)
        return None

    def gain_power(self, power):
        if power == self.c.BOMB_UP:
            self.current_bomb += 1
            self.max_bombs += 1
        elif power == self.c.POWER_UP:
            self.power += 1

    def set_score(self, score):
        self.score += score
        if self.score < 0:
            self.score = 0

    # RFCT this was a bad idea
    def lose_life_and_game_over(self):
        self.lives -= 1
        return self.lives <= 0
