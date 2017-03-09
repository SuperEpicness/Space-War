import pygame, math, random
from constants import *
from powerup import *
from effects import *

## OLD PLAYER CLASS (OBSELETE)
class PlayerClass(pygame.sprite.Sprite):
    """
Initializes the player's ship.
    """
    def __init__(self, img):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(img)
        self.rect = self.image.get_rect()
        self.rect.center = [WIDTH  / 2, HEIGHT - 25]
        self.angle = 0

    def move(self, speed):
        self.rect.centerx = self.rect.centerx + speed
        
        # Prevents the player from moving offscreen
        if self.rect.centerx < 30:  self.rect.centerx = 30
        if self.rect.centerx > WIDTH - 30: self.rect.centerx = WIDTH - 30

    ##def render(self, screen):
    ##    screen.blit(pygame.transform.scale2x(self.image), self.rect)

    def update(self):
        if pygame.key.get_pressed()[pygame.K_LEFT]:
            self.rect.center = [self.rect.center[0] - 5, self.rect.center[1]]
            if self.rect[0] < 0:
                self.rect[0] = 0
        if pygame.key.get_pressed()[pygame.K_RIGHT]:
            self.rect.center = [self.rect.center[0] + 5, self.rect.center[1]]
            if self.rect[0] > WIDTH - self.rect[2]:
                self.rect[0] = WIDTH - self.rect[2]

# Class for the crosshairs
class Crosshairs(PlayerClass):
    """
Crosshair Class
    """
    def __init__(self, img, pos, speed = 6):
        PlayerClass.__init__(self, img)
        self.rect.center = pos

        # Set up for the arc
        self.initialY = pos[1]
        self.lowestY = pos[1] - ARCSIZE
        self.rect.centery = HEIGHT - self.lowestY - (math.sin(math.pi*(self.rect.centerx / float(WIDTH))) * ARCSIZE)
        self.speed = 6

    def update(self):
        # Moves the crosshairs in an arc
        if pygame.key.get_pressed()[pygame.K_LEFT]:
            self.rect.centerx = self.rect.center[0] - self.speed
            self.rect.centery = HEIGHT - self.lowestY - (math.sin(math.pi*(self.rect.centerx / float(WIDTH))) * ARCSIZE)
            if self.rect[0] < 0:
                self.rect[0] = 0
        if pygame.key.get_pressed()[pygame.K_RIGHT]:
            self.rect.centerx = self.rect.center[0] + self.speed
            self.rect.centery = HEIGHT - self.lowestY - (math.sin(math.pi*(self.rect.centerx / float(WIDTH))) * ARCSIZE)
            if self.rect[0] > WIDTH - self.rect[2]:
                self.rect[0] = WIDTH - self.rect[2]

class LifeCounter():
    def __init__(self, lives, center):
        self.lives = lives
        self.center = center

    def render(self, screen):
        COLOR = [255, 0, 0]

        # For each live you have, draw one bar
        for i in range(self.lives):
            if i % 2 == 0:
                COLOR = [255, 0, 0]
            else:
                COLOR = [255, 255, 255]
            pygame.draw.rect(screen, COLOR, [self.center[0] - 5 + (i*10), self.center[1] - 12, 10, 25], 0)

class HealthBar():
    def __init__(self, health, center, width = 150, height = 10):
        self.current_hp = float(health)
        self.maximum_hp = health
        self.center = center
        self.width  = width
        self.height = height

    def render(self, screen):
        # First bar is for max health
        pygame.draw.rect(screen, [255,   0,   0], [self.center[0] - (self.width / 2), self.center[1] - (self.height / 2), self.width, self.height], 0)

        # Second bar is for current health
        pygame.draw.rect(screen, [255, 255, 255], [self.center[0] - (self.width / 2), self.center[1] - (self.height / 2),
                                                   self.width * (self.current_hp / self.maximum_hp), self.height], 0)

## UNUSED
##class GunSprite(pygame.sprite.Sprite):
##    def __init__(self, img, pos, crosshairs):
##        pygame.sprite.Sprite.__init__(self)
##        self.image = pygame.image.load(img)
##        self.rect = self.image.get_rect()
##        self.rect.center = pos
##        self.pos = pos
##        self.angle = 0
##        self.crosshairs = crosshairs
##
##    def render(self, screen):
##        surf = pygame.transform.rotate(self.image, self.angle)
##        surf_rect = surf.get_rect()
##        surf_rect[0], surf_rect[1] = self.rect[0], self.rect[1]
##        if self.angle > -90:
##            surf_rect.center = [surf_rect.center[0] + (self.crosshairs.rect.center[0] - surf_rect.center[0]), surf_rect.center[1]]
##        screen.blit(surf, surf_rect)
##
##    def update(self):
##        crosshairX, crosshairY = self.crosshairs.rect.center
##        spriteX, spriteY = self.rect.center
##        self.angle = math.atan2(crosshairY - spriteY, spriteX - crosshairX) * (180 / math.pi)

