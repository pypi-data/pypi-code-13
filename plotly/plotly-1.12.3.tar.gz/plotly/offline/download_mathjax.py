import urllib2
cdn_url = 'https://cdn.mathjax.org/mathjax/latest/MathJax.js?config=TeX-AMS-MML_SVG'
response = urllib2.urlopen(cdn_url)
html = response.read()
f = open('./MathJax.js', 'w')
f.write(html)
f.close()
