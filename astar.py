import time, math, random, sys

class Node():
    """A node class for A* Pathfinding"""

    def __init__(self, parent=None, position=None):
        self.parent = parent
        self.position = position

        self.g = 0
        self.h = 0
        self.f = 0

    def __eq__(self, other):
        return self.position == other.position


def astar(maze, start, end, heur):
    """Returns a list of tuples as a path from the given start to the given end in the given maze"""

    if maze[start[0]][start[1]] == 0 or maze[end[0]][end[1]] == 0: #Needed to add these lines of code because of infinite for loop caused by maze 2's goal node containing a 0
        print("\nStart or end position is a 0.")
        return None, -1, 0
    
    # Create start and end node
    start_node = Node(None, start)
    start_node.g = start_node.h = start_node.f = 0
    end_node = Node(None, end)
    end_node.g = end_node.h = end_node.f = 0

    # Initialize both open and closed list
    open_list = []
    closed_list = []

    # Add the start node
    open_list.append(start_node)

    # Loop until you find the end
    while len(open_list) > 0:

        # Get the current node
        current_node = open_list[0]
        current_index = 0
        for index, item in enumerate(open_list):
            if item.f < current_node.f:
                current_node = item
                current_index = index

        # Pop current off open list, add to closed list
        open_list.pop(current_index)
        closed_list.append(current_node)

        # Found the goal
        if current_node == end_node:
            path = []
            current = current_node
            while current is not None:
                path.append(current.position)
                current = current.parent
            return path[::-1], current_node.g , (len(open_list) + len(closed_list)) # Return reversed path, the cost of the path found, and the number of nodes created (len of lists)

        # Generate children
        children = []
        # for new_position in [(0, -1), (0, 1), (-1, 0), (1, 0), (-1, -1), (-1, 1), (1, -1), (1, 1)]: # Adjacent squares
        for new_position in [(0, -1), (0, 1), (-1, 0), (1, 0)]: # New Adjacent squares
            #Task 1 requires to restrict the moves, so this line needs to be changed 

            # Get node position
            node_position = (current_node.position[0] + new_position[0], current_node.position[1] + new_position[1])

            # Make sure within range
            if node_position[0] > (len(maze) - 1) or node_position[0] < 0 or node_position[1] > (len(maze[len(maze)-1]) -1) or node_position[1] < 0:
                continue

            # Make sure walkable terrain
            if maze[node_position[0]][node_position[1]] not in [1,2,3,4,5]: #Task 1 says that the path may use any node that is not out of bounds or 0
                continue

            # Create new node
            new_node = Node(current_node, node_position)

            # Append
            children.append(new_node)

        # Loop through children
        for child in children:

            # Child is on the closed list
            for closed_child in closed_list:
                if child == closed_child:
                    continue

            # Create the f, g, and h values TODO: THIS IS WHERE WE WILL ADD THE DIFFERENT HEURISTICS FOR TASK 2

            child.g = current_node.g + maze[child.position[0]][child.position[1]] #Task 1 asks to allow for multiple costs to be taken into consideration, so we update child.g to be the cost to get to the previous node plus the cost to reach child's position
            child.h = abs(child.position[0] - end_node.position[0]) + abs(child.position[1] - end_node.position[1]) #Task 1 asks to use Manhattan distance, so I changed this heuristic to be manhattan rather than the original use of pythagorean theorum
            child.f = child.g + child.h

            # Child is already in the open list
            for open_node in open_list:
                if child == open_node and child.g > open_node.g:
                    continue

            # Add the child to the open list
            open_list.append(child)
    return None, -1, (len(open_list) + len(closed_list)) # Added this return statement while debugging


