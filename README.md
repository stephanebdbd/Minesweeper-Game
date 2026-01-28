# Minesweeper Game

This project offers a complete implementation of the popular **Minesweeper game** in a terminal interface. The goal is to find all the mines or uncover all the cells without triggering any mines.

## 🎓 Academic Context

This is an **individual project** developed in **Python** for the *Projet d'informatique* course during the **first year of the Bachelor's in Computer Science** at the **Université libre de Bruxelles (ULB)** (2022-2023).

🏆 **Grade received:** **19/20**

---

## ✨ Features

1. **Customizable Parameters**:
* The user defines the **length** and **width** of the board.
* The user sets the **number of mines** to place.


2. **Interactive Gameplay**:
* Uncover cells to reveal empty spaces or clues.
* Place flags to mark suspected mines.


3. **Win/Loss Conditions**:
* **Win**: All cells are uncovered (excluding mines).
* **Loss**: A mine is uncovered.



---

## 🛠️ Installation

1. Clone the repository:
```bash
git clone https://github.com/stephanebdbd/Minesweeper-Game.git

```


2. Navigate to the project directory:
```bash
cd Minesweeper-Game

```



## 🚀 Execution

Run the game using Python 3 by providing the grid dimensions and mine count as arguments:

```bash
python3 demineur.py <length> <width> <number_of_mines>

```

**Example:**
To play on a 10x10 grid with 20 mines:

```bash
python3 demineur.py 10 10 20

```

---

## 🎮 How to Play

1. **The Board**:
* Cells marked `.` are unrevealed.
* Numbers indicate how many mines are adjacent to that cell.


2. **Commands**:
Each turn, you will be prompted to enter a command following this format: `Action Row Column`.
* **Uncover a cell**: Type `U` followed by coordinates.
* *Example:* `U 3 3` (Uncovers row 3, column 3).


* **Place a flag**: Type `F` followed by coordinates.
* *Example:* `F 2 4` (Flags row 2, column 4).





---

## 📂 Code Structure

* **`demineur.py`**: The main script containing the full game logic:
* Board initialization and display.
* Neighbor calculation and empty cell propagation (flood fill).
* Mine placement algorithms.
* User input handling and game loop.



---

## 👥 Author

**Chris Badi Budu** (Stéphane)

## 📜 License

This project is licensed under the **MIT License**.
