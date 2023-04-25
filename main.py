import sys
import pygame
import wiiplaytanks as mys


# Initialization
pygame.init()
gamewindow = pygame.display.set_mode((1280, 720))
pygame.display.set_caption("WiiPlay Retro")
clock = pygame.time.Clock()
running = True
dt = .01
gamestate = 0
Title_Font = pygame.font.Font('freesansbold.ttf', 64)

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
    global gamestate
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
    if gamestate == 0:
        if keys[pygame.K_SPACE]:
            gamestate = 1

        gamewindow.fill("black")

        Title_Text = Title_Font.render("Wii Play Retro", True, "orange")
        Title_Text_Rect = Title_Text.get_rect()
        Title_Text_Rect.center = 1280/2, 720/2
        gamewindow.blit(Title_Text, Title_Text_Rect)

        pygame.display.flip()

    if gamestate == 1:
        if keys[pygame.K_w]:
            player.y -= 300*dt
        if keys[pygame.K_s]:
            player.y += 300*dt
        if keys[pygame.K_SPACE]:
            player.shoot(pygame.mouse.get_pos(), BulletGroup)
        gamewindow.fill("white")
        update()
        clock.tick(60)


def update():
    TankGroup.update()
    BulletGroup.update()
    AllSprites.update()
    TankGroup.draw(gamewindow)
    BulletGroup.draw(gamewindow)
    AllSprites.draw(gamewindow)
    pygame.display.flip()


if __name__ == "__main__":
    while running:
        main()

pygame.quit()
