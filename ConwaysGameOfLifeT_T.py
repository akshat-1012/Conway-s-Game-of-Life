import pygame
import sys
import random


BLACK = (0, 0, 0)
GREY = (128,128,128)
WHITE = (200, 200, 200)
YELLOW = (255,255,0)

dispw,disph = 800,800
gridh = int(input("Enter the height of the grid: "))
gridw = int(input("Enter the width of the grid: "))

tileSizeH = disph/gridh 
tileSizeW = dispw/gridw 

screen = pygame.display.set_mode((dispw,disph))
clock = pygame.time.Clock()

#This function helps in drawing the grid, took a while loop in this manner because I am dividing the required number of tiles on a 800x800 display so it could be a floating number too
def drawgrid(): 
    x = 0
    while x < dispw:
        y = 0
        while y < disph:
            rect = pygame.Rect(x, y, tileSizeW, tileSizeH)
            pygame.draw.rect(screen, BLACK, rect, 1)
            y += tileSizeH
        x += tileSizeW

#This function colours all the positions in a set loc (bascially used to depict the alive blocks)
def colouring(loc):
     for posn in loc:
          col, row = posn
          rect = pygame.Rect(col*tileSizeW,row*tileSizeH,tileSizeW,tileSizeH)
          pygame.draw.rect(screen,YELLOW,rect)
          inner_rect = pygame.Rect(col*tileSizeW + 1, row*tileSizeH + 1, tileSizeW - 2, tileSizeH - 2)
          pygame.draw.rect(screen, BLACK, inner_rect, 1)

#I created this function to generate random alive positions 
def randomP(loc):
    for i in range(random.randint(max(gridh,gridw)-1, 20*(gridh+gridw))):
        x = random.randint(0,gridw-1)
        y = random.randint(0,gridh-1)
        loc.add((x,y))
        i = i+1

    return loc

#returns a list of all neighbours (which are in the grid) for a particular position 
def neighbours(pos):
    x, y = pos
    neighbor_positions = [
        (x-1, y-1), (x, y-1), (x+1, y-1),
        (x-1, y),           (x+1, y),
        (x-1, y+1), (x, y+1), (x+1, y+1)
    ]
    return [(x1, y1) for x1, y1 in neighbor_positions if 0 <= x1 < gridw and 0 <= y1 < gridh]

#This is the main function which will check all the conditions, I am only checking the neighbours of already alive blocks as the other cells don't have a chance anyways...Then simply checking the conditions, I came to the required conclusions
def gridcheck(loc):
    all_neighbors = set()
    new_positions = set()

    for pos in loc:
        neighbors = neighbours(pos)
        all_neighbors.update(neighbors)

        alive_neighbors = sum((n in loc) for n in neighbors)
        if alive_neighbors in [2, 3]:
            new_positions.add(pos)
    
    for pos in all_neighbors:
        if pos not in loc:
            alive_neighbors = sum((n in loc) for n in neighbours(pos))
            if alive_neighbors == 3:
                new_positions.add(pos)
    
    return new_positions
    

def main():
        Pause = True
        loc = set()
        fps = 5 #initial speed at which the simulation will move if left to play on its own
        while True:
            clock.tick(fps)

            pygame.display.set_caption("PLAYING" if not Pause else "PAUSED/STEP BY STEP MODE")

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.display.quit()
                    pygame.quit()
                    sys.exit()
                
                if event.type == pygame.MOUSEBUTTONDOWN:
                    x,y = pygame.mouse.get_pos()
                    col, row = x//tileSizeH, y//tileSizeW

                    posn = (col,row)

                    if posn in loc:
                        loc.remove(posn)
                    else:
                        loc.add(posn)

                if event.type == pygame.KEYDOWN:    
                    if event.key == pygame.K_SPACE: #space to pause/play
                         Pause = not Pause
                    
                    if event.key == pygame.K_r:     #R on the keyboard to reset the position
                        loc = set()               
                    
                    if event.key == pygame.K_UP:    #UP arrow to generate a random position
                        loc = set()
                        loc = randomP(loc)
                    if event.key == pygame.K_RIGHT: #To check the next move step by step
                        loc = gridcheck(loc)
                    if event.key == pygame.K_d:     #To increase the speed 
                        fps = fps+5
                    if event.key == pygame.K_s:     #To decrease the speed
                        if fps != 5:
                            fps = fps-5

                        

            if not Pause:
                loc = gridcheck(loc) #continously updating the grid after each iteration

            screen.fill(GREY)
            drawgrid()
            colouring(loc) #colouring it in after all the required events occur and we finally have the set loc with all the alive cells
            pygame.display.update()

if __name__ == "__main__":
    main()


