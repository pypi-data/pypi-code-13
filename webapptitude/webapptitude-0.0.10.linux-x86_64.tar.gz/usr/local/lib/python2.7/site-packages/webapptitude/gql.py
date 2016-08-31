
import webapp2

from handlers import adapt_request_params

"""
Constructs GQL queries for datastore operations, based on structures similar
to those of MongoDB. Note that GQL's logic capabilities are not as flexible
as might be expressed by humans. The compiler will attempt to build
GQL-compliant logic, rather than the full capabilities a developer might
otherwise intend.

Example: (in JSON)
    { // The following conditions will be ANDed together.
        metric_field: { '$gt': 7 },
        field_name: { "$in": [ "one", "two" ] },
        another_field: "literal_match",
    }


Numeric

"""


GQL_OPERATOR_MAP = {
    '$gt': '>',
    '$gte': '>=',
    '$lt': '<',
    '$lte': '<=',
    '$ne': '!=',
    '$eq': '=',
    '$in': 'IN',
    '$or': 'IN',
}


def construct_gql_where_parts(params, attrib=None, **kwargs):
    """Produce a series of GQL constraints for WHERE clause."""

    bindings = kwargs.pop('bindings', [])
    statements = kwargs.pop('statements', [])

    if isinstance(params, dict) and attrib is not None:
        for k, v in params.iteritems():
            if str(k) in ('OR', '$or', '$in'):
                bindings.append(v)
                statements.append('%s IN (:%d)' % (attrib, len(bindings)))
            if str(k) in GQL_OPERATOR_MAP:
                operator = GQL_OPERATOR_MAP[k]
                bindings.append(v)
                index = len(bindings)
                statements.append('%s %s :%d' % (attrib, operator, index))
    elif isinstance(params, dict):
        for k, v in params.iteritems():
            if isinstance(v, basestring):
                v = str(v)
            if isinstance(v, dict):
                construct_gql_where_parts(v, attrib=str(k),
                                          statements=statements,
                                          bindings=bindings)
            else:
                bindings.append(v)
                statements.append('%s = :%d' % (str(k), len(bindings)))

    return bindings, statements

def construct_gql_where(params):
    bindings, statements = construct_gql_where_parts(params)
    return bindings, ' AND '.join(statements)


def query(request, model):
    assert isinstance(request, webapp2.Request)
    query = dict(adapt_request_params(request))
    bindings, where = construct_gql_where(query)
    if len(bindings):
        return model.gql(("WHERE %s" % where), *bindings)
    else:
        return model.query()
