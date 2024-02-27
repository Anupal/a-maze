import maze
import time
import pandas as pd
from memory_profiler import profile, memory_usage


@profile
def test_memory(func):
    profile(func)()


def test_performance(func: callable):
    start_time = time.time()
    path, total_nodes, loops = func()
    end_time = time.time()

    return end_time - start_time, len(path), len(total_nodes), loops


def main():
    test_maze_sizes = [i for i in range(5, 51, 5)]

    df, i = pd.DataFrame(columns=["maze_size", "algorithm", "exec_time", "path_length", "nodes_visited", "loops", "memory_min", "memory_max"]), 0

    for test_size in test_maze_sizes:
        print("Testing size ", test_size, flush=True)
        for k in range(3):
            print("  sample =", k, flush=True)
            test_maze = maze.Maze(test_size, test_size, 0.3)
            funcs = [test_maze.solve_dfs, test_maze.solve_bfs, test_maze.solve_astar, test_maze.solve_mdppit, test_maze.solve_mdpvit]

            print("    ", end="", flush=True)
            for func in funcs:
                algorithm = func.__name__.split("_")[1].upper()
                print(algorithm, end=" ", flush=True)
                tt, path, total_nodes, loops = test_performance(func)
                mem_usage = memory_usage(func, interval=0.1, include_children=True)

                df.loc[i] = [test_size, algorithm, round(tt, 4), path, total_nodes, loops, min(mem_usage), max(mem_usage)]
                i += 1
            print(flush=True)

            del test_maze

    df.to_csv('results.csv', index=False)


if __name__ == '__main__':
    main()