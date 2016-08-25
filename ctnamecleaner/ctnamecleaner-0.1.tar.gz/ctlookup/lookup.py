import pandas as pd

class Lookup:
    # Default CSV for resolving CT place names
    def __init__(self, raw_name_col="name", clean_name_col="real.town.name",
                 csv_url="https://docs.google.com/spreadsheets/d/1WqZIGk2AkHXKYvd4uXy5a2nwyg529e7mMU5610Ale0g/pub?gid=0&single=true&output=csv"):
        self.csv_url = csv_url
        self.lookup_table = pd.read_csv(self.csv_url)
        self.raw_name_col=raw_name_col
        self.clean_name_col = clean_name_col
        
    def clean(self, raw_name, error=None):
        results = self.lookup_table[self.lookup_table[self.raw_name_col]\
                                    .str.upper() == raw_name.upper()]
        if len(results.index) < 1:
            return error
            # raise Exception("LookupError: No results found")
        elif len(results.index) > 1:
            return error
            # raise Exception("LookupError: More than one result found")
        else:
            return results[self.clean_name_col].unique()[0]

    def clean_dataframe(self, df, town_col):
        df = df.copy()
        df[town_col + "_CDF_UPPER"] = df.apply(lambda x: str(x[town_col]).upper(), axis=1)
        df = df.set_index(town_col + "_CDF_UPPER")
        lu = self.lookup_table
        lu = lu.set_index(self.raw_name_col)

        return df.join(lu,how="left")[self.clean_name_col].to_frame().reset_index()["real.town.name"]

