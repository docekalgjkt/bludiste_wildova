from abc import ABC, abstractmethod
import csv
import numpy as np
import xml.etree.ElementTree as ET
import tkinter as tk


class MazeDAO(ABC):
    # creation of main DAO class
    @abstractmethod
    def __init__(self, filename):
        self.filename = filename

    @abstractmethod
    def save_maze(self, input_maze):
        pass

    @abstractmethod
    def load_maze(self, level):
        return np.array([])


class MazeDAOCSV(MazeDAO):
    def __init__(self, filename):
        self.filename = filename

    def save_maze(self, input_maze):
        # loads csv file
        filepath = f"{self.filename}"
        maze_name = input("Enter maze name:\n> ")
        maze_level = input("Enter maze level:\n> ")

        with open(filepath, mode="a", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)

            # writes metadata: maze name and level
            writer.writerow([f"maze_name={maze_name}", f"level={maze_level}"])

            # writes maze cells row by row
            for row in input_maze:
                writer.writerow(row)

            # adds a blank row to separate mazes
            writer.writerow([])

    def load_maze(self, level):
        # loads csv file
        filepath = f"{self.filename}"
        try:
            with open(filepath, mode="r", encoding="utf-8") as file:
                reader = csv.reader(file)
                maze_found = False
                maze_data = []

                # reads through all rows:
                for row in reader:
                    # skips blank rows
                    if not row:
                        continue
                    # if it finds maze its goes to reading cells
                    if row[0].startswith("maze_name=") and row[1] == f"level={level}":
                        maze_found = True
                        continue
                    # if it encounters another maze after one was found, it breaks
                    elif row[0].startswith("maze_name="):
                        if maze_found:
                            break
                        continue

                    # reads cells
                    if maze_found:
                        maze_data.append([int(cell) for cell in row])

                if maze_data:
                    return np.array(maze_data)
                else:
                    raise ValueError(f"Maze with level {level} not found.")

        except FileNotFoundError:
            print("File not found.")


class MazeDAOText(MazeDAO):
    def __init__(self, filename):
        self.filename = filename

    def save_maze(self, input_maze):
        # loads txt file
        data = f"{self.filename}"

        maze_name = input("Enter maze name:\n> ")
        maze_level = input("Enter maze level:\n> ")

        # formats the maze as a string
        maze_string = f"Maze Name: {maze_name}\nMaze Level: {maze_level}\n"
        maze_string += "\n".join(" ".join(map(str, row)) for row in input_maze)

        # checks if the file exists and append or create it
        try:
            with open(data, "a") as file:
                file.write(maze_string + "\n\n")  # Append maze data with double blank lines
            print("Maze saved successfully.")
        except Exception as e:
            print(f"Error saving maze: {e}")

    def load_maze(self, level):
        # loads txt file
        data = f"{self.filename}"

        try:
            with open(data, "r") as file:
                content = file.read()

            # splits content into individual maze entries
            mazes = content.strip().split("\n\n")
            for maze_entry in mazes:
                lines = maze_entry.split("\n")
                maze_level = lines[1].split(":")[1].strip()  # extracts level number from first line
                if maze_level == str(level):
                    maze_data = lines[2:]  # extracts the maze rows
                    return np.array([[int(cell) for cell in row.split()] for row in maze_data])
        except FileNotFoundError:
            print("File not found.")
        except Exception as e:
            print(f"Error loading maze: {e}")
        return None


