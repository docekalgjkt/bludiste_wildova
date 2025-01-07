class Robot:
    def __init__(self, maze, start, finish):
        self.maze = maze
        self.position = start  # pozice robota ve formátu (řádek, sloupec)
        self.finish = finish  # pozice cíle ve formátu (řádek, sloupec)
        self.path = []  # seznam pro ukládání cesty robota

    def move(self, direction):
        """Pohyb robota v maze podle zadaného směru (nahoru, dolů, vlevo, vpravo)."""
        row, col = self.position
        if direction == "up" and row > 0 and self.maze[row - 1][col] != 1:
            self.position = (row - 1, col)
        elif direction == "down" and row < len(self.maze) - 1 and self.maze[row + 1][col] != 1:
            self.position = (row + 1, col)
        elif direction == "left" and col > 0 and self.maze[row][col - 1] != 1:
            self.position = (row, col - 1)
        elif direction == "right" and col < len(self.maze[0]) - 1 and self.maze[row][col + 1] != 1:
            self.position = (row, col + 1)

        # Uložíme aktuální pozici na cestu
        self.path.append(self.position)

    def flood_fill(self):
        """Flood Fill algoritmus pro nalezení cesty v bludišti."""
        # Inicializace fronty a navštívených buněk
        from collections import deque
        queue = deque([(self.position, [])])
        visited = set()
        visited.add(self.position)

        # Procházení bludiště
        while queue:
            current_pos, path = queue.popleft()

            # Pokud je dosaženo cíle, vrátíme cestu
            if current_pos == self.finish:
                return path

            # Prozkoumáme všechny možné směry
            for direction, move in [("up", (-1, 0)), ("down", (1, 0)), ("left", (0, -1)), ("right", (0, 1))]:
                new_pos = (current_pos[0] + move[0], current_pos[1] + move[1])

                # Zkontrolujeme, zda je nová pozice platná a není již navštívená
                if (0 <= new_pos[0] < len(self.maze) and 0 <= new_pos[1] < len(self.maze[0])
                        and self.maze[new_pos[0]][new_pos[1]] != 1 and new_pos not in visited):
                    visited.add(new_pos)
                    queue.append((new_pos, path + [direction]))

        # Pokud není cesta nalezena
        return None
