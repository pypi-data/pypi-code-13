from urllib import parse
from flask import Flask, json, request, redirect, abort

from .database import db
from .datatypes import generate_token


server = Flask('monzo-api-stub')


@server.route('/')
def root():
    state = request.args['state']
    redirect_uri = request.args['redirect_uri']
    code = generate_token()

    uri = parse.urlparse(redirect_uri)
    query = parse.parse_qsl(uri.query) + [('state', state), ('code', code)]
    uri = uri._replace(query=parse.urlencode(query))

    return redirect(parse.urlunparse(uri))


@server.route('/oauth2/token')
def oauth2_token():
    return json.dumps({
        'access_token': generate_token(),
        'client_id': request.args['client_id'],
        'expires_in': 21600,
        'refresh_token': generate_token(),
        'token_type': 'Bearer',
        'user_id': db['user'].user_id,
    })


@server.route('/ping/whoami')
def whoami():
    return json.dumps({
        'authenticated': True,
        'client_id': generate_token(),
        'user_id': db['user'].user_id,
    })


@server.route('/accounts')
def accounts():
    return json.dumps({
        'accounts': [
            {
                'id': account.account_id,
                'description': account.description,
                'created': account.created.strftime('%Y-%m-%dT%H:%M:%SZ'),
            }
            for account in db['accounts'].values()
        ]
    })


@server.route('/balance')
def balance():
    account_id = request.args['account_id']

    try:
        account = db['accounts'][account_id]
    except KeyError:
        abort(400)

    return json.dumps({
        'balance': account.balance,
        'spend_today': account.spend_today,
        'currency': account.currency,
    })


@server.route('/transaction/<transaction_id>')
def transaction(transaction_id):
    # http "https://api.monzo.com/transactions/$transaction_id" \
    # "Authorization: Bearer $access_token" \
    # # Here we are expanding the merchant \
    # "expand[]==merchant"
    # {
    #     "transaction": {
    #         "account_balance": 13013,
    #         "amount": -510,
    #         "created": "2015-08-22T12:20:18Z",
    #         "currency": "GBP",
    #         "description": "THE DE BEAUVOIR DELI C LONDON        GBR",
    #         "id": "tx_00008zIcpb1TB4yeIFXMzx",
    #         "merchant": {
    #             "address": {
    #                 "address": "98 Southgate Road",
    #                 "city": "London",
    #                 "country": "GB",
    #                 "latitude": 51.54151,
    #                 "longitude": -0.08482400000002599,
    #                 "postcode": "N1 3JD",
    #                 "region": "Greater London"
    #             },
    #             "created": "2015-08-22T12:20:18Z",
    #             "group_id": "grp_00008zIcpbBOaAr7TTP3sv",
    #             "id": "merch_00008zIcpbAKe8shBxXUtl",
    #             "logo": "https://pbs.twimg.com/profile_images/527043602623389696/68_SgUWJ.jpeg",
    #             "emoji": "🍞",
    #             "name": "The De Beauvoir Deli Co.",
    #             "category": "eating_out"
    #         },
    #         "metadata": {},
    #         "notes": "Salmon sandwich 🍞",
    #         "is_load": false,
    #         "settled": "2015-08-23T12:20:18Z"
    #     }
    # }
    pass


@server.route('/transactions')
def transactions():
    pass
