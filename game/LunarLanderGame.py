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

    def get_possible_moves(self, current_position):
        x, y = current_position
        moves = []

        # Pohyb doľava
        nx = x - 1
        while nx >= 0 and (nx, y) not in self.figures.values():
            nx -= 1
        if nx + 1 != x and nx > 0:
            moves.append((nx + 1, y))

        # Pohyb doprava
        nx = x + 1
        while nx < self.board_size and (nx, y) not in self.figures.values():
            nx += 1
        if nx - 1 != x and nx - 1 < self.board_size - 1:
            moves.append((nx - 1, y))

        # Pohyb nahor
        ny = y - 1
        while ny >= 0 and (x, ny) not in self.figures.values():
            ny -= 1
        if ny + 1 != y and ny > 0:
            moves.append((x, ny + 1))

        # Pohyb nadol
        ny = y + 1
        while ny < self.board_size and (x, ny) not in self.figures.values():
            ny += 1
        if ny - 1 != y and ny - 1 < self.board_size - 1:
            moves.append((x, ny - 1))

        return moves

    def dfs(self):
        """Performs Depth First Search to find a path to the goal."""
        stack = [(self.figures, self.red_position, [])]  # Stack: (figures_positions, red_position, path_to_red)
        visited = set()  # Tracks visited states

        print(stack)

        while stack:
            current_positions, red_position, path = stack.pop()

            # Generate unique state identifier for visited check
            state_identifier = (tuple(sorted(current_positions.items())), red_position)
            if state_identifier in visited:
                continue

            visited.add(state_identifier)
            new_path = path + [red_position]

            # Check if the red figure has reached the goal
            if red_position == self.goal:
                return new_path

            # Iterate over all figures to compute possible moves
            for figure, position in current_positions.items():
                possible_moves = self.get_possible_moves(position)
                print(possible_moves)
                for move in possible_moves:
                    # Create a new state where the current figure moves
                    new_positions = current_positions.copy()
                    new_positions[figure] = move

                    # Update red position if the moved figure is red
                    new_red_position = move if figure == "red" else red_position

                    # Add new state to the stack
                    stack.append((new_positions, new_red_position, new_path))

        # Return empty path if no solution is found
        return []