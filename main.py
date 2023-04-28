import sys
import pygame
import wiiplaytanks as mys
from basic import SpriteSheet, Hud


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

TankGroup = pygame.sprite.LayeredUpdates()
BulletGroup = pygame.sprite.Group()
AllSprites = pygame.sprite.Group()

playerTankBaseImg = tankSheet.image_at((647, 928, 333, 375), 25)
playerTankTurretImg = tankSheet.image_at((1092, 884, 159, 328), 25)
bulletSpriteImg = tankSheet.image_at((414, 419, 17, 66), 50)
testImg = pygame.transform.scale(pygame.image.load("Assets/testimg.png"), (159*.25, 328*.25))

player = mys.Player(300, 300, playerTankBaseImg, playerTankTurretImg, TankGroup)
TankGroup.add(player)
TankGroup.move_to_back(player)


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
        title_screen(keys)

    if gameState == 1:
        player_movement(player, keys)
        # pygame.sprite.groupcollide(BulletGroup, TankGroup, True, True)
        gameWindow.fill("white")
        hud.score = len(BulletGroup)
        hud.game_info()
        update()
    clock.tick(60)


def title_screen(keys):
    global gameState
    if keys[pygame.K_SPACE]:
        gameState = 1

    gameWindow.fill("black")
    hud.main_menu("Wii Play Retro", "orange", y_offset=-100)


def update():
    TankGroup.update()
    TankGroup.draw(gameWindow)
    AllSprites.update()
    AllSprites.draw(gameWindow)
    pygame.display.flip()


def player_movement(sprite, keys):
    if keys[pygame.K_w]:
        sprite.y -= 300 * dt
    if keys[pygame.K_s]:
        sprite.y += 300 * dt
    if keys[pygame.K_a]:
        sprite.x -= 300 * dt
    if keys[pygame.K_d]:
        sprite.x += 300 * dt
    if keys[pygame.K_SPACE]:
        if len(BulletGroup) <= 2:
            sprite.bulletShoot(bulletSpriteImg, pygame.mouse.get_pos(), BulletGroup, AllSprites)


if __name__ == "__main__":
    while running:
        main()

pygame.quit()
