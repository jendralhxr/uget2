import matplotlib.pyplot as plt
import csv
import numpy as np


def read_csv(csv_path: str) -> list:
    with open(csv_path, newline="") as csvfile:
        return list(csv.DictReader(csvfile, delimiter=","))

def moving_average(a, n) :
    ret = np.cumsum(a, dtype=float)
    ret[n:] = ret[n:] - ret[:-n]
    return ret[n - 1:] / n

def plot_1d(csv_path: str, x_key: str, y_key: str, winsize:int = 300, save_path: str = None):
    result = read_csv(csv_path)

    time_arr = []
    density_arr = []

    for res in result:
        time_arr.append(res[x_key])
        density_arr.append(res[y_key])

    plt.plot(moving_average(time_arr,winsize), moving_average(density_arr,winsize))
    plt.xlabel(x_key)
    plt.ylabel(y_key)
    plt.show()
    plt.close()


def plot_heatmap():
    return NotImplementedError


if __name__ == "__main__":
    plot_1d("result_MVI_8878.csv", "time", "density")
    plot_1d("result_MVI_8878.csv", "time", "density_ratio")
    plot_1d("result_MVI_8878.csv", "time", "count")
