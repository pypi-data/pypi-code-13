import hjson

x = hjson.dumps(['foo', {'bar': ('baz', None, 1.0, 2)}])

print hjson.loads('-')

print hjson.loads('[200,200]')


val = 200
val = {val: 'value'}
print hjson.dumps(val)
print hjson.loads(hjson.dumps(val))


a = hjson.loads("""

{
  name: "hjson"
  description: JSON for Humans, allows comments and is less error prone.
  main: "./lib/hjson.js",
  #hugo

  author: "Christian Zangl",
  // test
  /*

  "version2": "1.2.0",
  */
  "version": "1.2.0",
  "tags": [
    "json"
    "hjson",
  ]

  haiku:
    '''
    JSON I love you.
    But strangled is my data.
    This, so much better.'''
  a: 5

}
""")

print hjson.dumps(a)