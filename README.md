# Minesweeper Game

This project offers a simple implementation of the popular **Minesweeper game** in the terminal. The goal is to find all the mines or uncover all the cells without triggering any mines.

---

## General Information
- **Creator**: Stéphane Badi Budu
- **Date of Creation**: December 1, 2022

---

## Features
1. **User defines the following parameters**:
   - The **length** and **width** of the board.
   - The **number of mines** to place.
2. The player interacts with the board by:
   - Uncovering cells.
   - Placing flags to mark suspected mines.
3. The game ends when:
   - All cells are uncovered (excluding mines).
   - A mine is uncovered (loss).

---

## Inputs
- **Board dimensions**: length and width.
- **Number of mines**: number of cells to trap.
- Cell selection: action (U for uncover, F for flag) and the coordinates of the selected cell.

## Outputs
- Displays the game board, updated after every action.

---

## Installation
1. Clone the repository:
   ```
   git clone <URL_REPO>
   ```
2. Navigate to the project directory:
   ```bash
   cd infof106-projet1-TBKNbr1
   ```

---

## Execution
1. Simply run the game by executing:
   ```bash
   python3 demineur.py <length> <width> <number_of_mines>
   ```
   Replace `<length>`, `<width>`, and `<number_of_mines>` with your custom parameters.
   For example:
   ```bash
   python3 demineur.py 10 10 20
   ```

---

## Rules
1. **Game Board**:
   - Cells marked `.` are unrevealed.
   - Uncover a cell (action `U`) to reveal its content.
   - Place a flag (action `F`) to mark a suspected mine.
2. **Interactions**:
   - You are prompted to input the command, coordinates, and action each turn.
     Examples:
     - `U 3 3`: uncover cell (3, 3).
     - `F 2 4`: flag cell (2, 4).
3. **Winning Conditions**:
   - You win if all cells (excluding mines) are uncovered.
   - You lose if you click on a mine.

---

## Code Structure

- **Main Files**:
  - `demineur.py` — contains the full game logic, including:
    - Board creation and display.
    - Neighbor and propagation handling.
    - Mine placement.
    - User action handling.

---

## Author

This implementation of the Minesweeper game was developed by Stéphane Badi Budu.