import pygame
from random import randint
class Obstacle(pygame.sprite.Sprite):
    def __init__(self, type, paths, size, y_pos):
        super().__init__()
        self.frames = [pygame.transform.scale(pygame.image.load(p).convert_alpha(), size)
                       for p in paths]
        self.animation_index = 0
        self.image = self.frames[self.animation_index]
        self.rect = self.image.get_rect(bottomright=(randint(900, 1100), y_pos))

    def animation_state(self):
        self.animation_index += 0.1
        if self.animation_index >= len(self.frames): self.animation_index = 0
        self.image = self.frames[int(self.animation_index)]

    def update(self):
        self.animation_state()
        self.rect.x -=4
        self.destroy()
    def destroy(self):
         if self.rect.x <= -100:
             self.kill()