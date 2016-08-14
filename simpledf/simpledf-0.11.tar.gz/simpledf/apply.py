import pandas as pd


def apply(groupby_obj, func):
    ''' Easy Apply '''
    func_output_list = [func(df) for i, df in groupby_obj]
    df = pd.concat(func_output_list)
    return df

