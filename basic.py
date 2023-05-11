import math

import pygame


class SpriteSheet(object):

    def __init__(self, filename: str) -> None:
        """
        :param filename: File path
        """
        self.sheet = pygame.image.load(filename).convert()

    def image_at(self, rectangle, scalePercent=100, colorKey=-1) -> pygame.surface.Surface:
        """
        :param rectangle: X, Y, Length, Width
        :param scalePercent: Scale image by %
        :type scalePercent: int
        :param colorKey: Specify transparency layer
        :type colorKey:
        :return: Returns image
        """
        scaleAmount = scalePercent / 100
        rect = pygame.Rect(rectangle)
        image = pygame.Surface(rect.size).convert()
        image.blit(self.sheet, (0, 0), rect)
        image = image.convert_alpha()
        if colorKey is not None:
            if colorKey == -1:
                colorKey = image.get_at((0, 0))
            image.set_colorkey(colorKey, pygame.RLEACCEL)
        if scaleAmount != 1:
            image = pygame.transform.scale(image, (rectangle[2] * scaleAmount, rectangle[3] * scaleAmount))
        return image


class Hud:

    def __init__(self, gameWindow, windowSize,
                 titleFontFile='freesansbold.ttf', mainFontFile='freesansbold.ttf') -> None:
        self.score = 0
        self.lives = 3
        self.level = 1
        self.gameWindow = gameWindow
        self.windowSize = windowSize
        self.titleSize = 64
        self.mainSize = 24
        self.titleFont = pygame.font.Font(titleFontFile, self.titleSize)
        self.mainFont = pygame.font.Font(mainFontFile, self.mainSize)

    def main_menu(self, text, color, end=False, x_offset=0, y_offset=0) -> None:
        titleText = self.titleFont.render(text, True, color)
        if not end:
            instructText = self.mainFont.render("PRESS ENTER TO START", True, color)
        else:
            instructText = self.mainFont.render("PRESS ENTER TO RESTART", True, color)
            scoreText = self.mainFont.render(f"YOU MADE IT THROUGH {self.score} WAVES", True, color)
            scoreTextRect = scoreText.get_rect()
            scoreTextRect.center = self.windowSize[0] / 2 + x_offset, self.windowSize[1] / 2 + y_offset + 250
            self.gameWindow.blit(scoreText, scoreTextRect)
        titleTextRect = titleText.get_rect()
        instructTextRect = instructText.get_rect()
        titleTextRect.center = self.windowSize[0] / 2 + x_offset, self.windowSize[1] / 2 + y_offset
        instructTextRect.center = self.windowSize[0] / 2 + x_offset, self.windowSize[1] / 2 + y_offset + 150
        self.gameWindow.blit(titleText, titleTextRect)
        self.gameWindow.blit(instructText, instructTextRect)
        pygame.display.flip()

    def game_info(self, scoreLocation=0, levelLocation=0, livesLocation=0) -> None:
        scoreString = f"Waves Survived: {self.score}"
        scoreText = self.mainFont.render(scoreString, True, "red")
        scoreTextRect = scoreText.get_rect()
        scoreTextRect.topleft = 8, 8
        self.gameWindow.blit(scoreText, scoreTextRect)


class VectorManagement:
    def __init__(self, originCoords, targetCoords) -> None:
        try:
            self.unitVector = pygame.math.Vector2(targetCoords[0] - originCoords[0],
                                                  targetCoords[1] - originCoords[1]).normalize()
        except ValueError:
            self.unitVector = [1, 1]
        self.angle = angleFinder(self.unitVector)

    def invertDirection(self, axis) -> float:
        if axis.lower() == 'x':
            self.unitVector[0] = -self.unitVector[0]
            self.angle = angleFinder(self.unitVector)
            return self.unitVector[0]
        if axis.lower() == 'y':
            self.unitVector[1] = -self.unitVector[1]
            self.angle = angleFinder(self.unitVector)
            return self.unitVector[1]

    def updateTarget(self, originCoords, targetCoords) -> None:
        self.unitVector = pygame.math.Vector2(targetCoords[0] - originCoords[0],
                                              targetCoords[1] - originCoords[1]).normalize()
        self.angle = angleFinder(self.unitVector)

    def get_UnitVector(self) -> pygame.Vector2:
        return self.unitVector

    def get_Angle(self, units='degree') -> float:
        if units == 'degree':
            return self.angle
        if units == 'radian':
            return angleFinder(self.unitVector, 'radian')


def angleFinder(vector: tuple, units: str = 'degree') -> float:  # ONLY USE WITH LEFT HAND COORDS
    radians = math.atan2(-vector[1], vector[0])
    degrees = radians * (180 / math.pi) - 90
    if units == 'degree':
        return degrees
    if units == 'radian':
        return radians
