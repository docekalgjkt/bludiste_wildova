import tkinter as tk

class BludisteView:
    def __init__(self, master, bludiste):
        self.master = master
        self.bludiste = bludiste
        self.canvas = tk.Canvas(master, width=400, height=400)
        self.canvas.pack()
        self.robot_position = bludiste.start_position

        # Inicializace vykreslení bludiště
        self.draw_maze()

        # Tlačítko pro hledání východu
        find_exit_button = tk.Button(master, text="Najít východ", command=self.on_find_exit)
        find_exit_button.pack()

    def draw_maze(self):
        """Vykresluje bludiště na canvas."""
        cell_size = 20
        for i, row in enumerate(self.bludiste.maze_grid):
            for j, cell in enumerate(row):
                x0, y0 = j * cell_size, i * cell_size
                x1, y1 = x0 + cell_size, y0 + cell_size
                if cell == '#':  # Zeď
                    self.canvas.create_rectangle(x0, y0, x1, y1, fill="black")
                elif cell == 'S':  # Start
                    self.canvas.create_oval(x0, y0, x1, y1, fill="blue")
                elif cell == 'E':  # Východ
                    self.canvas.create_oval(x0, y0, x1, y1, fill="green")
                else:  # Cesta
                    self.canvas.create_rectangle(x0, y0, x1, y1, fill="white")

    def update_robot_position(self, x, y):
        """Aktualizuje pozici robota na canvasu."""
        self.canvas.create_oval(
            y * 20, x * 20, (y + 1) * 20, (x + 1) * 20,
            fill="red", outline=""
        )

    def on_find_exit(self):
        """Zahájí proces nalezení východu."""
        # Placeholder: simulace pohybu robota
        x, y = self.robot_position
        self.update_robot_position(x, y)
