import pygame, random, copy
from player import LaserBolt
from constants import *
from effects import *
from powerup import *

# Class for enemy lasers, bombs, missiles
class EnemyBolt(pygame.sprite.Sprite):
    def __init__(self, level, pos, color = [255, 0, 0], speed = 10, damage = 2, screen = 1, canBeDestroyed = False, img="RESOURCES/laser2.png"):
        # Initializes everything
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(img)
        self.rect = self.image.get_rect()
        self.rect.center = pos

        self.level = level
        self.speed = speed
        self.screen = screen
        self.damage = damage
        self.destroyable = canBeDestroyed
        self.color = color # for the minimap

        if self.destroyable:
            self.hitpoints = 0.5
        else:
            self.hitpoints = float("Infinity")

        self.move_vector = [0, speed]

    def render(self, screen):
        if self.level.screen == self.screen:
            screen.blit(self.image, self.rect)

    def update(self):
        self.rect.centery += self.speed

        # If it reaches the ship, delete the sprite and have the ship take damage
        if self.rect[1] > HEIGHT - 60:
            self.level.health -= self.damage
            self.level.sounds["Hit"].play()
            self.level.flash(8, [244, 133, 20])
            if self in self.level.groups["Enemies"]:
                self.level.groups["Enemies"].remove(self)
                self.level.sounds["Explosion" + str(random.randint(0, 3))].play()
            else:
                self.level.remove_sprite(self)

        if self.hitpoints <= 0 and self.destroyable:
            # Deletes the sprite and places and explosion in its place
            self.level.groups["Enemies"].remove(self)
            self.level.add_sprite(Explosion(self.rect.center, self.level, self.screen))

            self.level.sounds["Explosion" + str(random.randint(0, 3))].play()

# Alerts for enemies on the flanks
class Alert(pygame.sprite.Sprite):
    def __init__(self, level, enemy, alert_type = 1):
        pygame.sprite.Sprite.__init__(self)
        if enemy.screen == 0:
            self.image = pygame.image.load("RESOURCES/Alerts/alert" + str(alert_type) + "_left.png")
        else:
            self.image = pygame.image.load("RESOURCES/Alerts/alert" + str(alert_type) + "_right.png")

        self.rect = self.image.get_rect()
        if enemy.screen == 0:
            self.rect.center = [16, enemy.rect.centery]
        else:
            self.rect.center = [WIDTH - 16, enemy.rect.centery]
            
        self.level = level
        self.enemy = enemy

    # Alerts only appear on main screen (SCREEN 1)
    def render(self, screen):
        if self.level.screen == 1 and self.enemy.screen != 1:
            screen.blit(self.image, self.rect)

    def update(self):
        self.rect.centery = self.enemy.rect.centery
        if self.enemy not in self.level.groups["Enemies"] or self.enemy.screen == 1:
            self.level.remove_sprite(self)

# Base for all Enemy classes
class EnemyBase(pygame.sprite.Sprite):
    def __init__(self, level, pos, screen = 1, color=[255, 0, 0], img="RESOURCES/enemy01.png", hitpoints = 1):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(img)
        self.rect = self.image.get_rect()
        self.rect.center = pos
        
        self.level = level
        self.screen = screen
        self.hitpoints = hitpoints

        self.color = color

        self.move_vector = [0, 0]

    def render(self, screen):
        if self.level.screen == self.screen:
            screen.blit(self.image, self.rect)

    def update(self):
        if self.hitpoints <= 0:
            self.kill()

    def kill(self):
        self.level.groups["Enemies"].remove(self)

