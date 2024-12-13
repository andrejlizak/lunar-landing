import tkinter as tk
from PIL import Image, ImageTk
import time
from openpyxl import Workbook


class LunarLanderGUI:
    def __init__(self, root, game, board_size=5):
        self.root = root
        self.game = game
        self.root.title("Lunar Lander")

        # Board dimensions
        self.board_size = board_size
        self.cell_size = 100

        # Canvas for the game grid
        self.canvas = tk.Canvas(root, width=self.board_size * self.cell_size, height=self.board_size * self.cell_size,
                                bg="white")
        self.canvas.pack()

        # Draw the initial grid
        self.draw_grid()

        #stats section
        self.stats = tk.Frame(root)
        self.stats.pack()

        # Figures images
        self.figures_images = {
            "goal": self.load_and_resize_image("img/goal.png"),
            "red": self.load_and_resize_image("img/red.png"),
            "blue": self.load_and_resize_image("img/blue.png"),
            "green": self.load_and_resize_image("img/green.png"),
            "yellow": self.load_and_resize_image("img/yellow.png"),
            "orange": self.load_and_resize_image("img/orange.png"),
            "purple": self.load_and_resize_image("img/purple.png")
        }

        # Control buttons
        self.control_frame = tk.Frame(root)
        self.control_frame.pack()
        self.timeText = tk.Text(self.stats, height=4, width=30)
        self.timeText.pack(side=tk.LEFT)

        self.start_button = tk.Button(self.control_frame, text="Start", command=self.run_all)
        self.start_button.pack(side=tk.LEFT)

        self.dfs_button = tk.Button(self.control_frame, text="DFS", command=self.run_dfs)
        self.dfs_button.pack(side=tk.LEFT)

        self.bfs_button = tk.Button(self.control_frame, text="BFS", command=self.run_bfs)
        self.bfs_button.pack(side=tk.LEFT)

        self.greedy_button = tk.Button(self.control_frame, text="Greedy", command=self.run_greedy)
        self.greedy_button.pack(side=tk.LEFT)

        self.astar_button = tk.Button(self.control_frame, text="A*", command=self.run_A_star)
        self.astar_button.pack(side=tk.LEFT)

        # Initialize Excel workbook
        self.workbook = Workbook()
        self.sheet = self.workbook.active
        self.sheet.append(["Algoritmus", "Pocet krokov", "Cas"])

        # Data storage for averages
        self.results = {"DFS": [], "BFS": [], "GreedySearch": [], "A*": []}

    def load_and_resize_image(self, image_path):
        """Loads and resizes the image to match the cell size."""
        img = Image.open(image_path)
        img = img.resize((self.cell_size, self.cell_size), Image.Resampling.LANCZOS)  # Resize image
        return ImageTk.PhotoImage(img)

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

        # Draw the goal
        goal_x, goal_y = goal
        self.draw_cell(goal_x, goal_y, "goal")

        # Draw the other figurines
        for color, (x, y) in figures.items():
            self.draw_cell(x, y, color)

        # Draw the red figurine and bring it to the front
        if red_position is not None:
            x, y = red_position
            self.draw_cell(x, y, "red")

    def draw_cell(self, x, y, figure_key):
        """Draws an image instead of a color for the specified figure."""
        x1, y1 = x * self.cell_size, y * self.cell_size
        if figure_key in self.figures_images:
            self.canvas.create_image(x1 + self.cell_size // 2, y1 + self.cell_size // 2,
                                     image=self.figures_images[figure_key])

    def run_bfs(self):
        print("Running BFS...")
        start = time.time()
        path, steps = self.game.bfs()
        end = time.time()
        real_time = round((end - start), 3)
        if path:
            self.timeText.insert(tk.END, f"Čas algoritmu BFS: {real_time}\n")
            self.timeText.yview(tk.END)
            self.sheet.append(["BFS", steps, real_time])
            self.results["BFS"].append((steps, real_time))
            self.root.update_idletasks()
            return real_time
        else:
            self.timeText.insert(tk.END, "Nenašlo sa riešenie\n")
            self.timeText.yview(tk.END)
            self.sheet.append(["BFS", steps, -1])
            self.root.update_idletasks()
            return -1

    def run_dfs(self):
        print("Running DFS...")
        start = time.time()
        path, steps = self.game.dfs()
        end = time.time()
        real_time = round((end - start), 3)
        if path:
            self.timeText.insert(tk.END, f"Čas algoritmu DFS: {real_time}\n")
            self.timeText.yview(tk.END)
            self.sheet.append(["DFS", steps, real_time])
            self.results["DFS"].append((steps, real_time))
            self.root.update_idletasks()
            return real_time
        else:
            self.timeText.insert(tk.END, "Nenašlo sa riešenie\n")
            self.timeText.yview(tk.END)
            self.sheet.append(["DFS", steps, -1])
            self.root.update_idletasks()
            return -1

    def run_greedy(self):
        print("Running GreedySearch...")
        start = time.time()
        path, steps = self.game.greedy_search()
        end = time.time()
        real_time = round((end - start), 3)
        if path:
            self.timeText.insert(tk.END, f"Čas algoritmu GreedySearch: {real_time}\n")
            self.timeText.yview(tk.END)
            self.sheet.append(["GreedySearch", steps, real_time])
            self.results["GreedySearch"].append((steps, real_time))
            self.root.update_idletasks()
            return real_time
        else:
            self.timeText.insert(tk.END, "Nenašlo sa riešenie\n")
            self.timeText.yview(tk.END)
            self.sheet.append(["GreedySearch", steps, -1])
            self.root.update_idletasks()
            return -1

    def run_A_star(self):
        print("Running A*...")
        start = time.time()
        path, steps = self.game.greedy_search()
        end = time.time()
        real_time = round((end - start), 3)
        if path:
            self.timeText.insert(tk.END, f"Čas algoritmu A*: {real_time}\n")
            self.timeText.yview(tk.END)
            self.sheet.append(["A*", steps, real_time])
            self.results["A*"].append((steps, real_time))
            self.root.update_idletasks()
            return real_time
        else:
            self.timeText.insert(tk.END, "Nenašlo sa riešenie\n")
            self.timeText.yview(tk.END)
            self.sheet.append(["A*", steps, -1])
            self.root.update_idletasks()
            return -1

    def run_all(self):
        # Append the times to the Excel sheet
        self.run_dfs()
        self.run_bfs()
        self.run_greedy()
        self.run_A_star()

    def export(self):
        # Save the workbook after every state
        self.calculate_averages()
        self.workbook.save("game_results.xlsx")

    def calculate_averages(self):
        """Calculate average steps and times for each algorithm and write them to the Excel sheet."""
        self.sheet.append([])  # Empty row for separation
        self.sheet.append(["Algoritmus", "Priemerny pocet krokov", "Priemerny cas"])

        for algorithm, results in self.results.items():
            # Filter out invalid results (-1 indicates no solution found)
            valid_results = [r for r in results if r[1] != -1]

            if valid_results:
                avg_steps = round(sum(r[0] for r in valid_results) / len(valid_results), 2)
                avg_time = round(sum(r[1] for r in valid_results) / len(valid_results), 3)
            else:
                avg_steps = 0
                avg_time = 0

            # Append averages to the sheet
            self.sheet.append([algorithm, avg_steps, avg_time])