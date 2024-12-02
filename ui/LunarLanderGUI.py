import tkinter as tk


class LunarLanderGUI:
    def __init__(self, root, game, board_size=5):
        self.root = root
        self.game = game
        self.root.title("Lunar Lander")

        # Board dimensions
        self.board_size = board_size
        self.cell_size = 60

        # Canvas for the game grid
        self.canvas = tk.Canvas(root, width=self.board_size * self.cell_size, height=self.board_size * self.cell_size,
                                bg="white")
        self.canvas.pack()

        # Draw the initial grid
        self.draw_grid()

        # Control buttons
        self.control_frame = tk.Frame(root)
        self.control_frame.pack()

        self.bfs_button = tk.Button(self.control_frame, text="Run BFS", command=self.run_bfs)
        self.bfs_button.pack(side=tk.LEFT)

        self.a_star_button = tk.Button(self.control_frame, text="Run A*", command=self.run_a_star)
        self.a_star_button.pack(side=tk.LEFT)

    def draw_grid(self):
        for i in range(self.board_size):
            for j in range(self.board_size):
                x1, y1 = i * self.cell_size, j * self.cell_size
                x2, y2 = x1 + self.cell_size, y1 + self.cell_size

                # Highlight center cell with dark red color
                if (i, j) == (self.board_size // 2, self.board_size // 2):
                    self.canvas.create_rectangle(x1, y1, x2, y2, fill="#8B0000", outline="black", width=2)
                else:
                    self.canvas.create_rectangle(x1, y1, x2, y2, outline="black")

    def draw_game_elements(self, red_position, figures, goal):
        """Draws the red figurine, other figurines, and the goal"""
        # Clear previous drawings
        self.canvas.delete("all")

        # Redraw grid and elements
        self.draw_grid()

        # Draw the other figurines
        for color, (x, y) in figures.items():
            self.draw_cell(x, y, color)

        # Draw the goal
        goal_x, goal_y = goal
        self.draw_cell(goal_x, goal_y, "#780000")

        # Draw the red figurine and bring it to the front
        x, y = red_position
        red_id = self.draw_cell(x, y, "red")
        self.canvas.tag_raise(red_id)

    def draw_cell(self, x, y, color):
        x1, y1 = x * self.cell_size, y * self.cell_size
        x2, y2 = x1 + self.cell_size, y1 + self.cell_size
        return self.canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline="black")

    def run_bfs(self):
        print("Running BFS...")
        path = self.game.bfs()
        if path:
            for position in path:
                self.game.update_game_elements(position)
                self.root.update()
                self.root.after(500)

    def run_a_star(self):
        print("Running A*...")
        path = self.game.a_star()
        if path:
            for position in path:
                self.game.update_game_elements(position)
                self.root.update()
                self.root.after(500)