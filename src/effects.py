import pygame
from level import Level

# EXPLOSION for destroyed ships
class Explosion(pygame.sprite.Sprite):
    def __init__(self, position, level, screen, frames=6):
        pygame.sprite.Sprite.__init__(self)
        self.level  = level
        self.screen = screen
        self.frame  = 0
        self.frames = frames
        self.count  = 0
        
        self.image = pygame.image.load("RESOURCES/explode.png")
        self.rect = self.image.get_rect()
        self.rect[2] /= frames
        self.rect.center = position

    def render(self, screen):
        if self.level.screen == self.screen:
            screen.blit(self.image, self.rect, [self.rect[2] * self.frame, 0, self.rect[2], self.rect[3]])

    def update(self):
        self.count += 1
        if self.count > 1:
            self.count = 0
            self.frame += 1

            if self.frame > self.frames:
                self.level.remove_sprite(self)
        