def main():
    # Define your mazes and their start/end coordinates in a dictionary:
    mazes = {
        1: {
            "maze": [
                [2, 4, 2, 1, 4, 5, 2],
                [0, 1, 2, 3, 5, 3, 1],
                [2, 0, 4, 4, 1, 2, 4],
                [2, 5, 5, 3, 2, 0, 1],
                [4, 3, 3, 2, 1, 0, 1]
            ],
            "start": (1, 2),
            "end": (4, 3)
        },
        2: {
            "maze": [
                [1, 3, 2, 5, 1, 4, 3],
                [2, 1, 3, 1, 3, 2, 5],
                [3, 0, 5, 0, 1, 2, 2],
                [5, 3, 2, 1, 5, 0, 3],
                [2, 4, 1, 0, 0, 2, 0],
                [4, 0, 2, 1, 5, 3, 4],
                [1, 5, 1, 0, 2, 4, 1]
            ],
            "start": (3, 6),
            "end": (5, 1)
        },
        3: {
            "maze": [
                [2, 0, 2, 0, 2, 0, 0, 2, 2, 0],
                [1, 2, 3, 5, 2, 1, 2, 5, 1, 2],
                [2, 0, 2, 2, 1, 2, 1, 2, 4, 2],
                [2, 0, 1, 0, 1, 1, 1, 0, 0, 1],
                [1, 1, 0, 0, 5, 0, 3, 2, 2, 2],
                [2, 2, 2, 2, 1, 0, 1, 2, 1, 0],
                [1, 0, 2, 1, 3, 1, 4, 3, 0, 1],
                [2, 0, 5, 1, 5, 2, 1, 2, 4, 1],
                [1, 2, 2, 2, 0, 2, 0, 1, 1, 0],
                [5, 1, 2, 1, 1, 1, 2, 0, 1, 2]
            ],
            "start": (1, 2),
            "end": (8, 8)
        },
        4: {
            "maze": [
                [3, 4, 2, 1, 4, 5, 3, 2, 3, 0],
                [5, 0, 3, 1, 1, 1, 3, 0, 2, 1],
                [1, 2, 4, 3, 0, 1, 2, 4, 2, 2],
                [5, 2, 3, 0, 1, 0, 3, 2, 4, 1],
                [2, 5, 3, 1, 0, 3, 2, 4, 0, 2],
                [3, 5, 0, 0, 0, 2, 1, 3, 3, 4],
                [4, 0, 2, 1, 3, 4, 5, 1, 0, 1],
                [1, 1, 3, 4, 5, 0, 5, 3, 1, 3],
                [4, 0, 2, 3, 4, 5, 1, 5, 1, 2],
                [5, 5, 4, 3, 5, 2, 1, 3, 1, 0]
            ],
            "start": (3, 4),
            "end": (0, 0)
        },
        5: {
            "maze": [
                [2, 0, 3, 5, 1, 2, 4, 2, 1, 3],
                [3, 4, 2, 1, 4, 5, 3, 2, 0, 2],
                [5, 0, 3, 1, 1, 1, 3, 0, 1, 1],
                [1, 2, 4, 3, 0, 1, 2, 4, 0, 4],
                [5, 2, 3, 0, 1, 0, 3, 2, 5, 2],
                [2, 5, 3, 1, 5, 3, 2, 4, 1, 4],
                [3, 5, 0, 0, 0, 2, 1, 3, 5, 2],
                [4, 0, 2, 1, 3, 4, 5, 1, 4, 3],
                [1, 1, 3, 4, 5, 0, 5, 3, 2, 4],
                [0, 4, 2, 5, 1, 3, 4, 5, 3, 4]
            ],
            "start": (5, 1),
            "end": (4, 4)
        }
    }
    # ----------------------------------------------------------------------------------------- # Added a little menu for the user interaction
    maze_num = int(input("Hello, please enter the desired maze number(1-5): "))

    while(int(maze_num) not in [1,2,3,4,5]):
        maze_num = int(input("Please enter the desired maze number: "))
    

    print("These are the available heuristics to choose from:\n\n1: All zeros; for every node this just returns the value 0.\n2: The Manhattan distance\n3: A modified Manhattan distance\nH4: Manhattan distance with error\n")
    heuristic_num = 0
    while(int(heuristic_num) not in [1,2,3,4]):
        heuristic_num = int(input("Please enter the desired heuristic number(1-4): \n"))

    selected = mazes[maze_num]
    selected_maze = selected["maze"]
    start = selected["start"]
    end = selected["end"]
    
    start_time = time.time()
    path, cost_of_path, num_nodes = astar(selected_maze, start, end, heuristic_num)
    end_time = time.time()

    print("\n# ----------------------------------------------------------------------------------------- #")
    print("\nThe path taken was: ", path, "\n")
    print("The cost of the path was: ", cost_of_path, "\n")
    print("The number of nodes created were: ", num_nodes, "\n")
    print("The elapsed time was ", (end_time-start_time)*1000 ," milliseconds")


if __name__ == '__main__':
    main() 