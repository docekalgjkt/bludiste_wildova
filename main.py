import tkinter as tk
from bludiste import Bludiste
from bludiste_view import BludisteView

def main() -> object:
    root = tk.Tk()
    root.title("Bludiště")

    # Inicializace bludiště
    maze = Bludiste()
    maze.load_from_file("maze.txt")  # Ujistěte se, že máte soubor maze.txt

    # Inicializace zobrazení
    app = BludisteView(root, maze)

    root.mainloop()

if __name__ == "__main__":
    main()
