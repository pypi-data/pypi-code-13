import pandas
from pymongo import MongoClient


class DataEnrichment(object):

    def __init__(self, db_name, collection_name):
        self.collection_name = collection_name
        self.db_name = db_name

    def retrieve_data_from_db(self, chr=None, start=None, end=None):
        """
        Retrieve single query from mongoDB regarding the variant of interest
        """
        if chr is not None and start is not None and end is not None:

            client = MongoClient()
            db = getattr(client, self.db_name)
            collection = getattr(db, self.collection_name)
            query = collection.find({"$and": [{"Chr": chr}, {"Start": start}, {"End": end}]})
        else:
            raise ValueError("Location values not provided")

        return list(query)

    def retrieve_multiple(self, list_queries):
        client = MongoClient()
        db = getattr(client, self.db_name)
        collection = getattr(db, self.collection_name)

        list_out = []
        for i in list_queries:
            query = collection.find({"$and": [{"Chr": i[0]}, {"Start": i[1]}, {"End": i[2]}]})
            list_out.append(list(query))

        return list_out

    @staticmethod
    def retrieve_read_counts(list_queries):
        """
        From a list of documents retreived from MongoDB, retrive the read counts per allele
        """
        read_counts = []
        for i in list_queries:
            info = list([i[0]["Genotype_Call"]["AD"][0],
                         i[0]["Genotype_Call"]["AD"][1],
                         i[0]["Genotype_Call"]["DP"],
                         i[0]["hgvs_key"]])

            read_counts.append(info)

        return read_counts

    def integrate_data(self, df, read_and_ids, to_query, gene_data, type_data=None):
        """
        Integrates data coming from mongoDB with the existent dataframe. type_data
        refers to either of the following options: Normal, Tumor DNA ,Tumor RNA.
        """

        # Initialize empty columns to be filled
        df['Gene Exp FPKM'] = None
        df['AD_REF'] = None
        df['AD_ALT'] = None
        df['DP'] = None
        df['hgvs_key'] = None

        if len(to_query) != len(read_and_ids):
            raise ValueError("Mismatch between number of queries and queried data")

        new_cols = ['AD_REF', 'AD_ALT', 'DP', 'hgvs_key']

        for i in range(0, len(to_query)):
            df.loc[(df.Chromosome == to_query[i][0]) & (df.Start == to_query[i][1]) &
                   (df.Stop == to_query[i][2]), new_cols] = self.read_counts[i]
            df = self.add_gene_data(df, gene_data)

        return self.rename_cols(df, type_data)

    @staticmethod
    def rename_cols(df, type_data):
        """
        Internal Method to rename columns
        """
        if type_data == 'Normal':
            df = df.rename(columns={'AD_REF': 'Normal Ref Count', 'AD_ALT': 'Normal Alt Count'})
        elif type_data == 'Tumor DNA':
            df = df.rename(columns={'AD_REF': 'Tumor DNA Ref Count', 'AD_ALT': 'Tumor DNA Alt Count'})
        elif type_data == 'Tumor RNA':
            df = df.rename(columns={'AD_REF': 'Tumor RNA Ref Count', 'AD_ALT': 'Tumor RNA Alt Count'})
        else:
            raise ValueError('Invalid data type provided. Choose between "Normal", "Tumor DNA" and "Tumor RNA"')

        return df

    @staticmethod
    def add_gene_data(df, gene_data):
        possible_genes = df['Gene Name'].unique()
        for i in possible_genes:
            df.loc[df['Gene Name'] == i, 'Gene Exp FPKM'] = gene_data.loc[gene_data['Gen Exp'] == i].values[0][1]

        return df


def write_tsv_out(filepath, df):
    df.to_csv(filepath, sep='\t')


def retrieve_chr_start_end(df):
    to_query = pandas.unique(df[['Chromosome', 'Start', 'Stop']].values)
    return list(to_query)