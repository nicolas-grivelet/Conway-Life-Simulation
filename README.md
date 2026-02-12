# Conway's Game of Life – Python Simulation

An interactive, object-oriented implementation of John Conway's Game of Life built with Python's native `tkinter` library. This project demonstrates cellular automaton logic coupled with a dynamic graphical user interface, featuring real-time speed control and state management.

---

## 🚀 Features

- **Interactive Grid**: Click to toggle cells alive/dead or cycle through colors manually.
- **Dynamic Speed Control**: Real-time adjustment of the simulation speed using a slider.
- **Color Cycling**: Visual representation of cell states using a custom color palette.
- **Object-Oriented Design**: Clean separation between the UI controller and the simulation board logic.
- **Responsive Layout**: The grid adapts to the window size.

---

## 🛠️ Installation

No external dependencies are required. This project uses only the standard Python library.

Clone the repository:

```bash
git clone https://github.com/nicolas-grivelet/Conway-Life-Simulation.git
````

Navigate to the source directory:

```bash
cd Conway-Life-Simulation/src
```

---

## 🎮 Usage

Run the main script to start the simulation window:

```bash
python main.py
```

### Controls

* **Left Click**: Spawn a cell / Change its color.
* **Play/Pause Button**: Start or stop the evolution cycle.
* **Slider**: Adjust the refresh rate (Simulation Speed).

---

## 🧠 Logic

The simulation follows the standard rules:

* **Underpopulation**: A live cell with fewer than 2 neighbors dies.
* **Stasis**: A live cell with 2 or 3 neighbors lives on.
* **Overpopulation**: A live cell with more than 3 neighbors dies.
* **Reproduction**: A dead cell with exactly 3 neighbors becomes a live cell.

---

## 📂 Project Structure

```text
Conway-Life-Simulation/
├── README.md            # Project documentation
├── LICENSE             # MIT License
├── requirements.txt    # Dependencies (None required)
└── src/                # Source code
    └── main.py         # Main application entry point
```

---

## 📝 License

Distributed under the MIT License. See `LICENSE` for more information.
