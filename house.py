import pygame
class House(pygame.sprite.Sprite):
    def __init__(self, image_path, pos, size=(120,120), speed=2,wGame=735):
        super().__init__()
        img = pygame.image.load(image_path).convert_alpha()
        self.image = pygame.transform.scale(img, size)  # on redimensionne à la taille souhaitée
        self.rect = self.image.get_rect(topleft=pos)
        self.speed = speed
        self.wGame= wGame

    def update(self):
        self.rect.x -= self.speed
        if self.rect.right < 0:
            self.rect.left = self.wGame