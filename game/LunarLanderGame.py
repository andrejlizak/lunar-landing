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
        self.gui.draw_grid()  # Draw the empty grid
        self.gui.draw_game_elements(self.red_position, self.figures, self.goal)

    def update_game_elements(self, figures):
        self.gui.draw_game_elements(None, figures, self.goal)

    def get_possible_moves(self, current_position, figures):
        x, y = current_position
        moves = []

        # Pohyb doľava
        nx = x - 1
        while nx >= 0 and (nx, y) not in figures.values():
            nx -= 1
        if nx + 1 != x and nx > 0:
            moves.append((nx + 1, y))

        # Pohyb doprava
        nx = x + 1
        while nx < self.board_size and (nx, y) not in figures.values():
            nx += 1
        if nx - 1 != x and nx - 1 < self.board_size - 1:
            moves.append((nx - 1, y))

        # Pohyb nahor
        ny = y - 1
        while ny >= 0 and (x, ny) not in figures.values():
            ny -= 1
        if ny + 1 != y and ny > 0:
            moves.append((x, ny + 1))

        # Pohyb nadol
        ny = y + 1
        while ny < self.board_size and (x, ny) not in figures.values():
            ny += 1
        if ny - 1 != y and ny - 1 < self.board_size - 1:
            moves.append((x, ny - 1))

        return moves

    def dfs(self):
        """Performs Depth First Search to find a path to the goal."""
        figures_with_red = self.figures.copy()
        figures_with_red.update({'red': self.red_position})

        stack = [(figures_with_red, self.red_position, [])]  # Stack: (figures_positions, red_position, path_to_red)
        visited = set()


        while stack:
            current_positions, red_position, path = stack.pop()

            print(f"Current positions: {current_positions}")

            state_identifier = (tuple(sorted(current_positions.items())), red_position)
            if state_identifier in visited:
                continue

            visited.add(state_identifier)
            new_path = path + [red_position]

            if red_position == self.goal:
                stack.append((current_positions, red_position, new_path))
                print(stack)
                return stack

            for figure, position in current_positions.items():
                print(f"Current figure: {figure}, position: {position}")
                possible_moves = self.get_possible_moves(position, current_positions)
                print(f"Possible moves: {possible_moves}")
                for move in possible_moves:
                    # Create a new state where the current figure moves
                    new_positions = current_positions.copy()
                    new_positions[figure] = move

                    self.update_game_elements(new_positions)
                    self.gui.root.update()
                    delay_between_moves = 0
                    self.gui.root.after(delay_between_moves)

                    print(f"moving: {figure} from {position} to {move}")
                    print(f"Current positions: {new_positions}")

                    new_red_position = move if figure == "red" else red_position

                    stack.append((new_positions, new_red_position, new_path))
            print("\n")

        print("No solution found.")
        return []

    def greedy_search(self):
        """Performs Greedy Search to find a path to the goal."""
        figures_with_red = self.figures.copy()
        figures_with_red.update({'red': self.red_position})

        # Priority queue (heap) based on heuristic distance to the goal
        heap = []
        start_state = (
            self.heuristic(self.red_position), tuple(sorted(figures_with_red.items())), self.red_position, []
        )
        heapq.heappush(heap, start_state)

        visited = set()

        while heap:
            _, figures_tuple, red_position, path = heapq.heappop(heap)

            # Convert the tuple of figures back into a dictionary
            current_positions = dict(figures_tuple)

            # Use a tuple of sorted items to uniquely identify states
            state_identifier = (figures_tuple, red_position)
            if state_identifier in visited:
                continue

            visited.add(state_identifier)
            new_path = path + [red_position]

            # Check if the red position is the goal
            if red_position == self.goal:
                print("Goal reached!")
                return new_path

            for figure, position in current_positions.items():
                print(f"Current figure: {figure}, position: {position}")
                possible_moves = self.get_possible_moves(position, current_positions)
                print(f"Possible moves: {possible_moves}")
                for move in possible_moves:
                    # Create a new state
                    new_positions = current_positions.copy()
                    new_positions[figure] = move
                    new_red_position = move if figure == "red" else red_position

                    self.update_game_elements(new_positions)
                    self.gui.root.update()
                    delay_between_moves = 0
                    self.gui.root.after(delay_between_moves)

                    print(f"moving: {figure} from {position} to {move}")
                    print(f"Current positions: {new_positions}")

                    # Convert the dictionary into a sorted tuple
                    new_positions_tuple = tuple(sorted(new_positions.items()))

                    # Push the new state into the heap with its heuristic value
                    heapq.heappush(
                        heap,
                        (self.heuristic(new_red_position), new_positions_tuple, new_red_position, new_path),
                    )

        print("No solution found.")
        return []

    def a_star_search(self):
        """Performs A* Search to find a path to the goal."""
        figures_with_red = self.figures.copy()
        figures_with_red.update({'red': self.red_position})

        # Priority queue (heap) based on f(n) = g(n) + h(n)
        heap = []
        start_state = (
            self.heuristic(self.red_position) + 0,  # f(n) = h(n) + g(n)
            0,  # g(n), cost-so-far
            tuple(sorted(figures_with_red.items())),
            self.red_position,
            []
        )
        heapq.heappush(heap, start_state)

        visited = set()

        while heap:
            _, cost_so_far, figures_tuple, red_position, path = heapq.heappop(heap)

            # Convert the tuple of figures back into a dictionary
            current_positions = dict(figures_tuple)

            # Use a tuple of sorted items to uniquely identify states
            state_identifier = (figures_tuple, red_position)
            if state_identifier in visited:
                continue

            visited.add(state_identifier)
            new_path = path + [red_position]

            # Check if the red position is the goal
            if red_position == self.goal:
                print("Goal reached!")
                return new_path

            for figure, position in current_positions.items():
                print(f"Current figure: {figure}, position: {position}")
                possible_moves = self.get_possible_moves(position, current_positions)
                print(f"Possible moves: {possible_moves}")
                for move in possible_moves:
                    # Create a new state
                    new_positions = current_positions.copy()
                    new_positions[figure] = move
                    new_red_position = move if figure == "red" else red_position

                    self.update_game_elements(new_positions)
                    self.gui.root.update()
                    delay_between_moves = 0
                    self.gui.root.after(delay_between_moves)

                    print(f"moving: {figure} from {position} to {move}")
                    print(f"Current positions: {new_positions}")

                    # Calculate g(n) (cost-so-far) and f(n)
                    new_cost_so_far = cost_so_far + 1  # Assume every move has a cost of 1
                    heuristic_value = self.heuristic(new_red_position)
                    f_value = new_cost_so_far + heuristic_value

                    # Convert the dictionary into a sorted tuple
                    new_positions_tuple = tuple(sorted(new_positions.items()))

                    # Push the new state into the heap with its f(n) value
                    heapq.heappush(
                        heap,
                        (f_value, new_cost_so_far, new_positions_tuple, new_red_position, new_path),
                    )

        print("No solution found.")
        return []

    def heuristic(self, position):
        """Calculates the Manhattan distance from a position to the goal."""
        return abs(position[0] - self.goal[0]) + abs(position[1] - self.goal[1])