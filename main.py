import tkinter as tk

from game.LunarLanderGame import LunarLanderGame
from game.StateLoader import StateLoader
from ui.LunarLanderGUI import LunarLanderGUI

# Main program
root = tk.Tk()

# Center the window on the screen
window_width = 600  # Width of the window
window_height = 600  # Height of the window

# Get the screen width and height
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

# Calculate the position of the window
x_position = (screen_width // 2) - (window_width // 2)
y_position = (screen_height // 2) - (window_height // 2)

# Set the position of the window
root.geometry(f"{window_width}x{window_height}+{x_position}+{y_position}")

root.attributes("-topmost", 1)

# Načítanie počiatočných stavov
state_loader = StateLoader('game_states.json')
initial_states = state_loader.load_initial_states()

# Inicializácia ui
gui = LunarLanderGUI(root, None)

# Iterácia cez všetky počiatočné stavy
for initial_state in initial_states:
    gui.root.update_idletasks()
    game = LunarLanderGame(initial_state, gui)
    gui.game = game
    gui.run_all()

gui.export()
root.mainloop()