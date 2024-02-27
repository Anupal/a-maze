import heapq
import math
from random import choice, random
from collections import deque

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap



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

        plt.figure(figsize=(self.grid_width, self.grid_height))
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

    def solve_astar(self):
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
                        "h": (self.exit[0] - next_ij[0] + self.exit[1] - next_ij[1]) + math.sqrt(
                            (self.exit[0] - next_ij[0]) ** 2 + (self.exit[1] - next_ij[1]) ** 2)
                    }

                    heapq.heappush(open_list, (child["h"] + child["g"], node_count, child))
                    node_count += 1
                    open_list_tracker.add(child["ij"])

    def _mdp_agent_step(self, i, j, action):
        next_ij = (i + _directions[action][0], j + _directions[action][1])
        if 0 <= next_ij[0] < self.grid_height and 0 <= next_ij[1] < self.grid_width \
                and not self.maze[next_ij[0]][next_ij[1]]:
            return next_ij
        else:
            return i, j

    def _perform_action(self, state, action):
        next_state = (state[0] + _directions[action][0], state[1] + _directions[action][1])
        if 0 <= next_state[0] < self.grid_height and 0 <= next_state[1] < self.grid_width \
                and not self.maze[next_state[0]][next_state[1]]:
            return next_state
        else:
            return state

    def display_mdp_policy(self, policy):
        print(policy)

        mapping = {
            (-1, 0): "↑",
            (1, 0): "↓",
            (0, -1): "←",
            (0, 1): "→"
        }
        policy_grid = ""

        for i in range(policy.shape[0]):
            for j in range(policy.shape[1]):
                policy_grid += mapping[_directions[policy[i, j]]] if policy[i, j] != -1 else "█"
            policy_grid += "\n"
        print(policy_grid)

    def _reward(self, state):
        return 0 if state == self.exit else -1

    def solve_mdppit(self):
        # create initial random policy
        # policy = np.random.randint(0, 4, size=self.maze.shape)
        policy = np.zeros(self.maze.shape, dtype=np.int8)
        policy[self.maze == 1] = -1

        value_function, discount_factor, loops, theta = np.zeros(self.maze.shape), 0.9, 0, 1e-2
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
                print(f"warning: exiting MDP policy iteration due to incorrect policy, maze dimenstions=({self.height}x{self.width})", flush=True)
                return [], [], loops
            state = next_state
            path.append(state)

        return path, [], loops

    def solve_mdpvit(self):
        # create initial random policy
        policy = np.zeros(self.maze.shape, dtype=np.int8)
        policy[self.maze == 1] = -1

        value_function, discount_factor, loops, theta = np.zeros(self.maze.shape), 0.99, 0, 1e-2
        states = [(i, j) for j in range(self.grid_width) for i in range(self.grid_height) if self.maze[i][j] == 0]


        while True:
            delta = 0
            for state in states:
                if state == self.exit:
                    continue
                current_value = value_function[state[0]][state[1]]
                action_values = []
                for action in range(4):  # For each action, calculate value
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
                    f"warning: exiting MDP value iteration due to incorrect policy, maze dimenstions=({self.height}x{self.width})",
                    flush=True)
                return [], [], loops
            state = next_state
            path.append(state)

        return path, [], loops

    def display_final(self):
        plt.show()
