"""
Conway's Game of Life Simulation.

This module provides a GUI implementation of the famous cellular automaton
devised by the British mathematician John Horton Conway in 1970.
Implemented using Python's Tkinter library.

Author: nicolas-grivelet
Date: November 2022
"""

import tkinter as tk
from tkinter import font


class ControllerPanel(tk.Canvas):
    """
    Control panel for the simulation (Play/Pause, Speed).
    """
    def __init__(self, board, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.board = board
        self.symbols = ['⏸', '▷']  # Pause / Play symbols
        
        # UI Components
        self.pause_button = tk.Button(
            self, 
            text=self.symbols[1], 
            font=("Arial", 25), 
            command=self.change_pause_state
        )
        
        self.speed_var = tk.DoubleVar()
        self.speed_scale = tk.Scale(
            self, 
            var=self.speed_var, 
            from_=0, to=100, 
            orient=tk.HORIZONTAL, 
            command=self.set_speed,
            label="Simulation Speed"
        )
        
        self._init_layout()

    def _init_layout(self):
        """Initializes the layout of the control panel."""
        self.pause_button.place(relx=0.4, rely=0.4)
        self.speed_scale.place(relx=0.4, rely=0.25)
        self.speed_scale.set(self.board.speed)

    def set_speed(self, value):
        """Updates the simulation speed."""
        self.board.speed = int(value)

    def change_pause_state(self):
        """Toggles between Play and Pause states."""
        current_symbol_idx = self.symbols.index(self.pause_button["text"])
        next_idx = (current_symbol_idx + 1) % len(self.symbols)
        
        self.pause_button.config(text=self.symbols[next_idx])
        
        # Execute the corresponding method: resume() or stop()
        if next_idx == 0:
            self.board.resume()
        else:
            self.board.stop()


class Board(tk.Canvas):
    """
    Main simulation board handling the grid logic and rendering.
    """
    def __init__(self,
                 nrows: int = 20,
                 ncols: int = 50,
                 cell_dimensions: tuple[int, int] = (30, 30),
                 active_colors: tuple[str] = ("white", "#9BFF23", "#23EEFF", "#EB23FF", "#FFA523"),
                 disabled_color: str = "black",
                 speed: int = 20,
                 *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Configuration
        self.nrows = nrows
        self.ncols = ncols
        self.cell_dimensions = cell_dimensions
        self.active_colors = list(active_colors)
        self.disabled_color = disabled_color
        self.speed = speed
        
        # State
        self.cells = []
        self.active_cells = []
        self._stopped = True
        
        self.controller = ControllerPanel(self)

    def place(self, *args, **kwargs):
        """Overridden place method to setup the grid and controller."""
        self.controller.place(x=0, y=0, relwidth=0.1, relheight=1.0)
        self._init_grid()
        self.master.update()
        
        # Responsive sizing
        self.config(height=self.master.winfo_height(), width=self.master.winfo_width())
        tk.Canvas.place(self, x=int(self.controller.winfo_reqwidth() / 2), y=0)
        
        self._stopped = True
        # Initial delay before auto-start (optional)
        self.master.after(1000, self.update_cells)

    def _init_grid(self):
        """Generates the grid of buttons."""
        self.config(bg=self.disabled_color)
        self.cells = [
            [
                tk.Button(self, width=3, bg=self.disabled_color, borderwidth=1)
                for _ in range(self.ncols)
            ]
            for _ in range(self.nrows)
        ]
        
        for y in range(self.nrows):
            for x in range(self.ncols):
                button = self.cells[y][x]
                # Lambda capture fix
                button.configure(command=lambda b=button: self.toggle_cell(button=b))
                button.grid(column=x, row=y)

    def toggle_cell(self, col=None, row=None, button=None):
        """Manually activates or alters a cell's state."""
        if button is None and col is not None and row is not None:
             button = self.cells[row][col]

        if button in self.active_cells:
            # Cycle through colors if already active
            current_color_idx = self.active_colors.index(button["bg"])
            next_color = self.active_colors[(current_color_idx + 1) % len(self.active_colors)]
            button.config(bg=next_color)
        else:
            # Activate cell
            self.active_cells.append(button)
            button.configure(bg=self.active_colors[0])

    def deactivate_cell(self, button):
        """Kills a cell."""
        if button in self.active_cells:
            self.active_cells.remove(button)
        button.configure(bg=self.disabled_color)

    def get_neighbors_count(self, row, col):
        """Calculates alive neighbors for a specific cell."""
        count = 0
        for y in range(max(0, row-1), min(self.nrows, row+2)):
            for x in range(max(0, col-1), min(self.ncols, col+2)):
                if (y, x) != (row, col):
                    if self.cells[y][x] in self.active_cells:
                        count += 1
        return count

    def update_cells(self):
        """Main game loop: applies Conway's rules."""
        if self._stopped:
            return

        cells_to_activate = []
        cells_to_deactivate = []

        # Logic optimization possible here, but keeping original structure for stability
        for row in range(self.nrows):
            for col in range(self.ncols):
                alive_neighbors = self.get_neighbors_count(row, col)
                current_cell = self.cells[row][col]
                is_alive = current_cell in self.active_cells

                if not is_alive and alive_neighbors == 3:
                    cells_to_activate.append(current_cell)
                elif is_alive and alive_neighbors not in [2, 3]:
                    cells_to_deactivate.append(current_cell)

        # Batch update
        for btn in cells_to_activate:
            if btn not in self.active_cells:
                self.active_cells.append(btn)
                btn.configure(bg=self.active_colors[0])
        
        for btn in cells_to_deactivate:
            self.deactivate_cell(btn)

        # Calculate delay based on speed slider
        # Speed 100 -> small delay, Speed 0 -> large delay
        delay = max(10, int(1000 - (self.speed * 9)))
        self.master.after(delay, self.update_cells)

    def stop(self):
        self._stopped = True

    def resume(self):
        self._stopped = False
        self.update_cells()


if __name__ == "__main__":
    window = tk.Tk()
    window.title("Game of Life - Simulation")
    # Make it full screen or large enough
    window.geometry("1400x800")
    
    board = Board()
    board.place()
    
    window.mainloop()
