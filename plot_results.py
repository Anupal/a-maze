import pandas as pd
import matplotlib.pyplot as plt


def main():
    data = pd.read_csv("results.csv")

    data = data.groupby(["maze_size", "algorithm"]).mean().reset_index()

    print(data)

    # exit()

    # Separate data for each algorithm
    dfs_data = data[data["algorithm"] == "DFS"]
    bfs_data = data[data["algorithm"] == "BFS"]
    astar_data = data[data["algorithm"] == "ASTAR"]
    mdppit_data = data[data["algorithm"] == "MDPPIT"]
    mdpvit_data = data[data["algorithm"] == "MDPVIT"]

    # Define the columns to be plotted
    columns_to_plot = [
        "exec_time",
        "path_length",
        "nodes_visited",
        "loops",
        "memory_min",
        "memory_max",
    ]

    # Create separate plots for each column
    for col in columns_to_plot:
        plt.figure(figsize=(12, 6))

        # Plot DFS data
        plt.plot(dfs_data["maze_size"], dfs_data[col], label="DFS")

        # Plot BFS data
        plt.plot(bfs_data["maze_size"], bfs_data[col], label="BFS")

        # Plot A* data
        plt.plot(astar_data["maze_size"], astar_data[col], label="ASTAR")

        # Plot MDP Policy Iteration data
        plt.plot(mdppit_data["maze_size"], mdppit_data[col], label="MDP Policy Iteration")

        # Plot MDP Value Iteration data
        plt.plot(mdpvit_data["maze_size"], mdpvit_data[col], label="MDP Value Iteration")

        # Add labels and title
        plt.xlabel("Maze Size")
        plt.ylabel(col)
        plt.title(f"{col.capitalize()} vs. Maze Size")
        plt.legend()
        plt.grid(True)

        # Save the plot or display it interactively
        # plt.savefig(f"{col}.png")  # Uncomment to save the plot as an image
    plt.show()


if __name__ == '__main__':
    main()