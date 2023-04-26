import pygame
from basic import Direction


# Wii Play Tank Objects

class Tank(pygame.sprite.Sprite):
    def __init__(self, x, y, image):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale((pygame.transform.rotate(image, 270)), (100, 112.6))
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.x = x
        self.y = y
        self.firing = False
        self.firing_delay = 200
        self.firing_time = 0

    def loc(self):
        return self.x, self.y

    def bulletShoot(self, image, target_coord, group, AllGroup):
        if self.firing:
            pass
        else:
            self.firing_time = pygame.time.get_ticks()
            self.firing = True
            projectile = Bullet(image, self.x + 70, self.y + 30, target_coord[0], target_coord[1])
            group.add(projectile)
            AllGroup.add(projectile)

    def update(self):
        self.rect.center = self.x, self.y
        if self.firing and pygame.time.get_ticks() - self.firing_time > self.firing_delay:
            self.firing = False


class Bullet(pygame.sprite.Sprite):
    def __init__(self, image, x, y, target_x, target_y):
        pygame.sprite.Sprite.__init__(self)
        self.x = x
        self.y = y
        self.target_x = target_x
        self.target_y = target_y
        self.direction = Direction((self.x, self.y), (self.target_x, self.target_y))
        self.perTicDistance = self.direction.get_UnitVector()
        self.image = pygame.transform.rotate(image, self.direction.get_Angle())
        self.rect = self.image.get_rect()
        self.rect.center = self.x, self.y
        print(self.direction.get_Angle())

    def loc(self):
        return self.x, self.y

    def update(self):
        self.x += self.perTicDistance[0] * 10
        self.y += self.perTicDistance[1] * 10
        if not 0 < self.x < 1280:
            self.perTicDistance[0] = -self.perTicDistance[0]
        if not 0 < self.y < 720:
            self.perTicDistance[1] = -self.perTicDistance[1]
        self.rect.center = self.x, self.y


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
