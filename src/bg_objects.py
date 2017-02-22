import pygame, time
from constants import *

# Stars in the background
class BACKGROUND_Star(pygame.sprite.Sprite):
    def __init__(self, x, y, speed, delay=0.05):
        pygame.sprite.Sprite.__init__(self)
        self.rect = [x, y, 2, 2]
        self.speed = speed
        self.time = time.time()
        self.delay = delay

    def render(self, screen):
        pygame.draw.rect(screen, (255, 255, 255), self.rect, 0)

    def update(self):
        if time.time() - self.time > self.delay:
            self.time = time.time()
            self.rect[1] += self.speed
            if self.rect[1] > HEIGHT - 6:
                self.rect[1] = self.rect[1] - (HEIGHT - 6)
            elif self.rect[1] < -4:
                self.rect[1] = (HEIGHT - 6) + self.rect[1]

# Planets in the background
class BACKGROUND_Planet(pygame.sprite.Sprite):
    def __init__(self, image, x, y, xspeed, yspeed, delay):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(image)
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
        self.velocity = [xspeed, yspeed]
        self.time = time.time()
        self.delay = delay

    def update(self):
        if time.time() - self.time > self.delay:
            self.time = time.time()
            # Moves planet in the BG
            self.rect[0] += self.velocity[0]
            self.rect[1] += self.velocity[1]

            # Checks x & y pos if offscreen
            if self.rect[0] < -self.rect[2]:
                self.rect[0] = WIDTH
            elif self.rect[0] > WIDTH:
                self.rect[0] = -self.rect[2]
            if self.rect[1] < -self.rect[3]:
                self.rect[1] = HEIGHT
            elif self.rect[1] > HEIGHT:
                self.rect[1] = -self.rect[3]

# Flashing INSERT COIN text
class BACKGROUND_InsertCoin():
    def __init__(self, pos = [260, 360]):
        self.text = [pygame.font.Font('RESOURCES/ArcadeFont.TTF', 25),
                     "INSERT COIN", (255, 255, 255), pos]
        self.text_surface = self.text[0].render(self.text[1], 1, self.text[2])
        self.time = time.time()
        self.showing = True

    def render(self, screen):
        if self.showing:
            screen.blit(self.text_surface, self.text[3])

    def update(self):
        if time.time() - self.time > 0.499:
            self.showing = not self.showing
            self.time = time.time()

# Interactive instructions page
class BACKGROUND_Instructions(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('RESOURCES/Instructions/instructions.png')
        self.rect = self.image.get_rect()
        self.rect.center = [WIDTH / 2, HEIGHT - 140]
