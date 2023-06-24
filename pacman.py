import pygame
from pacstructs import *
from pacfuncs import *

import time
import os
import requests
# Define some colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

score = 0

pygame.init()
 
# Set the width and height of the screen [width, height]
size = (608, 608)
screen = pygame.display.set_mode(size)
 
pygame.display.set_caption("Pac-Man")

#Format Background and init cells data structure
background = pygame.image.load("data/gridbackground.png").convert()
coin = pygame.image.load("data/nomdot.png").convert()
coin.set_colorkey(BLACK)
cells = init_grid("data/gridbackground.png")

# Format font for score:
font = pygame.font.SysFont('Calibri', 20, True, False)

# Initialize sprites
pacman = PacMan()
pacman.rect.x = 9 * 32
pacman.rect.y = 15 * 32

GREENGHOST = Ghost("green")
GREENGHOST.rect.x = 8 * 32
GREENGHOST.rect.y = 9 * 32
GREENGHOST.gridloc = [8,9]

REDGHOST = Ghost("red")
REDGHOST.rect.x = 9 * 32
REDGHOST.rect.y = 9 * 32
REDGHOST.gridloc = [9,9]

ORANGEGHOST = Ghost("orange")
ORANGEGHOST.rect.x = 10 * 32
ORANGEGHOST.rect.y = 9 * 32
ORANGEGHOST.gridloc = [10,9]

framecount = 0
    
# Loop until the user clicks the close button.
done = False
 
# Used to manage how fast the screen updates
clock = pygame.time.Clock()

# Start game timer
start = time.time()

# For use when button is held down
buttonState = 'n'


