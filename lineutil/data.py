
import pandas as pd
import numpy as np


def read_dat(filepath_or_buffer, **kwargs):
    """ A simple wrapper of `pandas.read_csv()` except `sep` defaults to white spaces (\\s+) and
    `index_col` defaults to False.
    """
    
    kwargs1 = kwargs.copy()
    kwargs1.setdefault('index_col', False)
    kwargs1.setdefault('sep', '\\s+')

    return pd.read_csv(filepath_or_buffer, **kwargs1)


read_csv = pd.read_csv


def write_dat(data, path_or_buf, columns=None, sep='\t', transpose=False, **kwargs):
    """ A simple wrapper of `pandas.DataFrame.to_csv()`. Used for either a DataFrame, or numpy array + column titles.

    data: `DataFrame`, or 2D numpy array;
    columns: The columns used, if data is numpy array.
    sep: Separator for the output file;
    transpose: Whether transpose the data first before writing;

    Additional kwargs will be passed to `pandas.DataFrame.to_csv()`.
    """

    if isinstance(data, pd.DataFrame):
        df = data
    else:
        if not transpose:
            df = pd.DataFrame(data, columns=columns)
        else:
            df = pd.DataFrame(np.array(data).T, columns=columns)

    df.to_csv(path_or_buf, sep=sep, index=False, **kwargs)
