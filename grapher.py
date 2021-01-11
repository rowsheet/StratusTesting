import os
import numpy as np
import matplotlib.pyplot as plt

# Get the ".dat" files in ./data
def get_data_filenames():
    data_filenames = []
    filenames = os.listdir("./data")
    for filename in filenames:
        if filename.split("_")[0] == "archive":
            continue
        if filename.split(".")[1] == "dat":
            data_filenames.append(filename)
    return data_filenames

# Process the data sets and parse the files.
def get_data_set():
    data_set = {}
    data_filenames = get_data_filenames()
    for filename in data_filenames:
        with open("./data/" + filename, "r") as f:
            data = f.read()
            # Split the csv and convert to floats.
            data_array = [float(x) for x in str(data).split(",")]
            # Something like "Homepage_Public_BAL.dat" -> "Homepage Public BAL"
            set_label = " ".join([x for x in filename.split(".")[0].split("_")])
            # Add the data set
            data_set[set_label] = data_array
    return data_set

# Convert the datasets for graphing them in each windows.
def generate_windows():
    data_set = get_data_set()
    windows = {}
    for label, data in data_set.items():
        page = label.split(" ")[0]
        if page not in windows:
            windows[page] = {}
        windows[page][label] = data
    return windows

# Graph the datasets in for each window.
def graph_windows(windows, bins):
    fig, axes = plt.subplots(ncols=1, nrows=len(windows))
    count = 0
    for pagename, pageset in windows.items():
        hist_data = []
        hist_labels = []
        for requestname, dataset in pageset.items():
            hist_data.append(dataset)
            hist_labels.append(requestname)
        hist_labels = np.array(hist_labels)
        # We have to transpose this or the dataset will be backwards.
        hist_labels = np.transpose(hist_labels)
        ax = axes[count]
        count = count + 1
        ax.hist(hist_data, bins, density=True, histtype="bar", label=hist_labels)
        ax.legend(prop={"size": 10})
        ax.set_xlim(0,5)
        ax.set_title(pagename)
    fig.tight_layout()
    plt.show()

def run(bins = 100):
    # Each "page", regardless of the request types, are graphed in their own window.
    windows = generate_windows()
    # Graph it
    graph_windows(windows, bins)
