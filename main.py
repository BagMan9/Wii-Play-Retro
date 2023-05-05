from sys import exit

import pygame

import wiiplaytanks as mys
from basic import Hud, SpriteSheet

# Initialization
pygame.init()
verticalResolution = 720
aspectRatio = 16 / 9
windowSize = verticalResolution * aspectRatio, verticalResolution
gameWindow = pygame.display.set_mode(windowSize)
pygame.display.set_caption("WiiPlay Retro")
clock = pygame.time.Clock()
running = True
dt = .01
gameState = 0
hud = Hud(gameWindow, windowSize, titleFontFile="Assets/fonts/FOT-NewRodin Pro EB.otf")

# Sprite Vars
tankSheet = SpriteSheet("Assets/TanksSheet.png")

AllSprites = pygame.sprite.Group()
TankGroup = pygame.sprite.LayeredUpdates()
PlayerGroup = pygame.sprite.Group()
BulletGroup = pygame.sprite.Group()
BombGroup = pygame.sprite.Group()
ExplosionSpriteGroup = pygame.sprite.Group()

playerTankBaseImg = pygame.transform.rotate(tankSheet.image_at((647, 928, 333, 375), 20), 270)
playerTankTurretImg = tankSheet.image_at((1092, 884, 159, 328), 20)
bulletSpriteImg = tankSheet.image_at((414, 419, 17, 66), 40)
testImg = pygame.transform.scale(pygame.image.load("Assets/testimg.png"), (159 * .25, 328 * .25))
bombSpriteImg = pygame.transform.scale(pygame.image.load("Assets/bomb.png"), (64, 64))
bombSpriteImg_Red = pygame.transform.scale(pygame.image.load("Assets/bomb-red.png"), (64, 64))


started = False


# noinspection PyUnboundLocalVariable
def main() -> None:
    global running
    global started
    while running:
        global gameState
        # Quit Checking
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                pygame.quit()
                exit()
        # Grabbing player input
        keys = pygame.key.get_pressed()

        # Title Screen
        if gameState == 0:
            title_screen(keys)

        if gameState == 1:
            if not started:
                player = mys.Player(300, 300, playerTankBaseImg, playerTankTurretImg, TankGroup)
                TankGroup.add(player)
                TankGroup.move_to_back(player)
                PlayerGroup.add(player)
                started = True
            player_movement(player, keys)
            pygame.sprite.groupcollide(BombGroup, BulletGroup, True, True)
            pygame.sprite.groupcollide(ExplosionSpriteGroup, TankGroup, False, True)
            pygame.sprite.groupcollide(TankGroup, BulletGroup, False, False)
            gameWindow.fill("white")
            hud.score = len(BulletGroup)
            hud.game_info()
            if not PlayerGroup:
                gameState = -1

        if gameState == -1:
            gameWindow.fill("black")
            hud.main_menu("Game Over", "red")
        update()
        clock.tick(60)


def title_screen(keys) -> None:
    global gameState
    if keys[pygame.K_SPACE]:
        gameState = 1

    gameWindow.fill("black")
    hud.main_menu("Wii Play Retro", "orange", y_offset=-100)


def update() -> None:
    TankGroup.update()
    TankGroup.draw(gameWindow)
    AllSprites.update()
    AllSprites.draw(gameWindow)
    pygame.display.flip()


def player_movement(sprite: mys.Player, keys) -> None:
    moveAmount = 300
    if keys[pygame.K_w]:
        sprite.y -= moveAmount * dt
    if keys[pygame.K_s]:
        sprite.y += moveAmount * dt
    if keys[pygame.K_a]:
        sprite.x -= moveAmount * dt
    if keys[pygame.K_d]:
        sprite.x += moveAmount * dt
    if keys[pygame.K_b] and len(BombGroup) < 1:
        sprite.bombShoot(bombSpriteImg, bombSpriteImg_Red, BombGroup, ExplosionSpriteGroup, AllSprites)
    if keys[pygame.K_SPACE] and len(BulletGroup) <= 2:
        sprite.bulletShoot(bulletSpriteImg, BulletGroup, AllSprites)


if __name__ == "__main__":
    main()

pygame.quit()
