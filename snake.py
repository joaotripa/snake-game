import pygame  
import sys

def drawGrid(size, size_grid, screen):
    x=0
    y=0
    white = 255, 255, 255

    for i in range(size_grid[0]): 
        x = x + size[0] // size_grid[0]
        y = y + size[1] // size_grid[1]
        pygame.draw.line(screen, white, (x,0), (x,size[0]))
        pygame.draw.line(screen, white, (0,y), (size[1],y))

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

    def draw(self, screen, eyes=False):
        scale = self.width // self.rows
        x = self.pos[0]
        y = self.pos[1]

        pygame.draw.rect(screen, self.color, 
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
            
            
            pygame.draw.circle(screen, black, eye1, radius)
            pygame.draw.circle(screen, black, eye2, radius)
    
class snake(object):
    body = []
    turns = {}
    
    def __init__(self,color = (255,0,0), init_pos = (10,10)):
        self.color = color    # * Default red color
        self.head = pixel(init_pos, color)
        self.body.append(self.head)
        self.dirx = 0
        self.diry = 0

    def move(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT: sys.exit()

            keys =pygame.key.get_pressed()

            for key in keys:
                if keys[pygame.K_RIGHT]:
                    self.dirx = 1 
                    self.diry = 0
                    self.turns[self.head.pos[:]] = [self.dirx, self.diry]

                elif keys[pygame.K_LEFT]:
                    self.dirx = -1 
                    self.diry = 0
                    self.turns[self.head.pos[:]] = [self.dirx, self.diry]
                
                elif keys[pygame.K_UP]:
                    self.dirx = 0 
                    self.diry = -1
                    self.turns[self.head.pos[:]] = [self.dirx, self.diry]

                elif keys[pygame.K_DOWN]:
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
            else:
                if pix.dirx == -1 and pix.pos[0] <= 0: 
                    pix.pos = (pix.rows-1, pix.pos[1])
                elif pix.dirx == 1 and pix.pos[0] >= pix.rows-1:
                    pix.pos = (0,pix.pos[1])
                elif pix.diry == 1 and pix.pos[1] >= pix.rows-1: 
                    pix.pos = (pix.pos[0], 0)
                elif pix.diry == -1 and pix.pos[1] <= 0: 
                    pix.pos = (pix.pos[0],pix.rows-1)
                else:
                    pix.move(pix.dirx,pix.diry)


    def draw(self, screen):
        for i, pix in enumerate(self.body):
            if i ==0:
                pix.draw(screen, True)
            else:
                pix.draw(screen)

def redraw(snake, size, size_grid, screen):
    black = 0, 0, 0
    screen.fill(black)
    snake.draw(screen)
    drawGrid(size,size_grid, screen)
    pygame.display.update()
            

def main():
    pygame.init()
    size = width, height = 640, 640 # ! width and heigh must have same dimensions
    size_grid = rows, cols = 20, 20    
    
    screen = pygame.display.set_mode(size)

    # black = 0, 0, 0
    # screen.fill(black)
    # drawGrid(size,size_grid,screen)
    # pygame.display.flip()

    s = snake()

    clock = pygame.time.Clock()

    while True:
        pygame.time.delay(50)
        clock.tick(10)
        s.move()

        redraw(s, size, size_grid, screen)
        

main()
