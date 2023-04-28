import pygame

from basic import VectorManagement


# Wii Play Tank Objects

class Tank(pygame.sprite.Sprite):
    def __init__(self, x, y, image, gunImage, tankGroup) -> None:
        """
        TODO: Make image rotation reflect player movement
        :param x: X-Axis
        :type x: int
        :param y: Y-Axis
        :type y: int
        :param image: Sprite Image
        :type image: pygame.surface.Surface
        :param gunImage: Turret Image
        :type gunImage: pygame.surface.Surface
        :param tankGroup: Sprite Group (layered)
        """
        pygame.sprite.Sprite.__init__(self)
        self.image = image
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

    def loc(self) -> tuple:
        return self.x, self.y

    def bulletShoot(self, image, bulletGroup, allGroup) -> None:
        """
        :param image:
        :type image: pygame.surface.Surface
        :param bulletGroup:
        :type bulletGroup: pygame.sprite.Group
        :param allGroup:
        :type allGroup: pygame.sprite.Group
        """
        if self.firing:
            pass
        else:
            self.firing_time = pygame.time.get_ticks()
            self.firing = True
            self.tankTurret.bullet(image, bulletGroup, allGroup)

    def update(self) -> None:
        self.rect.center = self.x, self.y
        if self.firing and pygame.time.get_ticks() - self.firing_time > self.firing_delay:
            self.firing = False


class Bullet(pygame.sprite.Sprite):
    def __init__(self, image, x, y, vector, velocityMultiplier=10) -> None:
        """
        :param image: Sprite Image
        :type image: pygame.surface.Surface
        :param x: Spawn X-axis
        :type x: int
        :param y: Spawn Y-Axis
        :type y: int
        :param vector: Bullet Direction vector object
        :param velocityMultiplier: Speed factor
        :type velocityMultiplier: int
        """
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

    def loc(self) -> tuple:
        return self.x, self.y

    def update(self) -> None:
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
    def __init__(self, parentTank: Tank, image: pygame.surface.Surface) -> None:
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

    def update(self) -> None:
        self.x = self.parentTank.loc()[0] - 3
        self.y = self.parentTank.loc()[1]
        mouse = pygame.mouse.get_pos()
        self.aimVector = VectorManagement((self.x, self.y), mouse)

        lengthFactor = 19
        self.invertVector = self.aimVector.get_UnitVector()[0] * lengthFactor, \
            self.aimVector.get_UnitVector()[1] * lengthFactor

        self.aimVector = VectorManagement((self.x + self.invertVector[0], self.y + self.invertVector[1]), mouse)
        self.image = pygame.transform.rotate(self.OGImage, self.aimVector.get_Angle())
        self.rect = self.image.get_rect()
        self.rect.center = self.x + self.invertVector[0], self.y + self.invertVector[1]

    def bullet(self, image, bulletGroup=None, allGroup=None) -> None:
        """
        :param image: Sprite Image
        :type image: pygame.surface.Surface
        :param bulletGroup: Sprite Group (for projectiles)
        :param allGroup: All Sprite Group
        """
        projectile = Bullet(image, self.rect.center[0] + self.invertVector[0] * 2,
                            self.rect.center[1] + self.invertVector[1] * 2, self.aimVector)
        if bulletGroup is not None:
            bulletGroup.add(projectile)
        if allGroup is not None:
            allGroup.add(projectile)


class Player(Tank):
    def __init__(self, x, y, image, gunImage, allGroup) -> None:
        super().__init__(x, y, image, gunImage, allGroup)


class Bomb(pygame.sprite.Sprite):
    def __init__(self, image, coords) -> None:
        """

        :param image: Bomb Image
        :type image: pygame.surface.Surface
        :param coords: X Y position
        :type coords: tuple
        """
        pygame.sprite.Sprite.__init__(self)
        self.image = image
        self.x = coords[0]
        self.y = coords[1]
        self.rect = self.image.get_rect()
        self.rect.center = self.x, self.y
