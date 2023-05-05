import pygame
import pygame.examples.audiocapture

from basic import VectorManagement


pygame.mixer.init()
bulletBounce_Sound = pygame.mixer.Sound('Assets/Sound Effects/bounce.wav')
explode_sound = pygame.mixer.Sound('Assets/Sound Effects/explosion.wav')


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
        self.previousX = self.x
        self.previousY = self.y
        self.firing = False
        self.firing_delay = 200
        self.firing_time = 0
        self.tankTurret = Turret(self, gunImage)
        tankGroup.add(self.tankTurret)

    def loc(self) -> tuple:
        return self.x, self.y

    def bulletShoot(self, image, bulletGroup, isEnemy: bool, enemyBulletGroup, allGroup, sound) -> None:
        """
        :param isEnemy:
        :type isEnemy:
        :param sound:
        :param enemyBulletGroup:
        :type enemyBulletGroup:
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
            sound.play()
            self.tankTurret.bullet(image, enemyBulletGroup, isEnemy, bulletGroup, allGroup)

    def bombShoot(self, image, altImage, bombGroup, explosionGroup, allGroup, sound) -> None:
        """
        :param sound: Sound file
        :type sound:
        :param explosionGroup:
        :type explosionGroup:
        :param altImage: Alt Bomb Image
        :type altImage: pygame.surface.Surface
        :param image: Bomb Image
        :type image: pygame.surface.Surface
        :param bombGroup: Bomb Group
        :type bombGroup: pygame.sprite.Group
        :param allGroup: All Group
        :type allGroup: pygame.sprite.Group
        """
        bomb = Bomb(image, altImage, (self.x, self.y), explosionGroup, allGroup, sound)
        bombGroup.add(bomb)
        allGroup.add(bomb)

    def update(self) -> None:
        if not 0 < self.x < 1280:
            self.x = self.previousX
        if not 0 < self.y < 720:
            self.y = self.previousY
        self.rect.center = self.x, self.y
        self.previousX = self.x
        self.previousY = self.y
        if self.firing and pygame.time.get_ticks() - self.firing_time > self.firing_delay:
            self.firing = False

    def kill(self) -> None:
        super().kill()
        self.tankTurret.kill(1)


class Turret(pygame.sprite.Sprite):
    def __init__(self, parentTank: Tank, image: pygame.surface.Surface, playerTarget=None) -> None:
        pygame.sprite.Sprite.__init__(self)
        self.parentTank = parentTank
        self.OGImage = image
        self.x = self.parentTank.loc()[0] - 3
        self.y = self.parentTank.loc()[1]
        self.invertVector = 0, 0
        self.playerTarget = playerTarget
        if self.playerTarget is None:
            self.aimVector = VectorManagement((self.x, self.y), pygame.mouse.get_pos())
        else:
            self.aimVector = VectorManagement((self.x, self.y), (0, 0))
        self.image = pygame.transform.rotate(self.OGImage, self.aimVector.get_Angle())
        self.rect = self.image.get_rect()
        self.rect.center = self.x, self.y

    def update(self) -> None:
        self.x = self.parentTank.loc()[0] - 3
        self.y = self.parentTank.loc()[1]
        mouse = pygame.mouse.get_pos()
        if self.playerTarget is None:
            self.aimVector = VectorManagement((self.x, self.y), mouse)
        else:
            self.aimVector = VectorManagement((self.x, self.y), self.playerTarget.loc())
        lengthFactor = 19
        self.invertVector = self.aimVector.get_UnitVector()[0] * lengthFactor, \
            self.aimVector.get_UnitVector()[1] * lengthFactor
        if self.playerTarget is None:
            self.aimVector = VectorManagement((self.x + self.invertVector[0], self.y + self.invertVector[1]), mouse)
        else:
            self.aimVector = VectorManagement((self.x + self.invertVector[0], self.y + self.invertVector[1]), self.playerTarget.loc())
        self.image = pygame.transform.rotate(self.OGImage, self.aimVector.get_Angle())
        self.rect = self.image.get_rect()
        self.rect.center = self.x + self.invertVector[0], self.y + self.invertVector[1]

    def bullet(self, image, enemyBulletGroup, isEnemy: bool, bulletGroup=None, allGroup=None) -> None:
        """
        :param isEnemy:
        :type isEnemy:
        :param enemyBulletGroup:
        :type enemyBulletGroup:
        :param image: Sprite Image
        :type image: pygame.surface.Surface
        :param bulletGroup: Sprite Group (for projectiles)
        :param allGroup: All Sprite Group
        """
        projectile = Bullet(image, self.rect.center[0] + self.invertVector[0] * 1.5,
                            self.rect.center[1] + self.invertVector[1] * 1.5, self.aimVector, enemyBulletGroup, isEnemy)
        if bulletGroup is not None:
            bulletGroup.add(projectile)
        if allGroup is not None:
            allGroup.add(projectile)

    def kill(self, noRecur=0) -> None:
        super().kill()
        if noRecur == 0:
            self.parentTank.kill()


class Bullet(pygame.sprite.Sprite):
    def __init__(self, image, x, y, vector, enemyBulletGroup, isEnemy: bool, velocityMultiplier=10) -> None:
        """
        :param enemyBulletGroup:
        :type enemyBulletGroup: pygame.sprite.Group
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
        self.enemyBulletGroup = enemyBulletGroup
        self.isEnemy = isEnemy
        if isEnemy:
            enemyBulletGroup.add(self)

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
            if not self.isEnemy:
                self.enemyBulletGroup.add(self)
            bulletBounce_Sound.play()
        if not 0 < self.y < 720:
            self.perTicDistance[1] = self.direction.invertDirection('y')
            self.image = pygame.transform.rotate(self.originalImage, self.direction.get_Angle())
            self.rect = self.image.get_rect()
            self.bounceCount += 1
            if not self.isEnemy:
                self.enemyBulletGroup.add(self)
            bulletBounce_Sound.play()
        if self.bounceCount >= 3:
            self.kill()
        self.rect.center = self.x, self.y


