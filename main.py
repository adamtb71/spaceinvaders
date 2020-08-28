import random
import math
import pygame
from pygame import mixer


# init will initilize the pygame
pygame.init()

# create the screen, this is the width and the hight
screen = pygame.display.set_mode((800, 600))
# background
background = pygame.image.load('space_background.jpg')
#background sound
# something needst to go here
# title and Icon
pygame.display.set_caption("Death Star Defense")
icon = pygame.image.load('death_star.png')
pygame.display.set_icon(icon)

# Enemy

enemy_stat_movement = 2.1

enemyImg = []
enemyX = []
enemyY = []
# this chooses 2 random directions for the enemy to go in

enemyX_change = []
enemyY_change = []
num_of_enemies = 6
for i in range(num_of_enemies):
    enemyImg.append(pygame.image.load('enemy.png'))
    enemyX.append(random.randint(0, 736))
    enemyY.append(random.randint(50, 350))
    # this chooses 2 random directions for the enemy to go in
    enemyX_change.append(enemy_stat_movement)
    enemyY_change.append(40)

# Ready - you can't see the bullet on the screen
bulletImg = pygame.image.load('laser.png')
bulletX = 0
bulletY = 480
bulletX_change = 0
bulletY_change = 5
bullet_state = "ready"

playerImg = pygame.image.load('player.png')
playerX = 370
playerY = 480
playerX_change = 0

#Score
score_value = 0
font = pygame.font.Font('Starjedi.ttf',32)

textX = 10
textY = 5

#game over text
over_font = pygame.font.Font('Starjedi.ttf',64)

def game_over_text():
    over_text = font.render("game over", True, (255, 0, 0))
    screen.blit(over_text, (350,250))


def show_score(x,y):
    score = font.render("Score :" + str(score_value), True, (255,0,0))
    screen.blit(score, (x, y))




def player(x, y):
    # This draws the player
    screen.blit(playerImg, (x, y))


def enemy(x, y,i):
    # This draws the player
    screen.blit(enemyImg[i], (x, y))


def fire_bullet(x, y):
    global bullet_state
    bullet_state = "fire"
    screen.blit(bulletImg, (x + 16, y + 10))


def isCollision(enemyX, enemyY, bulletX, bulletY):
    distance = math.sqrt((math.pow(enemyX - bulletX, 2)) + (math.pow(enemyY - bulletY, 2)))
    if distance < 35:
        return True


# Game looop, makes sure window is running always
running = True
while running:
    # sets the screen to be a color
    screen.fill((255, 255, 255))
    # background image
    screen.blit(background, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        # if keystroak is pressed check weather it's right or left
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                playerX_change = -3
            if event.key == pygame.K_RIGHT:
                playerX_change = 3
            if event.key == pygame.K_SPACE:
                if bullet_state is "ready":
                    #bullet_sound = mixer.Sound('laser.wav')
                    #bullet_sound.play()
                    # get the current x cordinate for the spaceship
                    bulletX = playerX
                    fire_bullet(bulletX, bulletY)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                playerX_change = 0

    # checking for boundries of spaceship
    playerX += playerX_change
    if playerX <= 0:
        playerX = 0
    elif playerX >= 736:
        playerX = 736


    for i in range(num_of_enemies):

        #Game Over
        if enemyY[i] >450:
            for j in range(num_of_enemies):
                enemyY[j] = 2000
            game_over_text()
            break
        enemyX[i] += enemyX_change[i]
        if enemyX[i] <= 0:
            enemyX_change[i] = 2.1
            enemyY[i] += enemyY_change[i]
        elif enemyX[i] >= 736:
            enemyX_change[i] = -2.1
            enemyY[i] += enemyY_change[i]
        # collision
        collision = isCollision(enemyX[i], enemyY[i], bulletX, bulletY)
        if collision:
            bulletY = 480
            bullet_state = "ready"
            score_value += 1
            #Add more enemeis

            enemyX[i] = random.randint(0, 736)
            enemyY[i] = random.randint(50, 400)

        enemy(enemyX[i], enemyY[i],i)

    #increase dificulty



    # bullet movment
    if bulletY <= 0:
        bulletY = 480
        bullet_state = "ready"

    if bullet_state is "fire":
        fire_bullet(bulletX, bulletY)
        bulletY -= bulletY_change



    player(playerX, playerY)
    show_score(textX,textY)

    pygame.display.update()
