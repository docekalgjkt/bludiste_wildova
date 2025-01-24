import tkinter as tk
from collections import deque
import numpy as np


class Robot:
    def __init__(self, maze):
        self.maze = maze
        self.position = self.find_start()  # Automaticky najde start
        self.finish = self.find_finish()  # Automaticky najde cíl
        self.path = []  # seznam pro ukládání cesty robota

    def find_start(self):
        """Najde startovní pozici (označeno jako '8')."""
        result = np.where(self.maze == 8)
        if result[0].size > 0:
            return (result[0][0], result[1][0])  # Vrací první výskyt
        return None

    def find_finish(self):
        """Najde cílovou pozici (označeno jako '3')."""
        for r in range(len(self.maze)):
            for c in range(len(self.maze[0])):
                if self.maze[r][c] == 3:
                    return (r, c)
        return None

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

    def follow_path(self, path):
        """Simuluje pohyb robota po nalezené cestě."""
        for direction in path:
            self.move(direction)

    def find_and_move_to_finish(self):
        """Najde cestu a následně se přesune k cíli."""
        path = self.flood_fill()
        if path:
            self.follow_path(path)
            return self.path
        else:
            return None


def draw_maze(canvas, maze, robot_pos, square_size=50):
    """Vykreslí bludiště na canvasu."""
    for row in range(len(maze)):
        for col in range(len(maze[0])):
            color = "white" if maze[row][col] == 0 else "black"
            if maze[row][col] == 8:
                color = "green"  # Start je zelený
            elif maze[row][col] == 3:
                color = "red"  # Cíl je červený
            canvas.create_rectangle(col * square_size, row * square_size,
                                    (col + 1) * square_size, (row + 1) * square_size,
                                    fill=color)

    # Vykreslí robota
    robot_row, robot_col = robot_pos
    canvas.create_oval(robot_col * square_size + 5, robot_row * square_size + 5,
                       (robot_col + 1) * square_size - 5, (robot_row + 1) * square_size - 5,
                       fill="blue")


def animate_robot(canvas, robot, square_size=50):
    """Animuje pohyb robota po cestě."""
    path = robot.find_and_move_to_finish()
    if path:
        for position in path:
            robot.position = position
            canvas.delete("all")  # Vymaže vše před novým vykreslením
            draw_maze(canvas, robot.maze, robot.position)  # Vykreslí bludiště a robota
            canvas.after(500)  # Pauza mezi kroky
            canvas.update()


def start_robot(maze, canvas):
    # Maze s novými hodnotami

    robot = Robot(maze)

    # Vykreslí počáteční stav
    draw_maze(canvas, maze, robot.position)

    # Spustí animaci robota
    animate_robot(canvas, robot)
