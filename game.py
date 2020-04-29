import os
import random
import sys
import time

import pygame

import board
import config
import enemy
import highscore
import music
import player

sys.path.append(os.path.split(sys.path[0])[0])


class Game():
    players = []
    enemies = []
    bombs = []
    reset_tiles = []
    stage = 1
    level = 1
    first_run = True
    exit_game = False
    game_is_active = False

    # Multiplayer data
    tcp_data = []
    sending_data = []
    last_tcp_call = 0
    p_hash = {}

    def __init__(self, mode):
        self.c = config.Config()
        self.highscores = highscore.Highscore()
        self.force_quit = False
        self.mode = mode

        pygame.init()
        self.screen = pygame.display.set_mode((self.c.WIDTH, self.c.HEIGHT), pygame.DOUBLEBUF)
        pygame.display.set_caption("Bomberman")

        # init preloader / join server
        if self.mode == self.c.MULTI:
            preloader = pygame.image.load(self.c.IMAGE_PATH + "loading.png").convert()
            self.blit(preloader, (0, 0))
            pygame.display.flip()
            self.join_game()

        # repeat for multiple levels
        while not self.exit_game:
            self.reset_game()
            self.clear_background()
            self.init_game()

        # launch highscores
        if not self.force_quit:
            self.highscores.reload_score_data()
            self.highscores.display_score()

    def join_game(self):
        self.client = TCPClient()

        # Choose server connection
        if self.c.LOCALHOST:
            self.client.connect("localhost", 6317)
        else:
            self.client.connect("localhost", 6317)

        self.id = random.randint(0, 1000000)  # Unique player ID
        self.client.send_data(["update", "user joined", str(self.id)])

        while True:
            self.tcp_data = self.client.wait_for_data()
            self.client.send_data(["update", None])
            print(self.tcp_data)
            self.init_multi_users()
            if self.tcp_data[-1] == "[SERVER]|START":
                break

    def get_multi_start_position(self, id):
        if id == 1:
            return (40, 40)
        elif id == 2:
            return (760, 40)
        elif id == 3:
            return (40, 600)
        elif id == 4:
            return (760, 600)

    def init_multi_self(self, data):
        d = data[-1].split("|")
        self.user = player.Player("Player " + d[0], "p_" + d[0] + "_", d[2], self.get_multi_start_position(d[0]))
        self.players.append(self.user)

    def init_multi_users(self):
        for element in self.tcp_data:
            ary = element.split("|")
            if ary[0] > self.last_tcp_call:
                # Manipulate
                if ary[1] == "JOIN":
                    p = player.Player("Player " + ary[0], "p_" + ary[0] + "_", ary[2],
                                      self.get_multi_start_position(ary[0]))
                    self.p_hash[ary[2]] = p
                    self.players.append(p)
                    self.last_tcp_call = ary[0]

    def tcp_update(self):
        data = self.client.check_for_data()

        if data:
            self.tcp_data = data
            print("-" * 20)
            # print(self.tcp_data)
            if self.sending_data == []:
                self.sending_data = ["update", None]
            self.client.send_data(self.sending_data)
            self.sending_data = []

    # RFCT
    # ary[3] = key 			ary[2] = user
    def manipulate_tcp_data(self):
        for d in self.tcp_data:
            ary = d.split("|")
            try:
                print(ary[0] + " " + str(self.last_tcp_call))

                if int(ary[0]) > int(self.last_tcp_call):
                    if str(ary[2]) != str(self.id):
                        if ary[1] == "MOVE":
                            point = self.p_hash[ary[2]].movement(int(ary[3]))
                            self.movement_helper(self.p_hash[ary[2]], point)
                    elif ary[1] == "BOMB":
                        self.deploy_bomb(self.p_hash[ary[2]])
                self.last_tcp_call = ary[0]
            except ValueError:
                print("skip")

    def reset_game(self):
        self.field = None
        self.enemies = []
        self.bombs = []
        self.reset_tiles = []

    def clear_background(self):
        bg = pygame.Surface(self.screen.get_size())
        bg = bg.convert()
        bg.fill((0, 0, 0))
        self.blit(bg, (0, 0))

    def init_game(self):
        if self.mode == self.c.SINGLE:
            self.print_text("Level %d-%d" % (self.stage, self.level), (40, 15))
            self.field = board.Board(self.stage, self.level)
            self.timer = 3 * 60 + 1
        elif self.mode == self.c.MULTI:
            self.print_text("Multiplayer", (40, 15))
            self.field = board.Board(0, 0)
            self.timer = 5 * 60 + 1

        self.draw_board()
        self.draw_interface()
        self.update_timer()

        # Players do not have to be reinitialized in single player after the first time
        if self.first_run:
            self.first_run = False
            self.init_players()
        else:
            self.reset_player_position(self.user, False)

        # No enemies in multiplayer
        if self.mode == self.c.SINGLE:
            self.init_enemies()

        # Music player
        mp = music.Music()
        mp.play_music(self.mode)

        self.run_game()

    def draw_board(self):
        for row in range(1, len(self.field.board) - 1):
            for col in range(1, len(self.field.board[row]) - 1):
                image = self.field.board[row][col].image
                # RFCT fix the mess
                position = self.field.board[row][col].image.get_rect().move(
                    (col * self.c.TILE_SIZE, row * self.c.TILE_SIZE))
                self.blit(image, position)

    def update_display_info(self):
        self.print_text(self.user.score, (65, 653))
        self.print_text(self.user.lives, (775, 653))
        self.print_text(self.user.max_bombs, (630, 653))
        self.print_text(self.user.power, (700, 653))

    def draw_interface(self):
        player = pygame.image.load(self.c.IMAGE_PATH + "screen/player.png").convert()
        life = pygame.image.load(self.c.IMAGE_PATH + "screen/life.png").convert()
        bomb = pygame.image.load(self.c.IMAGE_PATH + "screen/bomb.png").convert()
        power = pygame.image.load(self.c.IMAGE_PATH + "screen/power.png").convert()
        clock = pygame.image.load(self.c.IMAGE_PATH + "screen/clock.png").convert()

        self.blit(player, (40, 650))
        self.blit(clock, (365, 650))

        self.blit(bomb, (590, 647))
        self.blit(power, (670, 650))
        self.blit(life, (740, 652))

    def init_players(self):
        if self.mode == self.c.SINGLE:
            self.user = player.Player("Player 1", "p_1_", 0, (40, 40))
            self.players.append(self.user)
            self.blit(self.user.image, self.user.position)
        elif self.mode == self.c.MULTI:
            for p in self.players:
                if str(p.id) == str(self.id):
                    self.user = p
                self.blit(p.image, p.position)

    def init_enemies(self):
        # Generates 5 enemies
        for i in range(0, 5):
            while True:
                x = random.randint(6, self.field.width - 2) * 40
                y = random.randint(6, self.field.height - 2) * 40

                if self.field.get_tile((x, y)).can_pass():
                    break

            e = enemy.Enemy("Enemy", "e_%d_" % (random.randint(1, self.c.MAX_ENEMY_SPRITES)), (x, y))
            self.enemies.append(e)
            self.blit(e.image, e.position)

    def run_game(self):
        clock = pygame.time.Clock()
        pygame.time.set_timer(pygame.USEREVENT, 1000)
        pygame.time.set_timer(pygame.USEREVENT + 1, 500)
        cyclic_counter = 0
        self.game_is_active = True

        while self.game_is_active:
            clock.tick(self.c.FPS)

            self.check_player_enemy_collision()
            self.check_win_conditions()

            # Multiplayer
            if self.mode == self.c.MULTI:
                self.tcp_update()
                self.manipulate_tcp_data()

            # self.c.FPS is set to 30, 30 ticks = 1 second
            cyclic_counter += 1
            if cyclic_counter == self.c.FPS:
                cyclic_counter = 0
                self.update_timer()

            if cyclic_counter % 5 == 1:
                self.clear_explosion()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.forceQuit()
                elif event.type == pygame.KEYDOWN:
                    # Deploy bomb
                    k = event.key

                    if k == pygame.K_SPACE:
                        if self.mode == self.c.MULTI:
                            self.sending_data = ["update", "bomb", k, self.id]
                        self.deploy_bomb(self.user)
                    elif k == pygame.K_ESCAPE:
                        self.forceQuit()
                    elif k == pygame.K_UP or k == pygame.K_DOWN or k == pygame.K_LEFT or k == pygame.K_RIGHT:
                        if self.mode == self.c.MULTI:
                            self.sending_data = ["update", "movement", k, self.id]

                        # player's move method
                        point = self.user.movement(k)  # Next point
                        self.movement_helper(self.user, point)
                    elif k == pygame.K_g:  # God mode, cheat xD
                        self.user.gain_power(self.c.BOMB_UP)
                        self.user.gain_power(self.c.POWER_UP)

                elif event.type == pygame.USEREVENT:  # RFCT change definition
                    self.update_bombs()
                elif event.type == pygame.USEREVENT + 1:  # RFCT
                    for e in self.enemies:
                        self.movement_helper(e, e.next_move())

                self.update_display_info()
                pygame.display.update()

    def deploy_bomb(self, player):
        b = player.deploy_bomb()  # Returns a bomb if available
        if b != None:
            tile = self.field.get_tile(player.position)
            tile.bomb = b
            self.bombs.append(b)

    def blit(self, obj, pos):
        self.screen.blit(obj, pos)

    def movement_helper(self, char, point):
        n_point = char.position.move(point)

        tile = self.field.get_tile(n_point)

        # also check for bomb/special power ups here
        if tile.can_pass():
            if char.instance_of == "player" and tile.is_power_up():
                char.set_score(50)  # RFCT | BUG Varies depeding on power up
                char.gain_power(tile.type)
                tile.destroy()
                self.blit(tile.get_background(), n_point)
            char.move(point)

            self.blit(char.image, char.position)

            t = self.field.get_tile(char.old)
            if t.bomb != None:
                self.blit(t.get_background(), char.old)
            self.blit(t.get_image(), char.old)

    def update_bombs(self):
        for bomb in self.bombs:
            if bomb.tick() == 0:
                self.activate_bomb(bomb)

    def activate_bomb(self, bomb):
        if not bomb.triggered:
            bomb.explode()
            self.trigger_bomb_chain(bomb)
            self.bombs.remove(bomb)
            tile = self.field.get_tile(bomb.position)
            tile.bomb = None
            self.blit(tile.get_image(), bomb.position)
            self.reset_tiles.append(bomb.position)

            explosion = pygame.image.load(self.c.IMAGE_PATH + "explosion_c.png").convert()
            self.blit(explosion, bomb.position)

    def trigger_bomb_chain(self, bomb):
        if bomb == None:
            return
        else:
            bomb.triggered = True
            self.bomb_helper(bomb, 'left')
            self.bomb_helper(bomb, 'right')
            self.bomb_helper(bomb, 'up')
            self.bomb_helper(bomb, 'down')

    # RFCT
    def bomb_helper(self, bomb, direction):
        if direction == 'right':
            point = (40, 0)
        elif direction == 'left':
            point = (-40, 0)
        elif direction == 'up':
            point = (0, -40)
        elif direction == 'down':
            point = (0, 40)

        x = y = 0
        while True:
            x += point[0]
            y += point[1]

            n_point = bomb.position.move((x, y))
            t = self.field.get_tile(n_point)

            # Hot a block or indestructible object
            if not t.can_bomb_pass():
                # Trigger new bomb explosion
                if t.bomb != None:
                    self.activate_bomb(t.bomb)
                elif t.destroyable == True:
                    # If brick or powerup or player
                    t.destroy()
                    self.blit(t.get_image(), n_point)
                    self.user.set_score(10)
                break
            else:
                # Path which explosion can travel on
                self.check_player_enemy_bomb_collision(n_point)

                explosion = pygame.image.load(self.c.IMAGE_PATH + "explosion_c.png").convert()
                self.blit(explosion, n_point)
                self.reset_tiles.append(n_point)

            # Check bomb power, this terminates the recursive lopp
            if int(abs(x) / 40) == bomb.range or int(abs(y) / 40) == bomb.range:
                print("(x,y) => (" + str(x) + "," + str(y) + ")")
                break

    def clear_explosion(self):
        for point in self.reset_tiles:
            t = self.field.get_tile(point)
            self.blit(t.get_image(), point)
            self.reset_tiles.remove(point)

    def reset_player_position(self, player, death):
        player.reset(death)
        self.blit(player.image, player.position)

    def check_player_enemy_bomb_collision(self, position):
        # Check if player was hit by bomb
        for player in self.players:
            if player.position == position:
                if player.lose_life_and_game_over():
                    self.game_over(player)
                else:
                    # if the player gets hit by a blast, reset it's position to the starting position
                    self.reset_player_position(player, True)

        # Check if enemy was hit by bomb
        for enemy in self.enemies:
            if enemy.position == position:
                self.enemies.remove(enemy)
                self.user.set_score(100)

    def check_player_enemy_collision(self):
        for enemy in self.enemies:
            if enemy.position == self.user.position:
                # RFCT code repetition
                if self.user.lose_life_and_game_over():
                    self.game_over(self.user)
                self.user.set_score(-250)
                self.reset_player_position(self.user, True)

    def check_win_conditions(self):
        if self.mode == self.c.SINGLE:
            if len(self.enemies) == 0:
                self.victory()

    def game_over(self, player):
        if self.mode == self.c.SINGLE:
            print("Game Over - perdeu todas as vidas | ou o tempo acabou")
            self.highscores.add_score(player.score)
            self.game_is_active = False
            self.exit_game = True

    def forceQuit(self):
        self.game_is_active = False
        self.exit_game = True
        self.force_quit = True

    def print_text(self, text, point):
        font = pygame.font.Font("fonts/Lucida Console.ttf", 20)
        label = font.render(str(text) + " ", True, (255, 255, 255), (0, 0, 0))
        textRect = label.get_rect()
        textRect.x = point[0]
        textRect.y = point[1]
        self.blit(label, textRect)

    def victory(self):
        self.game_is_active = False
        self.user.set_score(500)

        self.level += 1

        if self.level > 6:
            self.stage += 1
            self.level = 1

        mp = music.Music()
        mp.play_sound("victory")
        time.sleep(2)

    def update_timer(self):
        self.timer -= 1

        # User lost
        if self.timer == 0:
            self.game_over(self.user)

        mins = str(int(self.timer / 60))
        secs = str(int(self.timer % 60))

        if len(mins) == 1:
            mins = "0" + mins
        if len(secs) == 1:
            secs = "0" + secs

        txt = "%s:%s" % (mins, secs)
        self.print_text(txt, (400, 653))
