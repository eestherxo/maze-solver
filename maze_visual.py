import pygame

from maze_solver import astar, bfs, dfs, greedy_best_first


MAZE = [
	[1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
	[1, "S", 0, 1, 0, 0, 1, 0, 0, 1],
	[1, 0, 0, 0, 1, 0, 1, 1, 0, 1],
	[1, 1, 1, 0, 0, 1, 0, 0, 0, 1],
	[1, 0, 1, 0, 0, 0, 0, 0, 0, 1],
	[1, 0, 0, 0, 0, 0, 1, 1, 0, 1],
	[1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
	[1, 1, 1, 0, 0, 0, 0, 1, 0, 1],
	[1, 0, 0, 1, 0, 0, 0, 0, "G", 1],
	[1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
]
START = (1, 1)
GOAL = (8, 8)

WIDTH = 1040
HEIGHT = 760
CELL_SIZE = 51
CELL_GAP = 3
GRID_X = 42
GRID_Y = 132
VISIT_STEP_MS = 28
PATH_STEP_MS = 60

COLORS = {
	"background": (17, 25, 28),
	"panel": (27, 39, 42),
	"panel_active": (43, 62, 64),
	"text": (239, 239, 222),
	"muted": (157, 177, 169),
	"wall": (45, 65, 67),
	"open": (218, 226, 211),
	"visited": (70, 166, 177),
	"path": (244, 195, 83),
	"start": (53, 166, 119),
	"goal": (234, 111, 81),
	"accent": (167, 218, 133),
	"outline": (89, 114, 111),
}

ALGORITHMS = [
	("BFS", bfs),
	("DFS", dfs),
	("A*", astar),
	("GREEDY", greedy_best_first),
]


def draw_text(surface, font, text, color, position):
	surface.blit(font.render(text, True, color), position)


def main():
	pygame.init()
	screen = pygame.display.set_mode((WIDTH, HEIGHT))
	pygame.display.set_caption("Maze Solver")
	clock = pygame.time.Clock()

	title_font = pygame.font.SysFont("dejavusans", 30, bold=True)
	heading_font = pygame.font.SysFont("dejavusans", 18, bold=True)
	body_font = pygame.font.SysFont("dejavusans", 15)
	small_font = pygame.font.SysFont("dejavusans", 13)

	algorithm_buttons = {}
	for index, (name, _) in enumerate(ALGORITHMS):
		column = index % 2
		row = index // 2
		algorithm_buttons[name] = pygame.Rect(625 + column * 169, 190 + row * 57, 156, 45)
	run_button = pygame.Rect(625, 330, 325, 48)
	reset_button = pygame.Rect(625, 389, 325, 44)

	state = {
		"algorithm": "BFS",
		"phase": "idle",
		"status": "Choose an algorithm, then run it.",
		"visited_order": [],
		"visited_nodes": set(),
		"visible_visits": 0,
		"path": [],
		"path_nodes": set(),
		"visible_path": 0,
		"stats": {"nodes_expanded": 0, "path_length": 0, "path_cost": 0},
		"last_step": 0,
	}

	def reset_search():
		state["phase"] = "idle"
		state["status"] = "Ready. Press Space to run."
		state["visited_order"] = []
		state["visited_nodes"] = set()
		state["visible_visits"] = 0
		state["path"] = []
		state["path_nodes"] = set()
		state["visible_path"] = 0
		state["stats"] = {"nodes_expanded": 0, "path_length": 0, "path_cost": 0}

	def select_algorithm(name):
		state["algorithm"] = name
		reset_search()
		state["status"] = f"{name} selected. Press Space to run."

	def run_search():
		algorithm = next(function for name, function in ALGORITHMS if name == state["algorithm"])
		path, visited_order, stats = algorithm(MAZE, START, GOAL)
		state["visited_order"] = visited_order
		state["visited_nodes"] = set()
		state["visible_visits"] = 0
		state["path"] = path
		state["path_nodes"] = set()
		state["visible_path"] = 0
		state["stats"] = stats
		state["phase"] = "search"
		state["status"] = f"Running {state['algorithm']}..."
		state["last_step"] = pygame.time.get_ticks()

	def draw_button(rect, label, selected=False, primary=False):
		fill = COLORS["accent"] if primary else COLORS["panel_active"] if selected else COLORS["panel"]
		text_color = COLORS["background"] if primary else COLORS["text"]
		pygame.draw.rect(screen, fill, rect, border_radius=7)
		pygame.draw.rect(screen, COLORS["outline"], rect, width=1, border_radius=7)
		rendered = heading_font.render(label, True, text_color)
		screen.blit(rendered, rendered.get_rect(center=rect.center))

	def draw_maze():
		for row, cells in enumerate(MAZE):
			for col, cell in enumerate(cells):
				node = (row, col)
				x = GRID_X + col * (CELL_SIZE + CELL_GAP)
				y = GRID_Y + row * (CELL_SIZE + CELL_GAP)
				rect = pygame.Rect(x, y, CELL_SIZE, CELL_SIZE)

				if cell == 1:
					color = COLORS["wall"]
				elif node == START:
					color = COLORS["start"]
				elif node == GOAL:
					color = COLORS["goal"]
				elif node in state["path_nodes"]:
					color = COLORS["path"]
				elif node in state["visited_nodes"]:
					color = COLORS["visited"]
				else:
					color = COLORS["open"]

				pygame.draw.rect(screen, color, rect, border_radius=4)
				if node == START or node == GOAL:
					marker = heading_font.render("S" if node == START else "G", True, COLORS["text"])
					screen.blit(marker, marker.get_rect(center=rect.center))

	def draw_interface():
		screen.fill(COLORS["background"])
		draw_text(screen, title_font, "MAZE SOLVER", COLORS["text"], (42, 40))
		pygame.draw.line(screen, COLORS["outline"], (42, 108), (998, 108), 1)

		draw_maze()

		draw_text(screen, heading_font, "ALGORITHMS", COLORS["text"], (625, 143))
		for name, _ in ALGORITHMS:
			draw_button(algorithm_buttons[name], name, selected=state["algorithm"] == name)

		draw_button(run_button, "RUN SEARCH   [SPACE]", primary=True)
		draw_button(reset_button, "RESET   [R]")

		draw_text(screen, small_font, "Click an algorithm to select it.", COLORS["muted"], (625, 454))
		draw_text(screen, heading_font, "SEARCH RESULTS", COLORS["text"], (625, 496))
		draw_text(screen, body_font, f"Nodes expanded    {state['stats']['nodes_expanded']}", COLORS["text"], (625, 532))
		draw_text(screen, body_font, f"Path length           {state['stats']['path_length']}", COLORS["text"], (625, 559))
		draw_text(screen, body_font, f"Path cost               {state['stats']['path_cost']}", COLORS["text"], (625, 586))
		draw_text(screen, small_font, state["status"], COLORS["accent"], (625, 632))

		legend_y = 704
		legend = [
			("Wall", COLORS["wall"]),
			("Open", COLORS["open"]),
			("Visited", COLORS["visited"]),
			("Path", COLORS["path"]),
			("Start", COLORS["start"]),
			("Goal", COLORS["goal"]),
		]
		legend_x = 43
		for label, color in legend:
			pygame.draw.rect(screen, color, pygame.Rect(legend_x, legend_y, 15, 15), border_radius=3)
			draw_text(screen, small_font, label, COLORS["muted"], (legend_x + 21, legend_y - 1))
			legend_x += 91 if label != "Visited" else 105

	running = True
	while running:
		now = pygame.time.get_ticks()
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				running = False
			elif event.type == pygame.KEYDOWN:
				if event.key == pygame.K_ESCAPE:
					running = False
				elif event.key == pygame.K_SPACE:
					run_search()
				elif event.key == pygame.K_r:
					reset_search()
			elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
				if run_button.collidepoint(event.pos):
					run_search()
				elif reset_button.collidepoint(event.pos):
					reset_search()
				else:
					for name, rect in algorithm_buttons.items():
						if rect.collidepoint(event.pos):
							select_algorithm(name)
							break

		if state["phase"] == "search" and now - state["last_step"] >= VISIT_STEP_MS:
			if state["visible_visits"] < len(state["visited_order"]):
				node = state["visited_order"][state["visible_visits"]]
				state["visited_nodes"].add(node)
				state["visible_visits"] += 1
				state["last_step"] = now
			else:
				state["phase"] = "path"
				state["status"] = "Search complete. Revealing final path..."
				state["last_step"] = now

		if state["phase"] == "path" and now - state["last_step"] >= PATH_STEP_MS:
			if state["visible_path"] < len(state["path"]):
				node = state["path"][state["visible_path"]]
				state["path_nodes"].add(node)
				state["visible_path"] += 1
				state["last_step"] = now
			else:
				state["phase"] = "done"
				state["status"] = f"{state['algorithm']} complete. Select another algorithm to compare."

		draw_interface()
		pygame.display.flip()
		clock.tick(60)

	pygame.quit()


if __name__ == "__main__":
	main()
