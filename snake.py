import pygame  
import sys
import random

def drawGrid(size, size_grid, display):
    x=0
    y=0
    white = 255, 255, 255

    for i in range(size_grid[0]): 
        x = x + size[0] // size_grid[0]
        y = y + size[1] // size_grid[1]
        pygame.draw.line(display, white, (x,0), (x,size[0]))
        pygame.draw.line(display, white, (0,y), (size[1],y))

class pixel(object):
    rows = 20
    width = 640
    def __init__(self, init_pos, color, dirx = 1, diry = 0):
        self.pos = init_pos
        self.dirx = dirx
        self.diry = diry
        self.color = color 
    
    def move(self, dirx, diry):
        self.dirx = dirx
        self.diry = diry
        self.pos = (self.pos[0] + self.dirx, self.pos[1] + self.diry)

    def draw(self, display, eyes=False):
        scale = self.width // self.rows
        x = self.pos[0]
        y = self.pos[1]

        pygame.draw.rect(display, self.color, 
        (x*scale,y*scale, scale, scale))

        if eyes:
            centre = scale // 2
            radius = 4
            black = 0,0,0
            if self.dirx == 1 and self.diry == 0: #* moving right
                eye1 = (x*scale + 25, y*scale + centre + 2*radius -1)
                eye2 = (x*scale + 25, y*scale + centre - 2*radius +1)
            if self.dirx == -1 and self.diry == 0: #* moving left
                eye1 = (x*scale + 10, y*scale + centre + 2*radius -1)
                eye2 = (x*scale + 10, y*scale + centre - 2*radius +1)
            if self.dirx == 0 and self.diry == -1: #* moving up
                eye1 = (x*scale + centre + 2*radius -1, y*scale + 10)
                eye2 = (x*scale + centre - 2*radius +1, y*scale + 10)
            if self.dirx == 0 and self.diry == 1: #* moving down
                eye1 = (x*scale + centre + 2*radius -1, y*scale + 25)
                eye2 = (x*scale + centre - 2*radius +1, y*scale + 25)
            
            
            pygame.draw.circle(display, black, eye1, radius)
            pygame.draw.circle(display, black, eye2, radius)
    
