import pygame
from maze_solver import dfs, greedy_best_first, bfs
pygame.init()
DFS = False
ASTAR = False
BFS = False
GREEDY = False
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
maze_width = len(maze[0]) * CELL_SIZE
maze_height = len(maze) * CELL_SIZE
screen_length = int(1.5 * len(maze[0]) * CELL_SIZE) # calculate the height of the window based on the maze dimensions
screen_height = int(1.5 * len(maze) * CELL_SIZE) # calculate the width of the window based on the maze dimensions
offset_x = (screen_length - maze_width) // 2
offset_y = (screen_height - maze_height) // 2
def draw_main_menu():
    screen.fill((18, 19, 20)) # Fill the screen with white color
    font = pygame.font.Font(None, 24) # Create a font object with size 24
    d_text = font.render("DFS", True, (255, 255, 255)) # Render the text to be displayed
    b_text = font.render("BFS", True, (255, 255, 255)) # Render the text to be displayed
    a_text = font.render("A*", True, (255, 255, 255)) # Render the text to be displayed
    g_text = font.render("Greedy", True, (255, 255, 255)) # Render the text to be displayed
    d_text_rect = d_text.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2)) # Get the rectangle of the text and center it on the screen
    screen.blit(d_text, d_text_rect) # Draw the text on the screen
    pygame.display.flip() # Update the display to show the drawn text
def draw_maze(maze):
# Draw the maze
    for row in range(len(maze)): # Loop through each row in the maze
            for col in range(len(maze[row])): # Loop through each cell in the maze

                x = col * CELL_SIZE + offset_x # Calculate the x-coordinate of the cell based on its column index and cell size
                y = row * CELL_SIZE + offset_y    # Calculate the y-coordinate of the cell based on its row index and cell size

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

d = bfs(maze, (1, 1), (8, 8))  # Get the path from start to goal using BFS
path = d[0]  # Extract the path from the result
visited = d[1]  # Extract the visited order from the result

clock = pygame.time.Clock() # initialize the clock to control the frame rate
screen = pygame.display.set_mode((screen_length, screen_height)) # set the size of the window based on the maze dimensions
pygame.display.set_caption("Maze Solver") # set the title of the window
draw_main_menu() # Draw the main menu on the screen
waiting_for_input = True # Set the flag to wait for user input to start the animation
if waiting_for_input: # If waiting for user input, enter a loop to wait for a key press
    while True: # Infinite loop to keep checking for events
        for event in pygame.event.get(): # Loop through the events in the event queue
            if event.type == pygame.QUIT: # If the event is a quit event (e.g., closing the window)
                pygame.quit() # Quit pygame and close the window
                exit() # Exit the program
            elif event.type == pygame.KEYDOWN: # If any key is pressed down
                waiting_for_input = False # Set the flag to False to exit the waiting loop
                break # Break out of the inner loop to proceed with the animation
        if not waiting_for_input: # If not waiting for input anymore, break out of the outer loop as well
            break
draw_maze(maze) # Draw the maze on the screen

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

            x = col * CELL_SIZE + offset_x # Calculate the x-coordinate of the cell based on its column index and cell size
            y = row * CELL_SIZE + offset_y   # Calculate the y-coordinate of the cell based on its row index and cell size

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

                x = col * CELL_SIZE + offset_x # Calculate the x-coordinate of the cell based on its column index and cell size
                y = row * CELL_SIZE + offset_y  # Calculate the y-coordinate of the cell based on its row index and cell size

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

