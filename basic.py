import pygame
import math


class SpriteSheet(object):

    def __init__(self, filename):
        self.sheet = pygame.image.load(filename).convert()

    def image_at(self, rectangle, colorKey=-1):
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


class VectorManagement:
    def __init__(self, originCoords, targetCoords):
        self.unitVector = pygame.math.Vector2(targetCoords[0] - originCoords[0],
                                              targetCoords[1] - originCoords[1]).normalize()
        self.angle = angleFinder(self.unitVector)

    def invertDirection(self, axis):
        if axis.lower() == 'x':
            self.unitVector[0] = -self.unitVector[0]
            self.angle = angleFinder(self.unitVector)
            return self.unitVector[0]
        if axis.lower() == 'y':
            self.unitVector[1] = -self.unitVector[1]
            self.angle = angleFinder(self.unitVector)
            return self.unitVector[1]

    def updateTarget(self, originCoords, targetCoords):
        self.unitVector = pygame.math.Vector2(targetCoords[0] - originCoords[0],
                                              targetCoords[1] - originCoords[1]).normalize()
        self.angle = angleFinder(self.unitVector)

    def get_UnitVector(self):
        return self.unitVector

    def get_Angle(self, units='degree'):
        if units == 'degree':
            return self.angle
        if units == 'radian':
            return angleFinder(self.unitVector, 'radian')


def angleFinder(vector, units='degree'):  # ONLY USE WITH LEFT HAND COORDS
    radians = math.atan2(-vector[1], vector[0])
    degrees = radians*(180/math.pi) - 90
    if units == 'degree':
        return degrees
    if units == 'radian':
        return radians
