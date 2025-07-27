from queue import PriorityQueue
from typing import Dict, List, Set


def get_data():
    with open("data.txt") as f:
        data = [list(line.strip()) for line in f]
    return data


class Node:
    def __init__(self, point) -> None:
        self.point = point
        self.edges: List[Node] = []

    def __str__(self) -> str:
        return str(self.point)

    def __repr__(self) -> str:
        return str(self.point)

    def __eq__(self, value: object, /) -> bool:
        assert isinstance(value, Node)
        return self.point == value.point

    def __lt__(self, obj):
        return True

    def __hash__(self):
        return self.point.__hash__()


class Grid:
    def __init__(self, data) -> None:
        self.data = data
        self.start_point = (0, 0)
        self.end_point = (0, 0)
        self.cordinates = [
            (i, j) for i in range(len(self.data)) for j in range(len(self.data[0]))
        ]
        self.walls = set()
        self.nodes: Dict[tuple, Node] = {}
        self.initalize_grid()
        self.add_edges()

    def get_cord_value(self, point):
        row, col = point
        return self.data[row][col]

    def add_edges(self):
        for _, node in self.nodes.items():
            x, y = node.point
            # up
            new_node = Node((x - 1, y))
            if new_node.point in self.nodes:
                node.edges.append(new_node)
            # down
            new_node = Node((x + 1, y))
            if new_node.point in self.nodes:
                node.edges.append(new_node)
            # left
            new_node = Node((x, y - 1))
            if new_node.point in self.nodes:
                node.edges.append(new_node)
            # right
            new_node = Node((x, y + 1))
            if new_node.point in self.nodes:
                node.edges.append(new_node)

    def initalize_grid(self):
        start_point_found = False
        end_point_found = False
        for cord in self.cordinates:
            cord_value = self.get_cord_value(cord)
            if cord_value == "S":
                self.start_point = cord
                self.nodes[cord] = Node(cord)
                start_point_found = True
            if cord_value == "E":
                self.end_point = cord
                self.nodes[cord] = Node(cord)
                end_point_found = True
            if cord_value == "#":
                self.walls.add(cord)
            if cord_value == ".":
                self.nodes[cord] = Node(cord)

        if not (start_point_found and end_point_found):
            raise RuntimeError("Could not find start or end position")

    def __str__(self) -> str:

        to_ret = ["".join(d) for d in data]
        to_ret = "\n".join(to_ret)
        return to_ret


class GridWalk:
    def __init__(self, grid: Grid, direction) -> None:
        self.grid = grid
        self.visited_nodes = set()
        self.current_position: Node = self.grid.nodes[self.grid.start_point]
        self.next_steps = PriorityQueue()
        self.direction = direction
        self.total = 0
        self.add_next_steps()

    def take_step(self):
        self.visited_nodes.add(self.current_position)
        if (
            self.next_steps.empty()
            or self.current_position.point == self.grid.end_point
        ):
            return False
        next_step = self.next_steps.get()
        total, node, direction = next_step
        self.current_position = node
        self.direction = direction
        self.total = total
        self.add_next_steps()
        return True

    def add_next_steps(self):
        current_row, current_col = self.current_position.point

        for edge in self.current_position.edges:
            if edge in self.visited_nodes:
                continue
            e_row, e_col = edge.point
            e_row_dir = e_row - current_row
            e_col_dir = e_col - current_col
            if (e_row_dir, e_col_dir) == self.direction:
                self.next_steps.put(
                    (self.total + 1, self.grid.nodes[edge.point], self.direction)
                )

            else:
                d_row, d_col = self.direction
                if abs(d_row - e_row_dir) == 2 or abs(d_col - e_col_dir) == 2:
                    self.next_steps.put(
                        (
                            self.total + 2001,
                            self.grid.nodes[edge.point],
                            (e_row_dir, e_col_dir),
                        )
                    )
                else:
                    self.next_steps.put(
                        (
                            self.total + 1001,
                            self.grid.nodes[edge.point],
                            (e_row_dir, e_col_dir),
                        )
                    )


if __name__ == "__main__":

    data = get_data()
    grid = Grid(data)
    gw = GridWalk(grid, (0, 1))
    keep_going = True
    while keep_going:
        keep_going = gw.take_step()
    print(gw.total)
