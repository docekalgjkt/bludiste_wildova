import numpy as np
from bludiste import MazeDAOCSV, MazeDAOText, MazeDAOXML
def create_maze_file(input_maze, file_format, filename):
    if file_format == 'csv':
        dao = MazeDAOCSV(filename)
    elif file_format == 'txt':
        dao = MazeDAOText(filename)
    elif file_format == 'xml':
        dao = MazeDAOXML(filename)
    else:
        raise ValueError("Unsupported file format")
    dao.save_maze(input_maze)


# Example usage:
if __name__ == "__main__":
    # create your new maze; 0 = empty, 1 = wall, 8 = start, 3 = finish
    input_maze = np.array([[0, 1, 0],
                           [0, 8, 0],
                           [0, 0, 3]])

    # choose on of the following commands to create a file in the desired format
    create_maze_file(input_maze, 'csv', 'levels.csv')
    # create_maze_file(input_maze, 'txt', 'levels.txt')
    # create_maze_file(input_maze, 'xml', 'levels.xml')