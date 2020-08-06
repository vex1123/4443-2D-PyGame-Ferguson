#animal sprites from whtdragon on rpgmaker forums, used with permission
#bullet sprites and background from freepik.com edited by myself
#target dummy sprite from maplestory


import sys
import os
import pprint
import pygame
import math

#initialize pygame
pygame.init()

#create window x by y
screen = pygame.display.set_mode((1600,600))

#change window title and icon
pygame.display.set_caption("Corgi Run")
mydir = os.path.dirname(__file__) 
icon = pygame.image.load(os.path.join(mydir, 'dog.png'))
pygame.display.set_icon(icon)

#define backgrounds
bg = pygame.image.load(os.path.join(mydir, 'mountain_bg.jpg'))
bgbottom = pygame.image.load(os.path.join(mydir, 'bottom_BGnew.png'))
ob1 = pygame.image.load(os.path.join(mydir, "hill_small.png"))
#character sprite animation lists
walkRight = [pygame.image.load(os.path.join(mydir, 'CorgiRN.png')),pygame.image.load(os.path.join(mydir,'CorgiR1.png')), pygame.image.load(os.path.join(mydir,'CorgiR2.png'))]
walkLeft = [pygame.image.load(os.path.join(mydir, 'CorgiLN.png')),pygame.image.load(os.path.join(mydir,'CorgiL1.png')), pygame.image.load(os.path.join(mydir,'CorgiL2.png'))]
bulletShoot = [pygame.image.load(os.path.join(mydir, 'Bullet1.png')), pygame.image.load(os.path.join(mydir, 'Bullet2.png')), pygame.image.load(os.path.join(mydir, 'Bullet3.png'))]
bulletsplosion = [pygame.image.load(os.path.join(mydir, 'Bulletsplosion1.png')), pygame.image.load(os.path.join(mydir, 'Bulletsplosion2.png')), pygame.image.load(os.path.join(mydir, 'Bulletsplosion3.png'))]
catRight = [pygame.image.load(os.path.join(mydir, 'CatRN.png')), pygame.image.load(os.path.join(mydir, 'CatR1.png')), pygame.image.load(os.path.join(mydir, 'CatR2.png'))]
catLeft = [pygame.image.load(os.path.join(mydir, 'CatLN.png')), pygame.image.load(os.path.join(mydir, 'CatL1.png')), pygame.image.load(os.path.join(mydir, 'CatL2.png'))]
target = pygame.image.load(os.path.join(mydir, "dummy2.png"))

#clock
clock = pygame.time.Clock()



#player data

playerX = 100
playerY = 480
playervel = 24
playerW = 48
playerH = 26
left = False
right = False
alive = True
#rectangle hitbox

#experimental shooting up code
up = False
walkCount = 0
#used to help face correct direction after stopping input
standing = True
facing = 1
#used in determining if you get hit
hit = False

#jump stuff
isjump = False
jumpcount = 10

#bullet stuff
shotcount = 0
splosion = 0
shoot = False
upShoot = False
rShoot = False
lShoot = False
shot = False
bulletX = playerX
bulletY = playerY
bulletVel = 15

#enemy cat here to touch you
catCount = 0
catX = 500
catY = 468
catVel = 3
catW = 51
catH = 42
catStanding = False
Cleft = False
Cright = False
gone = False

#dummy here to stand in place/ wiggle
dummyX = 1200
dummyY = 430
idle = True

