import pygame, sys

pygame.init()
screen = pygame.display.set_mode([800, 600])
pygame.display.set_caption("Asteroid Test")

sprite = pygame.sprite.Sprite()
sprite.image = pygame.image.load("RESOURCES/missile1.png")
sprite_surf = sprite.image.copy()
sprite.rect = sprite.image.get_rect()
sprite_rect = sprite.rect.copy()
angle = 0

clock = pygame.time.Clock()

while True:
    pygame.display.flip()
    clock.tick(60)

    screen.fill([0, 0, 0])
    screen.blit(sprite_surf, sprite.rect)

    angle -= 2
    sprite_surf = pygame.transform.rotate(sprite.image, angle)
    sprite.rect.centerx = sprite_rect.centerx - (sprite_surf.get_rect().w - sprite_rect.w) / 2
    sprite.rect.centery = sprite_rect.centery - (sprite_surf.get_rect().h - sprite_rect.h) / 2

    sprite_rect.centerx += 1
    sprite_rect.centery += 1

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
