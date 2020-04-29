import config
import pygame


class Highscore():

    def __init__(self):
        self.c = config.Config()
        self.reload_score_data()

    def reload_score_data(self):
        file = open(self.c.HIGHSCORES_PATH, 'r').readlines()

        self.scores = []
        row = 0
        for line in file:
            self.scores.append(int(line))

        # sort scores
        self.scores.sort()
        self.scores.reverse()

    def add_score(self, score):
        file = open(self.c.HIGHSCORES_PATH, 'a')
        file.write(str(score) + "\n")

    def display_score(self):
        pygame.init()
        self.screen = pygame.display.set_mode((self.c.WIDTH, self.c.HEIGHT))
        self.clear_background()

        index = 1
        self.print_text("Highscores", (375, 40))
        for score in self.scores:
            self.print_text("%d) %d" % (index, score), (40, 75 + 25 * index))
            index += 1
        pygame.display.flip()

        exit = False
        while not exit:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit = True
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    exit = True

    # RFCT - this method is in every class, make it a global
    def clear_background(self):
        bg = pygame.Surface(self.screen.get_size())
        bg = bg.convert()
        bg.fill((0, 0, 0))
        self.screen.blit(bg, (0, 0))

    # RFCT - this method is also in Game.py, make it global
    def print_text(self, text, point):
        font = pygame.font.Font("fonts/Lucida Console.ttf", 20)

        label = font.render(str(text) + '  ', True, (255, 255, 255), (0, 0, 0))
        textRect = label.get_rect()
        textRect.x = point[0]
        textRect.y = point[1]
        self.screen.blit(label, textRect)

    def print_scores(self):
        index = 1
        for score in self.scores:
            print("%d) %d" % (index, score))
            index += 1


if __name__ == "__main__":
    h = Highscore()
    # h.add_score(1000)
    # h.reload_score_data()
    # h.print_scores()
    h.display_score()