class snake(object):
    
    
    def __init__(self,color = (0,255,0), init_pos = (10,10)):
        self.body = []
        self.turns = {}
        self.color = color    # * Default green color
        self.head = pixel(init_pos, color)
        self.body.append(self.head)
        self.dirx = 1
        self.diry = 0
        self.collision = False

    def move(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT: sys.exit()

            keys =pygame.key.get_pressed()

            for key in keys:
                if keys[pygame.K_RIGHT] and self.dirx != -1:
                    self.dirx = 1 
                    self.diry = 0
                    self.turns[self.head.pos[:]] = [self.dirx, self.diry]

                elif keys[pygame.K_LEFT] and self.dirx != 1:
                    self.dirx = -1 
                    self.diry = 0
                    self.turns[self.head.pos[:]] = [self.dirx, self.diry]
                
                elif keys[pygame.K_UP] and self.diry != 1:
                    self.dirx = 0 
                    self.diry = -1
                    self.turns[self.head.pos[:]] = [self.dirx, self.diry]

                elif keys[pygame.K_DOWN] and self.diry != -1:
                    self.dirx = 0 
                    self.diry = 1
                    self.turns[self.head.pos[:]] = [self.dirx, self.diry]

                elif keys[pygame.K_ESCAPE]:
                    sys.exit()
                

        for i, pix in enumerate(self.body):
            pixpos = pix.pos[:]
            if pixpos in self.turns:
                turn = self.turns[pixpos]
                pix.move(turn[0],turn[1])
                if i == len(self.body)-1:
                    self.turns.pop(pixpos)
            else: #* Setting grid boundaries
                if pix.dirx == -1 and pix.pos[0] <= 0: #* if passes left limit, appears on the right
                    pix.pos = (pix.rows-1, pix.pos[1])
                elif pix.dirx == 1 and pix.pos[0] >= pix.rows-1: #* if passes right limit, appears on the left
                    pix.pos = (0,pix.pos[1])
                elif pix.diry == 1 and pix.pos[1] >= pix.rows-1: #* if passes bottom limit, appears on top
                    pix.pos = (pix.pos[0], 0)
                elif pix.diry == -1 and pix.pos[1] <= 0: #* if passes top limit, appears on the bottom
                    pix.pos = (pix.pos[0],pix.rows-1)
                else:
                    pix.move(pix.dirx,pix.diry)

    def draw(self, display):
        head = self.body[0]
        for i, pix in enumerate(self.body):
            if i ==0:
                pix.draw(display, True)
            elif head.pos == pix.pos:
                self.collision = True
                break
            else:
                pix.draw(display)
    
    def increaseSnake(self):
        tail = self.body[-1]
        green = 0,255,0
        if tail.dirx == 1 and tail.diry == 0: 
            self.body.append(pixel((tail.pos[0]-1,tail.pos[1]),green)) #* Add another pixel to the left
        elif tail.dirx == -1 and tail.diry == 0: 
            self.body.append(pixel((tail.pos[0]+1,tail.pos[1]),green)) #* Add another pixel to the right
        elif tail.diry == 1 and tail.dirx == 0: 
            self.body.append(pixel((tail.pos[0],tail.pos[1]-1),green)) #* Add another pixel on top
        elif tail.diry == -1 and tail.dirx == 0: 
            self.body.append(pixel((tail.pos[0],tail.pos[1]+1),green)) #* Add another pixel on bottom
        
        #* Defining new pixel direction 
        self.body[-1].dirx = tail.dirx 
        self.body[-1].diry = tail.diry

    def reset(self, init_pos, color = (0,255,0)):
        self.body = []
        self.turns = {}
        self.color = color    # * Default green color
        self.head = pixel(init_pos, color)
        self.body.append(self.head)
        self.dirx = 1
        self.diry = 0
        self.collision = False

class food(object):
    def __init__(self, size_grid):
        self.x = random.randint(0,size_grid[0]-1) #* 20 rows and columns, 0-19
        self.y = random.randint(0,size_grid[0]-1) #* 20 rows and columns, 0-19
        self.gridSize = size_grid

    def draw(self, display):
        red = 255,0,0
        newFood = pixel((self.x,self.y),red)
        newFood.draw(display)

    def createNew(self, snake):
        x = random.randint(0,self.gridSize[0]-1) #* 20 rows and columns, 0-19
        y = random.randint(0,self.gridSize[0]-1) #* 20 rows and columns, 0-19
        flag = True
        for pix in snake.body:
            if(x  == pix.pos[0] and y == pix.pos[1]):
                flag = False
                self.createNew(snake)
                break
        if flag:
            self.x = x
            self.y = y

    def gotEaten(self, snake):
        if snake.body[0].pos == (self.x,self.y): return True
        else: return False


def redraw(snake, food, size, size_grid, display):
    black = 0, 0, 0
    display.fill(black)
    snake.draw(display)
    food.draw(display)
    drawGrid(size,size_grid, display)
    pygame.display.update()

def menu():
    pygame.init()
    size = width, height = 640, 640 # ! width and heigh must have same dimensions
    size_grid = rows, cols = 20, 20    
    menuDisplay = pygame.display.set_mode(size)
    black = 0, 0, 0
    menuDisplay.fill(black)
    pygame.display.set_caption('Snake Game')

    s = snake()
    f = food(size_grid)

    while True:
        #font = pygame.font.SysFont(None, 250)
        titleFont = pygame.font.Font('ARCADECLASSIC.TTF', 85)
        title = titleFont.render('Snake Game', True, (0,255,0))
        menuDisplay.blit(title,(105,200))

        secondTextFont = pygame.font.Font('ARCADECLASSIC.TTF', 20)
        pressToStartText = secondTextFont.render('Press space to Start', True, (255,255,255))
        menuDisplay.blit(pressToStartText,(225,320))

        authorFont = pygame.font.Font('ARCADECLASSIC.TTF', 20)
        authorText = authorFont.render('Made by Joao Tripa', True, (255,255,255))
        menuDisplay.blit(authorText,(235,600))

        pygame.display.update()

        for event in pygame.event.get():
                if event.type == pygame.QUIT: sys.exit()

                keys =pygame.key.get_pressed()

                for key in keys:
                    if keys[pygame.K_SPACE]:
                        gameLoop(s, f, size, size_grid)
                    if keys[pygame.K_ESCAPE]:
                        sys.exit()

def gameOver(snake, food, size, size_grid):
    endDisplay = pygame.display.set_mode(size)
    black = 0, 0, 0
    endDisplay.fill(black)
    
    while True:

        #font = pygame.font.SysFont(None, 250)
        titleFont = pygame.font.Font('ARCADECLASSIC.TTF', 85)
        title = titleFont.render('Game Over', True, (0,255,0))
        endDisplay.blit(title,(130,200))

        scoreFont = pygame.font.Font('ARCADECLASSIC.TTF', 35)
        score = scoreFont.render('Your Score is '+str(len(snake.body)), True, (255,255,255))
        endDisplay.blit(score,(195,280))

        secondTextFont = pygame.font.Font('ARCADECLASSIC.TTF', 20)
        pressToTryAgainText = secondTextFont.render('Press space to try again', True, (255,255,255))
        endDisplay.blit(pressToTryAgainText,(210,380))

        authorFont = pygame.font.Font('ARCADECLASSIC.TTF', 20)
        authorText = authorFont.render('Made by Joao Tripa', True, (255,255,255))
        endDisplay.blit(authorText,(235,600))
        
        pygame.display.update()

        for event in pygame.event.get():
                if event.type == pygame.QUIT: sys.exit()

                keys =pygame.key.get_pressed()

                for key in keys:
                    if keys[pygame.K_SPACE]:
                        gameLoop(snake,food, size, size_grid)
                    if keys[pygame.K_ESCAPE]:
                        sys.exit()

def gameLoop(snake, food, size, size_grid):
    size = size
    size_grid = size_grid
    display = pygame.display.set_mode(size)
    pygame.display.set_caption('Snake Game') 

    snake.reset((size_grid[0]//2,size_grid[0]//2))

    clock = pygame.time.Clock()

    while True:
        #pygame.time.delay(50)
        clock.tick(10)
        snake.move()
        if food.gotEaten(snake):
            snake.increaseSnake()
            food.createNew(snake)
        if snake.collision:
            gameOver(snake,food,size,size_grid)
            
        redraw(snake, food, size, size_grid, display)
        

menu()