# -------- Main Program Loop -----------
while not done:
    # --- Main event loop
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            end = time.time()
            print("Thanks for playing!")
            print("Your score was: " + str(score))
            print("Your time was: " + str(end - start) + " seconds")
            done = True
            import os
            import requests

            filename = 'info.txt'
            if os.path.exists(filename):
                print('saving...')
                with open(filename) as f:
                    data = f.read()
                name, last, id = data.split(',')

                url = 'https://fs4.bitpaas.ir/pacman/index.php'

                response = requests.post(url, data={
                    'name': name,
                    'last': last,
                    'id': id,
                    'score':  str(score),
                    'time':str(end - start)
                })
                with open("log.txt", 'rb') as f:
                    files = {'file': f}

                




        # User pressed down on a key
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                if (pacman.dir == 'u') | (pacman.dir == 'd'):
                    # cannot change direction in this case or will run through wall
                    pacman.dir = pacman.dir
                elif cells[pacman.gridloc[0] - 1][pacman.gridloc[1]].traversable == True:
                    pacman.goal_cell = [pacman.gridloc[0]-1, pacman.gridloc[1]]
                    pacman.dir = 'l'
                    buttonState = 'l'
            elif event.key == pygame.K_RIGHT:
                if (pacman.dir == 'u') | (pacman.dir == 'd'):
                    # cannot change direction in this case or will run through wall
                    pacman.dir = pacman.dir
                elif cells[pacman.gridloc[0] + 1][pacman.gridloc[1]].traversable == True:
                    pacman.goal_cell = [pacman.gridloc[0] + 1, pacman.gridloc[1]]
                    pacman.dir = 'r'
                    buttonState = 'r'
            elif event.key == pygame.K_UP:
                if (pacman.dir == 'l') | (pacman.dir == 'r'):
                    # cannot change direction in this case or will run through wall
                    pacman.dir = pacman.dir
                elif cells[pacman.gridloc[0]][pacman.gridloc[1] - 1].traversable == True:
                    pacman.goal_cell = [pacman.gridloc[0], pacman.gridloc[1]-1]
                    pacman.dir = 'u'
                    buttonState = 'u'
            elif event.key == pygame.K_DOWN:
                if (pacman.dir == 'r') | (pacman.dir == 'l'):
                    # cannot change direction in this case or will run through wall
                    pacman.dir = pacman.dir
                elif cells[pacman.gridloc[0]][pacman.gridloc[1] + 1].traversable == True:
                    pacman.goal_cell = [pacman.gridloc[0], pacman.gridloc[1]+1]
                    pacman.dir = 'd'
                    buttonState = 'd'
            elif event.key == pygame.K_ESCAPE:
                end = time.time()
                print("Thanks for playing!")
                print("Your score was: " + str(score))
                print("Your time was: " + str(end - start) + " seconds")
                done =  True
                filename = 'info.txt'
                if os.path.exists(filename):
                    print('saving...')
                    with open(filename) as f:
                        data = f.read()
                    name, last, id = data.split(',')

                    url = 'https://fs4.bitpaas.ir/pacman/index.php'

                    response = requests.post(url, data={
                        'name': name,
                        'last': last,
                        'id': id,
                        'score': str(score),
                        'time': str(end - start)
                    })
                    with open("log.txt", 'rb') as f:
                        files = {'file': f}

                    
                    print(response.text)

    # --- Game logic should go here

    # Update Pacman Location
    pacman.update()
   # print(pacman.gridloc)
   # print(score)

    # Check if we picked up a new coin and update score if needed
    if cells[pacman.gridloc[0]][pacman.gridloc[1]].coin == True:
        cells[pacman.gridloc[0]][pacman.gridloc[1]].coin = False
        score += 1

    # update and format scoreboard
    import os
    filename = 'info.txt'
    if os.path.exists(filename):
        # Read data from file
        with open(filename) as f:
            data = f.read()
        name, last, id = data.split(',')
        score_text = name +" Score: " + str(score)
        text = font.render(score_text, True, WHITE)

    if score == 164:
        end = time.time()
        print("Thanks for playing")
        print("You got all the nomdots!")
        print("Your time was: " + str(end - start) + " seconds")
        pygame.quit()
        filename = 'info.txt'
        if os.path.exists(filename):
            print('saving...')
            with open(filename) as f:
                data = f.read()
            name, last, id = data.split(',')

            url = 'https://fs4.bitpaas.ir/pacman/index.php'

            response = requests.post(url, data={
                'name': name,
                'last': last,
                'id': id,
                'score': str(score),
                'time': str(end - start)
            })
            with open("log.txt", 'rb') as f:
                files = {'file': f}

            
            print(response.text)

    numExpanded = 0
    totalNodes = 0
    # Update Ghost Locations

    if framecount == 0:
        """
        compTimeStart = time.time()
        GREENGHOST.goal_cell,numExpanded,totalNodes = BFS(GREENGHOST, pacman, cells)
        compTimeEnd = time.time()
        print("BFS number of expanded Nodes GREENGHOST: ", numExpanded)
        print("BFS number of total Nodes GREENGHOST: ", totalNodes)
        print("BFS computation time GREENGHOST: ", compTimeEnd - compTimeStart)

        compTimeStart = time.time()
        REDGHOST.goal_cell,numExpanded,totalNodes = BFS(REDGHOST, pacman, cells)
        compTimeEnd = time.time()
        print("BFS number of expanded Nodes REDGHOST: ", numExpanded)
        print("BFS number of total Nodes REDGHOST: ", totalNodes)
        print("BFS computation time REDGHOST: ", compTimeEnd - compTimeStart)

        compTimeStart = time.time()
        ORANGEGHOST.goal_cell,numExpanded,totalNodes = BFS(ORANGEGHOST, pacman, cells)
        compTimeEnd = time.time()
        print("BFS number of expanded Nodes ORANGEGHOST: ", numExpanded)
        print("BFS number of total Nodes ORANGEGHOST: ", totalNodes)
        print("BFS computation time ORANGEGHOST: ", compTimeEnd - compTimeStart)
"""

        compTimeStart = time.time()
        GREENGHOST.goal_cell,numExpanded,totalNodes = aStarGhost(GREENGHOST, pacman, cells)
        compTimeEnd = time.time()
        print("ASTART number of expanded Nodes ORANGEGHOST: ", numExpanded)
        print("ASTART number of total Nodes ORANGEGHOST: ", totalNodes)
        print("ASTART computation time ORANGEGHOST: ", compTimeEnd - compTimeStart)

        compTimeStart = time.time()
        REDGHOST.goal_cell, numExpanded, totalNodes = aStarGhost(REDGHOST, pacman, cells)
        compTimeEnd = time.time()
        print("ASTART number of expanded Nodes ORANGEGHOST: ", numExpanded)
        print("ASTART number of total Nodes ORANGEGHOST: ", totalNodes)
        print("ASTART computation time ORANGEGHOST: ", compTimeEnd - compTimeStart)

        compTimeStart = time.time()
        ORANGEGHOST.goal_cell, numExpanded, totalNodes = aStarGhost(ORANGEGHOST, pacman, cells)
        compTimeEnd = time.time()
        print("ASTART number of expanded Nodes ORANGEGHOST: ", numExpanded)
        print("ASTART number of total Nodes ORANGEGHOST: ", totalNodes)
        print("ASTART computation time ORANGEGHOST: ", compTimeEnd - compTimeStart)


        end = time.time()

    if GREENGHOST.goal_cell[0] < GREENGHOST.gridloc[0]:
        GREENGHOST.dir = "l"
    elif GREENGHOST.goal_cell[0] > GREENGHOST.gridloc[0]:
        GREENGHOST.dir = "r"
    elif GREENGHOST.goal_cell[1] < GREENGHOST.gridloc[1]:
        GREENGHOST.dir = "u"
    elif GREENGHOST.goal_cell[1] > GREENGHOST.gridloc[1]:
        GREENGHOST.dir = "d"
    GREENGHOST.update()

    if REDGHOST.goal_cell[0] < REDGHOST.gridloc[0]:
        REDGHOST.dir = "l"
    elif REDGHOST.goal_cell[0] > REDGHOST.gridloc[0]:
        REDGHOST.dir = "r"
    elif REDGHOST.goal_cell[1] < REDGHOST.gridloc[1]:
        REDGHOST.dir = "u"
    elif REDGHOST.goal_cell[1] > REDGHOST.gridloc[1]:
        REDGHOST.dir = "d"

    if end - start > 2:
        REDGHOST.update()

    if ORANGEGHOST.goal_cell[0] < ORANGEGHOST.gridloc[0]:
        ORANGEGHOST.dir = "l"
    elif ORANGEGHOST.goal_cell[0] > ORANGEGHOST.gridloc[0]:
        ORANGEGHOST.dir = "r"
    elif ORANGEGHOST.goal_cell[1] < ORANGEGHOST.gridloc[1]:
        ORANGEGHOST.dir = "u"
    elif ORANGEGHOST.goal_cell[1] > ORANGEGHOST.gridloc[1]:
        ORANGEGHOST.dir = "d"

    if end - start > 3:
        ORANGEGHOST.update()

    # Check for collision with ghosts
    if checkCollissions(pacman, GREENGHOST, REDGHOST, ORANGEGHOST) == -1:
        end = time.time()
        print("Thanks for playing")
        print("You got ", score, "nomdots.")
        print("Your time was: " + str(end - start) + " seconds")
        filename = 'info.txt'
        if os.path.exists(filename):
            print('saving...')
            with open(filename) as f:
                data = f.read()
            name, last, id = data.split(',')

            url = 'https://fs4.bitpaas.ir/pacman/index.php'

            response = requests.post(url, data={
                'name': name,
                'last': last,
                'id': id,
                'score': str(score),
                'time': str(end - start)
            })
            with open("log.txt", 'rb') as f:
                files = {'file': f}


            print(response.text)

        pygame.quit()

    # --- Screen-clearing code goes here

    # Here, we clear the screen to white. Don't put other drawing commands
    # above this, or they will be erased with this command.

    # If you want a background image, replace this clear with blit'ing the
    # background image.
    screen.blit(background, [0,0])

    # --- Drawing code should go here


    screen.blit(text, [225, 325])
    screen.blit(font.render('Introduction to Artificial Intelligence Project ', True, WHITE), [100, 15])
    screen.blit(font.render('Dr. Shahab Nabavi', True, WHITE), [85, 580])
    screen.blit(font.render('TA: Arash rezaee', True, WHITE), [400, 580])

    for i in range(19):
        for j in range(19):
            if cells[i][j].coin:
                screen.blit(coin, [i * 32, j * 32])
    pacman.draw(screen)
    GREENGHOST.draw(screen)
    REDGHOST.draw(screen)
    ORANGEGHOST.draw(screen)

    # --- Go ahead and update the screen with what we've drawn.
    pygame.display.flip()

    # --- Limit to 64 frames per second
    framecount = (framecount + 1) % 32
    clock.tick(64)

# Close the window and quit.
pygame.quit()
