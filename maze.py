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

clock = pygame.time.Clock() # initialize the clock to control the frame rate
screen = pygame.display.set_mode((len(maze[0]) * CELL_SIZE,len(maze) * CELL_SIZE)) # set the size of the window based on the maze dimensions
pygame.display.set_caption("Maze Solver") # set the title of the window
# Draw the maze
for row in range(len(maze)): # Loop through each row in the maze
        for col in range(len(maze[row])): # Loop through each cell in the maze

            x = col * CELL_SIZE # Calculate the x-coordinate of the cell based on its column index and cell size
            y = row * CELL_SIZE    # Calculate the y-coordinate of the cell based on its row index and cell size

            if maze[row][col] == 1: # If the cell is a wall, set the color to black
                color = (0, 0, 0)

            elif maze[row][col] == "S": # If the cell is the start position, set the color to green
                color = (0, 255, 0)

            elif maze[row][col] == "G": # If the cell is the goal position, set the color to red
                color = (255, 0, 0)

            else: # If the cell is an open path, set the color to white
                color = (255, 255, 255)

            pygame.draw.rect( 
                screen,
                color,
                (x, y, CELL_SIZE, CELL_SIZE)
            ) # Draw the rectangle representing the cell on the screen with the specified color and position

pygame.display.flip() # Update the display to show the drawn maze

path_idx = 0 # Initialize the index for the path to 0
visited_idx = 0 # Initialize the index for the visited order to 0
last_update = pygame.time.get_ticks() # Get the current time in milliseconds since pygame was initialized to control the update rate
running = True # Set the running flag to True to start the main loop

while running: # Main loop to keep the window open and update the display
    for event in pygame.event.get(): # Loop through the events in the event queue
        if event.type == pygame.QUIT: # If the event is a quit event (e.g., closing the window)
            running = False # Set the running flag to False to exit the loop and close the window
    current_time = pygame.time.get_ticks() # Get the current time in milliseconds since pygame was initialized

    if current_time - last_update >= 200: # Check if 200 milliseconds have passed since the last update

        if visited_idx < len(visited): # If there are still nodes in the visited order to be drawn

            row, col = visited[visited_idx] # Get the row and column of the current node in the visited order

            x = col * CELL_SIZE # Calculate the x-coordinate of the cell based on its column index and cell size
            y = row * CELL_SIZE   # Calculate the y-coordinate of the cell based on its row index and cell size

            pygame.draw.rect(
                    screen,
                    (70, 130, 180),
                    (x, y, CELL_SIZE, CELL_SIZE)
                ) # Draw the rectangle representing the visited node on the screen with a specific color and position

            # Show the newly drawn tile
            pygame.display.flip()
            visited_idx += 1 # Increment the index for the visited order to move to the next node in the next iteration

        else: # If all visited nodes have been drawn, start drawing the path from start to goal
            if path_idx < len(path): # If there are still nodes in the path to be drawn

                row, col = path[path_idx] # Get the row and column of the current node in the path

                x = col * CELL_SIZE # Calculate the x-coordinate of the cell based on its column index and cell size
                y = row * CELL_SIZE  # Calculate the y-coordinate of the cell based on its row index and cell size

                pygame.draw.rect(
                        screen,
                        (240, 180, 70),
                        (x, y, CELL_SIZE, CELL_SIZE)
                    ) # Draw the rectangle representing the path node on the screen with a specific color and position

                # Show the newly drawn tile
                pygame.display.flip()
                path_idx += 1 # Increment the index for the path to move to the next node in the next iteration

        last_update = current_time # Update the last_update time to the current time to control the update rate of the animation

        clock.tick(60) # Limit the frame rate to 60 frames per second to ensure smooth animation

pygame.quit() # Quit pygame and close the window when the main loop ends