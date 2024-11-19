class Bludiste:
    def __init__(self, maze):
        self.maze = maze
        self.start = self.find_position(2)
        self.exit = self.find_position(3)
        self.path_found = False

    def find_position(self, value):
        """Najde pozici startu nebo východu."""
        for x, row in enumerate(self.maze):
            for y, cell in enumerate(row):
                if cell == value:
                    return (x, y)
        return None

    def can_move_to(self, x, y):
        """Kontroluje, zda je možné se pohybovat na danou pozici."""
        return 0 <= x < len(self.maze) and 0 <= y < len(self.maze[0]) and (self.maze[x][y] == 0 or self.maze[x][y] == 3)

    def flood_fill(self, x, y):
        """Rekurzivní algoritmus pro hledání východu."""
        if not self.can_move_to(x, y) or self.path_found:
            return
        if (x, y) == self.exit:
            self.path_found = True
            print(f"Východ nalezen na pozici: {x, y}")
            return

        # Označíme pozici jako prošlou
        self.maze[x][y] = 4  # Číslo 4 značí prošlou pozici
        print(f"Pohyb na {x, y}")

        # Rekurze pro pohyb do 4 směrů
        self.flood_fill(x + 1, y)  # dolů
        self.flood_fill(x - 1, y)  # nahoru
        self.flood_fill(x, y + 1)  # doprava
        self.flood_fill(x, y - 1)  # doleva

    def solve_maze(self):
        """Spouští řešení bludiště od startovní pozice."""
        x, y = self.start
        self.flood_fill(x, y)
