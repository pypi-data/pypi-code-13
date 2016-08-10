import os

jss = os.path.join("js", "store")

dirs = [jss]

copies = {
	".": ["model.py"],
	"css": ["custom.css"],
	"html": ["index.html"]
}
copies[jss] = ["config.js", "data.js"]

syms = {
	"js": ["store.js"],
	"css": ["store.css", "layouts"],
	"html": ["results.html", "checkout.html"]
}
syms[jss] = ["core.js", "core", "pages"]
#syms[jss] = ["pay.js", "results.js", "home.js"]
#syms[jsc] = ["cart.js", "search.js", "util.js"]

requires = ["ctuser"]