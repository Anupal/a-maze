import pandas as pd
import matplotlib.pyplot as plt


def main():
    result_file_name = input("Enter result file name (results.csv): ")
    if not result_file_name:
        result_file_name = "results.csv"

    data = pd.read_csv(result_file_name)

    data = data.groupby(["maze_size", "algorithm"]).mean().reset_index()

    print(data)

    # exit()

    algorithms = data["algorithm"].unique()

    algorithm_data = {}
    for algorithm in algorithms:
        algorithm_data[algorithm] = data[data["algorithm"] == algorithm]

    # Define the columns to be plotted
    columns_to_plot = [
        "exec_time",
        "path_length",
        "nodes_visited",
        "loops",
        "memory_max",
    ]

    # Create separate plots for each column
    for col in columns_to_plot:
        plt.figure(figsize=(12, 6))

        for algorithm in algorithms:
            plt.plot(algorithm_data[algorithm]["maze_size"], algorithm_data[algorithm][col], label=algorithm)

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