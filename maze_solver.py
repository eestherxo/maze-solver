from collections import deque
import heapq

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


def get_greedy_actions(maze, node, goal):
    actions = get_actions(maze, node)
    actions.sort(key=lambda x: manhattan_distance(x, goal))
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

    stats = {"nodes_expanded": 0, "path_length": 0, "path_cost": 0}

    if start == goal:
        return [start], [], stats

    parents = {start: None}
    frontier = deque([start])
    expanded = []

    while frontier:
        node = frontier.popleft()
        expanded.append(node)

        for child in get_actions(maze, node):
            if child in parents:
                continue

            parents[child] = node

            # check if child is the goal before adding it to the frontier/discovered nodes
            if child == goal:
                path = []
                current = goal
                while current is not None:
                    path.append(current)
                    current = parents[current]
                path.reverse()

                stats["nodes_expanded"] = len(expanded)
                stats["path_length"] = len(path) - 1
                return path, expanded, stats

            frontier.append(child)

    stats["nodes_expanded"] = len(expanded)
    return [], expanded, stats


# esther


def dfs(maze, start, goal):
    # Same signature and return format as bfs()
    explored = set()
    explorred_order = []
    path = {}
    frontier = [start]
    while True:
        if not frontier:
            return (
                [],
                explorred_order,
                {"nodes_expanded": len(explored), "path_length": 0, "path_cost": 0},
            )
        node = frontier.pop()
        if node == goal:
            break
        explored.add(node)
        explorred_order.append(node)
        for action in get_actions(maze, node):
            child = action
            if child not in explored and child not in frontier:
                frontier.append(child)
                path[child] = node
    node = goal
    path_set = []
    while node in path:
        path_set.append(node)
        node = path[node]
    path_set.append(start)
    path_set.reverse()
    return (
        path_set,
        explorred_order,
        {
            "nodes_expanded": len(explored),
            "path_length": len(path_set) - 1,
            "path_cost": 0,
        },
    )


# daniel


def astar(maze, start, goal, heuristic=manhattan_distance):
    # Same signature and return format as bfs()

    path = []

    expanded = []

    stats = {"nodes_expanded": 0, "path_length": 0, "path_cost": 0}

    if start == goal:
        return [goal], expanded, stats
    parents = {start: None}
    frontier = [(heuristic(start, goal), 0, start)]
    frontier_node_costs = {start: 0}

    while frontier:
        _, current_cost, node = heapq.heappop(frontier)

        if current_cost != frontier_node_costs.get(node):
            continue

        if node == goal:
            break

        expanded.append(node)

        for child in get_actions(maze, node):
            new_cost = current_cost + 1
            if new_cost < frontier_node_costs.get(child, float("inf")):
                parents[child] = node
                frontier_node_costs[child] = new_cost
                priority = new_cost + heuristic(child, goal)
                heapq.heappush(frontier, (priority, new_cost, child))

    node = goal
    while node is not None:
        path.append(node)
        node = parents[node]
    path.reverse()

    stats["path_length"] = len(path) - 1
    stats["path_cost"] = frontier_node_costs[goal]
    stats["nodes_expanded"] = len(expanded)
    return path, expanded, stats


# esther


def greedy_best_first(maze, start, goal, heuristic=manhattan_distance):
    # using the heuristic function to guide the search and using the priority queue to select the next node to explore based on the heuristic value.
    explored = set()
    explored_order = []
    path = {}
    frontier = [(heuristic(start, goal), start)]
    while True:
        if not frontier:
            return (
                [],
                explored_order,
                {"nodes_expanded": len(explored), "path_length": 0, "path_cost": 0},
            )
        _, node = frontier.pop(0)
        if node == goal:
            break
        explored.add(node)
        explored_order.append(node)
        for action in get_greedy_actions(maze, node, goal):
            child = action
            if child not in explored and all(child != n for _, n in frontier):
                frontier.append((heuristic(child, goal), child))
                path[child] = node
        frontier.sort(key=lambda x: x[0])
    node = goal
    path_set = []
    while node in path:
        path_set.append(node)
        node = path[node]
    path_set.append(start)
    path_set.reverse()
    return (
        path_set,
        explored_order,
        {
            "nodes_expanded": len(explored),
            "path_length": len(path_set) - 1,
            "path_cost": 0,
        },
    )


# daniel