# Your laser
class LaserBolt(pygame.sprite.Sprite):
    def __init__(self, starting_position, ending_position, level, damage = 1, screen = 1, img = "RESOURCES/laser1.png", speed = 20):
        pygame.sprite.Sprite.__init__(self)
        
        self.image = pygame.image.load(img)
        self.original_image = self.image.copy()
        self.rect = self.image.get_rect()
        self.rect.center = starting_position

        # Used for making the sprite face the crosshairs at their current position
        self.start = starting_position
        self.points_towards = ending_position
        self.set_angle((math.atan2(self.start[1] - self.points_towards[1], self.points_towards[0] - self.start[0]) * (180 / math.pi)) + random.randint(-3, 3))
        
        self.move_vector = [math.cos(self.get_angle() * (math.pi / 180)), math.sin(self.angle * (math.pi / 180))]
        self.speed = speed

        # Turns the image accordingly
        self.image = pygame.transform.rotate(self.image, self.get_angle())
        self.rect = self.image.get_rect()
        self.rect.center = starting_position

        self.level = level
        self.screen = screen
        self.damage = damage

    def set_angle(self, angle):
        self.angle = angle

    def get_angle(self):
        return self.angle

    def render(self, screen):
        if self.level.screen == self.screen:
            screen.blit(self.image, self.rect)

    def update(self):
        # Moves the spirte
        self.rect.centerx += self.move_vector[0] * self.speed
        self.rect.centery -= self.move_vector[1] * self.speed

        # If the sprite reaches the top, delete the sprite
        if self.rect[1] < -self.rect[3]:
            self.level.remove_sprite(self)

        # If the sprite reaches the edges of the screen, move to an adjacent screen or delete the sprite
        if self.rect[0] < -self.rect[2]:
            if self.screen > 0:
                self.screen -= 1
                self.rect.centerx = WIDTH
            else:
                self.level.remove_sprite(self)
        elif self.rect[0] > WIDTH:
            if self.screen < 2:
                self.screen += 1
                self.rect.centerx = 0
            else:
                self.level.remove_sprite(self)

        # Checks for enemy collision
        hit_list = pygame.sprite.spritecollide(self, self.level.groups["Enemies"], False) + pygame.sprite.spritecollide(self, self.level.groups["Powerups"], False)
        if len(hit_list) > 0:
            for sprite in hit_list:
                if sprite.screen == self.screen:
                    try:
                        if sprite.powerup:
                            sprite.kill()
                    except Exception:
                        sprite.hitpoints -= self.damage
                    self.delete()

    def delete(self):
        self.level.remove_sprite(self)
        self.level.hits += 1

# Subclass of LaserBolt, the missiles on the adjacent screens
class Missile(LaserBolt):
    def __init__(self, starting_position, level, screen, speed = 1):
        LaserBolt.__init__(self, starting_position, [starting_position[0], starting_position[1] - 1], level, 4, screen, "RESOURCES/missile_off.png", speed)
        self.set_angle(90)
        self.state = 0
        self.counter = 0
        self.target = None

    # Points the missile at the target and activates the sprite
    def fire_at(self, target):
        if type(target) == list:
            LaserBolt.__init__(self, self.rect.center, target, self.level, 4, self.screen, "RESOURCES/missile1.png", self.speed)
            self.state = 1
        else:
            LaserBolt.__init__(self, self.rect.center, self.points_towards, self.level, 4, self.screen, "RESOURCES/missile1.png", self.speed)
            self.set_angle(90)
            self.state = 2
            self.target = target
            self.original_img = self.image.copy()
        pygame.mixer.Sound("RESOURCES/Sounds/Rocket.wav").play()

    def render(self, screen):
        if self.level.screen == self.screen:
            screen.blit(pygame.transform.rotate(self.original_image, self.angle), self.rect)

    def update(self):
        if self.state != 0:
            LaserBolt.update(self)
            if self.speed < 14:
                self.speed += 1

        if self.state == 2:
            if self.target in self.level.groups["Enemies"] and self.target.screen == self.screen and self.speed > 5:
                start = self.rect.center
                end = self.target.rect.center
                angle = math.atan2(start[1] - end[1], end[0] - start[0]) * (180 / math.pi)
                delta_angle = angle - self.angle
                if delta_angle < -180:
                    delta_angle = 360 - delta_angle
                max_turning_angle = 5
                if delta_angle >= -max_turning_angle and delta_angle <= max_turning_angle:
                    self.angle -= delta_angle
                elif delta_angle > max_turning_angle:
                    self.angle += max_turning_angle
                else:
                    self.angle -= max_turning_angle
                self.move_vector = [math.cos(self.angle * (math.pi / 180)), math.sin(self.angle * (math.pi / 180))]

    def delete(self):
        # Deletes the sprite and places an explosion in its place
        self.level.remove_sprite(self)
        self.level.add_sprite(Explosion(self.rect.center, self.level, self.screen))
        self.level.sounds["Explosion" + str(random.randint(0, 3))].play()
        
        self.level.hits += 1
