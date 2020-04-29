import config
import pygame


class Music():

    def __init__(self):
        self.c = config.Config()

    def play_music(self, mode):
        if mode == self.c.SINGLE:
            music = "leveltheme.mid"
        elif mode == self.c.MULTI:
            music = "multiplayer.mid"

        pygame.mixer.music.load(self.c.AUDIO_PATH + music)
        pygame.mixer.music.play(-1)

    def play_sound(self, type):
        if type == "bomb":
            sound = "blast_02.wav"
        elif type == "power up":
            sound = "ping_01.wav"
        elif type == "victory":
            sound = "stage_clear.mid"

        pygame.mixer.music.load(self.c.AUDIO_PATH + sound)
        pygame.mixer.music.play()
