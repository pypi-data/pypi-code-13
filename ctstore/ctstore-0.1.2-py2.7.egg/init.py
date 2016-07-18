import os

jsc = os.path.join("js", "core")

dirs = [jsc]

copies = {
	".": ["model.py"],
	"css": ["custom.css"],
	"html": ["index.html"]
}
copies[jsc] = ["config.js", "data.js"]

syms = {
	"js": ["pay.js", "results.js", "store.js"],
	"css": ["store.css"],
	"html": ["results.html", "checkout.html"]
}
syms[jsc] = ["cart.js", "search.js", "util.js"]