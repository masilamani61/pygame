import pygame
from pygame import mixer
import random
import math
pygame.init()
screen = pygame.display.set_mode((800, 600))
running = True
pygame.display.set_caption('space invader')
icon = pygame.image.load('space invader/alien (1).png')
pygame.display.set_icon(icon)
playerimg = pygame.image.load('space invader/space (2).png')

mixer.music.load('space invader/bleeps-and-bloops-classic-arcade-game-116838.mp3')
mixer.music.play(-1)

playerx = 370
playery = 480
playerxchange = 0
score = 0
font = pygame.font.Font('freesansbold.ttf', 12)
textx = 10
texty = 10

overfont = pygame.font.Font('freesansbold.ttf', 64)

bulletimg = pygame.image.load('space invader/bullet.png')
bulletx = 0
bullety = 480
bulletxchange = 0
bulletychange = 5
bullet_state = 'ready'
enemyimg = []
enemyx = []
enemyy = []
enemyxchange = []
enemyychange = []
for i in range(6):

    enemyimg.append(pygame.image.load('space invader/alien (1).png'))
    enemyx.append(random.randint(0, 735))
    enemyy.append(random.randint(50, 150))
    enemyxchange.append(0.6)
    enemyychange.append(30)
backgroundimg = pygame.image.load("space invader/2299682.jpg")


def gameover():
    overtext = overfont.render('GAME OVER', True, (255, 255, 255))
    screen.blit(overtext, (175, 250))


def score2(x, y):
    score1 = font.render('Score :' + str(score), True, (255, 255, 255))
    screen.blit(score1, (x, y))


def enemy(x, y, i1):
    screen.blit(enemyimg[i1], (x, y))


def player(x, y):
    screen.blit(playerimg, (x, y))


def bullet(x, y):
    global bullet_state
    bullet_state = 'fire'
    screen.blit(bulletimg, (x+16, y+10))


def collision(enemyx1, enemyy1, bullety1, bulletyx1):
    distance = math.sqrt((math.pow(enemyx1 - bullety1, 2) + math.pow(enemyy1 - bulletyx1, 2)))

    if distance <= 27:
        return True
    else:
        return False


while running:
    screen.fill((0, 0, 0))
    screen.blit(backgroundimg, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerxchange = -0.7
            if event.key == pygame.K_RIGHT:
                playerxchange = 0.7
            if event.key == pygame.K_SPACE:
                if bullet_state == 'ready':
                    bulletsound = mixer.Sound('space invader/gun-shots-from-a-distance-14-39756.mp3')
                    bulletsound.play()
                    bulletx = playerx
                    bullet(playerx, bullety)
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerxchange = 0

    playerx = playerx+playerxchange
    if playerx <= 0 or playerx >= 736:
        playerxchange = 0
    player(playerx, playery)
    for i in range(6):
        if enemyy[i] > 440:
            for j in range(6):
                enemyy[j] = 2000
            gameover()
            break

        enemyx[i] = enemyx[i]+enemyxchange[i]
        if enemyx[i] <= 0:
            enemyxchange[i] = 1
            enemyy[i] = enemyy[i]+enemyychange[i]
        if enemyx[i] >= 736:
            enemyxchange[i] = -1
            enemyy[i] = enemyy[i]+enemyychange[i]
        collisiona = collision(enemyx[i], enemyy[i], bulletx, bullety)
        if collisiona is True:
            bullety = 480
            bullet_state = 'ready'
            enemyx[i] = random.randint(0, 735)
            enemyy[i] = random.randint(50, 150)

            score = score + 1
        enemy(enemyx[i], enemyy[i], i)

    if bullet_state == 'fire':
        bullet(bulletx, bullety)
        bullety = bullety-bulletychange
    if bullety < 0:
        bullety = 480
        bullet_state = 'ready'
    score2(textx, texty)
    pygame.display.update()