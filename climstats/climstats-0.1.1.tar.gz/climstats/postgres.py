from dataset import BaseVariable, Dataset, Dimension
import psycopg2


class PostgresDataset(Dataset):

	def __init__(self, name, dsn='host=localhost'):

		self.dsn = dsn
		self.conn = psycopg2.connect(dsn)

		cur = self.conn.cursor()


