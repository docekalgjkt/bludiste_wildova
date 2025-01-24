import tkinter as tk

class RobotView:
    def __init__(self, root, robot, cell_size):
        self.root = root
        self.robot = robot
        self.cell_size = cell_size
        self.canvas = tk.Canvas(root, width=self.robot.maze.shape[1] * cell_size,
                                height=self.robot.maze.shape[0] * cell_size, bg="white")
        self.canvas.pack(side="left")
        self.robot_sprite = None

        # Inicializace robota na startovní pozici
        self.update_position()

    def update_position(self):
        """Aktualizuje pozici robota na plátno."""
        row, col = self.robot.position
        x1, y1 = col * self.cell_size + self.cell_size * 0.2, row * self.cell_size + self.cell_size * 0.2
        x2, y2 = x1 + self.cell_size * 0.6, y1 + self.cell_size * 0.6

        # Pokud robot již existuje, odstraní předchozí sprite
        if self.robot_sprite:
            self.canvas.delete(self.robot_sprite)

        # Vykreslení nového robota
        self.robot_sprite = self.canvas.create_oval(x1, y1, x2, y2, fill="blue", outline="black")

    def move(self, direction):
        """Pohyb robota na plátně podle zadaného směru."""
        self.robot.move(direction)
        self.update_position()

    def animate_move(self):
        """Animuje pohyb robota, pohybujícího se po své cestě."""
        for direction in self.robot.path:
            self.move(direction)
            self.root.after(200)  # 200 ms mezi kroky
