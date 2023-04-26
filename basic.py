import pygame
import math


class SpriteSheet(object):

    def __init__(self, filename):
        self.sheet = pygame.image.load(filename).convert()

    def image_at(self, rectangle, colorKey=None):
        rect = pygame.Rect(rectangle)
        image = pygame.Surface(rect.size).convert()
        image.blit(self.sheet, (0, 0), rect)
        image = image.convert_alpha()
        if colorKey is not None:
            if colorKey == -1:
                colorKey = image.get_at((0, 0))
            image.set_colorkey(colorKey, pygame.RLEACCEL)
        return image


class Hud:

    def __init__(self, GameWindow, WindowSize, titleFontFile='freesansbold.ttf', mainFontFile='freesansbold.ttf'):
        self.score = 0
        self.lives = 3
        self.level = 1
        self.gameWindow = GameWindow
        self.windowSize = WindowSize
        self.titleSize = 64
        self.mainSize = 24
        self.titleFont = pygame.font.Font(titleFontFile, self.titleSize)
        self.mainFont = pygame.font.Font(mainFontFile, self.mainSize)

    def main_menu(self, text, color, x_offset=0, y_offset=0):
        titleText = self.titleFont.render(text, True, color)
        titleTextRect = titleText.get_rect()
        titleTextRect.center = self.windowSize[0] / 2 + x_offset, self.windowSize[1] / 2 + y_offset
        self.gameWindow.blit(titleText, titleTextRect)
        pygame.display.flip()

    def game_info(self, scoreLocation=0, levelLocation=0, livesLocation=0):
        scoreString = f"Score: {self.score}"
        scoreText = self.mainFont.render(scoreString, True, "red")
        scoreTextRect = scoreText.get_rect()
        scoreTextRect.topleft = 8, 8
        self.gameWindow.blit(scoreText, scoreTextRect)


class Direction:
    def __init__(self, originCoords, targetCoords):
        self.origin = originCoords
        self.target = targetCoords
        self.displacementVector = self.target[0] - self.origin[0], self.target[1] - self.origin[1]
        self.displacementVectorMagnitude = abs(math.sqrt(((self.target[0] - self.origin[0]) ** 2) +
                                                         ((self.target[1] - self.origin[1]) ** 2)))
        self.unitVector = [self.displacementVector[0] / self.displacementVectorMagnitude,
                           self.displacementVector[1] / self.displacementVectorMagnitude]
        self.angleRadians = math.atan2(self.displacementVector[1], self.displacementVector[0])
        self.angleDegrees = self.angleRadians*(180/math.pi)

    def get_UnitVector(self):
        return self.unitVector

    def get_Angle(self, units='deg'):
        if units == 'deg':
            return self.angleDegrees - 90
        if units == 'rad':
            return self.angleRadians
