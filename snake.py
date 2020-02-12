import pygame  
import sys

def drawGrid(size, size_grid, surface):
    x=0
    y=0
    white = 255, 255, 255

    for i in range(size_grid[0]): 
        x = x + size[0] // size_grid[0]
        y = y + size[1] // size_grid[1]
        pygame.draw.line(surface, white, (x,0), (x,size[0]))
        pygame.draw.line(surface, white, (0,y), (size[1],y))

class pixel(object):
    rows = 20
    width = 640
    def __init__(self, init_pos, color):
        self.pos = init_pos
        self.color = color # * Default red color
    

    def draw(self, surface, eyes=False):
        scale = self.width // self.rows
        x = self.pos[0]
        y = self.pos[1] 

        pygame.draw.rect(surface, self.color, 
        (x*scale,y*scale, scale + 1, scale + 1))

        if eyes:
            centre = scale // 2
            radius = 3
            black = 0,0,0
            eye1 = (x*scale + centre - radius, y*scale + 8)
            eye2 = (x*scale + scale - 2*radius, y*scale + 8)
            pygame.draw.circle(surface, black, eye1, radius)
            pygame.draw.circle(surface, black, eye2, radius)
    
class snake(object):
    body = []
    
    def __init__(self,color = (255,0,0), init_pos = (10,10)):
        self.color = color
        self.head = pixel(init_pos, color)
        self.body.append(self.head)

    def draw(self, surface):
        for i, c in enumerate(self.body):
            if i ==0:
                c.draw(surface, True)
            else:
                c.draw(surface)

            

def main():
    pygame.init()
    size = width, height = 640, 640 # ! width and heigh must have same dimensions
    size_grid = rows, cols = 20, 20    
    
    black = 0, 0, 0
    red = 255, 0, 0
    screen = pygame.display.set_mode(size)

    screen.fill(black)
    drawGrid(size,size_grid,screen)
    pygame.display.flip()

    s = snake()
    s.draw(screen)
    pygame.display.update()

    while 1:
        for event in pygame.event.get():
            if event.type == pygame.QUIT: sys.exit()

main()
