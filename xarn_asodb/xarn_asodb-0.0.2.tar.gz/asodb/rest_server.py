import bottle
import query
import json
#import canister
import engine

app = bottle.Bottle()
#app.install(canister.Canister())


@app.route('<path:path>')
def serve(path):
    req = bottle.request
    res = query.executeHttp(req.method, req.path, req.query, req.body)
    #print(request.method)
    #print(request.path)
    #print(request.query)
    
    return res


if __name__ == "__main__":
    cards = open('../test_data/mtg_cards.json', encoding='utf-8').read()
    
    print('------------------')
    res = engine.set('/cards', None, cards)
    print('------------------')
    print(res)
    print('------------------')
    
    app.run(host='0.0.0.0', port=8080, debug=True)
