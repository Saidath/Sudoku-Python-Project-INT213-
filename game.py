import pygame
import requests

WIDTH = 550
bg_color = (251,247,245)
original_grid_element_color= (52,31,151)    #To separate the input elements from the elements already provided
buffer=5
response = requests.get("https://sugoku.herokuapp.com/board?difficulty=easy") #pre-fetched api to fill out the boxes initially from this website
grid=response.json()['board']
grid_original = [[grid[x][y] for y in range(len(grid[0]))] for x in range(len(grid))]



def insert(win, position): #function to take input from user
    i,j = position[1], position[0]
    myfont = pygame.font.SysFont('Comic Sans MS', 35)
    
    while True:
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                return
            if event.type == pygame.KEYDOWN:
                #This leads to 3 cases
                #1. user tries to edit default values
                if(grid_original[i-1][j-1] != 0): #if the grid element is filled then we simply return
                        return
                #2. user edits his values
                if(event.key == 48): #checking with 0 as 0 is 48 in ascii 
                    grid[i-1][j-1] = event.key - 48 #clears the previous input to allow for editing
                    pygame.draw.rect(win, bg_color, (position[0]*50 + buffer, position[1]*50+ buffer,50 -2*buffer , 50 - 2*buffer)) #superimposing a block with bg color to make it look like the block has been cleared
                    pygame.display.update()
                    return
                #3. users enters his own values
                if(0 < event.key - 48 <10):  #Checking for valid input
                    pygame.draw.rect(win, bg_color, (position[0]*50 + buffer, position[1]*50+ buffer,50 -2*buffer , 50 - 2*buffer))
                    value = myfont.render(str(event.key-48), True, (0,0,0))
                    win.blit(value, (position[0]*50 +15, position[1]*50))
                    grid[i-1][j-1] = event.key - 48
                    pygame.display.update()
                    return
                return
                


def main():
    pygame.init()
    win = pygame.display.set_mode((WIDTH, WIDTH))
    pygame.display.set_caption("Sudoku Player")
    win.fill(bg_color)
    myfont = pygame.font.SysFont('Comic Sans MS', 35)
    
    for i in range(0,10):
        if(i%3==0):
            pygame.draw.line(win, (0,0,0), (50 + 50*i, 50), (50 + 50*i, 500), 5)    #making every third line bold to separate the boxes in the game
            pygame.draw.line(win, (0,0,0), (50, 50+50*i), (500, 50 + 50*i), 5)
        pygame.draw.line(win, (0,0,0), (50 + 50*i, 50), (50 + 50*i, 500), 2) #drawing the grids
        pygame.draw.line(win, (0,0,0), (50, 50+50*i), (500, 50 + 50*i), 2)   #drawing the grids
    pygame.display.update()
    
    for i in range(0, len(grid[0])):
        for j in range (0, len(grid[0])):
            if(0<grid[i][j]<10):
                value = myfont.render(str(grid[i][j]), True, original_grid_element_color) #adding some values by default
                win.blit(value, ((j+1)*50+15, (i+1)*50)) #Specifying the places where the values are to be added
    pygame.display.update()
    
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                pos = pygame.mouse.get_pos()
                insert(win, (pos[0]//50, pos[1]//50))
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            
main()