class Bomb(pygame.sprite.Sprite):
    def __init__(self, image, alt_Image, coords, explosionGroup, allGroup, sound) -> None:
        """
        :param sound:
        :type sound:
        :param explosionGroup: pygame.sprite.Group
        :type explosionGroup: pygame.sprite.Group
        :param allGroup: pygame.sprite.Group
        :type allGroup: pygame.sprite.Group
        :param image: Bomb Image
        :type image: pygame.surface.Surface
        :param coords: X Y position
        :type coords: tuple
        """
        pygame.sprite.Sprite.__init__(self)
        self.OGImage = image
        self.image = image
        self.altImage = alt_Image
        self.x = coords[0]
        self.y = coords[1]
        self.rect = self.image.get_rect()
        self.rect.center = self.x, self.y
        self.timer = 0
        self.explosionGroup = explosionGroup
        self.allGroup = allGroup
        self.sound = sound

    def update(self) -> None:
        self.timer += 1
        self.image = self.OGImage
        if self.timer % 50 == 0 or self.timer >= 500:
            self.image = self.altImage
        if self.timer >= 600:
            self.kill()

    def kill(self) -> None:
        super().kill()
        explode = Explosion(self.x, self.y, 5.5, self.sound)
        self.explosionGroup.add(explode)
        self.allGroup.add(explode)


class Explosion(pygame.sprite.Sprite):

    def __init__(self, x, y, size, sound) -> None:
        """
        :param sound:
        :type sound:
        :param x: X Axis location
        :type x: float
        :param y: Y Axis location
        :type y: float
        """
        super().__init__()
        self.x = x
        self.y = y
        self.size = size
        self.images = []
        self.imageNumber = 0
        for i in range(1, 9):
            image = pygame.image.load('Assets/explosionImages/' + str(i) + '.png')
            image = pygame.transform.scale_by(image, size)
            self.images.append(image)
        self.image = self.images[0]
        self.rect = self.image.get_rect()
        self.rect.center = self.x - 32, self.y - 32
        self.sound = sound

    def update(self) -> None:
        if self.imageNumber == 8:
            self.sound.play()
            self.kill()
        else:
            self.image = self.images[self.imageNumber]
            self.rect = self.image.get_rect()
            self.rect.center = self.x, self.y
            self.imageNumber += 1


class Player(Tank):
    def __init__(self, x, y, image, gunImage, allGroup) -> None:
        super().__init__(x, y, image, gunImage, allGroup)


class Enemy(Tank):
    def __init__(self, x, y, image, gunImage, allGroup, playerTarget) -> None:
        super().__init__(x, y, image, gunImage, allGroup)
        self.tankTurret = Turret(self, gunImage, playerTarget)

    def kill(self) -> None:
        super().kill()
        Explosion(self.x, self.y, 1, pygame.mixer.Sound('Assets/Sound Effects/explosion.wav'))


class Wall(pygame.sprite.Sprite):
    def __init__(self, coords: tuple, image: pygame.surface.Surface):
        super().__init__()
        self.x = coords[0]
        self.y = coords[1]
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.center = self.x, self.y


class Target(pygame.sprite.Sprite):

    def __init__(self, imagefile, x, y, vel_x, vel_y, ax, ay, explosionGroup, allGroup):
        super().__init__()
        # Position Init
        self.x = x
        self.y = y
        # Vel Init
        self.vel_x = vel_x
        self.vel_y = vel_y
        # Accel Init
        self.ax = ax
        self.ay = ay
        # Image Init
        self.image = imagefile
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y
        self.explosionGroup = explosionGroup
        self.allGroup = allGroup

    def update(self):
        # Border Checks
        if self.x >= 1280 or self.x <= 0:
            self.vel_x *= -1
        if self.y >= 720 or self.y <= 0:
            self.vel_y *= -1
        # Acceleration
        self.vel_x += self.ax
        self.vel_y += self.ay

        # Pos Update
        self.x += self.vel_x
        self.y += self.vel_y

        # Render Update
        self.rect.x = self.x
        self.rect.y = self.y

    def locate(self):
        return self.x, self.y

    def kill(self) -> None:
        super().kill()
        explode = Explosion(self.x, self.y, 2, pygame.mixer.Sound('Assets/Sound Effects/explosion.wav'))
        self.explosionGroup.add(explode)
        self.allGroup.add(explode)