# ASTEROID CLASS
class EnemyAsteroid(EnemyBase):
    def __init__(self, level, screen = 1, pos = None, size = 2, ast_type = 1, color=[247, 139, 33]):
        if pos == None:
            pos = [random.randint(40, WIDTH -40), -25]

        # Creates the correct asteroid depending on its size
        if size == 2:
            EnemyBase.__init__(self, level, pos, screen, color, "RESOURCES/Asteroids/asteroid" + str(ast_type) + ".png", 1)
        elif size == 1:
            EnemyBase.__init__(self, level, pos, screen, color, "RESOURCES/Asteroids/sm" + str(ast_type) + "_asteroid" + str(random.randint(1, 3)) + ".png", 1)
        elif size == 0:
            EnemyBase.__init__(self, level, pos, screen, color, "RESOURCES/Asteroids/xs" + str(ast_type) + "_asteroid" + str(random.randint(1, 2)) + ".png", 1)

        self.size = size
        self.type = ast_type

        # Set up for rotation
        self.angle = random.randint(0, 270)
        self.angle_change = random.uniform(-3, 3)

        self.surf = pygame.transform.rotate(self.image, self.angle)
        self.surf_rect = self.rect

        # For moving the sprite
        self.move_vector = [random.randint(-3, 3), random.randint(1, 4)]

    def render(self, screen):
        if self.level.screen == self.screen:
            screen.blit(self.surf, self.rect)

    def update(self):
        # Moves the sprite
        self.rect.centerx += self.move_vector[0]
        self.rect.centery += self.move_vector[1]
        pos = [self.rect.centerx, self.rect.centery]

        # Changes the angle
        self.angle += self.angle_change

        # Rotates the image
        self.surf = pygame.transform.rotate(self.image, self.angle)
        self.rect = self.image.get_rect()
        self.rect.center = pos

        # Checks if the sprite went off the left or right side of the screen
        if self.rect.x < -self.rect.w:
            if self.screen > 0:
                self.rect[0] = WIDTH - 1
                self.screen -= 1
            else:
                self.level.groups["Enemies"].remove(self)
        elif self.rect.x > WIDTH:
            if self.screen < 2:
                self.rect[0] = 1 - self.rect[2]
                self.screen += 1
            else:
                self.level.groups["Enemies"].remove(self)

        # If the asteroid makes it to the ship, have the ship take damage and delete the sprite
        if pos[1] > HEIGHT - 50:
            self.level.health -= 5 * self.size
            self.level.sounds["Hit"].play()
            self.level.flash(8, [255, 170, 68])
            self.level.groups["Enemies"].remove(self)
        
        if self.hitpoints <= 0:
            self.kill()

    def kill(self):
        # The Hydra effect for asteroid sizes 1 and 2
        if self.size > 0:
            for i in range(2):
                ast = EnemyAsteroid(self.level, self.screen, self.rect.center, self.size - 1, self.type)
                self.level.groups["Enemies"].add(ast)
                if self.screen != 1:
                    self.level.add_sprite(Alert(self.level, ast, 2))

            self.level.score += 50 * self.size
        else:
            self.level.score += 10

        # Deletes the sprite and places and explosion in its place
        self.level.groups["Enemies"].remove(self)
        self.level.add_sprite(Explosion(self.rect.center, self.level, self.screen))

        #########################
        # AN ASTEROID IS NOT A WEAPONS CACHE OR SILO, SO NO POWERUPS FOR IT
        #########################
            
