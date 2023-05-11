import random
from sys import exit
import os
import sys
import pygame
from math import ceil
import wiiplaytanks as mys
from basic import Hud, SpriteSheet

# Initialization
pygame.init()
pygame.mixer.init()
verticalResolution = 720
aspectRatio = 16 / 9
windowSize = verticalResolution * aspectRatio, verticalResolution
gameWindow = pygame.display.set_mode(windowSize)
pygame.display.set_caption("WiiPlay Retro")
clock = pygame.time.Clock()
gameStarted = False
running = True
looped = False
dt = 0.01
completed = False
gameStage = 0
levelStarted = False
prevFireTime = 99999999
hud = Hud(
    gameWindow,
    windowSize,
    titleFontFile="Assets/fonts/FOT-NewRodin Pro EB.otf",
    mainFontFile="Assets/fonts/FOT-NewRodin Pro EB.otf",
)

# Sprite Vars
tankSheet = SpriteSheet("Assets/TanksSheet.png")

AllSprites = pygame.sprite.Group()
TankGroup = pygame.sprite.LayeredUpdates()
EnemyTankGroup = pygame.sprite.LayeredUpdates()
PlayerGroup = pygame.sprite.Group()
PlayerBulletGroup = pygame.sprite.Group()
EnemyBulletGroup = pygame.sprite.Group()
BombGroup = pygame.sprite.Group()
ExplosionSpriteGroup = pygame.sprite.Group()
WallGroup = pygame.sprite.Group()

playerTankBaseImg = pygame.transform.rotate(
    tankSheet.image_at((647, 928, 333, 375), 15), 270
)
playerTankTurretImg = tankSheet.image_at((1092, 884, 159, 328), 15)
bulletSpriteImg = tankSheet.image_at((414, 419, 17, 66), 30)
testImg = pygame.transform.scale(
    pygame.image.load("Assets/testimg.png"), (159 * 0.25, 328 * 0.25)
)
bombSpriteImg = pygame.transform.scale(pygame.image.load("Assets/bomb.png"), (48, 48))
bombSpriteImg_Red = pygame.transform.scale(
    pygame.image.load("Assets/bomb-red.png"), (48, 48)
)
hayBaleScalar = 0.2
hayBale = pygame.transform.scale(
    pygame.image.load("Assets/haybale_crop.png"),
    (421 * hayBaleScalar, 254 * hayBaleScalar),
)

# Sounds
fire = pygame.mixer.Sound("Assets/Sound Effects/norm_fire.wav")
explode_sound = pygame.mixer.Sound("Assets/Sound Effects/explosion.wav")
pygame.mixer.music.load("Assets/Music/Tanks Main BGM.mp3")


