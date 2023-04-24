import pygame

# Wii Play Tank Objects


class Tank(pygame.sprite.Sprite):
    def __init__(self, x, y, image, speed, direction):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(image)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.speed = speed
        self.direction = direction
        self.x = x
        self.y = y


class Bullet(pygame.sprite.Sprite):
    def __init__(self, image, x, y, target_x, target_y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(image)
        self.rect = self.image.get_rect()
        self.rect.center = x, y
        self.x = x
        self.y = y
        self.target_x = target_x
        self.target_y = target_y
        
    def loc(self):
        return self.x, self.y


class RocketBullet(Bullet):
    def __init__(self, image, x, y, target_x, target_y):
        super().__init__(image, x, y, target_x, target_y)


