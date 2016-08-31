"""
Google BigQuery abstraction & convenience methods.

BigQuery provides a massively scaling database environment. Data tables are
organized into datasets, which exist within projects. Most analysis functions
are constrained to the dataset scope, i.e. they cannot span across datasets.

Useful classes:
    - BigQueryService  (i.e. a project)
    - Dataset
    - Table


References
https://developers.google.com/resources/api-libraries/documentation/bigquery/v2/python/latest/index.html
https://developers.google.com/resources/api-libraries/documentation/bigquery/v2/python/latest/bigquery_v2.tables.html

"""
from webapp2 import cached_property

from . import googleapi
from .util import odict

import datetime
import uuid


class BigQueryStateException(Exception):
    pass


class JobNotReady(BigQueryStateException):
    def __init__(self, job_id):
        self.job_id = job_id
        super(JobNotReady, self).__init__()


# Google notes that "standard SQL" is not ready for production use.
# https://cloud.google.com/bigquery/sql-reference/
DEFAULT_LEGACY_BIGQUERY_SQL = True
TIMESTAMP_FORMAT = '%Y-%m-%d %H:%M:%S.%fZ'


RECORD_FIELD_TYPE_CONVERT = {
    "INTEGER": int,
    "FLOAT": float,
    "BOOLEAN": (lambda v: v in ('True', 'true', 'TRUE')),
    "STRING": str,
    "TIMESTAMP": (lambda s: datetime.datetime.strptime(s, TIMESTAMP_FORMAT))
}


def named_record(page, record):
    """Compose a dictionary of each record, with valid type conversion."""
    result = {}
    for i, fielddef in enumerate(page['schema']['fields']):
        value = record['f'][i].get('v')
        converter = RECORD_FIELD_TYPE_CONVERT.get(fielddef['type'], None)
        if converter is not None:
            value = converter(value)
        result[fielddef['name']] = value
    return result






class BigQueryService(googleapi.ServiceBase):

    API_SCOPE = [
        'https://www.googleapis.com/auth/bigquery',
        'https://www.googleapis.com/auth/bigquery.insertdata',
        'https://www.googleapis.com/auth/cloud-platform'
    ]

    @property
    def projects(self):
        result = self.execute(self.connection.projects().list)
        for project in result.get('projects', []):
            yield project.get('id'), project.get('friendlyName'), \
                Project(self, project.get('id'), base=project)

    def get_project(self, project_id):
        # NB the BigQuery v2 API doesn't support a datasets().get query.
        # We therefore iterate to find the project by ID.
        for this_id, this_name, this_project in self.projects:
            if this_id == project_id:
                return this_project

        # else
        message = "Could not find a matching project (id=%r)"
        raise KeyError(message % (project_id,))

    @cached_property
    def connection(self):
        return self.discover('bigquery', 'v2')

    def query(self, project_id, query_text, timeout=10000, retries=5):
        """
        Run a query synchronously.

        Returns the result set (when it finishes...)
        """
        props = dict(
            projectId=project_id,
            body=dict(
                query=query_text,
                timeoutMs=timeout
            )
        )
        query = self.connection.jobs().query
        result = self.execute(query, retries=retries, **props)

        for record in result.get('rows', []):
            yield named_record(result, record)

    def query_async(self, project_id, query_text, batch=True, large=False,
                    retries=5):
        """
        Run a query asynchronously.

        Returns the associated job ID.
        """
        bigquery = self.connection
        job_id = str(uuid.uuid4())
        jobdata = dict(
            jobReference=dict(
                projectId=project_id,
                jobId=job_id,
                allowLargeResults=large
            ),
            configuration=dict(
                query=dict(
                    query=query_text,
                    priority=('BATCH' if batch else 'INTERACTIVE')
                )
            )
        )
        factory = bigquery.jobs().insert
        self.execute(factory, retries=retries,
                     projectId=project_id,
                     body=jobdata)
        return job_id

    def get_results(self, project_id, job_id):
        bigquery = self.connection
        factory = bigquery.jobs().get
        jobstate = self.execute(factory, projectId=project_id, jobId=job_id)

        status = jobstate.get('status', {}).get('state', None)
        if status not in ('DONE',):
            raise JobNotReady(job_id)

        results = bigquery.jobs().getQueryResults
        results = self.executor.map(results, 'rows',
                                    projectId=project_id,
                                    jobId=job_id)

        for page_id, page, row_id, record in results:
            yield named_record(page, record)


