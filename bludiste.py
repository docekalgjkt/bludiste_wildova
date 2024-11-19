class Bludiste:
    def __init__(self):
        self.maze_grid = []
        self.start_position = (0, 0)
        self.exit_position = None

    def load_from_file(self, filename):
        """Načítá bludiště z textového souboru."""
        with open(filename, 'r') as file:
            for line in file:
                row = list(line.strip())
                self.maze_grid.append(row)
                if 'S' in row:  # Startovací pozice označená 'S'
                    self.start_position = (len(self.maze_grid) - 1, row.index('S'))
                if 'E' in row:  # Východ označený 'E'
                    self.exit_position = (len(self.maze_grid) - 1, row.index('E'))

    def can_move_to(self, x, y):
        """Kontroluje, zda je pozice (x, y) v mezích a není zdí."""
        return 0 <= x < len(self.maze_grid) and 0 <= y < len(self.maze_grid[0]) and self.maze_grid[x][y] != '#'

    def find_exit(self):
        """Algoritmus pro navigaci bludištěm."""
        # Zde lze implementovat algoritmus jako DFS nebo BFS pro hledání východu.
        pass
