from stampery import Stampery

client = Stampery('2d4cdee7-38b0-4a66-da87-c1ab05b43768', 'prod')

def on_ready():
    digest = client.hash("Hello, blockchain!")
    client.stamp(digest)

def on_proof(hash, proof):
    print("Received proof for")
    print(hash)
    print("Proof")
    print(proof)

def on_error(err):
    print("Woot: %s" % err)

client.on("error", on_error)
client.on("proof", on_proof)
client.on("ready", on_ready)

client.start()
