import tkinter as tk

from game.LunarLanderGame import LunarLanderGame
from game.StateLoader import StateLoader
from ui.LunarLanderGUI import LunarLanderGUI

# Main program
root = tk.Tk()

# Načítanie počiatočných stavov
state_loader = StateLoader('game_states.json')
initial_state = state_loader.get_random_state()

# Inicializácia hry s náhodným počiatočným stavom
if initial_state:
    gui = LunarLanderGUI(root, None)
    game = LunarLanderGame(initial_state, gui)
    gui.game = game

root.mainloop()