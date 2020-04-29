import config
import highscore
import pygame
import game
import sys


class TitleScreen():

    def __init__(self):
        self.c = config.Config()
        exit_main = False

        while not exit_main:
            pygame.init()
            self.screen = pygame.display.set_mode((1024, 768))
            pygame.display.set_caption("Bomberman")

            image_path = self.c.IMAGE_PATH + "titlescreen.png"
            img = pygame.image.load(image_path).convert()
            self.screen.blit(img, (0, 0))

            pygame.mixer.music.load(self.c.AUDIO_PATH + "title.mid")
            pygame.mixer.music.play()

            clock = pygame.time.Clock()
            pygame.mouse.set_visible(True)
            pygame.display.flip()
            user_interacted = False

            while not user_interacted:
                clock.tick(self.c.FPS)

                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        user_interacted = True
                        exit_main = True
                        pygame.quit()
                    elif event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_ESCAPE:
                            user_interacted = True
                            exit_main = True
                            pygame.quit()
                    elif event.type == pygame.MOUSEBUTTONDOWN:
                        if self.within_boundary(25, 250, 500, 540):
                            user_interacted = True
                            self.single_player()  # Single Player game clicked
                        elif self.within_boundary(25, 240, 605, 645):
                            user_interacted = True
                            self.instructions()  # Multiplayer game clicked
                        elif self.within_boundary(25, 240, 655, 700):
                            user_interacted = True
                            self.high_scores()  # High Scores clicked
                        elif self.within_boundary(25, 105, 705, 745):
                            user_interacted = True
                            exit_main = True
                            pygame.quit()  # Exit clicked

    def within_boundary(self, x1, x2, y1, y2):
        if x1 <= pygame.mouse.get_pos()[0] <= x2 and y1 <= pygame.mouse.get_pos()[1] <= y2:
            return True
        return False

    def single_player(self):
        game.Game(self.c.SINGLE)

    def multiplayer(self):
        game.Game(self.c.MULTI)

    def instructions(self):
        print("Instructions clicked!")

    def high_scores(self):
        high = highscore.Highscore()
        high.display_score()

    def clear_background(self):
        bg = pygame.Surface(self.screen.get_size())
        bg = bg.convert()
        bg.fill((0, 0, 0))
        self.blit(bg, (0, 0))


if __name__ == "__main__":
    title = TitleScreen()
