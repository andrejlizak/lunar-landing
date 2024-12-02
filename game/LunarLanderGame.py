import heapq
from queue import Queue

class LunarLanderGame:
    def __init__(self, initial_state, gui):
        self.board_size = initial_state["board_size"]
        self.red_position = tuple(initial_state["red"])
        self.figures = {color: tuple(pos) for color, pos in initial_state["figures"].items()}
        self.goal = tuple(initial_state["goal"])
        self.gui = gui
        self.create_board()

    def create_board(self):
        """Creates the game grid and draws the elements on it using the GUI"""
        self.gui.draw_grid()  # Draw the empty grid
        self.gui.draw_game_elements(self.red_position, self.figures, self.goal)  # Draw the game pieces

    def update_game_elements(self, new_red_position):
        """Updates the positions of the game elements and redraws them"""
        self.red_position = new_red_position
        self.gui.draw_game_elements(self.red_position, self.figures, self.goal)

