import csv

import matplotlib.pyplot as plt
import numpy as np


def read_csv(csv_path: str) -> list:
    """
    Reads a CSV file and returns a list of dictionaries.

    :param csv_path: The path to the CSV file to read.

    :return: A list of dictionaries representing the rows of the CSV file.
    """
    with open(csv_path, newline="") as csvfile:
        return list(csv.DictReader(csvfile, delimiter=","))


def moving_average(a, n):
    """
    Calculates the moving average of an array.

    :param a: Input array.
    :param n: Number of elements to include in the moving average.

    :return: Moving average of the input array.
    """
    ret = np.cumsum(a, dtype=float)
    ret[n:] = ret[n:] - ret[:-n]
    return ret[n - 1 :] / n


def plot_1d(
    csv_path: str,
    x_key: str,
    y_key: str,
    winsize: int = 300,
    save_path: str = None,
    show_result: bool = True,
):
    """
    Plot a 1D graph from a CSV file.

    :param csv_path: Path to the CSV file.
    :param x_key: Name of the column to be used as the x-axis.
    :param y_key: Name of the column to be used as the y-axis.
    :param winsize: Size of the moving window for smoothing the data. 
    :param save_path: Optional path to save the plot as an image. 
    :param show_result: Display the plot on the screen. 

    :return: None
    """
    result = read_csv(csv_path)

    time_arr = []
    density_arr = []

    for res in result:
        time_arr.append(res[x_key])
        density_arr.append(res[y_key])

    plt.plot(moving_average(time_arr, winsize), moving_average(density_arr, winsize))
    plt.xlabel(x_key)
    plt.ylabel(y_key)

    if show_result:
        plt.show()
        plt.close()

    if save_path:
        plt.savefig(save_path)


def plot_heatmap():
    return NotImplementedError


if __name__ == "__main__":
    plot_1d("result_MVI_8878.csv", "time", "density")
    plot_1d("result_MVI_8878.csv", "time", "density_ratio")
    plot_1d("result_MVI_8878.csv", "time", "count")
