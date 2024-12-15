from typing import List
import numpy as np
from tqdm import tqdm
from scipy.stats import entropy
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, PillowWriter


ROW_DIMENSION = 103
COLUMN_DIMENSION = 101


class Robot:
    def __init__(self, start_pos, velocity):
        self.current_position = start_pos
        self.velocity = velocity

    def get_current_position(self):
        return self.current_position

    def get_velocity(self):
        return self.velocity

    def propose_move(self):
        next_pos_row = self.current_position[0] + self.velocity[0]
        next_pos_col = self.current_position[1] + self.velocity[1]
        return (next_pos_row, next_pos_col)

    def move(self, row, col):
        self.current_position = (row, col)


class Board:
    def __init__(
        self, robots, row_dimension=ROW_DIMENSION, col_dimension=COLUMN_DIMENSION
    ):
        self.robots: Robot = robots
        self.positions = {}
        self.row_dimension = row_dimension
        self.col_dimension = col_dimension
        self.compute_initial_board_positions()
        self.col_bound = int(self.col_dimension / 2)
        self.row_bound = int(self.row_dimension / 2)
        self.compute_quadrant_dividers()
        self.quadrants = {1: [], 2: [], 3: [], 4: []}

    def _load_new_position(self, pos, robot):
        if pos not in self.positions:
            self.positions[pos] = [robot]
        else:
            self.positions[pos].append(robot)

    def compute_initial_board_positions(self):
        self.positions = {}
        for robot in self.robots:
            pos = robot.get_current_position()
            self._load_new_position(pos, robot)

    def advance_positions(self):
        self.positions = {}
        for robot in self.robots:
            next_possible_row, next_possible_col = robot.propose_move()
            if 0 > next_possible_row:
                next_row = self.row_dimension - (-next_possible_row)
            elif next_possible_row >= self.row_dimension:
                next_row = next_possible_row - self.row_dimension
            else:
                next_row = next_possible_row

            if 0 > next_possible_col:
                next_col = self.col_dimension - (-next_possible_col)
            elif next_possible_col >= self.col_dimension:
                next_col = next_possible_col - self.col_dimension
            else:
                next_col = next_possible_col

            robot.move(next_row, next_col)
            self._load_new_position((next_row, next_col), robot)

    def compute_quadrant_dividers(self):
        self.col_bound = int(self.col_dimension / 2)
        self.row_bound = int(self.row_dimension / 2)

    def _compute_quandrant(self, robots, pos):
        row, col = pos

        if col < self.col_bound and row < self.row_bound:
            self.quadrants[1].extend(robots)
        elif col > self.col_bound and row < self.row_bound:
            self.quadrants[2].extend(robots)
        elif col < self.col_bound and row > self.row_bound:
            self.quadrants[3].extend(robots)
        elif col > self.col_bound and row > self.row_bound:
            self.quadrants[4].extend(robots)

    #

    def compute_quadrants(self):
        self.quadrants = {1: [], 2: [], 3: [], 4: []}
        for pos, robots in self.positions.items():
            self._compute_quandrant(robots, pos)

    def print_board(self):
        board = self.construct_board()
        for row in board:
            print("".join(row))

    def construct_board(self):
        board = []
        num_bots = 0
        other = 0
        for pos, bots in self.positions.items():
            num_bots += len(bots)
        for i in range(self.row_dimension):
            col = []
            for j in range(self.col_dimension):
                if (i, j) in self.positions:
                    other += len(self.positions[(i, j)])
                    col.append(str(len(self.positions[(i, j)])))
                else:
                    col.append(".")
            board.append(col)

        return board

    def multiply_quadrants(self):
        self.compute_quadrants()
        result = 1
        for _, robots in self.quadrants.items():
            result *= len(robots)
        return result


def parse_input() -> List[Robot]:
    robots = []
    with open("input.txt") as file:
        for line in file:
            robot_data = line.rstrip().split(" ")
            robot_starting_pos, robot_velocity = robot_data
            robot_start_col = int(robot_starting_pos.split("=")[1].split(",")[0])
            robot_start_row = int(robot_starting_pos.split("=")[1].split(",")[1])
            robot_velocity_col = int(robot_velocity.split("=")[1].split(",")[0])
            robot_velocity_row = int(robot_velocity.split("=")[1].split(",")[1])
            robot = Robot(
                start_pos=(robot_start_row, robot_start_col),
                velocity=(robot_velocity_row, robot_velocity_col),
            )
            robots.append(robot)
    return robots


def part_1(robots: List[Robot], row_dimension: int, col_dimension: int) -> int:
    board = Board(
        robots=robots, row_dimension=row_dimension, col_dimension=col_dimension
    )
    for _ in tqdm(range(100)):
        board.advance_positions()

    return board.multiply_quadrants()


def measure_entropy_simple(board: List[List[int | str]]) -> bool:
    """
    Measure entropy of the board by looking for contiguous columns of robots.

    """
    curr_longest = 0
    prev_idx = 0
    curr_idx = 0
    for row in board:
        for idx, col in enumerate(row):
            if col.isdigit():
                prev_idx = curr_idx
                curr_idx = idx

            if col.isdigit() and (curr_idx - prev_idx) == 1:
                curr_longest += 1

            if curr_longest > 20:
                return True
        curr_idx = 0
        curr_longest = 0
    return False


