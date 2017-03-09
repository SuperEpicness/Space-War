import pygame, random, time
from level import Level
from player import *
from bg_objects import *
from enemy import *
from constants import *

class LevelOne(Level):
    def __init__(self, lives = 3, score = 0, lv = 1):
        Level.__init__(self, "Game")
        self.background_color = [10, 10, 10]

        # Sets up the background stars
        self.bg_stars = {}
        self.bg_stars[0] = set()
        self.bg_stars[1] = set()
        self.bg_stars[2] = set()
        
        for i in range(75):
            self.bg_stars[0].add(BACKGROUND_Star(random.randint(20, WIDTH - 20),
                                                 random.randint(20, HEIGHT - 20), 2))
        for i in range(75):
            self.bg_stars[1].add(BACKGROUND_Star(random.randint(20, WIDTH - 20),
                                                 random.randint(20, HEIGHT - 20), 2))
        for i in range(75):
            self.bg_stars[2].add(BACKGROUND_Star(random.randint(20, WIDTH - 20),
                                                 random.randint(20, HEIGHT - 20), 2))

        # Setting up the player crosshairs
        self.crosshairs = Crosshairs("RESOURCES/crosshairs.png", [WIDTH / 2, (HEIGHT / 2) - 100])
        self.speed = 0

        # Lives & the life counter
        self.lives = lives
        self.lifecounter = LifeCounter(self.lives, [(WIDTH / 2) - 5, 25])
        self.add_sprite(self.lifecounter)

        # Health and the health bar
        self.health = 100
        self.healthbar = HealthBar(self.health, [WIDTH / 2, HEIGHT - 120])
        self.add_sprite(self.healthbar)

        self.screen = 1
        
        # Sets up ship on the bottom screen
        self.ship = PlayerClass("RESOURCES/shiptexture.png")
        self.ship.rect[0] = 0
        self.ship.rect[1] = HEIGHT - self.ship.rect[3]
        self.ship.rect[2] = WIDTH

        self.score = score
        self.score_text = [pygame.font.Font('RESOURCES/ArcadeFont.TTF', 25),
                  "SCORE  " + str(self.score), (255, 255, 255), (13, 20)]
        self.add_text(self.score_text)

        self.lv = lv
        self.level_text = [pygame.font.Font('RESOURCES/ArcadeFont.TTF', 25),
                  "LV  " + str(self.lv), (255, 255, 255), (13, 40)]
        self.add_text(self.level_text)

        # Adds the enemy and powerup groups
        self.add_group(pygame.sprite.Group(), "Enemies")
        self.add_group(pygame.sprite.Group(), "Powerups")

        # Cooldown timer for firing shots
        self.cooldown = 0

        # Add missiles to sides
        missileY = HEIGHT - 100
        self.left_missiles = [Missile([40, missileY], self, 0),
                              Missile([70, missileY], self, 0),
                              Missile([WIDTH - 40, missileY], self, 0),
                              Missile([WIDTH - 70, missileY], self, 0)]

        for missile in self.left_missiles:
            self.add_sprite(missile)

        self.right_missiles = [Missile([40, missileY], self, 2),
                               Missile([70, missileY], self, 2),
                               Missile([WIDTH - 40, missileY], self, 2),
                               Missile([WIDTH - 70, missileY], self, 2)]

        for missile in self.right_missiles:
            self.add_sprite(missile)

        # Rapidfire boolean
        self.rapidfire = False
        self.rapid_timer = time.time()

        # Used for hit/fire ratio
        self.hits = 0
        self.fired = 0

        # To turn off enemy spawning, set to False
        self.enemies = True

        # Adds in the sounds
        self.add_sound(pygame.mixer.Sound("RESOURCES/Sounds/LaserSFX.wav"), "LaserBolt")
        self.add_sound(pygame.mixer.Sound("RESOURCES/Sounds/Hit.wav"), "Hit")
        for i in range(4):
            self.add_sound(pygame.mixer.Sound("RESOURCES/Sounds/Explosion" + str(i + 1) + ".wav"), "Explosion" + str(i))
        for i in range(3):
            self.add_sound(pygame.mixer.Sound("RESOURCES/Sounds/Powerup" + str(i + 1) + ".wav"), "Powerup" + str(i))

        # Timers
        self.bomber_timer   = time.time()
        self.asteroid_timer = time.time()
        self.level_timer = time.time()
        self.level_state = 0

        # For flashes
        self.flash_frame = -1
        self.flash_color = None
        self.flash_frames = 0

        # Health bonuses between levels
        self.level_complete_text = [pygame.font.Font('RESOURCES/ArcadeFont.TTF', 36),
                                    "Level Complete!", (255, 255, 0), [0, (HEIGHT / 2) - 36]]
        self.bonus_text = [pygame.font.Font('RESOURCES/ArcadeFont.TTF', 24),
                           "Health  Bonus  ", (255, 255, 255), [0, (HEIGHT / 2) + 10]]

        self.timer_flag = True

    def enable_rapidfire(self):
        self.rapidfire = True
        self.rapid_timer = time.time()

    def flash(self, frames = 5, color = [0, 0, 200]):
        self.flash_frame = 0
        self.flash_color = color
        self.background_color = color
        self.flash_frames = frames

    def center_text(self, text):
        text[3][0] = (WIDTH / 2) - (text[0].size(text[1])[0] / 2)

    def animate(self, screen):
        if self.timer_flag:
            self.timer_flag = False
            self.level_timer = time.time()
            self.level_state = 0
            
        screen.fill(self.background_color)

        self.lifecounter.lives = self.lives
        
        # Ensures that the stars are rendered first (at the bottom)
        for star in self.bg_stars[self.screen]:
            star.render(screen)
            
            if not self.paused:
                star.update()
        
        # Animates the other objects on the screen
        Level.animate(self, screen, False)

        # Update all text & the healthbar
        self.score_text[1] = "SCORE  " + str(self.score)
        self.level_text[1] = "LV  " + str(self.lv)
        self.healthbar.current_hp = float(self.health)

        # Ensures that the crosshairs & ship are on top of all other objects
        screen.blit(self.ship.image, self.ship.rect, [WIDTH * self.screen, 0, WIDTH, self.ship.rect[2]])

        # Limits rapidfire ability to 10 seconds
        if self.rapidfire and time.time() - self.rapid_timer > 10:
            self.rapidfire = False
            self.sounds["Powerup2"].play()

        if self.screen == 1:
            screen.blit(self.crosshairs.image, self.crosshairs.rect)

        if time.time() - self.level_timer > 60 + (5 * self.lv) and self.level_state == 0:
            self.level_state = 1
            self.level_timer = time.time()
            self.enemies = False
            
        if self.level_state == 1 and len(self.groups["Enemies"]) < 1:
            self.level_timer = time.time()
            self.level_state = 2

        if self.level_state == 2 and time.time() - self.level_timer > 2:
            self.level_complete_text[1] = "Level  " + str(self.lv) + "  Complete!"
            self.center_text(self.level_complete_text)
            self.add_text(self.level_complete_text)
            self.level_timer = time.time()
            self.level_state = 3
            
        if self.level_state == 3 and time.time() - self.level_timer > 1:
            self.bonus_text[1] = "Health  Bonus  " + str((self.health) * 100)
            self.center_text(self.bonus_text)
            self.score += (self.health) * 100
            self.add_text(self.bonus_text)
            self.level_state = 4
            self.level_timer = time.time()

            # Add missiles to sides & replace remaining ones
            for missile in self.left_missiles:
                self.remove_sprite(missile)
            for missile in self.right_missiles:
                self.remove_sprite(missile)
            missileY = HEIGHT - 100
            self.left_missiles = [Missile([40, missileY], self, 0),
                                  Missile([70, missileY], self, 0),
                                  Missile([WIDTH - 40, missileY], self, 0),
                                  Missile([WIDTH - 70, missileY], self, 0)]

            for missile in self.left_missiles:
                self.add_sprite(missile)

            self.right_missiles = [Missile([40, missileY], self, 2),
                                   Missile([70, missileY], self, 2),
                                   Missile([WIDTH - 40, missileY], self, 2),
                                   Missile([WIDTH - 70, missileY], self, 2)]

            for missile in self.right_missiles:
                self.add_sprite(missile)
            
        if time.time() - self.level_timer > 3 and self.level_state == 4:
            self.level_state = 0
            self.level_time = time.time()
            self.remove_text(self.bonus_text)
            self.remove_text(self.level_complete_text)
            self.lv += 1

            self.health += int((100 - self.health) / 3)
            self.bomber_timer   = time.time()
            self.asteroid_timer = time.time()
            self.enemies = True

        if not self.paused:
            self.crosshairs.update()

            # Main gun (FIRES LASERS)
            if self.cooldown < 1:
                if pygame.key.get_pressed()[pygame.K_SPACE]:
                    self.fired += 1
                    self.sounds["LaserBolt"].play()
                    if self.rapidfire:
                        self.cooldown = 3
                        self.add_sprite(LaserBolt([325, 550], self.crosshairs.rect.center, self, 0.25))
                    else:
                        self.cooldown = 20
                        self.add_sprite(LaserBolt([325, 550], self.crosshairs.rect.center, self))
            else:
                self.cooldown -= 1

            # ENEMY SPAWNING
            if self.enemies:
                # Interceptors
                if random.randint(0, 1000) > 985:
                    if self.lv < 4:
                        self.groups["Enemies"].add(EnemyInterceptor(self))
                    else:
                        scr = 1
                        if random.random() > 0.9:
                            if random.random() > 0.5:
                                scr = 0
                            else:
                                scr = 2
                        inc = EnemyInterceptor(self, scr)
                        self.groups["Enemies"].add(inc)
                        if screen != 1:
                            self.add_sprite(Alert(self, inc, 1))

                # Asteroids
                t = random.randint(11, 22) - (self.lv - 1)
                if t < 6:
                    t = 6
                if time.time() - self.asteroid_timer > t and self.lv > 1:
                    ast = EnemyAsteroid(self, random.randint(0, 2), size = random.randint(1, 2), ast_type = random.randint(1, 3))
                    self.groups["Enemies"].add(ast)
                    if ast.screen != 1:
                        self.add_sprite(Alert(self, ast, 2))
                    self.asteroid_timer = time.time()

                # Bombers
                t = random.randint(30, 48) - ((self.lv * 3) - 2)
                if t < 17:
                    t = 17
                if time.time() - self.bomber_timer > t and self.lv > 2:
                    if random.random() > 0.5:
                        bomb = EnemyBomber(self)
                    else:
                        bomb = EnemyBomber(self, img="RESOURCES/bomber_l.png")
                    self.groups["Enemies"].add(bomb)
                    self.add_sprite(Alert(self, bomb, 3))
                    self.bomber_timer = time.time()

        # Minimap
        pygame.draw.rect(screen, (145, 145, 145), [WIDTH - 65, 0, 65, 65], 0)

        # Crosshairs on the minimap
        pygame.draw.rect(screen, [255, 255, 255], [(self.crosshairs.rect.center[0] / 10) + (WIDTH - 66), self.crosshairs.rect.center[1] / 10, 3, 1], 1)
        pygame.draw.rect(screen, [255, 255, 255], [(self.crosshairs.rect.center[0] / 10) + (WIDTH - 65), (self.crosshairs.rect.center[1] / 10) - 1, 1, 3], 0)

        # Enemies on the minimap
        for enemy in iter(self.groups["Enemies"]):
            if enemy.screen == 1:
                pygame.draw.rect(screen, enemy.color, [(enemy.rect.center[0] / 10) + (WIDTH - 65), enemy.rect.center[1] / 10, 3, 3], 0)

        # Lasers on the minimap
        for sprite in self.sprites:
            try:
                if sprite.screen == 1:
                    if type(sprite) == LaserBolt:
                        pygame.draw.rect(screen, [0, 255, 0], [(sprite.rect.center[0] / 10) + (WIDTH - 65), sprite.rect.center[1] / 10, 2, 2], 0)
                    if type(sprite) == EnemyBolt:
                        pygame.draw.rect(screen, sprite.color, [(sprite.rect.center[0] / 10) + (WIDTH - 65), sprite.rect.center[1] / 10, 2, 2], 0)
            except Exception:
                pass

        # Your ship on the minimap
        pygame.draw.rect(screen, [100, 100, 100], [WIDTH - 65, 54, 65, 11], 0)
        pygame.draw.rect(screen, [100, 100, 100], [WIDTH - 40, 45, 20, 20], 0)

        # Flashes on the screen
        if self.flash_frame > -1:
            self.background_color = [int((self.flash_frames - self.flash_frame) * (self.flash_color[0] / self.flash_frames)),
                                     int((self.flash_frames - self.flash_frame) * (self.flash_color[1] / self.flash_frames)),
                                     int((self.flash_frames - self.flash_frame) * (self.flash_color[2] / self.flash_frames))]
            self.flash_frame += 1
            if self.flash_frame > self.flash_frames:
                self.flash_frame = -1
        else:
            self.background_color = [10, 10, 10]

        # Checks if if you are out of health
        if self.health < 1:
            self.stopped_flag = True

    def fire_missile(self, missiles, screen = 0):
        if len(self.left_missiles) > 0 and len(self.groups["Enemies"]) > 0:
            enemies_on_screen = []
            for enemy in iter(self.groups["Enemies"]):
                if enemy.screen == screen:
                    enemies_on_screen.append(enemy)

            if len(enemies_on_screen) > 0:
                # Selects a random enemy on its screen and gets its position
                for enemy in enemies_on_screen:
                    if type(enemy) == EnemyBolt:
                        target_enemy = enemy
                        break
                    elif type(enemy) == EnemyBomber:
                        target_enemy = enemy
                        break
                target_enemy = random.choice(enemies_on_screen)

                missile = random.choice(missiles)
            
                missile.fire_at(target_enemy)

                return missile

    def keydown(self, key):
        # To navigate to the other screens
        if key == pygame.K_a and self.screen > 0:
            self.screen -= 1
            if self.screen == 1:
                self.sounds["LaserBolt"].set_volume(1.0)
            else:
                self.sounds["LaserBolt"].set_volume(0.4)
        elif key == pygame.K_d and self.screen < 2:
            self.screen += 1
            if self.screen == 1:
                self.sounds["LaserBolt"].set_volume(1.0)
            else:
                self.sounds["LaserBolt"].set_volume(0.4)

        # To fire off your missiles
        if key == pygame.K_c: # Left missiles
            missile = self.fire_missile(self.left_missiles)
            if missile != None:
                self.left_missiles.remove(missile)
        if key == pygame.K_m: # Right missiles
            missile = self.fire_missile(self.right_missiles, 2)
            if missile != None:
                self.right_missiles.remove(missile)

    def keyup(self, key):
        pass
