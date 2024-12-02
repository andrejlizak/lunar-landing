import json
import random


class StateLoader:
    def __init__(self, file_path):
        self.file_path = file_path
        self.states = self.load_initial_states()

    def load_initial_states(self):
        """Načíta počiatočné stavy zo súboru"""
        try:
            with open(self.file_path, 'r') as file:
                data = json.load(file)
            return data
        except FileNotFoundError:
            print(f"Chyba: Súbor {self.file_path} neexistuje.")
            return []
        except json.JSONDecodeError:
            print("Chyba pri načítaní JSON súboru.")
            return []

    def get_state(self, index):
        """Získa konkrétny stav podľa indexu"""
        if 0 <= index < len(self.states):
            return self.states[index]
        else:
            print("Neplatný index stavu.")
            return None

    def get_random_state(self):
        """Získa náhodný stav"""
        return random.choice(self.states) if self.states else None
