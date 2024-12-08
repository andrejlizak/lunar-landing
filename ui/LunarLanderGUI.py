import tkinter as tk
import time

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

        #stats section
        self.stats = tk.Frame(root)
        self.stats.pack()

        # Control buttons
        self.control_frame = tk.Frame(root)
        self.control_frame.pack()
        self.timeText = tk.Text(self.stats, height=2, width=30)
        self.timeText.pack(side=tk.LEFT)

        self.dfs_button = tk.Button(self.control_frame, text="Run DFS", command=self.run_dfs)
        self.dfs_button.pack(side=tk.LEFT)

        self.bfs_button = tk.Button(self.control_frame, text="Run BFS", command=self.run_bfs)
        self.bfs_button.pack(side=tk.LEFT)

        self.a_star_button = tk.Button(self.control_frame, text="Run A*", command=self.run_A_star)
        self.a_star_button.pack(side=tk.LEFT)

        self.greeedy_search_button = tk.Button(self.control_frame, text="Run GreedySearch", command=self.run_greedy)
        self.greeedy_search_button.pack(side=tk.LEFT)

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
        middle_id = self.draw_cell(goal_x, goal_y, "#780000")
        self.canvas.tag_lower(middle_id)

        #Draw the red figurine and bring it to the front
        if red_position is not None:
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

    def run_dfs(self):
        print("Running DFS...")
        self.timeText.delete(1.0, tk.END)
        start = time.time()
        path = self.game.dfs()
        end = time.time()
        if path:
            self.timeText.insert(tk.END, f"Čas algoritmu DFS: {round((end - start), 3)}\n")
        else:
            self.timeText.insert(tk.END, "Nenašlo sa riešenie\n")

    def run_greedy(self):
        print("Running GreedySearch...")
        self.timeText.delete(1.0, tk.END)
        start = time.time()
        path = self.game.greedy_search()
        end = time.time()
        if path:
            self.timeText.insert(tk.END, f"Čas algoritmu GreedySearch: {round((end - start), 3)}\n")
        else:
            self.timeText.insert(tk.END, "Nenašlo sa riešenie\n")

    def run_A_star(self):
        print("Running A*...")
        self.timeText.delete(1.0, tk.END)
        start = time.time()
        path = self.game.greedy_search()
        end = time.time()
        if path:
            self.timeText.insert(tk.END, f"Čas algoritmu A*: {round((end - start), 3)}\n")
        else:
            self.timeText.insert(tk.END, "Nenašlo sa riešenie\n")