class MazeDAOXML(MazeDAO):
    def __init__(self, filename):
        self.filename = filename

    def save_maze(self, input_maze):
        # loads xml file
        data = f"{self.filename}"
        # checks if old file is present
        try:
            # reads the xml file
            tree = ET.parse(data)
            # accesses the levels element
            levels = tree.getroot()
        except FileNotFoundError:
            print("File not found, creating a new save file.")
            # creates the root (levels) element if file is not present
            levels = ET.Element('levels')
            tree = ET.ElementTree(levels)
        except Exception as e:
            print(f"Error when loading data: {e}")

        # user input for maze customization
        maze_name = str(input("Enter maze name:\n> "))
        maze_level = str(input("Enter maze level:\n> "))

        # creates maze element with an attribute
        maze = ET.SubElement(levels, 'maze', name=maze_name)

        # creates the level element
        ET.SubElement(maze, "level", number=maze_level)

        # iterates over rows and its cells
        for i, row in enumerate(input_maze):
            row_element = ET.SubElement(maze, 'row', id=str(i))
            for cell in row:
                ET.SubElement(row_element, 'cell', number=str(cell))

        # converts the tree to a byte string and writes it to a file
        tree.write(data, encoding="utf-8", xml_declaration=True)

        # for pretty-printing
        import xml.dom.minidom
        # converts xml tree (newly created maze) to string, goes through elements and adds indentations and line breaks
        maze_str = ET.tostring(maze, encoding="unicode")
        maze_dom = xml.dom.minidom.parseString(maze_str)
        # excludes the XML declaration when pretty-printing (otherwise it breaks the whole thing)
        pretty_maze_str = maze_dom.toprettyxml(indent="  ").split("\n", 1)[-1]

        # loads the file back as a string to insert the formatted maze
        with open(data, "r") as file:
            file_content = file.read()

        # finds the new maze's location (cuz its already saved) and replace it with the formatted version
        # this ensures old mazes stay formated only once
        file_content = file_content.replace(ET.tostring(maze, encoding="unicode"), pretty_maze_str)

        # writes the updated content back to the file
        with open(data, "w") as file:
            file.write(file_content)

    def load_maze(self, level):
        # loads xml file
        data = f"{self.filename}"
        try:
            # reads the xml file
            tree = ET.parse(data)
            root = tree.getroot()

            # find right maze, then row and reads number attribute of all elements named cell
            maze = [maze for maze in root.findall('maze') if maze.find('level').get('number') == str(level)]
            rows = []
            for row_element in maze[0].findall('row'):
                row = [int(cell.get('number')) for cell in row_element.findall('cell')]
                rows.append(row)

            # converts the indented list to an array
            return np.array(rows)
        except FileNotFoundError:
            print("File not found.")


class MazeApp:
    # draws the GUI
    def __init__(self, root):
        self.root = root
        self.root.title("Maze")

        # draws GUI
        self.frame = tk.Frame(root)
        self.frame.pack(side="right")

        self.button_start = tk.Button(self.frame, text="Start", width=10, height=4)
        self.button_start.pack()


class Maze:
    def __init__(self, level):
        # init of parameters, used for further referencing
        self.maze = mazeDAO.load_maze(level)
        self.size = None
        self.start = None
        self.finish = None
        self.get_info()

    def get_info(self):
        self.size = self.maze.shape
        self.start = (np.where(self.maze == 8)[0][0],np.where(self.maze == 8)[1][0])
        self.finish = (np.where(self.maze == 3)[0][0],np.where(self.maze == 3)[1][0])


class MazeView:
    # draws maze onto a canvas in root (MazeApp)
    def __init__(self, root):
        self.maze = maze
        self.root = root
        self.root.title("Maze")

        # creates canvas, sized according to maze size (complex calculus by og chat)
        max_canvas_size = 600  # maximum size for the canvas (square)
        rows, cols = self.maze.size
        self.cell_size = min(max_canvas_size // cols, max_canvas_size // rows)
        self.width = self.cell_size * cols
        self.height = self.cell_size * rows

        self.canvas = tk.Canvas(root, width=self.width, height=self.height, bg="white", relief="solid", border=5)
        self.canvas.pack(side="left")

        self.maze_creation()

    def maze_creation(self):
        # draws maze as a grid of black and white squares
        for row in range(len(self.maze.maze)):
            for col in range(len(self.maze.maze[row])):
                color = "black" if self.maze.maze[row][col] == 1 else "white"
                x1, y1 = col * self.cell_size + 7, row * self.cell_size + 7
                x2, y2 = x1 + self.cell_size, y1 + self.cell_size
                self.canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline="")

                # draws finish on canvas
                finish_x, finish_y = self.maze.finish
                x1, y1, x2, y2 = self.get_xy(finish_x, finish_y)
                self.canvas.create_rectangle(x1, y1, x2, y2, fill="green", outline="lightgreen")

    def get_xy(self, posx, posy):
        # helper function for x and y
        x1, y1 = posy * self.cell_size + self.cell_size * 0.2 + 7, posx * self.cell_size + self.cell_size * 0.2 + 7
        x2, y2 = x1 + self.cell_size * 0.6, y1 + self.cell_size * 0.6
        return x1, y1, x2, y2


root = tk.Tk()
window = MazeApp(root)

# choose one of the DAOs (delete the # in front of the desired DAO)
mazeDAO = MazeDAOCSV("levels.csv")
# mazeDAO = MazeDAOText("levels.txt")
# mazeDAO = MazeDAOXML("levels.xml")

# replace 1 with desired level (1)
maze = Maze(1)
maze_view = MazeView(root)


if __name__ == "__main__":
    root.mainloop()