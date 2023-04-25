import pygame
import math


# Wii Play Tank Objects

class SpriteSheet(object):

    def __init__(self, filename):
        self.sheet = pygame.image.load(filename).convert()

    def image_at(self, rectangle, colorkey=None):
        rect = pygame.Rect(rectangle)
        image = pygame.Surface(rect.size).convert()
        image.blit(self.sheet, (0, 0), rect)
        if colorkey is not None:
            if colorkey == -1:
                colorkey = image.get_at((0, 0))
            image.set_colorkey((colorkey, pygame.RLEACCEL))
        return image

# Basic Objects


class Tank(pygame.sprite.Sprite):
    def __init__(self, x, y, image):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale((pygame.transform.rotate(image, 270)), (100, 100))
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.x = x
        self.y = y

    def loc(self):
        return self.x, self.y

    def shoot(self, target_coord, group):
        projectile = Bullet("Assets/bullet16.jpg", self.x+100, self.y+50, target_coord[0], target_coord[1])
        group.add(projectile)

    def update(self):
        self.rect.center = self.x, self.y


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
        self.x += self.unitVector[0]*10
        self.y += self.unitVector[1]*10
        self.rect.center = self.x, self.y

    def __str__(self):
        return "Location: " + str(self.x) + ", " + str(self.y) + "\n" \
                                                                 "Target: " + str(self.target_x) + ", " + str(
            self.target_y) + "\n" \
                             "Vector (X, Y, Magnitude): " + str(self.displaceVector) + ", " + str(
            self.displaceVectorMagnitude)


class Player(Tank):
    def __init__(self, x, y, image):
        super().__init__(x, y, image)


class Enemy(Tank):
    def __init__(self, x, y, image):
        super().__init__(x, y, image)


class RocketBullet(Bullet):
    def __init__(self, image, x, y, target_x, target_y):
        super().__init__(image, x, y, target_x, target_y)


class SilverTank(Tank):
    def __init__(self, x, y, image):
        super().__init__(x, y, image)
