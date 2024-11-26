import tkinter as tk
from bludiste_view import BludisteView
from flood_fill_argorytmus import flood_fill  # Import funkce z flood_fill_argorytmus

maze = [
    [0, 0, 1, 0, 0],
    [0, 1, 1, 3, 1],
    [2, 0, 1, 0, 1],
    [0, 0, 0, 0, 1],
    [0, 1, 1, 1, 1]
]

root = tk.Tk()
root.title("Bludiště")

# Vytvoření zobrazení bludiště
bludiste_view = BludisteView(root, maze)

# Funkce pro spuštění Flood Fill algoritmu po 1 sekundě
root.after(1000, lambda: flood_fill(maze, bludiste_view.start_pos, bludiste_view.end_pos, bludiste_view))

root.mainloop()
