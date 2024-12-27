import tkinter as tk
import numpy as np #type:ignore
import random
import time
import requests #type:ignore
from io import BytesIO
from PIL import Image, ImageTk, ImageSequence #type:ignore




class Connect4:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Connect 4")
        self.rows = 6
        self.cols = 7
        self.board = np.zeros((self.rows, self.cols), dtype=int)
        self.turn = 1  # Player 1 starts
        self.mode = None
        self.player_names = ["Player 1", "Player 2"]
        self.player_colors = ["red", "yellow"]
        self.setup_mode_selection()

    def setup_mode_selection(self):
        tk.Label(self.window, text="Choose Game Mode:", font=("Arial", 40)).pack(pady=10)

        # Create a frame for centering the buttons
        button_frame = tk.Frame(self.window)
        button_frame.pack(expand=True)

        # Style for the buttons
        button_style = {
            'font': ("Arial", 16, "bold"),
            'width': 20,  # Button width
            'height': 3,  # Button height
            'bd': 5,  # Border width
            'relief': 'solid',  # Button border
            'bg': '#4CAF50',  # Button background color
            'fg': 'white',  # Text color
            'activebackground': '#45a049',  # Active background color
            'activeforeground': 'white',  # Active text color
            'highlightthickness': 0,  # Remove button border when clicked
        }

        # Pack the buttons side by side inside the frame
        tk.Button(button_frame, text="Two Players", command=self.setup_two_player, **button_style).pack(side="left", padx=10, pady=10)
        tk.Button(button_frame, text="Play Against Computer", command=self.start_vs_computer, **button_style).pack(side="left", padx=10, pady=10)

        # Adjust the window size to fit the buttons in the center
        self.window.geometry("500x400")  # Set window size
        self.window.mainloop()


    def setup_two_player(self):
        self.mode = "two_player"

        # Clear previous widgets
        for widget in self.window.winfo_children():
            widget.destroy()

        # Set a background color and padding for the window
        self.window.config(bg="#f0f0f0")
        
        # Title Label
        title_label = tk.Label(self.window, text="Two Player Setup", font=("Arial", 24, "bold"), bg="#f0f0f0", fg="#4CAF50")
        title_label.pack(pady=20)

        # Player 1 Name
        player1_name_label = tk.Label(self.window, text="Enter Player 1 Name:", font=("Arial", 14), bg="#f0f0f0")
        player1_name_label.pack(pady=5)
        self.player1_name_entry = tk.Entry(self.window, font=("Arial", 14), width=25)
        self.player1_name_entry.pack(pady=10)

        # Player 2 Name
        player2_name_label = tk.Label(self.window, text="Enter Player 2 Name:", font=("Arial", 14), bg="#f0f0f0")
        player2_name_label.pack(pady=5)
        self.player2_name_entry = tk.Entry(self.window, font=("Arial", 14), width=25)
        self.player2_name_entry.pack(pady=10)

        # Player 1 Color
        player1_color_label = tk.Label(self.window, text="Choose Player 1 Color:", font=("Arial", 14), bg="#f0f0f0")
        player1_color_label.pack(pady=5)
        self.player1_color_var = tk.StringVar(value=self.player_colors[0])
        color_options = ["red", "yellow", "green", "blue"]
        self.player1_color_menu = tk.OptionMenu(self.window, self.player1_color_var, *color_options, command=self.update_color_options)
        self.player1_color_menu.config(font=("Arial", 12), width=20)
        self.player1_color_menu.pack(pady=10)

        # Player 2 Color
        player2_color_label = tk.Label(self.window, text="Choose Player 2 Color:", font=("Arial", 14), bg="#f0f0f0")
        player2_color_label.pack(pady=5)
        self.player2_color_var = tk.StringVar(value=self.player_colors[1])
        self.player2_color_menu = tk.OptionMenu(self.window, self.player2_color_var, *color_options)
        self.player2_color_menu.config(font=("Arial", 12), width=20)
        self.player2_color_menu.pack(pady=10)

        # Start Game Button
        start_button = tk.Button(self.window, text="Start Game", command=self.start_two_player, font=("Arial", 16, "bold"), bg="#4CAF50", fg="white", width=20, height=2)
        start_button.pack(pady=20)

    def update_color_options(self, selected_color):
        # Update available colors for Player 2
        color_options = ["red", "yellow", "green", "blue"]
        color_options.remove(selected_color)
        self.player2_color_var.set(color_options[0])  # Set default color for Player 2
        self.player2_color_menu['menu'].delete(0, 'end')  # Clear existing options
        for color in color_options:
            self.player2_color_menu['menu'].add_command(label=color, command=tk._setit(self.player2_color_var, color))


    def start_two_player(self):
        self.player_names[0] = self.player1_name_entry.get() or "Player 1"
        self.player_names[1] = self.player2_name_entry.get() or "Player 2"
        self.player_colors[0] = self.player1_color_var.get()
        self.player_colors[1] = self.player2_color_var.get()
        self.setup_game_board()

    def start_vs_computer(self):
        self.mode = "vs_computer"
        self.setup_game_board()

    def setup_game_board(self):
        for widget in self.window.winfo_children():
            widget.destroy()

        self.canvas = tk.Canvas(self.window, width=self.cols*100, height=self.rows*100, bg="skyblue")
        self.canvas.pack()
        self.canvas.bind("<Button-1>", self.handle_click)

        for r in range(self.rows):
            for c in range(self.cols):
                self.draw_circle(c, r, "white")

    def draw_circle(self, col, row, color):
        x1 = col * 100 + 10
        y1 = row * 100 + 10
        x2 = x1 + 80
        y2 = y1 + 80
        self.canvas.create_oval(x1, y1, x2, y2, fill=color)

    def animate_drop(self, col, row, color):
        for r in range(row + 1):
            self.draw_circle(col, r, color)
            self.window.update()
            time.sleep(0.05)
            if r != row:
                self.draw_circle(col, r, "white")

    def handle_click(self, event):
        col = event.x // 100
        if self.is_valid_move(col):
            row = self.get_next_open_row(col)
            self.animate_drop(col, row, self.player_colors[self.turn - 1])
            self.make_move(row, col, self.turn)

            if self.check_win(self.turn):
                self.display_winner_screen(self.player_names[self.turn - 1])
                return


            self.turn = 3 - self.turn  # Switch turns

            if self.mode == "vs_computer" and self.turn == 2:
                self.computer_move()

    def computer_move(self):
        best_score = -float("inf")
        best_col = random.choice([c for c in range(self.cols) if self.is_valid_move(c)])

        for col in range(self.cols):
            if self.is_valid_move(col):
                row = self.get_next_open_row(col)
                self.board[row, col] = 2
                score = self.minimax(self.board, 3, False, -float("inf"), float("inf"))
                self.board[row, col] = 0
                if score > best_score:
                    best_score = score
                    best_col = col

        row = self.get_next_open_row(best_col)
        self.animate_drop(best_col, row, self.player_colors[1])
        self.make_move(row, best_col, 2)

        if self.check_win(2):
            self.display_winner_screen(self.player_names[1])
            return


        self.turn = 1

    def minimax(self, board, depth, is_maximizing, alpha, beta):
        if self.check_win(2):
            return 100
        elif self.check_win(1):
            return -100
        elif not any(self.is_valid_move(c) for c in range(self.cols)) or depth == 0:
            return 0

        if is_maximizing:
            max_eval = -float("inf")
            for col in range(self.cols):
                if self.is_valid_move(col):
                    row = self.get_next_open_row(col)
                    board[row, col] = 2
                    eval = self.minimax(board, depth-1, False, alpha, beta)
                    board[row, col] = 0
                    max_eval = max(max_eval, eval)
                    alpha = max(alpha, eval)
                    if beta <= alpha:
                        break
            return max_eval
        else:
            min_eval = float("inf")
            for col in range(self.cols):
                if self.is_valid_move(col):
                    row = self.get_next_open_row(col)
                    board[row, col] = 1
                    eval = self.minimax(board, depth-1, True, alpha, beta)
                    board[row, col] = 0
                    min_eval = min(min_eval, eval)
                    beta = min(beta, eval)
                    if beta <= alpha:
                        break
            return min_eval

    def is_valid_move(self, col):
        return self.board[0, col] == 0

    def get_next_open_row(self, col):
        for r in range(self.rows-1, -1, -1):
            if self.board[r, col] == 0:
                return r

    def make_move(self, row, col, player):
        self.board[row, col] = player

    def check_win(self, player):
        # Check horizontal, vertical, and diagonal wins
        for r in range(self.rows):
            for c in range(self.cols-3):
                if all(self.board[r, c+i] == player for i in range(4)):
                    return True

        for r in range(self.rows-3):
            for c in range(self.cols):
                if all(self.board[r+i, c] == player for i in range(4)):
                    return True

        for r in range(self.rows-3):
            for c in range(self.cols-3):
                if all(self.board[r+i, c+i] == player for i in range(4)):
                    return True

        for r in range(3, self.rows):
            for c in range(self.cols-3):
                if all(self.board[r-i, c+i] == player for i in range(4)):
                    return True

        return False


    def display_winner_screen(self, winner):
    # Clear the screen
        for widget in self.window.winfo_children():
            widget.destroy()

    # Display winner message
        tk.Label(self.window, text=f"{winner} wins!", font=("Arial", 24)).pack()

    # URL of the GIF
        gif_url = "https://media.tenor.com/1IPOZiZ6Z4AAAAAM/congratulations.gif"

    # Download the GIF
        response = requests.get(gif_url)
        gif_data = BytesIO(response.content)  # Save GIF in memory buffer

    # Create a label for the GIF
        gif_label = tk.Label(self.window)
        gif_label.pack()

    # Animate the GIF
        self.animate_gif(gif_data, gif_label)

    def animate_gif(self, gif_data, gif_label):
        gif = Image.open(gif_data)  # Load the GIF from memory buffer
        frames = []
        
        # Resize the frames
        new_width = 500  # Set desired width
        new_height = 300  # Set desired height
        for frame in ImageSequence.Iterator(gif):
            resized_frame = frame.resize((new_width, new_height))  # Resize each frame
            frames.append(ImageTk.PhotoImage(resized_frame))

        def update_frame(index):
            frame = frames[index]
            gif_label.configure(image=frame)
            index = (index + 1) % len(frames)
            self.window.after(100, update_frame, index)  # Adjust delay for animation speed

        update_frame(0)
    def run(self):
        self.window.mainloop()


if __name__ == "__main__":
    Connect4().run()