# noinspection PyUnboundLocalVariable
def main() -> None:
    global running
    global gameStarted
    global looped
    global completed
    hud.score = 0
    while running:
        global gameStage
        # Quit Checking
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                exit()
        # Grabbing player input
        keys = pygame.key.get_pressed()

        # Title Screen
        if gameStage == 0:
            if pygame.mixer.music.get_busy():
                pygame.mixer.music.stop()
            title_screen(keys)
            completed = False
            played = False

        if gameStage == 1:
            if not pygame.mixer.music.get_busy() and not looped:
                pygame.mixer.music.load("Assets/Music/BGM Loop.mp3")
                pygame.mixer.music.play(-1)
                looped = True
            if not gameStarted:
                player = mys.Player(
                    300, 300, playerTankBaseImg, playerTankTurretImg, TankGroup
                )
                TankGroup.add(player.tankTurret)
                TankGroup.add(player)
                TankGroup.move_to_back(player)
                PlayerGroup.add(player)
                gameStarted = True
                x_offset = 0
                for _ in range(3):
                    target = mys.Target(
                        hayBale,
                        600 + x_offset,
                        1,
                        0,
                        4,
                        0,
                        0,
                        ExplosionSpriteGroup,
                        AllSprites,
                    )
                    EnemyTankGroup.add(target)
                    AllSprites.add(target)
                    x_offset += 100

            if not PlayerGroup:
                gameStage = -1
            if len(EnemyTankGroup) == 0:
                hud.score += 1
                gameStarted = False
                gameStage = 1.1
            player_movement(player, keys)
            gameWindow.fill("white")
            hud.game_info()
        if gameStage == 1.1:
            if not gameStarted:
                x_offset = 50
                for _ in range(5):
                    target = mys.Target(
                        hayBale,
                        300 + x_offset + random.randrange(-25, 26),
                        1,
                        random.randrange(-2, 2),
                        4,
                        0,
                        0,
                        ExplosionSpriteGroup,
                        AllSprites,
                    )
                    EnemyTankGroup.add(target)
                    AllSprites.add(target)
                    x_offset += 50
                gameStarted = True
            if not PlayerGroup:
                gameStage = -1
            if len(EnemyTankGroup) == 0:
                hud.score += 1
                gameStarted = False
                gameStage = 1.2
            player_movement(player, keys)
            gameWindow.fill("white")
            hud.game_info()
        if gameStage == 1.2:
            if not gameStarted:
                x_offset = 25
                for _ in range(5):
                    target = mys.Target(
                        hayBale,
                        400 + x_offset + random.randrange(-150, 150),
                        1,
                        random.randrange(-10, 10),
                        random.randrange(-10, 10),
                        0,
                        0,
                        ExplosionSpriteGroup,
                        AllSprites,
                    )
                    EnemyTankGroup.add(target)
                    AllSprites.add(target)
                    x_offset += 50
                gameStarted = True
            if not PlayerGroup:
                gameStage = -1
            if len(EnemyTankGroup) == 0:
                hud.score += 1
                gameStarted = False
                gameStage = 1.3
            player_movement(player, keys)
            gameWindow.fill("white")
            hud.game_info()
        if gameStage == 1.3:
            if not gameStarted:
                x_offset = 25
                for _ in range(9):
                    target = mys.Target(
                        hayBale,
                        400 + x_offset + random.randrange(-350, 350),
                        1,
                        random.randrange(-5, 5),
                        random.randrange(-5, 5),
                        random.randrange(-1, 2),
                        0,
                        ExplosionSpriteGroup,
                        AllSprites,
                    )
                    EnemyTankGroup.add(target)
                    AllSprites.add(target)
                    x_offset += 50
                gameStarted = True
            if not PlayerGroup:
                gameStage = -1
            if len(EnemyTankGroup) == 0:
                hud.score += 1
                gameStarted = False
                gameStage = 2
            player_movement(player, keys)
            gameWindow.fill("white")
            hud.game_info()

        pygame.sprite.groupcollide(BombGroup, PlayerBulletGroup, True, True)
        pygame.sprite.groupcollide(ExplosionSpriteGroup, TankGroup, False, True)
        pygame.sprite.groupcollide(TankGroup, EnemyTankGroup, True, True)
        pygame.sprite.groupcollide(TankGroup, EnemyBulletGroup, True, True)
        pygame.sprite.groupcollide(PlayerBulletGroup, EnemyTankGroup, True, True)
        pygame.sprite.groupcollide(EnemyBulletGroup, EnemyTankGroup, True, True)
        if gameStage == -1:
            AllSprites.empty()
            if not played:
                pygame.mixer.music.stop()
                pygame.mixer.music.load("Assets/Music/Round Failure.mp3")
                pygame.mixer.music.play()
                played = True
            gameWindow.fill("black")
            hud.main_menu("Game Over", "red", True)
            if keys[pygame.K_RETURN]:
                os.execl(sys.executable, sys.executable, *sys.argv)

        if gameStage == 2:
            AllSprites.empty()
            player.kill()
            if not played:
                pygame.mixer.music.stop()
                pygame.mixer.music.load("Assets/Music/Super BGM Loop.mp3")
                pygame.mixer.music.play()
                played = True
            gameWindow.fill("black")
            hud.main_menu("You win!", "green", True)
            if keys[pygame.K_RETURN]:
                os.execl(sys.executable, sys.executable, *sys.argv)
        update()

        clock.tick(60)


def title_screen(keys) -> None:
    global gameStage
    if keys[pygame.K_RETURN]:
        pygame.mixer.music.play()
        gameStage = 1

    gameWindow.fill("black")
    hud.main_menu("Wii Play: Tanks!", "orange", y_offset=-100)


def update() -> None:
    TankGroup.update()
    TankGroup.draw(gameWindow)
    AllSprites.update()
    AllSprites.draw(gameWindow)
    pygame.display.flip()


def player_movement(sprite: mys.Player, keys) -> None:
    moveAmount = 300
    offset = 2
    if keys[pygame.K_w]:
        sprite.y -= moveAmount * dt
    if keys[pygame.K_s]:
        sprite.y += moveAmount * dt
    if keys[pygame.K_a]:
        sprite.x -= moveAmount * dt
    if keys[pygame.K_d]:
        sprite.x += moveAmount * dt
    if keys[pygame.K_b] and len(BombGroup) < 1:
        sprite.bombShoot(
            bombSpriteImg,
            bombSpriteImg_Red,
            BombGroup,
            ExplosionSpriteGroup,
            AllSprites,
            explode_sound,
        )
    if keys[pygame.K_SPACE] and len(PlayerBulletGroup) <= 2:
        sprite.bulletShoot(
            bulletSpriteImg,
            PlayerBulletGroup,
            False,
            EnemyBulletGroup,
            AllSprites,
            fire,
        )


if __name__ == "__main__":
    main()

pygame.quit()
