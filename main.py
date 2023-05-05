from sys import exit

import pygame

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
running = True
dt = .01
gameStage = 0
hud = Hud(gameWindow, windowSize, titleFontFile="Assets/fonts/FOT-NewRodin Pro EB.otf",
          mainFontFile="Assets/fonts/FOT-NewRodin Pro EB.otf")

# Sprite Vars
tankSheet = SpriteSheet("Assets/TanksSheet.png")

AllSprites = pygame.sprite.Group()
TankGroup = pygame.sprite.LayeredUpdates()
PlayerGroup = pygame.sprite.Group()
PlayerBulletGroup = pygame.sprite.Group()
EnemyBulletGroup = pygame.sprite.Group()
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
            title_screen(keys)

        if gameStage == 1:
            if not started:
                player = mys.Player(300, 300, playerTankBaseImg, playerTankTurretImg, TankGroup)
                TankGroup.add(player)
                TankGroup.move_to_back(player)
                PlayerGroup.add(player)
                started = True
            player_movement(player, keys)
            pygame.sprite.groupcollide(BombGroup, PlayerBulletGroup, True, True)
            pygame.sprite.groupcollide(ExplosionSpriteGroup, TankGroup, False, True)
            pygame.sprite.groupcollide(TankGroup, EnemyBulletGroup, True, True)
            gameWindow.fill("white")
            hud.score = len(PlayerBulletGroup)
            hud.game_info()
            if not PlayerGroup:
                gameStage = -1

        if gameStage == -1:
            gameWindow.fill("black")
            hud.main_menu("Game Over", "red")
        update()
        clock.tick(60)


def title_screen(keys) -> None:
    global gameStage
    if keys[pygame.K_RETURN]:
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
    if keys[pygame.K_SPACE] and len(PlayerBulletGroup) <= 2:
        sprite.bulletShoot(bulletSpriteImg, PlayerBulletGroup, EnemyBulletGroup, AllSprites)


if __name__ == "__main__":
    main()

pygame.quit()
