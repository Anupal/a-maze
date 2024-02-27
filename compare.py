import maze
import time
import pandas as pd
from memory_profiler import memory_usage


def test_performance(func: callable):
    print("      compute", flush=True)
    start_time = time.time()
    path, total_nodes, loops = func()
    end_time = time.time()

    if not path:
        print("     retrying...", flush=True)
        return test_performance(func)

    print("      memory", flush=True)
    mem_usage, retval = memory_usage(func, interval=0.1, include_children=True, retval=True)

    if not retval[0]:
        print("     retrying...", flush=True)
        return test_performance(func)

    return end_time - start_time, len(path), len(total_nodes), loops, mem_usage


def main():
    test_maze_sizes = [i for i in range(50, 51, 5)]

    df, i = pd.DataFrame(columns=["maze_size", "algorithm", "exec_time", "path_length", "nodes_visited", "loops", "memory_min", "memory_max"]), 0
    df["exec_time"] = df["exec_time"].astype(float)

    for test_size in test_maze_sizes:
        print("Testing maze size =", test_size, flush=True)
        for k in range(3):
            print("  sample =", k, flush=True)
            test_maze = maze.Maze(test_size, test_size, 0.3)
            funcs = [test_maze.solve_dfs, test_maze.solve_bfs, test_maze.solve_astar, test_maze.solve_mdppit, test_maze.solve_mdpvit]

            for func in funcs:
                algorithm = func.__name__.split("_")[1].upper()
                print("   ", algorithm, flush=True)
                tt, path, total_nodes, loops, mem_usage = test_performance(func)

                df.loc[i] = [test_size, algorithm, tt, path, total_nodes, loops, min(mem_usage), max(mem_usage)]
                i += 1

            del test_maze

    print("Collected results:")
    print(df)
    print("Saving to 'results.csv'")
    df.to_csv('results.csv', index=False)


if __name__ == '__main__':
    main()