# INTERCEPTOR CLASS
class EnemyInterceptor(EnemyBase):
    def __init__(self, level, screen = 1, color=[255, 0, 0], img="RESOURCES/enemy01.png"):
        EnemyBase.__init__(self, level, [random.randint(20, WIDTH - 50), -20], screen, color, img, 1)
        self.state = 0
        self.move_vector = [0, 2]

    def update(self):
        self.rect.centery = self.rect.centery + self.move_vector[1]
        
        # State 0: flying down
        if self.state == 0:
            if self.rect.center[1] > HEIGHT - random.randint(225, 290):
                self.state = 1
                self.level.add_sprite(EnemyBolt(self.level, self.rect.center, self.color, damage = 1 + self.level.lv, screen = self.screen))
                self.move_vector = [0, -3]
        # State 1: escaping after a successful raid
        elif self.state == 1:
            if self.rect[1] < -self.rect[3] - 1:
                self.level.groups["Enemies"].remove(self)

        EnemyBase.update(self)

    def kill(self):
        self.level.score += 100

        # Deletes the sprite and places an explosion in its place
        self.level.add_sprite(Explosion(self.rect.center, self.level, self.screen))
        self.level.groups["Enemies"].remove(self)

        self.level.sounds["Explosion" + str(random.randint(0, 3))].play()

        # Random chance of powerup
        if random.random() < 0.12 + (0.01 * self.level.lv):
            r = random.random()
            if r > 0.4:
                self.level.groups["Powerups"].add(HealthUp(self.level, self.screen, self.rect.center))
            elif r > 0.05:
                self.level.groups["Powerups"].add(Rapidfire(self.level, self.screen, self.rect.center))
            else:
                self.level.groups["Powerups"].add(LifeUp(self.level, self.screen, self.rect.center))

# BOMBER CLASS
class EnemyBomber(EnemyBase):
    def __init__(self, level, color=[255, 255, 0], img="RESOURCES/bomber_r.png"):
        self.img_name = img
        if img == "RESOURCES/bomber_r.png":
            EnemyBase.__init__(self, level, [-45, random.randint(55, 85)], 0, color, img, 1.5)
            self.move_vector = [random.randint(4, 6), 0]
        else:
            EnemyBase.__init__(self, level, [WIDTH - 45, random.randint(55, 85)], 2, color, img, 1.5)
            self.move_vector = [random.randint(-6, -4), 0]

        self.bomb_flag = True
        self.bombs_dropped = 0

    def update(self):
        self.rect.centerx += self.move_vector[0]

        # Checks if the sprite went off the left or right side of the screen
        if self.rect.x < -self.rect.w:
            if self.screen > 0:
                self.rect[0] = WIDTH - 1
                self.screen -= 1
                if self.bombs_dropped < 2:
                    self.bomb_flag = True
            else:
                self.level.groups["Enemies"].remove(self)
        elif self.rect.x > WIDTH:
            if self.screen < 2:
                self.rect[0] = 1 - self.rect[2]
                self.screen += 1
                if self.bombs_dropped < 2:
                    self.bomb_flag = True
            else:
                self.level.groups["Enemies"].remove(self)

        # Drops bombs towards your ship
        if (self.rect.centerx > WIDTH / 2 and self.img_name == "RESOURCES/bomber_r.png" and self.bomb_flag) or (
            self.rect.centerx < WIDTH / 2 and self.img_name == "RESOURCES/bomber_l.png" and self.bomb_flag):

            bomb = EnemyBolt(self.level, self.rect.center, self.color, 8, 15, self.screen, True, "RESOURCES/bomb.png")
            self.level.groups["Enemies"].add(bomb)
            if self.screen != 1:
                self.level.add_sprite(Alert(self.level, bomb, 3))
            self.bomb_flag = False
            self.bombs_dropped += 1

        EnemyBase.update(self)

    def kill(self):
        self.level.score += 200

        # Deletes the sprite and places an explosion in its place
        self.level.add_sprite(Explosion(self.rect.center, self.level, self.screen))
        self.level.groups["Enemies"].remove(self)

        self.level.sounds["Explosion" + str(random.randint(0, 3))].play()

        # Random chance of powerup
        if random.random() < 0.15 + (0.05 * (self.level.lv - 1)):
            r = random.random()
            if r > 0.5:
                self.level.groups["Powerups"].add(HealthUp(self.level, self.screen, self.rect.center))
            elif r > 0.1:
                self.level.groups["Powerups"].add(Rapidfire(self.level, self.screen, self.rect.center))
            else:
                self.level.groups["Powerups"].add(LifeUp(self.level, self.screen, self.rect.center))
