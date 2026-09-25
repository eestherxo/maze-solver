import pygame

pygame.init()

WIDTH = 600
HEIGHT = 600

screen = pygame.display.set_mode((HEIGHT, WIDTH))
pygame.display.set_caption("Maze Solver")

maze = [
     [1,1,1,1,1,1,1,1,1,1],
     [1,"S",0,1,0,0,1,0,0,1],
     [1,0,0,0,1,0,1,1,0,1],
     [1,1,1,0,0,1,0,0,0,1],
     [1,0,1,0,0,0,0,0,0,1],
     [1,0,0,0,0,0,1,1,0,1],
     [1,0,0,0,0,0,0,0,0,1],
     [1,1,1,0,0,0,0,1,0,1],
     [1,0,0,1,0,0,0,0,"G",1],
     [1,1,1,1,1,1,1,1,1,1]
]

running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    screen.fill("white")

    pygame.display.flip()

pygame.quit()