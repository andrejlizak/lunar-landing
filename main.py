import tkinter as tk
from itertools import count

from game.LunarLanderGame import LunarLanderGame
from game.StateLoader import StateLoader
from ui.LunarLanderGUI import LunarLanderGUI

# Main program
root = tk.Tk()

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