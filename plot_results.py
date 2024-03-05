import pandas as pd
import matplotlib.pyplot as plt


def main():
    plt.style.use("seaborn-v0_8-bright")

    result_file_name = input("Enter result file name (results.csv): ")
    if not result_file_name:
        result_file_name = "results/results.csv"
    else:
        result_file_name = "results/" + result_file_name

    print("Reading data from file:", result_file_name)

    data = pd.read_csv(result_file_name)
    data = data.groupby(["maze_size", "algorithm"]).mean().reset_index()
    print(data)

    data["memory_max"] = data["memory_max"] // (1024)

    algorithms = data["algorithm"].unique()

    algorithm_data = {}
    for algorithm in algorithms:
        algorithm_data[algorithm] = data[data["algorithm"] == algorithm]

    columns_to_plot = [
        "exec_time",
        "path_length",
        "memory_max",
    ]

    for col in columns_to_plot:
        plt.figure(figsize=(8, 6))

        for algorithm in algorithms:
            plt.plot(algorithm_data[algorithm]["maze_size"], algorithm_data[algorithm][col], label=algorithm)

        col_title = col.replace("_", " ")
        # Add labels and title
        plt.xlabel("Maze Size")
        if col == "memory_max":
            plt.ylabel(col_title.capitalize() + " (KB)")
        else:
            plt.ylabel(col_title.capitalize())
        plt.title(f"{col_title.capitalize()} vs. Maze Size")
        # plt.ylim([0, data[col].max() + data[col].max()//10])
        plt.legend()
        plt.grid(True)
        image_name = "images/" + result_file_name.replace(".csv", "_").replace("results/", "") + f"{col}.png"
        print("Saving image:", image_name)
        plt.savefig(image_name, bbox_inches='tight', pad_inches=0)
    plt.show()


if __name__ == "__main__":
    main()