class Job(object):

    def __init__(self, service, project_id, job_id):
        self.service = service
        self.project_id = project_id
        self.job_id = job_id

    @property
    def results(self):
        return self.service.get_results(self.project_id, self.job_id)


class Project(object):
    def __init__(self, service, project_id, base=None):
        assert isinstance(service, BigQueryService)
        self.project_id = project_id
        self.service = service
        self.connection = service.connection
        self.executor = service.executor
        self.base = None  # to be used for handling native API models.

    def query(self, text, **kwargs):
        _async = kwargs.pop('async', False)
        if _async:
            job_id = self.service.query_async(self.project_id, text, **kwargs)
            return Job(self.service, self.project_id, job_id)
        else:
            return self.service.query(self.project_id, text, **kwargs)

    def get_dataset(self, dataset_id):
        query = self.connection.datasets().get
        result = self.service.execute(query,
                                      projectId=self.project_id,
                                      datasetId=dataset_id)
        return Dataset(self.service, self.project_id, dataset_id,
                       base=result)

    def dataset_exists(self, dataset_id):
        for this_id, this_name, dataset in self.datasets:
            if this_id == dataset_id:
                return True

        # else
        return False

    def create_dataset(self, dataset_id, name, **kwargs):
        request = dict(
            projectId=self.project_id,
            datasetReference=dict(
                projectId=self.project_id,
                datasetId=dataset_id
            ),
            description=kwargs.pop('description', None),
            friendlyName=name,
            defaultTableExpiration=kwargs.pop('tables_expire', None)
        )
        query = self.connection.datasets().insert
        result = self.service.execute(query,
                                      projectId=self.project_id,
                                      body=request)
        return Dataset(self.service, self.project_id, dataset_id, base=result)

    @property
    def datasets(self):
        query = self.connection.datasets().list
        datasets = self.executor.map(query, 'datasets',
                                     projectId=self.project_id)
        for page_id, page, row_id, record in datasets:
            dataset_id = record.get('datasetReference', {}).get('datasetId')
            yield dataset_id, record.get('friendlyName'), \
                Dataset(self.service, self.project_id, dataset_id)


class Dataset(Project):

    def __init__(self, service, project_id, dataset_id, base=None):
        self.dataset_id = dataset_id
        super(Dataset, self).__init__(service, project_id, base=base)

    def delete(self, all_tables=True):
        query = self.connection.datasets().delete
        request = self.service.execute(query,
                                       projectId=self.project_id,
                                       datasetId=self.dataset_id,
                                       deleteContents=all_tables)
        return request

    def __autopatch_table__(self, table_id, schema):
        if self.table_exists(table_id):
            query = self.connection.tables().patch
        else:
            query = self.connection.tables().insert
            schema.pop('tableId', None)  # not allowed when creating fresh

        result = self.service.execute(query, **schema)
        return Table(self.service, self.project_id, self.dataset_id, table_id,
                     base=result)

    def prepare_table(self, table_id, table_name, schema):
        assert isinstance(schema, dict)
        schema = Table.create_schema(self.project_id,
                                     self.dataset_id,
                                     table_id,
                                     table_name,
                                     schema)
        return self.__autopatch_table__(table_id, schema)

    def prepare_view(self, view_id, view_name, view_sql, **kwargs):
        assert isinstance(view_sql, basestring)
        base = Table.create_schema(self.project_id, self.dataset_id,
                                   view_id, view_name, view_sql, **kwargs)

        return self.__autopatch_table__(view_id, base)

    def table_exists(self, table_id):
        return table_id in list(self.table_ids_known)

    def get_table(self, table_id):
        query = self.connection.tables().get
        result = self.service.execute(query,
                                      projectId=self.project_id,
                                      datasetId=self.dataset_id,
                                      tableId=table_id)
        return Table(self.service,
                     self.project_id,
                     self.dataset_id,
                     table_id,
                     base=result)

    @property
    def table_ids_known(self):
        for record in self.tables_raw:
            yield record.get('tableReference', {}).get('tableId', None)

    @property
    def tables_raw(self):
        query = self.connection.tables().list
        tables = self.executor.map(query, 'tables',
                                   projectId=self.project_id,
                                   datasetId=self.dataset_id)
        for page_id, page, row_id, record in tables:
            yield record

    @property
    def tables(self):
        for record in self.tables_raw:
            yield record.get('id'), record.get('friendlyName'), \
                Table(self.service, self.project_id, self.dataset_id,
                      record.get('id'), base=record)

    def fetchTable(self, friendlyName):
        for id_, name, table in self.tables:
            if name == friendlyName:
                return table


