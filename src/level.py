import pygame

# Base class for Level objects
class Level:
    """
Base class for Levels, or layers of objects, in the game
    """
    def __init__(self, name):
        self.background_color = [150,150,150]
        self.name = name
        self.sprites = []
        self.groups = {}
        self.texts = []  # Text = (font, text, color, position)
        self.sounds = {}
        self.paused = False # Pauses the Level (freezes it in time)
        self.stopped_flag = False # For when the Level is done with its work

    def set_background(self, color):
        self.background_color = color

    def add_sprite(self, sprite):
        self.sprites.append(sprite)

    def remove_sprite(self, sprite):
        if sprite in self.sprites: # Checks if the given sprite is in the Sprite group (error checker)
            self.sprites.remove(sprite) # If it is, it removes it

    def add_group(self, group, name):
        self.groups[name] = group

    def add_text(self, text):
        self.texts.append(text)

    def remove_text(self, text):
        if text in self.texts:
            self.texts.remove(text)

    def add_sound(self, sound, name):
        self.sounds[name] = sound

# Draws everything on the Level
    def animate(self, screen, draw_background = True):
        if draw_background:
            # Fills the screen
            screen.fill(self.background_color)

        # Renders all of the sprites
        for sprite in self.sprites:
            try:
                sprite.render(screen)
            except Exception:
                screen.blit(sprite.image, sprite.rect)

        # Renders & updates all sprite groups
        for group in self.groups.values():
            if len(group) > 0:
                for sprite in iter(group):
                    try:
                        sprite.render(screen)
                    except Exception:
                        screen.blit(sprite.image, sprite.rect)

                    if not self.paused:
                        try:
                            sprite.update()
                        except Exception:
                            pass

        # Renders all of the text
        for text in self.texts:
            text_surface = text[0].render(text[1], 1, text[2])
            screen.blit(text_surface, text[3])

        if not self.paused:
            # Updates all of the sprites
            for sprite in self.sprites:
                try:
                    sprite.update()
                except Exception:
                    pass

    def keydown(self, key):
        pass

    def keyup(self, key):
        pass
