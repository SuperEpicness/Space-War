import pygame, random, time
from level import Level
from constants import *
from bg_objects import *

class GameOverLevel(Level):
    def __init__(self, hits = 0, shots = 1, score = 1, lv = 1, highscores = []):
        Level.__init__(self, "Game Over")
        self.background_color = [10, 10, 10]
        
        for i in range(75):
            self.add_sprite(BACKGROUND_Star(random.randint(20, WIDTH - 20),
                                            random.randint(20, HEIGHT - 20), 1))

        textX = (WIDTH / 2) - 150

        self.game_over_text = [pygame.font.Font('RESOURCES/ArcadeFont.TTF', 64),
                  "GAME   OVER", [255, 255, 255], ((WIDTH / 2) - 150, (HEIGHT / 2) - 10)]
        self.add_text(self.game_over_text)

        self.score = score
        self.score_text = [pygame.font.Font('RESOURCES/ArcadeFont.TTF', 24),
                           "SCORE  " + str(score), (255, 255, 255), (textX, (HEIGHT / 2) - 64)]
        self.fired_text = [pygame.font.Font('RESOURCES/ArcadeFont.TTF', 24),
                           "Shots  Fired  " + str(shots), (255, 255, 255), (textX, self.score_text[3][1] + 16)]
        self.hit_text = [pygame.font.Font('RESOURCES/ArcadeFont.TTF', 24),
                         "Enemies  Hit  " + str(hits), (255, 255, 255), (textX, self.fired_text[3][1] + 16)]

        # Calculates bonus for hit-fired ratio.
        self.bonus = 0
        if shots > 50:
            if float(hits) / shots >= 0.9: # 90% hit-fire ratio (i.e. 90% of shots fired hit a target)
                self.bonus = 250000
            elif float(hits) / shots >= 0.85: # 85%
                self.bonus = 100000
            elif float(hits) / shots >= 0.8: # 80%
                self.bonus = 50000
            elif float(hits) / shots >= 0.75: # 75%
                self.bonus = 25000
            elif float(hits) / shots >= 0.7: # 70%
                self.bonus = 10000
            elif float(hits) / shots >= 0.65: # 65%
                self.bonus = 5000
            elif float(hits) / shots >= 0.55: # 55%
                self.bonus = 2000
        
        self.bonus_text = [pygame.font.Font('RESOURCES/ArcadeFont.TTF', 24),
                         "Hit  Rate  Bonus  " + str(self.bonus), (255, 255, 255), (textX, self.hit_text[3][1] + 16)]

        self.fscore_text = [pygame.font.Font('RESOURCES/ArcadeFont.TTF', 30),
                            "FINAL  SCORE  " + str(score + self.bonus), (255, 255, 0), (textX, self.bonus_text[3][1] + 16)]

        self.time = time.time()
        self.counter = 0
        self.state = 0

        # FOR HIGHSCORE LOGIC
        if len(highscores) > 0:
            self.highscores = highscores
        else:
            self.highscores = None
        self.alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ" # For inputing initials
        self.nickname = "AAA"
        self.char     = 0
        self.selected = 0
        self.value    = 0

        self.insert_text = [pygame.font.Font('RESOURCES/ArcadeFont.TTF', 24),
                            "INPUT  NICKNAME", (255, 128, 0), (textX, self.fscore_text[3][1] + 45)]
        self.nick_text = [pygame.font.Font('RESOURCES/ArcadeFont.TTF', 64),
                          self.nickname, (255, 255, 255), (textX, self.insert_text[3][1] + 20)]
        self.highscore_flag = False

        self.highlight = [textX, self.nick_text[3][1] + 56, 35, 6]

    def animate(self, screen):
        Level.animate(self, screen)

        self.nick_text[1] = self.nickname

        if self.state == 0:
            self.counter += 1
            if self.counter > 6:
                if self.game_over_text[2] == [255, 255, 255]:
                    self.game_over_text[2] = [255, 0, 0]
                else:
                    self.game_over_text[2] = [255, 255, 255]
                self.counter = 0

            if time.time() - self.time > 5:
                self.remove_text(self.game_over_text)
                self.time = time.time()
                self.state = 1

                self.add_text(self.score_text)
        elif self.state == 1:
            if time.time() - self.time > 1:
                self.time = time.time()
                self.state = 2

                self.add_text(self.fired_text)
        elif self.state == 2:
            if time.time() - self.time > 1:
                self.time = time.time()
                self.state = 3

                self.add_text(self.hit_text)
        elif self.state == 3:
            if time.time() - self.time > 1:
                self.time = time.time()
                self.state = 4

                self.add_text(self.bonus_text)
        elif self.state == 4:
            if time.time() - self.time > 2:
                self.time = time.time()
                self.state = 5

                self.add_text(self.fscore_text)
        elif self.state == 5:
            if time.time() - self.time > 4:
                if self.highscores != None:
                    # Gets all of the highscores
                    scores = []
                    for score in self.highscores:
                        scores.append(int(score[1]))
                    scores.append(self.score)
                    if min(scores) != self.score: # If your score isn't the lowest highscore, you're on the leaderboard!
                        self.state = 6

                        self.add_text(self.nick_text)
                        self.add_text(self.insert_text)
                    else:
                        self.stopped_flag = True
                else:
                    self.stopped_flag = True
        elif self.state == 6:
            pygame.draw.rect(screen, (255, 255, 255), self.highlight)
        elif self.state == 7:
            if time.time() - self.time > 2:
                self.stopped_flag = True
                self.highscore_flag = True

    def keydown(self, key):
        def set_nickname():
            nick = self.nickname
            letter = self.alphabet[self.value]

            n = ''
            for i in range(3):
                if i == self.selected:
                    n = n + letter
                else:
                    n = n + nick[i]
            self.nickname = n
            
        if self.state == 6:
            if key == pygame.K_UP:
                self.value += 1
                self.value = self.value % len(self.alphabet)
                set_nickname()
            if key == pygame.K_DOWN:
                self.value -= 1
                self.value = self.value % len(self.alphabet)
                set_nickname()
            if key == pygame.K_SPACE or key == pygame.K_RIGHT:
                self.selected += 1
                self.highlight[0] += self.highlight[2]
                if self.selected > 2:
                    self.state = 7
                    self.time = time.time()
                self.value = 0

class LostALifeLevel(Level):
    def __init__(self, lives = 2, score = 0, lv = 1):
        Level.__init__(self, "Lost a Life")

        self.score = score
        self.lives = lives
        self.lv = lv

        self.background_color = [10, 10, 10]
        
        for i in range(75):
            self.add_sprite(BACKGROUND_Star(random.randint(20, WIDTH - 20),
                                            random.randint(20, HEIGHT - 20), 1))

        self.time = time.time()

    def animate(self, screen):
        Level.animate(self, screen)

        if time.time() - self.time > 3:
            self.stopped_flag = True