class Table(Project):

    def __init__(self, service, project_id, dataset_id, table_id, base=None):
        self.dataset_id = dataset_id
        self.table_id = table_id
        super(Table, self).__init__(service, project_id, base=base)

    @classmethod
    def table_schema_base(cls, project_id, dataset_id, table_id, name):
        return odict(
            projectId=project_id,
            datasetId=dataset_id,
            tableId=table_id,
            body=dict(
                tableReference=dict(
                    projectId=project_id,
                    datasetId=dataset_id,
                    tableId=table_id,
                ),
                friendlyName=name
            )
        )

    @classmethod
    def assemble_schema_body(cls, schema):
        fieldset = []
        for fieldname, attribs in schema.items():
            fieldset.append(dict(
                name=fieldname,
                type=attribs[0],
                mode=(attribs[1] or 'NULLABLE'),
                description=(attribs[2] or fieldname)
            ))
        return dict(schema=dict(fields=fieldset))

    @classmethod
    def assemble_view_body(cls, view_sql, kwargs):
        legacy = kwargs.pop('legacy_sql', DEFAULT_LEGACY_BIGQUERY_SQL)

        udf = kwargs.pop('functions', [])
        assert isinstance(udf, list)

        # Mutate the UDF components to pseudo-typed objects.
        udf_keys = ['resourceUri', 'inlineCode']
        udf = map(lambda u: {(udf_keys[int(u.startswith('gs://'))]): u}, udf)

        return dict(
            view=dict(
                query=view_sql,
                useLegacySql=bool(legacy),
                userDefinedFunctionResources=udf
            )
        )

    @classmethod
    def create_schema(cls, project_id, dataset_id, table_id, name,
                      *args, **kwargs):
        """
        Construct the query model for creating table schemata sanely.

        Usage:
            schema = Table.create_schema(
                project_id, dataset_id, table_id,
                "My Table Friendly Name",
                dict(
                    # argument name becomes the name of the field in the table.
                    count_field=('INTEGER', 'REQUIRED', "my field counter"),
                    time_field=('TIMESTAMP', 'REQUIRED', "my timestamp"),
                    name_field=('STRING', None, None)
                )
            )

            bigquery.service.tables().insert(**schema)
        """

        schema = kwargs.pop('schema', None)
        view_sql = kwargs.pop('view_sql', None)

        if len(args):
            if isinstance(args[0], dict):
                schema = args[0]
            if isinstance(args[0], basestring):
                view_sql = args[0]

        base = cls.table_schema_base(project_id, dataset_id, table_id,
                                     name)
        if isinstance(schema, dict):
            base.body.update(cls.assemble_schema_body(schema))

        if isinstance(view_sql, basestring):
            base.body.update(cls.assemble_view_body(view_sql, kwargs))

        return base

    def coerce_record(self, record):
        result = []
        for name, val in record.items():
            if val in ('NOW',):
                val = datetime.datetime.utcnow()
            if isinstance(val, datetime.datetime):
                val = val.strftime(TIMESTAMP_FORMAT)
            result.append((name, val))
        return dict(result)

    def insert(self, *records):
        records = [self.coerce_record(r) for r in records]
        query = dict(
            projectId=self.project_id,
            datasetId=self.dataset_id,
            tableId=self.table_id,
            body=dict(
                rows=[dict(json=r) for r in records],
                insertId=str(uuid.uuid4())
            )
        )

        factory = self.connection.tabledata().insertAll
        return self.service.execute(factory, retries=5, **query)

