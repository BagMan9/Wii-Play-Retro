import pygame
from basic import VectorManagement


# Wii Play Tank Objects

class Tank(pygame.sprite.Sprite):
    def __init__(self, x, y, image, gunImage, tankGroup):
        """
        TODO: Move image rotation outside class
        TODO: Make image rotation reflect player movement
        """
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

    def bulletShoot(self, image, bulletGroup, allGroup):
        if self.firing:
            pass
        else:
            self.firing_time = pygame.time.get_ticks()
            self.firing = True
            self.tankTurret.bullet(image, bulletGroup, allGroup)

    def update(self):
        self.rect.center = self.x, self.y
        if self.firing and pygame.time.get_ticks() - self.firing_time > self.firing_delay:
            self.firing = False


class Bullet(pygame.sprite.Sprite):
    def __init__(self, image, x, y, vector, velocityMultiplier=10):
        pygame.sprite.Sprite.__init__(self)
        self.x = x
        self.y = y
        self.originalImage = image
        self.velocityMultiplier = velocityMultiplier
        self.direction = vector
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
        self.x = self.parentTank.loc()[0] - 3
        self.y = self.parentTank.loc()[1]
        self.invertVector = 0, 0
        self.aimVector = VectorManagement((self.x, self.y), pygame.mouse.get_pos())
        self.image = pygame.transform.rotate(self.OGImage, self.aimVector.get_Angle())
        self.rect = self.image.get_rect()
        self.rect.center = self.x, self.y

    def update(self):
        self.x = self.parentTank.loc()[0] - 3
        self.y = self.parentTank.loc()[1]
        mouse = pygame.mouse.get_pos()
        self.aimVector = VectorManagement((self.x, self.y), mouse)
        self.invertVector = self.aimVector.get_UnitVector()[0] * 19, self.aimVector.get_UnitVector()[1] * 19
        self.aimVector = VectorManagement((self.x+self.invertVector[0], self.y+self.invertVector[1]), mouse)
        self.image = pygame.transform.rotate(self.OGImage, self.aimVector.get_Angle())
        self.rect = self.image.get_rect()
        self.rect.center = self.x+self.invertVector[0], self.y+self.invertVector[1]

    def bullet(self, image, bulletGroup, allGroup):
        projectile = Bullet(image, self.rect.center[0]+self.invertVector[0]*2,
                            self.rect.center[1]+self.invertVector[1]*2, self.aimVector)
        bulletGroup.add(projectile)
        allGroup.add(projectile)


class Player(Tank):
    def __init__(self, x, y, image, gunImage, allGroup):
        super().__init__(x, y, image, gunImage, allGroup)
