import maze
import time
import pandas as pd
import tracemalloc


def test_performance(func: callable):
    print("      compute", flush=True)
    start_time = time.time()
    path, total_nodes, loops = func()
    end_time = time.time()

    if not path:
        print("     retrying...", flush=True)
        return test_performance(func)

    print("      memory", flush=True)
    tracemalloc.start()
    retval = func()
    mem_usage = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    if not retval[0]:
        print("     retrying...", flush=True)
        return test_performance(func)

    return end_time - start_time, len(path), len(total_nodes), loops, mem_usage


def main():
    algos = input("Enter algos: ").split()

    if not algos:
        print("No algorithm specified, defaulting to all.")
        algos = ["dfs", "bfs", "astar", "mdppit", "mdpvit"]

    samples = int(input("Enter sample size: "))
    test_size_range = [int(e) for e in input("Enter test maze size range: ").split()]
    test_maze_sizes = [i for i in range(*test_size_range)]

    result_file_name = input("Enter result file name (results.csv): ")
    if not result_file_name:
        result_file_name = "results/results.csv"
    else:
        result_file_name = "results/" + result_file_name

    df, i = pd.DataFrame(columns=["maze_size", "algorithm", "exec_time", "path_length", "nodes_visited", "loops", "memory_min", "memory_max"]), 0
    df["exec_time"] = df["exec_time"].astype(float)

    for test_size in test_maze_sizes:
        print("Testing maze size =", test_size, flush=True)
        for k in range(samples):
            print("  sample =", k, flush=True)
            test_maze = maze.Maze(test_size, test_size, 0.3)
            funcs = [test_maze.solve_dfs, test_maze.solve_bfs, test_maze.solve_astar, test_maze.solve_mdppit, test_maze.solve_mdpvit]

            for func in funcs:
                algorithm = func.__name__.split("_")[1]
                if algorithm not in algos:
                    continue
                algorithm = algorithm.upper()
                print("   ", algorithm, flush=True)
                tt, path, total_nodes, loops, mem_usage = test_performance(func)
                print("        time taken =", tt)

                df.loc[i] = [test_size, algorithm, tt, path, total_nodes, loops, min(mem_usage), max(mem_usage)]
                i += 1

            del test_maze

    print("Collected results:")
    print(df)
    print(f"Saving to '{result_file_name}'")
    df.to_csv(result_file_name, index=False)


if __name__ == '__main__':
    main()
