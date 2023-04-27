import pygame
from basic import VectorManagement


# Wii Play Tank Objects

class Tank(pygame.sprite.Sprite):
    def __init__(self, x, y, image, gunImage, tankGroup):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.rotate(image, 270)
        self.rect = self.image.get_rect()
        self.gunImage = gunImage
        self.rect.center = (x, y)
        self.x = x
        self.y = y
        self.firing = False
        self.firing_delay = 200
        self.firing_time = 0
        self.tankTurret = Turret(self, gunImage)
        tankGroup.add(self.tankTurret)

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
    def __init__(self, image, x, y, target_x, target_y, velocityMultiplier=10):
        pygame.sprite.Sprite.__init__(self)
        self.x = x
        self.y = y
        self.originalImage = image
        self.target_x = target_x
        self.target_y = target_y
        self.velocityMultiplier = velocityMultiplier
        self.direction = VectorManagement((self.x, self.y), (self.target_x, self.target_y))
        self.perTicDistance = self.direction.get_UnitVector()
        self.angle = self.direction.get_Angle()
        self.image = pygame.transform.rotate(self.originalImage, self.angle)
        self.rect = self.image.get_rect()
        self.rect.center = self.x, self.y
        self.bounceCount = 0

    def loc(self):
        return self.x, self.y

    def update(self):
        self.x += self.perTicDistance[0] * self.velocityMultiplier
        self.y += self.perTicDistance[1] * self.velocityMultiplier
        if not 0 < self.x < 1280:
            self.perTicDistance[0] = self.direction.invertDirection('x')
            self.image = pygame.transform.rotate(self.originalImage, self.direction.get_Angle())
            self.rect = self.image.get_rect()
            self.bounceCount += 1
        if not 0 < self.y < 720:
            self.perTicDistance[1] = self.direction.invertDirection('y')
            self.image = pygame.transform.rotate(self.originalImage, self.direction.get_Angle())
            self.rect = self.image.get_rect()
            self.bounceCount += 1
        if self.bounceCount >= 3:
            self.kill()
        self.rect.center = self.x, self.y


class Turret(pygame.sprite.Sprite):
    def __init__(self, parentTank, image):
        pygame.sprite.Sprite.__init__(self)
        self.parentTank = parentTank
        self.OGImage = image
        self.x = self.parentTank.loc()[0] + 41.5
        self.y = self.parentTank.loc()[1] + 47
        self.aimVector = VectorManagement((self.x, self.y), pygame.mouse.get_pos())
        self.image = pygame.transform.rotate(self.OGImage, self.aimVector.get_Angle())
        self.rect = self.image.get_rect()
        self.rect.center = self.x, self.y

    def update(self):
        self.x = self.parentTank.loc()[0] + 21.5
        self.y = self.parentTank.loc()[1] + 23
        self.aimVector = VectorManagement((self.x, self.y), pygame.mouse.get_pos())
        self.image = pygame.transform.rotate(self.OGImage, self.aimVector.get_Angle())
        self.rect.center = self.x, self.y


class Player(Tank):
    def __init__(self, x, y, image, gunImage, allGroup):
        super().__init__(x, y, image, gunImage, allGroup)
