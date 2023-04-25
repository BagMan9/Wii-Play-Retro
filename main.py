import sys
import pygame
import wiiplaytanks as mys


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
hud = mys.Hud(gameWindow, windowSize)

# Sprite

# Sprite Groups
TankGroup = pygame.sprite.Group()
BulletGroup = pygame.sprite.Group()
AllSprites = pygame.sprite.Group()

# Sprite Sheets

tankSheet = mys.SpriteSheet("Assets/TanksSheet.png")

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

        hud.main_menu("Wii Play Retro", "orange")

        pygame.display.flip()

    if gameState == 1:
        if keys[pygame.K_w]:
            player.y -= 300*dt
        if keys[pygame.K_s]:
            player.y += 300*dt
        if keys[pygame.K_SPACE]:
            player.shoot(pygame.mouse.get_pos(), BulletGroup)
        gameWindow.fill("white")
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
