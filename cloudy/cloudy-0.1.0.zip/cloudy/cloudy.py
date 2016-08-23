import numpy as np
import pandas as pd


class Cloudy(object):
    """
    Parses Cloudy output files into Pandas DataFrames for analysis.

    There is one main DataFrame and a list of data frames (see Attributes).
    The reasoning for the list is to make it easier to graph and analyze.

    Parameters
    ----------
    grd : str
        Path to the .grd file from the Cloudy output.
    data : str
        Path to the output file with the data to be analyzed.
    grd_labels : list[None]
        Strings labeling the different variables iterated in cloudy. Defining
        this parameter will attach the grd data to the data frame.

    Attributes
    ----------
    grd : numpy array
        Array(s) of the data from the grd file.
    df : DataFrame
        DataFrame of the data file.
    grd_labels : list[None]
        Strings labeling the different variables iterated in cloudy. Defining
        this parameter will attach the grd data to the data frame.
    labels : list
        The column headers of the data file. Makes easier access to df.
    """

    def __init__(self, grd, data, grd_labels=None):
        self.grd = self._read_grd(grd)
        self.df = self._make_df(data)
        if grd_labels is not None:
            if len(self.grd) != len(grd_labels):
                print(
                    "Number of labels must match number of cloudy variables")
            else:
                for variable, label in zip(self.grd, grd_labels):
                    self.df[label] = variable
        self.grd_labels = grd_labels
        self.labels = sorted(list(self.df.columns[:]))

    def __repr__(self):
        return repr(self.labels)

    def __getitem__(self, key):
        return self.df[key]

    def _read_grd(self, grd):
        """Read the grd file into a numpy array"""
        df = self._make_df(grd)  # Turn grd into a data frame
        array = df['grid parameter string'].as_matrix()  # Column with Data
        # If the values are not floats, convert.
        if array.dtype != 'float64':
            # Turn [('1', '2'), ('3', '4')] to [[1.,2.], [3.,4.]]
            array = np.array(
                [item.split(',') for item in array]).astype('float')
        return np.column_stack(array)

    def _make_df(self, data):
        """Turn the data file into a DataFrame"""
        names = self._get_header(data)  # Get Column names
        # Create DataFrame
        df = pd.read_table(
            data, sep='\t', header=None, skiprows=1, names=names, comment='#')
        return df

    def _get_header(self, filep):
        """Grab the column headers for the df"""
        with open(filep, 'r') as filein:
            line = filein.readline()[1:-1]
            header = line.split('\t')
        return header
