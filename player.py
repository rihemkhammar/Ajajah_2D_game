import pygame

class Player(pygame.sprite.Sprite):
    def __init__(self, walk_paths, jump_path, size=(100, 100), pos=(80, 240)):
        super().__init__()
        self.walk_paths = walk_paths
        self.jump_path = jump_path
        self.player_walk = [pygame.transform.scale(pygame.image.load(path).convert_alpha(), size) for path in
                            walk_paths]
        self.player_jump = pygame.transform.scale(pygame.image.load(jump_path).convert_alpha(), size)

        self.player_index = 0
        self.image = self.player_walk[self.player_index]
        self.rect = self.image.get_rect(midbottom=pos)
        self.gravity = 0

    def player_input(self):
         keys = pygame.key.get_pressed()
         if keys[pygame.K_SPACE] and self.rect.bottom >=300:
              self.gravity = -22

    def apply_gravity(self):
         self.gravity +=1
         self.rect.y += self.gravity
         if self.rect.bottom >= 340: self.rect.bottom = 340

    def update(self):
         self.player_input()
         self.apply_gravity()
         self.animation_state()

    def animation_state(self):
         if self.rect.bottom < 340:
             self.image = self.player_jump
         else:
             self.player_index += 0.1
             if self.player_index >= len(self.player_walk): self.player_index =0
             self.image = self.player_walk[int(self.player_index)]