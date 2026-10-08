from collections import deque
manhattan_distance = lambda a, b: abs(a[0] - b[0]) + abs(a[1] - b[1])
def get_actions(maze, node):
     row, col = node 
     actions = []

     # up
     if row > 0 and maze[row - 1][col] in (0, "G"):
          actions.append((row - 1, col))

     # down
     if row < len(maze) - 1 and maze[row + 1][col] in (0, "G"):
          actions.append((row + 1, col))

     # left 
     if col > 0 and maze[row][col - 1] in (0, "G"):
          actions.append((row, col - 1))

     # right
     if col < len(maze[0]) - 1 and maze[row][col + 1] in (0, "G"):
          actions.append((row, col + 1))

     return actions


def bfs(maze, start, goal):
     """
     maze: 2D list of '0'/'1' (or 0/1), same layout as the input maze
     start: (row, col) tuple
     goal: (row, col) tuple

     Returns a tuple: (path, visited_order, stats)
     path           - list of (row, col) from start to goal, inclusive.
                    Empty list [] if no path exists.
     visited_order  - list of (row, col), in the order your algorithm
                    expanded/visited them (used to animate the search).
     stats          - dict with keys:
                    'nodes_expanded' (int), 'path_length' (int),
                    'path_cost' (int or float)
     """

     path = []

     visited = []

     stats = {
          "nodes_expanded": 0,
          "path_length": 0,
          "path_cost": 0.0
     }

     

     if start == goal:
          return [], visited, stats
     parents = {start: None}
     discovered = deque([start])
     

     while(discovered):
          node = discovered.popleft()
          visited.append(node)

          if node == goal:
               break

          for action in get_actions(maze, node):
               child = action 
               if (child not in visited) and (child not in discovered):
                    parents[child] = node
                    if child == goal:
                         break
                    discovered.append(child)
     node = goal
     while node is not None:
          path.append(node)
          node = parents[node]
     path.reverse()

     stats["nodes_expanded"] = len(visited)
     stats["path_length"] = len(path) - 1
     return path, visited, stats
# esther


def dfs(maze, start, goal):
# Same signature and return format as bfs()
     explored = set()
     explorred_order = []
     path={}
     frontier = [start]
     while True:
          if not frontier:
               return ([], explorred_order, {"nodes_expanded": len(explored), "path_length": 0, "path_cost": 0.0})
          node = frontier.pop()
          explored.add(node)
          explorred_order.append(node)
          if node == goal:
               break
          for action in get_actions(maze, node):
               child = action
               if child not in explored and child not in frontier:
                    frontier.append(child)
                    path[child] = node
     node = goal
     path_set= []
     while node in path:
          path_set.append(node)
          node = path[node]
     path_set.append(start)
     path_set.reverse()
     return (path_set, explorred_order, {"nodes_expanded": len(explored), "path_length": len(path_set) - 1, "path_cost": 0.0})
# daniel
     


def astar(maze, start, goal, heuristic=manhattan_distance):
# Same signature and return format as bfs()
     pass
# esther



def greedy_best_first(maze, start, goal, heuristic=manhattan_distance):
# Same signature and return format as bfs()
     pass
# daniel


if __name__ == "__main__":
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
     start = (1 , 1)
     goal = (8 , 8)
     path_dfs , visited_dfs , stats_dfs = dfs(maze , start , goal)
     print("DFS Path: ", path_dfs)
     print("DFS Visited: ", visited_dfs)
     print("DFS Stats: ", stats_dfs)
