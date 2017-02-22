import pygame, random, time
from constants import *
from effects import *

# Base class for all powerups
class Powerup(pygame.sprite.Sprite):
    def __init__(self, level, screen, pos, img = "RESOURCES/Powerups/blank.png"):
        # Initializes everything
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(img)
        self.rect = self.image.get_rect()
        self.rect.center = pos

        self.level = level
        self.screen = screen
        self.powerup = True

        self.move_vector = [0, 3]

    def render(self, screen):
        if self.level.screen == self.screen:
            screen.blit(self.image, self.rect)

    def update(self):
        self.rect.centery += self.move_vector[1]
        if self.rect.y > HEIGHT - 100:
            self.collect()

    def kill(self):
        self.level.add_sprite(Explosion(self.rect.center, self.level, self.screen))
        self.level.groups["Powerups"].remove(self)

        self.level.sounds["Explosion" + str(random.randint(0, 3))].play()

    def collect(self):
        self.level.groups["Powerups"].remove(self)

# LIFE UP
class LifeUp(Powerup):
    def __init__(self, level, screen, pos):
        Powerup.__init__(self, level, screen, pos, "RESOURCES/Powerups/lifeup.png")

    def collect(self):
        self.level.lives += 1
        self.level.groups["Powerups"].remove(self)
        self.level.sounds["Powerup0"].play()

# HEALTH UP
class HealthUp(Powerup):
    def __init__(self, level, screen, pos):
        Powerup.__init__(self, level, screen, pos, "RESOURCES/Powerups/healthup.png")

    def collect(self):
        self.level.health += 5
        if self.level.health > 100: # Makes sure your health <= 100
            self.level.health = 100
        self.level.groups["Powerups"].remove(self)
        self.level.sounds["Powerup0"].play()

# RAPIDFIRE FTW
class Rapidfire(Powerup):
    def __init__(self, level, screen, pos):
        Powerup.__init__(self, level, screen, pos, "RESOURCES/Powerups/rapidfire.png")

    def collect(self):
        if not self.level.rapidfire:
            self.level.enable_rapidfire()
        self.level.groups["Powerups"].remove(self)
        self.level.sounds["Powerup1"].play()
