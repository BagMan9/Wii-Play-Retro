import sys
import pygame

import objects as mys

# Initialization
pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True
dt = 0

# Sprite Groups
TankGroup = pygame.sprite.Group()
BulletGroup = pygame.sprite.Group()
AllSprites = pygame.sprite.Group()


def main():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            global running
            running = False
            pygame.quit()
            sys.exit()
    screen.fill("white")
    update()
    clock.tick(60)


def update():
    TankGroup.update()
    BulletGroup.update()
    AllSprites.update()
    TankGroup.draw(screen)
    BulletGroup.draw(screen)
    AllSprites.draw(screen)
    pygame.display.flip()


if __name__ == "__main__":
    while running:
        main()

pygame.quit()
