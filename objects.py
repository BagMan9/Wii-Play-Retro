import pygame
import math


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

    def loc(self):
        return self.x, self.y

    def shoot(self, target_coord):
        Bullet("Assets/bullet16.jpg", self.x, self.y, target_coord[0], target_coord[1])


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
        self.displaceVector = self.target_x - self.x, self.target_y - self.y
        self.displaceVectorMagnitude = abs(math.sqrt(((self.target_x - self.x) ** 2) + ((self.target_y - self.y) ** 2)))
        self.unitVector = self.displaceVector[0] / self.displaceVectorMagnitude, \
                          self.displaceVector[1] / self.displaceVectorMagnitude

    def loc(self):
        return self.x, self.y

    def update(self):
        self.x += self.unitVector[0]
        self.y += self.unitVector[1]


class RocketBullet(Bullet):
    def __init__(self, image, x, y, target_x, target_y):
        super().__init__(image, x, y, target_x, target_y)

