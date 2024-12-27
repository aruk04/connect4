**CONNECT4**
A graphical user interface (GUI) implementation of the classic Connect 4 game using Python's Tkinter library.

**Features:**
  Play against another player (2-player mode).
  Play against the computer (AI mode).
  Color and name customization for players.
  Animated drop of discs.
  Displays a winner with a congratulatory GIF (sourced from Google).

**Requirements:**
  Python 3.x
  Tkinter (usually bundled with Python)
  Numpy
  Pillow
  Requests

**Installation:**
  Clone the repository or download the source code.
  Install the required libraries by running:
  bash
  Copy code
  pip install numpy pillow requests

**How to Play:**
Run the script to launch the game window.
Choose a game mode (either 2-player or play against the computer).
Customize player names and colors.
Click on the columns to drop your disc.
_The game checks for a win condition after each move. The first player to align four discs horizontally, vertically, or diagonally wins._

**Running the Game:**
To run the game, simply execute the script:

bash
Copy code
python connect4.py


- The game uses an AI implementation (minimax algorithm) for playing against the computer.
- The congratulatory GIF is sourced from Tenor.
