import argparse
import maze
import time


def main():
    parser = argparse.ArgumentParser(description="Maze solver script")
    parser.add_argument('-a', '--algorithm', type=str, help='Maze solver algorithm', required=True)
    parser.add_argument('-s', '--maze-size', type=int, help='Maze size', required=True)
    parser.add_argument('-g', '--mdp-discount-factor', type=float, help='MDP gamma', required=False, default=0.99)
    parser.add_argument('-t', '--mdp-theta', type=float, help='MDP theta', required=False, default=0.001)


    args = parser.parse_args()
    solver = args.algorithm
    maze_size = args.maze_size

    test_maze = maze.Maze(maze_size, maze_size, 0.3)
    solver_args = ()
    if solver == "dfs":
        solver_func = test_maze.solve_dfs
    elif solver == "bfs":
        solver_func = test_maze.solve_bfs
    elif solver == "astar":
        solver_func = test_maze.solve_astar
    elif solver == "mdpvit":
        solver_func = test_maze.solve_mdpvit
        solver_args = (args.mdp_discount_factor, args.mdp_theta)
    elif solver == "mdppit":
        solver_func = test_maze.solve_mdppit
        solver_args = (args.mdp_discount_factor, args.mdp_theta)
    else:
        print("Invalid solver algorithm.")
        exit()

    start_time = time.time()
    path, total_nodes, _ = solver_func(*solver_args)
    end_time = time.time()

    print("PATH LEN:", len(path))
    print("TIME TAKEN (s):", end_time - start_time)

    if path:
        test_maze.display_result(path, total_nodes)

    test_maze.display_final()


if __name__ == '__main__':
    main()