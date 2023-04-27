import sys
import pygame
import wiiplaytanks as mys
from basic import SpriteSheet, Hud


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
hud = Hud(gameWindow, windowSize, titleFontFile="Assets/fonts/FOT-NewRodin Pro EB.otf")

# Sprite

# Sprite Groups
TankGroup = pygame.sprite.Group()
BulletGroup = pygame.sprite.Group()
AllSprites = pygame.sprite.Group()

# Sprite + Images

tankSheet = SpriteSheet("Assets/TanksSheet.png")
player = mys.Player(300, 300, tankSheet.image_at((647, 928, 333, 375)),
                    tankSheet.image_at((1090, 884, 157, 328)))
bulletSprite = pygame.transform.scale(tankSheet.image_at((414, 419, 17, 66)), (5, 19.4))
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

    if gameState == 1:
        player_movement(player, keys)
        gameWindow.fill("white")
        hud.score = len(BulletGroup)
        hud.game_info()
        update()
    clock.tick(60)


def update():
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
        sprite.bulletShoot(bulletSprite, pygame.mouse.get_pos(), BulletGroup, AllSprites)


if __name__ == "__main__":
    while running:
        main()

pygame.quit()
