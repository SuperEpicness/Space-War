import pygame, sys, threading, random, time
from player import *
from level import Level
from bg_objects import *
from constants import *

from levelone import LevelOne
from gameover import GameOverLevel, LostALifeLevel

pygame.init()
screen = pygame.display.set_mode([WIDTH, HEIGHT])
pygame.display.set_caption("Mothership ~ FBLA CG&SP_SimonS_FWHS")
pygame.display.set_icon(pygame.image.load("RESOURCES/icon.png"))
level = None

SCORE  = 0
LEVEL  = 1
HEALTH = 100
speed  = 0

playing = True # To allow the player to exit the game

clock = pygame.time.Clock() # Used to control the game's FPS

def parse_highscores(filename):
    # HELPER FUNCTION FOR SORTING HIGHSCORES
    def sort(value1, value2):
        val1, val2 = int(value1[1]), int(value2[1])
        if val1 > val2:
            return -1
        elif val1 < val2:
            return 1
        else:
            return 0
    
    highscores = open(filename, 'r')
    highscore_list = highscores.readlines()
    highscore_lst = []

    for highscore in highscore_list:
        key = ""
        val = ""
        mode = 0
        for char in highscore:
            if mode == 0:
                if char == ',':
                    mode = 1
                else:
                    key = key + char
            else:
                if char == '\n':
                    break
                else:
                    val = val + char

        highscore_lst.append([key, val])

    highscores.close()

    highscore_lst.sort(sort)
    return highscore_lst

## Adds a highscore to the highscore file
def add_highscore(filename, nickname, score):
    # HELPER FUNCTION FOR SORTING HIGHSCORES
    def sort(value1, value2):
        val1, val2 = int(value1[1]), int(value2[1])
        if val1 > val2:
            return -1
        elif val1 < val2:
            return 1
        else:
            return 0
    
    highscores = parse_highscores(filename)
    highscore_file = open(filename, 'r')
    highscore_lines = highscore_file.readlines()
    highscore_file.close()
    
    highscore_file = open(filename, 'w')

    highscores.append([nickname, str(score)])
    highscores.sort()

    scores = []
    for score in highscores:
        scores.append(int(score[1]))

    if min(scores) != score:
        index = scores.index(min(scores)) # Indexes the lowest score

        highscores.pop(index)

        for i in range(len(highscore_lines)):
            highscore_file.write(highscores[i][0] + ',' + highscores[i][1] + '\n')

        highscore_file.close()    

# Sets up title screen
def set_up_title_screen():
    title_level = Level("Title")
    title_level.set_background([10,10,10])

    for i in range(75):
        title_level.add_sprite(BACKGROUND_Star(random.randint(20, WIDTH - 20),
                                               random.randint(20, HEIGHT - 20), -1))

    title_level.add_sprite(BACKGROUND_Planet("RESOURCES/Planets/Planet01.png", 250, 270, -2, -1, 0.1))

    title_logo = PlayerClass("RESOURCES/logo.png")
    title_logo.rect.center = [WIDTH / 2, 235]

    # HIGHSCORES
    scores = parse_highscores("RESOURCES/highscores.txt")
    title_level.add_text([pygame.font.Font('RESOURCES/ArcadeFont.TTF', 16),
                         "H I G H S C O R E S", (255, 128, 0), (WIDTH - 125, 15)])
    for i in range(5):
        title_level.add_text([pygame.font.Font('RESOURCES/ArcadeFont.TTF', 16),
                              scores[i][0] + "  " + scores[i][1], (255, 255, 255), (WIDTH - 105, 15 + (15*(i+1)))])
    
    title_level.add_sprite(title_logo)
    title_level.add_sprite(BACKGROUND_InsertCoin([260, 365]))
    title_level.add_sprite(BACKGROUND_Instructions())

    return title_level

###### OBSELETE ######
##def set_up_game_level(lives, score, lv):
##    game_level = Level("Game")
##    game_level.set_background([10,10,10])
##    game_level.add_sprite(player)
##
##    for i in range(75):
##        game_level.add_sprite(BACKGROUND_Star(random.randint(20, WIDTH - 20),
##                                              random.randint(20, HEIGHT - 20), 2))
##
##    score_text = [pygame.font.Font('RESOURCES/ArcadeFont.TTF', 15),
##                  "SCORE  " + str(score), (255, 255, 255), (13, HEIGHT - 20)]
##    lives_text = [pygame.font.Font('RESOURCES/ArcadeFont.TTF', 15),
##                  "LIVES  " + str(lives), (255, 255, 255), (300, HEIGHT - 20)]
##    level_text = [pygame.font.Font('RESOURCES/ArcadeFont.TTF', 15),
##                  "LV " + str(lv), (255, 255, 255), (WIDTH - 40, HEIGHT - 20)]
##    game_level.add_text(score_text)
##    game_level.add_text(lives_text)
##    game_level.add_text(level_text)
##
##    return game_level

# Creates the title screen
title_level = set_up_title_screen()
game_level  = None
level = title_level

pygame.mixer.set_num_channels(20)

while playing:
    clock.tick(60) # Loop updates 60 times per second

    level.animate(screen) # Updates the current level
    
    pygame.display.flip()
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            playing = False

        if event.type == pygame.KEYDOWN:
            # Activates the current level's keydown events
            level.keydown(event.key)
            
            # Quits the game
            if event.key == pygame.K_ESCAPE:
                playing = False

        if event.type == pygame.KEYUP:
            speed = 0
            level.keyup(event.key)

            if event.key == pygame.K_SPACE:
                if level == title_level and game_level == None:
                    game_level = LevelOne(LIVES, 0, 1)
                    level = game_level

    if level == game_level and level.stopped_flag:
        if level.lives < 1:
            level = GameOverLevel(level.hits, level.fired, level.score, level.lv, parse_highscores(HIGHSCORE_FILE))
            game_level = LevelOne(LIVES)
        else:
            level = LostALifeLevel(level.lives - 1, level.score, level.lv)
            game_level = LevelOne(level.lives, level.score, level.lv)
    elif level != title_level and level.stopped_flag:
        if level.name == "Lost a Life":
            level = game_level
        else:
            if level.highscore_flag:
                add_highscore(HIGHSCORE_FILE, level.nickname, level.score)
            title_level = set_up_title_screen()
            level = title_level

pygame.quit()
sys.exit()
