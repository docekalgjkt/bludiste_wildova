import tkinter as tk
import time

class BludisteView:
    def __init__(self, root, maze):
        self.root = root
        self.maze = maze
        self.canvas_width = 500
        self.canvas_height = 500
        self.cell_size = self.calculate_cell_size()
        self.canvas = tk.Canvas(root, width=self.canvas_width, height=self.canvas_height, bg="white")
        self.canvas.pack()
        self.start_pos = self.find_position(2)  # Najde startovní pozici (2)
        self.end_pos = self.find_position(3)  # Najde cílovou pozici (3)
        self.character = None
        self.draw_maze()
        self.place_character()

        # Tlačítko pro spuštění pohybu
        self.start_button = tk.Button(root, text="Start", command=self.flood_fill)
        self.start_button.pack()

    def calculate_cell_size(self):
        rows = len(self.maze)
        cols = len(self.maze[0])
        return min(self.canvas_width // cols, self.canvas_height // rows)

    def draw_maze(self):
        for row_index, row in enumerate(self.maze):
            for col_index, cell in enumerate(row):
                x1 = col_index * self.cell_size
                y1 = row_index * self.cell_size
                x2 = x1 + self.cell_size
                y2 = y1 + self.cell_size

                if cell == 1:
                    color = "black"
                elif cell == 2:
                    color = "green"
                elif cell == 3:
                    color = "red"
                else:
                    color = "white"

                self.canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline="gray")

    def find_position(self, value):
        for row_index, row in enumerate(self.maze):
            for col_index, cell in enumerate(row):
                if cell == value:
                    return row_index, col_index
        return None

    def place_character(self):
        """Umístí postavičku na startovní pozici."""
        if self.start_pos:
            row, col = self.start_pos
            x1 = col * self.cell_size + self.cell_size // 4
            y1 = row * self.cell_size + self.cell_size // 4
            x2 = x1 + self.cell_size // 2
            y2 = y1 + self.cell_size // 2
            self.character = self.canvas.create_oval(x1, y1, x2, y2, fill="green")

    def move_character(self, new_row, new_col):
        """Pohybuje postavičkou na nové políčko."""
        if self.character:
            x1 = new_col * self.cell_size + self.cell_size // 4
            y1 = new_row * self.cell_size + self.cell_size // 4
            x2 = x1 + self.cell_size // 2
            y2 = y1 + self.cell_size // 2
            self.canvas.coords(self.character, x1, y1, x2, y2)
            time.sleep(0.5)  # Zpomaleno na 0.5 sekundy mezi kroky
            self.root.update()

    def flood_fill(self):
        """Implementace flood fill algoritmu pro pohyb robota do cíle."""
        current_pos = self.start_pos
        stack = [current_pos]

        while stack:
            current_pos = stack.pop()

            # Získáme aktuální pozici
            row, col = current_pos

            # Pohybujeme postavičkou na aktuální pozici
            self.move_character(row, col)

            # Pokud je dosaženo cíle, zastavíme
            if current_pos == self.end_pos:
                print("Cíl dosažen!")
                break

            # Zkoumáme sousední políčka (4 směry)
            neighbors = [(row + 1, col), (row - 1, col), (row, col + 1), (row, col - 1)]
            for n_row, n_col in neighbors:
                if 0 <= n_row < len(self.maze) and 0 <= n_col < len(self.maze[0]):
                    if self.maze[n_row][n_col] == 0:  # Pokud je políčko volné
                        stack.append((n_row, n_col))  # Přidáme sousední pozici do zásobníku
