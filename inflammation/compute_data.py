"""Module containing mechanism for calculating standard deviation between datasets.
"""

import glob
import os
import numpy as np
from pathlib import Path
from inflammation import models, views


def analyse_data(data_source):
    """Calculate the standard deviation by day between datasets

    Gets all the inflammation csvs within a directory, works out the mean
    inflammation value for each day across all datasets, then graphs the
    standard deviation of these means."""
    data = data_source.load_inflammation_data()

    daily_standard_deviation = compute_standard_deviation_by_day(data)

    return daily_standard_deviation

def compute_standard_deviation_by_day(data):
    means_by_day = map(models.daily_mean, data)
    means_by_day_matrix = np.stack(list(means_by_day))
    return np.std(means_by_day_matrix, axis=0)

def load_inflammation_data(dir_path):
    data_file_paths = glob.glob(os.path.join(dir_path, 'inflammation*.csv'))
    if len(data_file_paths) == 0:
        raise ValueError(f"No inflammation csv's found in path {dir_path}")
    return map(models.load_csv, data_file_paths)

class CSVDataSource():
    def __init__(self, dir_path):
        self._dir_path = dir_path
    
    def load_inflammation_data(self):
        data_file_paths = glob.glob(os.path.join(self._dir_path, 'inflammation*.csv'))
        if len(data_file_paths) == 0:
            raise ValueError(f"No inflammation csv's found in path {self._dir_path}")
        return map(models.load_csv, data_file_paths)
        
class JSONDataSource():
    def __init__ (self, dir_path):
        self._dir_path = dir_path

    def load_inflammation_data(self):
        """Load a numpy array from a JSON document.

        Expected format:
        [
            {
                observations: [0, 1]
            },
            {
                observations: [0, 2]
            }
        ]

        :param filename: Filename of CSV to load

        """
        data_file_paths = glob.glob(os.path.join(self._dir_path, 'inflammation*.json'))
        if len(data_file_paths) == 0:
            raise ValueError(f"No inflammation json's found in path {self._dir_path}")
        return map(models.load_json, data_file_paths)

# data_source = CSVDataSource(Path.cwd() / "data")
# analyse_data(data_source)