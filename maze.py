import pygame
from maze_solver import dfs
pygame.init()

CELL_SIZE = 60
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
d = dfs(maze, (1, 1), (8, 8))  # Get the path from start to goal using DFS
path = d[0]  # Extract the path from the result
visited = d[1]  # Extract the visited order from the result

clock = pygame.time.Clock()
screen = pygame.display.set_mode((len(maze[0]) * CELL_SIZE,len(maze) * CELL_SIZE))
pygame.display.set_caption("Maze Solver")
# Draw the maze
for row in range(len(maze)):
        for col in range(len(maze[row])):

            x = col * CELL_SIZE
            y = row * CELL_SIZE

            if maze[row][col] == 1:
                color = (0, 0, 0)

            elif maze[row][col] == "S":
                color = (0, 255, 0)

            elif maze[row][col] == "G":
                color = (255, 0, 0)

            else:
                color = (255, 255, 255)

            pygame.draw.rect(
                screen,
                color,
                (x, y, CELL_SIZE, CELL_SIZE)
            )

pygame.display.flip()

path_idx = 0
visited_idx = 0
last_update = pygame.time.get_ticks()
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    current_time = pygame.time.get_ticks()

    if current_time - last_update >= 200:

        if visited_idx < len(visited):

            row, col = visited[visited_idx]

            x = col * CELL_SIZE
            y = row * CELL_SIZE

            pygame.draw.rect(
                    screen,
                    (70, 130, 180),
                    (x, y, CELL_SIZE, CELL_SIZE)
                )

            # Show the newly drawn tile
            pygame.display.flip()
            visited_idx += 1

        else:
            if path_idx < len(path):

                row, col = path[path_idx]

                x = col * CELL_SIZE
                y = row * CELL_SIZE

                pygame.draw.rect(
                        screen,
                        (240, 180, 70),
                        (x, y, CELL_SIZE, CELL_SIZE)
                    )

                # Show the newly drawn tile
                pygame.display.flip()
                path_idx += 1

        last_update = current_time

        clock.tick(60)

pygame.quit()