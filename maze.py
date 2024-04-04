import matplotlib.pyplot as plt
from collections import deque

class Node:
    def __init__(self, x, y, is_wall):
        self.x = x
        self.y = y
        self.is_wall = is_wall
        self.neighbors = []

    def add_neighbor(self, neighbor):
        self.neighbors.append(neighbor)

class Maze:
    def __init__(self, maze_layout, start_node, end_node, obstacles):
        self.maze_layout = maze_layout
        self.start_node = start_node
        self.end_node = end_node
        self.obstacles = obstacles
        self.nodes = []
        self.visited = set()  # Keep track of visited nodes
        self.create_maze()

    def create_maze(self):
        rows = len(self.maze_layout)
        cols = len(self.maze_layout[0])

        for i in range(rows):
            row = []
            for j in range(cols):
                node = Node(i, j, self.maze_layout[i][j])
                row.append(node)
            self.nodes.append(row)

        for i in range(rows):
            for j in range(cols):
                if not self.nodes[i][j].is_wall:
                    # Connect neighboring nodes (considering only right, left, up, and down movements)
                    for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                        new_x, new_y = i + dx, j + dy
                        if 0 <= new_x < rows and 0 <= new_y < cols and not self.nodes[new_x][new_y].is_wall:
                            self.nodes[i][j].add_neighbor(self.nodes[new_x][new_y])

    def visualize(self, current_path, ax):
        ax.clear()

        for i in range(len(self.maze_layout)):
            for j in range(len(self.maze_layout[0])):
                if (i, j) in self.obstacles:  # Obstacle
                    ax.fill([j, j+1, j+1, j], [len(self.maze_layout)-i, len(self.maze_layout)-i, len(self.maze_layout)-i-1, len(self.maze_layout)-i-1], 'red', edgecolor='black', linewidth=1)
                elif (i, j) == self.start_node:  # Start Node
                    ax.fill([j, j+1, j+1, j], [len(self.maze_layout)-i, len(self.maze_layout)-i, len(self.maze_layout)-i-1, len(self.maze_layout)-i-1], 'blue', edgecolor='black', linewidth=1)
                elif (i, j) == self.end_node:  # End Node
                    ax.fill([j, j+1, j+1, j], [len(self.maze_layout)-i, len(self.maze_layout)-i, len(self.maze_layout)-i-1, len(self.maze_layout)-i-1], 'blue', edgecolor='black', linewidth=1)
                elif (i, j) in current_path:  # Current Path
                    ax.fill([j, j+1, j+1, j], [len(self.maze_layout)-i, len(self.maze_layout)-i, len(self.maze_layout)-i-1, len(self.maze_layout)-i-1], 'green', edgecolor='black', linewidth=1)
                else:  # Non-visitable Node
                    ax.fill([j, j+1, j+1, j], [len(self.maze_layout)-i, len(self.maze_layout)-i, len(self.maze_layout)-i-1, len(self.maze_layout)-i-1], 'skyblue', edgecolor='black', linewidth=1)

        # Adding labels
        for i in range(len(self.maze_layout)):
            for j in range(len(self.maze_layout[0])):
                ax.text(j+0.5, len(self.maze_layout)-i-0.5, f'{i},{j}', ha='center', va='center', fontsize=8, fontweight='bold')

        ax.set_xlim(0, len(self.maze_layout[0]))
        ax.set_ylim(0, len(self.maze_layout))
        ax.set_xticks([])
        ax.set_yticks([])
        plt.draw()  # Update the plot without closing the window
        plt.pause(0.1)  # Pause to display the plot

class MazeSolver:
    def __init__(self, maze_layout, start_node, end_node, obstacles):
        self.maze = Maze(maze_layout, start_node, end_node, obstacles)
        self.current_path = []
        self.success = False
        self.fig, self.ax = plt.subplots()

    def is_valid_move(self, x, y):
        return 0 <= x < len(self.maze.maze_layout) and 0 <= y < len(self.maze.maze_layout[0]) and (x, y) not in self.maze.obstacles and (x, y) not in self.maze.visited

    def bfs(self):
        queue = deque([(self.maze.nodes[self.maze.start_node[0]][self.maze.start_node[1]], [])])

        while queue:
            current_node, current_path = queue.popleft()
            x, y = current_node.x, current_node.y

            if (x, y) == self.maze.end_node:
                self.current_path = current_path + [(x, y)]
                self.success = True
                break

            if current_node not in self.maze.visited:
                self.maze.visited.add(current_node)
                self.current_path = current_path + [(x, y)]

                for neighbor in current_node.neighbors:
                    new_x, new_y = neighbor.x, neighbor.y
                    if self.is_valid_move(new_x, new_y):
                        queue.append((neighbor, self.current_path))

            # Visualize the current step
            self.maze.visualize(self.current_path, self.ax)

        if self.success:
            print("Success! Shortest path:")
            print(self.current_path)
        else:
            print("Failed to reach the end node.")

        plt.ioff()
        plt.show()
        return self.success

# Example Usage
maze_layout = [
    [0, 1, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0],
    [0, 1, 0, 1, 0, 0],
    [0, 1, 0, 0, 1, 0],
    [0, 0, 0, 0, 1, 0]
]

start_node = (0, 0)
end_node = (4, 5)
obstacles = [(0, 1), (2, 1), (3, 1), (2, 3), (3, 4), (4, 4)]

solver = MazeSolver(maze_layout, start_node, end_node, obstacles)
solver.bfs()