def part_2_simple_heuristic(robots, row_dimension, col_dimension):
    board = Board(
        robots=robots, row_dimension=row_dimension, col_dimension=col_dimension
    )
    for i in tqdm(range(10000)):
        board.advance_positions()
        curr_board = board.construct_board()
        if measure_entropy_simple(curr_board):
            print(f"Iteration: {i+1}")
            board.print_board()


def compute_entropy(board: List[List[int | str]]) -> float:
    int_board = []
    for i in board:
        col = []
        for j in i:
            if j.isdigit():
                col.append(j)
            else:
                col.append(0)
        int_board.append(col)

    matrix = np.array(int_board)

    # Flatten the 2D array
    flat_array = matrix.flatten()

    # Calculate the probabilities of each unique value
    _, counts = np.unique(flat_array, return_counts=True)
    probabilities = counts / len(flat_array)

    # Calculate entropy
    return entropy(probabilities, base=2)  # Base 2 for entropy in bits


def part_2_minimize_entropy(
    robots: List[Robot], row_dimension: int, col_dimension: int, iterations: int
) -> int:
    board = Board(
        robots=robots, row_dimension=row_dimension, col_dimension=col_dimension
    )
    entropies = []
    for _ in tqdm(range(iterations)):
        board.advance_positions()
        curr_board = board.construct_board()
        entropy = compute_entropy(curr_board)
        entropies.append(entropy)

    min_entropy = min(entropies)
    return entropies.index(min_entropy) + 1


def part_2_animate(
    robots: List[Robot], row_dimension: int, col_dimension: int, iterations: int
):
    """
    Utility function to animate the robot movements
    """
    board = Board(
        robots=robots, row_dimension=row_dimension, col_dimension=col_dimension
    )
    current_board = board.construct_board()

    # Convert the array to a numerical format for visualization
    numerical_array = np.array(
        [[int(x) if x != "." else 0 for x in row] for row in current_board]
    )

    fig, ax = plt.subplots(figsize=(8, 7))
    im = ax.imshow(numerical_array, cmap="viridis", interpolation="nearest")
    title = ax.set_title("Iteration: 0")  # Initial title

    def update(frame):
        board.advance_positions()
        current_board = board.construct_board()
        numerical_array = np.array(
            [[int(x) if x != "." else 0 for x in row] for row in current_board]
        )
        im.set_array(numerical_array)
        title.set_text(f"Iteration: {frame}")
        return [im, title]

    ani = FuncAnimation(fig, update, frames=iterations, interval=0.1)
    ani.save("robot_movement.gif", writer=PillowWriter(fps=10))  # Set fps as needed
    plt.show()


def get_board_with_tree(
    robots: List[Robot], row_dimension: int, col_dimension: int, iteration: int
):
    board = Board(
        robots=robots, row_dimension=row_dimension, col_dimension=col_dimension
    )
    for _ in range(iteration + 1):
        # plt.figure(figsize=(10, 10))
        if _ == iteration:
            return board
        board.advance_positions()


def visualize_tree(array: List[List[int | str]], iteration: int):
    # Convert the array to a numerical format for visualization
    numerical_array = np.array(
        [[int(x) if x != "." else 0 for x in row] for row in array]
    )

    plt.clf()  # Clear the current figure
    plt.imshow(numerical_array, cmap="viridis", interpolation="nearest")
    plt.title(f"Iteration: {iteration}")

    plt.savefig("tree.png")


if __name__ == "__main__":
    robots = parse_input()
    result_part1 = part_1(
        robots=robots, row_dimension=ROW_DIMENSION, col_dimension=COLUMN_DIMENSION
    )
    print(f"Solution part 1: {result_part1}")

    # Simple heuristic to print out boards that have small "entropy"
    # robots = parse_input()
    # part_2_simple_heuristic(robots=robots, row_dimension=ROW_DIMENSION, col_dimension=COLUMN_DIMENSION)

    # Animate part 2 movements
    # robots = parse_input()
    # result_part2 = part_2_animate(
    #     robots=robots,
    #     row_dimension=ROW_DIMENSION,
    #     col_dimension=COLUMN_DIMENSION,
    #     iterations=10000,
    # )

    # Solution that actually minimizes entropy
    robots = parse_input()
    result_part2 = part_2_minimize_entropy(
        robots=robots,
        row_dimension=ROW_DIMENSION,
        col_dimension=COLUMN_DIMENSION,
        iterations=10000,
    )
    print(f"Solution part 2: {result_part2}")

    robots = parse_input()
    board_with_tree = get_board_with_tree(
        robots=robots,
        row_dimension=ROW_DIMENSION,
        col_dimension=COLUMN_DIMENSION,
        iteration=result_part2,
    )

    # Visualize
    visualize_tree(board_with_tree.construct_board(), result_part2)
    board_with_tree.print_board()