def redrawWindow():
    #add global variables
    global alive
    global playerY
    global playerX
    global walkCount
    global shotcount
    global bulletCount
    global catCount
    global bulletX
    global bulletY
    global shoot
    global upShoot
    global lShoot
    global rShoot
    global shot
    global splosion
    global catStanding
    global Cright
    global Cleft
    global idle
    #create background in window
    screen.blit(bg, (0,0))
    screen.blit(bgbottom, (0, 500))
    screen.blit(ob1, (400, 409))
    #initialise animations index overflow preventions
    if walkCount  >= 18:
        walkCount = 0
    if shotcount >= 18:
        shotcount = 0
    if splosion >= 18:
        splosion = 0
    if catCount >= 18:
        catCount = 0
    #hitbox for player
    hbp = pygame.Surface((49,27))  # the size of your rect
    hbp.set_alpha(128)                # alpha level
    hbp.fill((255,255,255))           # this fills the entire surface
    screen.blit(hbp, (playerX,playerY))    # (0,0) are the top-left coordinates
    #player walking code
    if not standing:
        if left:
            screen.blit(walkLeft[walkCount//6],(playerX, playerY))
            walkCount += 1
        elif right:
            screen.blit(walkRight[walkCount//6], (playerX, playerY))
            walkCount +=1
    else:
        if right:
            screen.blit(walkRight[0], (playerX,playerY))
        else:
            screen.blit(walkLeft[0], (playerX, playerY))

##shooting animation code
    #bullet starting  X and Y updates
    if not shoot:
        bulletX = playerX
        bulletY = playerY

    if shoot:
        hbp = pygame.Surface((30,30))  # the size of your rect
        hbp.set_alpha(128)                # alpha level
        hbp.fill((255,255,255))           # this fills the entire surface
        screen.blit(hbp, (bulletX,bulletY))    # (0,0) are the top-left coordinates
        #check if shooting up and prevent bullet direction change
        if up and not lShoot and not rShoot:
            upShoot = True
        if upShoot:
            bulletY -= bulletVel 
        #check if  not shooting up and prevent bullet direction change
            
        elif not upShoot:
            if facing > 0 and not lShoot:
                rShoot = True
            if rShoot and not lShoot:
                bulletX += bulletVel * 1
                shootX = bulletX
            if facing < 0 and not rShoot:
                lShoot = True
            if lShoot and not rShoot:
                bulletX += bulletVel * -1
            

        

        #bullet animation code and bounds checking
        if bulletX < 1500 and bulletX > 5 and bulletY > 20 and bulletY < 550 :
            screen.blit(bulletShoot[shotcount//6], (bulletX,bulletY))
            shotcount +=1
        else:
            screen.blit(bulletsplosion[splosion//6], (bulletX,bulletY - 35))
            splosion +=1
            shoot = False
            upShoot = False
            lShoot = False
            rShoot = False
            shot = False
            bulletX = playerX
            playerY = 480
            bulletY = playerY

    
    #code for cat enemy
    if not catStanding:
        if catX == playerX:
            screen.blit(bulletsplosion[splosion//6], (playerX,playerY))
            splosion +=1
            alive = False
        if Cleft:
            screen.blit(catLeft[catCount//6],(catX, catY))
            catCount += 1
        elif Cright:
            screen.blit(catRight[catCount//6], (catX, catY))
            catCount +=1
    else:
        if Cright:
            screen.blit(catRight[0], (catX,catY))
        else:
            screen.blit(catLeft[0], (catX, catY))

    #cat enemy ai logic
    if catX > playerX:
        Cright = False
        Cleft = True
        catStanding = False
    
    elif catX < playerX:
        Cleft = False
        Cright = True
        catStanding = False
    if idle:
        screen.blit(target, (dummyX, dummyY))


        
    
    
        

    pygame.display.update()

#game loop all movements go inside here and background rgb
running = True
while running:
    clock.tick(18)
    pygame.time.delay(50)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False



    keys = pygame.key.get_pressed()
    #player facing bullet direction
    if keys[pygame.K_SPACE] :
        if left:
            facing = -1
        else:
            facing = 1

        shoot = True
    
    #player directional input and states
    if keys[pygame.K_LEFT] and playerX > playervel - playervel:
        playerX -= playervel
        left = True
        right = False
        standing = False
    elif keys[pygame.K_RIGHT] and playerX < 1500:
            if playerX > 1155:
                running = False
            playerX += playervel
            right = True
            left = False
            standing = False
    else:
        standing = True
        walkCount = 0

    #cat directional input and states
    if Cleft and catX > catVel - catVel:
        catX -= catVel
        Cright = False
        catStanding = False
    
    elif Cright and catX < 800 - catW:
        catX += catVel
        Cleft = False
        catStanding = False
    else:
        catStanding = True
        catCount = 0
    
    #experimental up key presses
    if keys[pygame.K_UP]:
        up = True

        walkCount = 0
    else:
        up = False
    redrawWindow()




    if not(isjump):
        if keys[pygame.K_x]:
            isjump = True
            standing = True
            walkcount = 0
    else:
        if jumpcount >= -10:
            neg = 1
            if jumpcount < 0:
                neg = -1
            #modify float value to lower val to decrease jump height
            playerY -= (jumpcount **2) * 0.3 * neg
            jumpcount -= 1

        else:
            isjump = False
            jumpcount = 10



   