def flood_fill(maze, start_pos, end_pos, view):
    """Flood Fill algoritmus s pohybem postavičky."""
    visited = set()
    stack = [start_pos]

    while stack:
        current_pos = stack.pop()
        if current_pos in visited:
            continue

        visited.add(current_pos)
        row, col = current_pos

        # Pohyb postavičky
        view.move_character(row, col)

        # Pokud jsme na cíli
        if current_pos == end_pos:
            print("Cíl dosažen!")
            return

        # Přidáme sousedy (nahoru, dolů, vlevo, vpravo)
        neighbors = [
            (row - 1, col),  # Nahoru
            (row + 1, col),  # Dolů
            (row, col - 1),  # Vlevo
            (row, col + 1),  # Vpravo
        ]
        for n_row, n_col in neighbors:
            if 0 <= n_row < len(maze) and 0 <= n_col < len(maze[0]):  # Ověříme hranice
                if maze[n_row][n_col] in (0, 3) and (n_row, n_col) not in visited:
                    stack.append((n_row, n_col))

    print("Cíl nelze dosáhnout.")
