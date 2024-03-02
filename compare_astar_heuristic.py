import maze
import time
import pandas as pd


def get_test_params(func, heuristic):
    start_time = time.time()
    path, _, _ = func(heuristic)
    end_time = time.time()

    return len(path), end_time - start_time


def comparison():
    test_maze_sizes = [50, 100, 1500, 2000]
    options = ["euclidean", "manhattan", "both"]
    exec_times_tab, path_len_tab = {}, {}

    print(f"Testing sizes:")
    for test_size in test_maze_sizes:
        print(f"  {test_size}")
        test_maze = maze.Maze(test_size, test_size, 0.3)
        exec_times, path_lens = {}, {}
        for heuristic in options:
            path_len, exec_time = get_test_params(test_maze.solve_astar, heuristic)
            exec_times[heuristic] = exec_time
            path_lens[heuristic] = path_len

        exec_times_tab[test_size] = exec_times
        path_len_tab[test_size] = path_lens

    print("\nEXEC TIMES")
    print(pd.DataFrame(exec_times_tab).T)
    print("\nPATH LENS")
    print(pd.DataFrame(path_len_tab).T)


if __name__ == "__main__":
    comparison()
