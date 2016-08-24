from utilities import convert
from utilities import final_joint
import myvariant_parsing_utils
from annovar_processing import get_list_from_annovar_csv
from mongo_DB_export import export
import csv_to_df
import logging


class AnnotationMethods(object):

    def __init__(self):
        self.step = 0
        self.chunksize = 10000

    def by_chunks(self, collection_name=None, db_name=None, vcf_file=None, csv_file=None):

        """
        Export data to MongoDB by chunks, iteratively. It retrives annovar data from a csv file and myvariant data from
        their web-server, joins it, and exports it.
        This method is well-fitted for large files. Only the 1000 documents are held in memory and processed at a time,
        instead of attempting to parse and process an entire csv file at once.
        As soon as the method is run, the data will automatically be stored to it. Database and collection name should
        be specified, and there must be a running MongoDB connection. The script will set up a client to communicate
        between python (through pymongo) and the the database.

        :param vcf_file: from where the variant ids will be retrieved
        :param csv_file: name of the collection to which store the data
        :param chunksize: set at 1000 usually for simplicity, since the queries to myvariant.info also have a cap of
        1000 variants per query
        :param step: just a counter object

        :param collection_name:
        :param db_name: name of the database to which store the collection
        :return: nothing, simply exports data to MongoDB
        """

        import logging
        logging.basicConfig(level=logging.DEBUG,
                            format='%(asctime)s %(message)s',
                            datefmt='%a, %d %b %Y %H:%M:%S')

        logging.info('calculating length of file...')

        num_lines = sum(1 for line in open(csv_file))
        seconds = 67*(num_lines/10000)
        m, s = divmod(seconds, 60)
        h, m = divmod(m, 60)

        time_message = 'File is {} lines long. This will take approximately {} hours, {} ' \
                       'minutes to run.'.format(num_lines, h, m)
        logging.info(time_message)

        if vcf_file is None:
            raise KeyError('No input vcf file given')

        if csv_file is None:
            raise KeyError('No input vcf file given')

        if collection_name is None:
            print 'Collection name not provided, setting it to "New_Collection"'
            collection_name = 'New_Collection'

        if db_name is None:
            print 'Database name not provided, setting it to "New_Database"'
            db_name = 'New_Database'

        variant_list = [0, 1] * self.chunksize

        while len(variant_list) >= self.chunksize:

            logging.getLogger("urllib3").setLevel(logging.WARNING)
            logging.getLogger("requests").setLevel(logging.WARNING)

            open_file = myvariant_parsing_utils.VariantParsing()
            variant_list = open_file.get_variants_from_vcf_chunk(vcf_file, self.chunksize, self.step)

            df = csv_to_df.parse_to_df(csv_to_df.open_and_parse_chunks(csv_file, len(variant_list), self.step))
            from_annovar = get_list_from_annovar_csv(df, variant_list)
            from_myvariant = open_file.get_dict_myvariant(variant_list)

            final_joint(from_annovar, from_myvariant)
            joined_list = from_annovar

            # From unicode to string
            joined_list = convert(joined_list)

            logging.info('Parsing to MongoDB ...')
            export(joined_list, collection_name, db_name)
            self.step += 1

        return 'Finished!'

    @staticmethod
    def full_file(vcf_file, csv_file):
        """
        Retrives annovar data from a csv file and myvariant data from their web-server and return a list of documents
        containing info from both services. All done at once.
        This method is well-fitted for smaller files.

        :param vcf_file: vcf file from where HGVS IDs will be extracted
        :param csv_file: name of csv_file to be used (coming from annovar's output)
        :return: nothing, simply exports data to MongoDB
        """

        open_file = myvariant_parsing_utils.VariantParsing()
        variant_list = open_file.get_variants_from_vcf(vcf_file)

        df = csv_to_df.parse_to_df(csv_to_df.open_and_parse(csv_file))
        from_annovar = get_list_from_annovar_csv(df, variant_list)

        open_file = myvariant_parsing_utils.VariantParsing()
        from_myvariant = open_file.get_dict_myvariant(variant_list)

        final_joint(from_annovar, from_myvariant)
        joined_list = from_annovar
        joined_list = convert(joined_list)

        print 'Finished!'
        return joined_list

    def myvariant_chunks(self, chunksize=None, vcf_file=None, collection_name=None, db_name=None):
        """
        Export data to MongoDB by chunks, iteratively. It retrives myvariant data from their web-server solely.
        Annovar, and a processed csv file are not required.
        This method is well-fitted for large files. Only the 1000 documents are held in memory and processed at a time,
        instead of attempting to hold in memory data from all the variants at the same time.
        As soon as the method is run, the data will automatically be stored to it. Database and collection name should
        be specified, and there must be a running MongoDB connection. The script will set up a client to communicate
        between python (through pymongo) and the the database.

        :param vcf_file: vcf file from where HGVS IDs will be extracted
        :param chunksize: set at 1000 usually for simplicity, since the queries to myvariant.info also have a cap of
        1000 variants per query
        :param step: just a counter object
        :param collection_name: name of the collection to which store the data
        :param db_name: name of the database to which store the collection
        :return: nothing, simply exports data to MongoDB
        """
        if vcf_file is None:
            raise KeyError('No input vcf file given')

        if collection_name is None:
            print 'Collection name not provided, setting it to "New_Collection"'
            collection_name = 'New_Collection'

        if db_name is None:
            print 'Database name not provided, setting it to "New_Database"'
            db_name = 'New_Database'

        if chunksize is None:
            chunksize = self.chunksize

        while self.step * chunksize < len(variant_list):
            open_file = myvariant_parsing_utils.VariantParsing()
            variant_list = open_file.get_variants_from_vcf_chunk(vcf_file, chunksize, self.step)
            chunk_ids = variant_list[chunksize * self.step:chunksize * (self.step + 1)]

            open_file = myvariant_parsing_utils.VariantParsing()
            from_myvariant = open_file.get_dict_myvariant(chunk_ids)

            export(from_myvariant, collection_name, db_name)
            self.step += 1

            print 'Step: {} of {}'.format(self.step, (len(variant_list) / chunksize) + 1)

        return 'Finished!'

    @staticmethod
    def my_variant_at_once(vcf_file):
        """
        Retrives myvariant data from their web-server and return a list of documents. All done at once.
        This method is well-fitted for smaller files.

        :param vcf_file: vcf file from where HGVS IDs will be extracted
        :return: list of documents containing the joint data, can be exporter easily later on
        """
        open_file = myvariant_parsing_utils.VariantParsing()
        variant_list = open_file.get_variants_from_vcf_chunk(vcf_file)
        from_myvariant = open_file.get_dict_myvariant(variant_list)

        print 'Finished!'
        return from_myvariant
