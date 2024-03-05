import heapq
import math
from random import choice, random, seed
from collections import deque

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap


seed(999)
_maze_cmap = ListedColormap(['white', 'black', 'blue', 'red', 'yellow'])
_directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]


class Maze:
    def __init__(self, height, width, branching):
        self.height, self.width = height, width
        self.grid_height = 2 * height + 1
        self.grid_width = 2 * width + 1
        self.entry, self.exit = (0, 1), (self.grid_height - 1, self.grid_width - 2)
        self.branching = branching
        self._generate_base()
        self._generate_paths_dfs()

    def _generate_base(self):
        self.maze = np.ones((self.grid_height, self.grid_width))
        for i in range(self.height):
            for j in range(self.width):
                self.maze[2 * i + 1, 2 * j + 1] = 0

    def _generate_paths_dfs(self):
        stack, tracker = [(0, 0)], set()

        while stack:
            (i, j) = stack.pop()
            tracker.add((i, j))

            if next_cell := self._next_cell(i, j, tracker):
                stack.append((i, j))

                # convert adjacent wall into a cell
                x, y = 2 * i + 1 + next_cell[0], 2 * j + 1 + next_cell[1]
                stack.append((i + next_cell[0], j + next_cell[1]))
                self.maze[x, y] = 0

                if random() < self.branching:
                    tracker.remove((i, j))

        # convert top and bottom walls into entry, exit cells
        self.maze[self.entry[0], self.entry[1]] = 0
        self.maze[self.exit[0], self.exit[1]] = 0

    def _next_cell(self, i, j, tracker):
        options = []
        for ij in _directions:
            next_ij = i + ij[0], j + ij[1]
            if 0 <= next_ij[0] < self.height and 0 <= next_ij[1] < self.width and next_ij not in tracker:
                options.append(ij)
        return choice(options) if options else None

    def display(self):
        plt.figure(figsize=(self.grid_width, self.grid_height))
        plt.imshow(self.maze, cmap="binary", interpolation="nearest")
        plt.xticks([]), plt.yticks([])
        plt.show()

    def display_result(self, path, tracker):
        _maze = self.maze.copy()
        for (i, j) in tracker:
            _maze[i, j] = 2
        for (i, j) in path:
            _maze[i, j] = 3

        _maze[self.entry[0], self.entry[1]] = 4
        _maze[self.exit[0], self.exit[1]] = 4

        plt.figure() #figsize=(self.grid_width, self.grid_height))
        plt.imshow(_maze, cmap=_maze_cmap, interpolation="nearest")
        plt.xticks([]), plt.yticks([])

    def solve_dfs(self):
        stack, tracker, loops = [self.entry], {self.entry: None}, 0

        while stack:
            (i, j) = stack.pop()

            if (i, j) == self.exit:
                path = []
                current = self.exit
                while current:
                    path.append(current)
                    current = tracker[current]
                return path, tracker, loops

            for ij in _directions:
                loops += 1
                next_ij = i + ij[0], j + ij[1]
                if 0 <= next_ij[0] < self.grid_height and 0 <= next_ij[1] < self.grid_width \
                        and not self.maze[next_ij[0]][next_ij[1]] and next_ij not in tracker:
                    stack.append(next_ij)
                    tracker[next_ij] = (i, j)

    def solve_bfs(self):
        queue, tracker, loops = deque([self.entry]), {self.entry: None}, 0

        while queue:
            (i, j) = queue.popleft()

            if (i, j) == self.exit:
                path = []
                current = self.exit
                while current:
                    path.append(current)
                    current = tracker[current]
                return path, tracker, loops

            for ij in _directions:
                loops += 1
                next_ij = i + ij[0], j + ij[1]
                if 0 <= next_ij[0] < self.grid_height and 0 <= next_ij[1] < self.grid_width \
                        and not self.maze[next_ij[0]][next_ij[1]] and next_ij not in tracker:
                    queue.append(next_ij)
                    tracker[next_ij] = (i, j)

    def _heuristic(self, p1, p2, h):
        if h == "euclidean":
            return math.sqrt((p2[0] - p1[0]) ** 2 + (p2[1] - p1[1]) ** 2)
        elif h == "manhattan":
            return abs(p2[0] - p1[0]) + abs(p2[1] - p1[1])
        elif h == "both":
            return abs(p2[0] - p1[0]) + abs(p2[1] - p1[1]) + math.sqrt((p2[0] - p1[0]) ** 2 + (p2[1] - p1[1]) ** 2)

    def solve_astar(self, heuristic="both"):
        node_count = 1
        open_list, open_list_tracker, closed_list, loops = [(0, 0, {"g": 0, "f": 0, "ij": self.entry, "prev": None})], {
            self.entry}, {}, 0

        while open_list:
            _, _, curr_node = heapq.heappop(open_list)
            open_list_tracker.remove(curr_node["ij"])

            closed_list[curr_node["ij"]] = curr_node
            if curr_node["ij"] == self.exit:
                path = []
                current = curr_node

                while current:
                    path.append(current["ij"])
                    current = current["prev"]
                return path, closed_list, loops

            # Adjacent points
            for ij in _directions:
                loops += 1
                next_ij = (curr_node["ij"][0] + ij[0], curr_node["ij"][1] + ij[1])

                if 0 <= next_ij[0] < self.grid_height and 0 <= next_ij[1] < self.grid_width and not \
                        self.maze[next_ij[0]][next_ij[1]]:
                    # children.append()
                    if next_ij in closed_list or next_ij in open_list_tracker:
                        continue

                    child = {
                        "prev": curr_node,
                        "ij": next_ij,
                        "g": curr_node["g"] + 1,
                        "h": self._heuristic(next_ij, self.exit, heuristic)
                    }

                    heapq.heappush(open_list, (child["h"] + child["g"], node_count, child))
                    node_count += 1
                    open_list_tracker.add(child["ij"])

    def _perform_action(self, state, action):
        next_state = (state[0] + _directions[action][0], state[1] + _directions[action][1])
        if 0 <= next_state[0] < self.grid_height and 0 <= next_state[1] < self.grid_width \
                and not self.maze[next_state[0]][next_state[1]]:
            return next_state
        else:
            return state

    def display_mdp_policy(self, policy):
        mapping = {
            (-1, 0): "↑",
            (1, 0): "↓",
            (0, -1): "←",
            (0, 1): "→"
        }
        table_data = []
        for i in range(policy.shape[0]):
            row_data = []
            for j in range(policy.shape[1]):
                if policy[i, j] != -1:  # Check if the state is not blocked
                    row_data.append(mapping[_directions[policy[i, j]]])
                else:  # For blocked states
                    row_data.append(" ")
            table_data.append(row_data)

        fig_width, fig_height = policy.shape[1] * 0.2, policy.shape[0] * 0.2
        fig, ax = plt.subplots(figsize=(fig_width, fig_height))
        ax.axis('tight')
        ax.axis('off')

        ax.table(cellText=table_data, cellLoc='center', loc='center', edges='closed')

        plt.tight_layout()

    def _reward(self, state):
        return 1 if state == self.exit else -0.01

    def solve_mdppit(self, discount_factor=0.99, theta=1e-4):
        # create initial random policy
        policy = np.random.randint(0, 4, size=self.maze.shape)
        policy[self.maze == 1] = -1

        value_function, loops = np.zeros(self.maze.shape), 0
        states = [(i, j) for j in range(self.grid_width) for i in range(self.grid_height) if self.maze[i][j] == 0]

        while True:
            # policy evaluation phase
            while True:
                delta = 0
                for state in states:
                    if state == self.exit:
                        continue

                    current_value = value_function[state[0]][state[1]]
                    next_state = self._perform_action(state, policy[state[0]][state[1]])
                    value_function[state[0]][state[1]] = self._reward(state) + discount_factor * value_function[next_state[0]][next_state[1]]
                    delta = max(delta, abs(current_value - value_function[state[0]][state[1]]))

                    loops += 1

                if delta < theta:
                    break

            # policy improvement phase
            policy_stable = True
            for state in states:
                if state == self.exit:
                    continue

                old_action = policy[state[0]][state[1]]
                action_values = []
                for action in range(4):
                    next_state = self._perform_action(state, action)
                    action_values.append(self._reward(state) + discount_factor * value_function[next_state[0]][next_state[1]])
                    loops += 1
                best_action = np.argmax(action_values)
                policy[state[0]][state[1]] = best_action
                if old_action != best_action:
                    policy_stable = False

            if policy_stable:
                break

        # generate return path
        path, state = [self.entry], self.entry
        while state != self.exit:
            action = policy[state[0]][state[1]]
            next_state = self._perform_action(state, action)
            if state == next_state:
                print(f"warning: exiting MDP policy iteration due to incorrect policy, maze dimenstions=({self.height}x{self.width})"
                      f" gamma={discount_factor} theta={theta}", flush=True)
                self.display_mdp_policy(policy)
                return [], [], loops
            state = next_state
            path.append(state)

        self.display_mdp_policy(policy)
        return path, [], loops

    def solve_mdpvit(self, discount_factor=0.99, theta=1e-4):
        # create initial random policy
        policy = np.random.randint(0, 4, size=self.maze.shape)
        policy[self.maze == 1] = -1

        value_function, loops = np.zeros(self.maze.shape), 0
        states = [(i, j) for j in range(self.grid_width) for i in range(self.grid_height) if self.maze[i][j] == 0]

        while True:
            delta = 0
            for state in states:
                if state == self.exit:
                    continue
                current_value = value_function[state[0]][state[1]]
                action_values = []
                for action in range(4):
                    next_state = self._perform_action(state, action)
                    action_values.append(self._reward(state) + discount_factor * value_function[next_state[0]][next_state[1]])
                    loops += 1

                best_action = np.argmax(action_values)
                policy[state[0]][state[1]] = best_action

                best_value = action_values[best_action]
                value_function[state[0]][state[1]] = best_value
                delta = max(delta, abs(current_value - best_value))

            if delta < theta:
                break

        # generate return path
        path, state = [self.entry], self.entry
        while state != self.exit:
            action = policy[state[0]][state[1]]
            next_state = self._perform_action(state, action)
            if state == next_state:
                print(
                    f"warning: exiting MDP value iteration due to incorrect policy, maze dimenstions=({self.height}x{self.width})"
                    f" gamma={discount_factor} theta={theta}", flush=True)
                self.display_mdp_policy(policy)
                return [], [], loops
            state = next_state
            path.append(state)

        self.display_mdp_policy(policy)
        return path, [], loops

    def display_final(self):
        plt.show()
