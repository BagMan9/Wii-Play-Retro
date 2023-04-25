import sys
import pygame
import wiiplaytanks as mys


class SpriteSheet(object):

    def __init__(self, filename):
        self.sheet = pygame.image.load(filename).convert()

    def image_at(self, rectangle, colorKey=None):
        rect = pygame.Rect(rectangle)
        image = pygame.Surface(rect.size).convert()
        image.blit(self.sheet, (0, 0), rect)
        if colorKey is not None:
            if colorKey == -1:
                colorKey = image.get_at((0, 0))
            image.set_colorkey((colorKey, pygame.RLEACCEL))
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

    def game_info(self, scoreLocation=0, levelLocation=0, livesLocation=0):
        scoreString = f"Score: {self.score}"
        scoreText = self.mainFont.render(scoreString, True, "red")
        scoreTextRect = scoreText.get_rect()
        scoreTextRect.topleft = 8, 8
        self.gameWindow.blit(scoreText, scoreTextRect)


# Initialization
pygame.init()
verticalResolution = 720
windowSize = verticalResolution * (16 / 9), verticalResolution
gameWindow = pygame.display.set_mode(windowSize)
pygame.display.set_caption("WiiPlay Retro")
clock = pygame.time.Clock()
running = True
dt = .01
gameState = 0
Title_Font = pygame.font.Font('freesansbold.ttf', 64)
hud = Hud(gameWindow, windowSize, titleFontFile="Assets/fonts/FOT-NewRodin Pro EB.otf")

# Sprite

# Sprite Groups
TankGroup = pygame.sprite.Group()
BulletGroup = pygame.sprite.Group()
AllSprites = pygame.sprite.Group()

# Sprite Sheets

tankSheet = SpriteSheet("Assets/TanksSheet.png")

# Player Spawn
player = mys.Player(300, 300, tankSheet.image_at((60, 895, 330, 410)))
AllSprites.add(player)


def main():
    global gameState
    # Quit Checking
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            global running
            running = False
            pygame.quit()
            sys.exit()
    # Grabbing player input
    keys = pygame.key.get_pressed()

    # Title Screen
    if gameState == 0:
        if keys[pygame.K_SPACE]:
            gameState = 1

        gameWindow.fill("black")

        hud.main_menu("Wii Play Retro", "orange", y_offset=-100)

        pygame.display.flip()

    if gameState == 1:
        if keys[pygame.K_w]:
            player.y -= 300*dt
        if keys[pygame.K_s]:
            player.y += 300*dt
        if keys[pygame.K_SPACE]:
            player.shoot(pygame.mouse.get_pos(), BulletGroup)
        gameWindow.fill("white")
        hud.score = len(BulletGroup)
        hud.game_info()
        update()
    clock.tick(60)


def update():
    TankGroup.update()
    BulletGroup.update()
    AllSprites.update()
    TankGroup.draw(gameWindow)
    BulletGroup.draw(gameWindow)
    AllSprites.draw(gameWindow)
    pygame.display.flip()


if __name__ == "__main__":
    while running:
        main()

pygame.quit()
