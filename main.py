from bludiste import Bludiste

# Definice bludiště
maze = [
    [1, 1, 1, 1, 1],
    [1, 2, 0, 3, 1],
    [1, 0, 1, 0, 1],
    [1, 0, 0, 0, 1],
    [1, 1, 1, 1, 1]
]

# Inicializace a spuštění algoritmu
bludiste = Bludiste(maze)
bludiste.solve_maze()

# Výstup bludiště
for row in bludiste.maze:
    print(row)
