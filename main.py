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


# Sprite Stuff

tankSheet = mys.SpriteSheet("Assets/TanksSheet.png")
player = mys.Player(300, 300, tankSheet.image_at((48, 895, 390, 1330)))

# Sprite Groups
TankGroup = pygame.sprite.Group()
BulletGroup = pygame.sprite.Group()
AllSprites = pygame.sprite.Group()
AllSprites.add(player)


def main():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            global running
            running = False
            pygame.quit()
            sys.exit()
    keys = pygame.key.get_pressed()
    if keys[pygame.K_w]:
        player.y -= 300*dt
    if keys[pygame.K_s]:
        player.y += 300*dt
    if keys[pygame.K_SPACE]:
        player.shoot(pygame.mouse.get_pos())
    gamewindow.fill("black")
    update()
    gamewindow.blit(player.image, player.rect)
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
