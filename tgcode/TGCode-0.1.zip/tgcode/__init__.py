import threading

global default_charset
default_charset = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890!@#$%&*()-_+,;:?/\|"\'[]{}<>'

global delimiter
delimiter = '='

global double_delimiter
double_delimiter = '.'

class Encoder(threading.Thread):
  def run(self):
    self.encoded = self.func(self.data)
    self.finished = True

class CorruptedData(Exception):
  pass

class TableError(Exception):
  pass

def default_make_table(charset):
  dict = {}
  n = -1
  for char in charset:
    n = n + 1
    dict[n] = char
  n = -1
  for char in charset:
    n = n + 1
    dict[char] = n
  dict['biggest'] = n
  return dict

def parser(encoded):
  for char in encoded:
    if char not in default_charset and char != delimiter:
      raise CorruptedData('Invalid encoded text.')
  terms = []
  long_list = []
  in_long_term = False
  long_term = ''
  for char in encoded:
    if in_long_term and char == delimiter:
      for each in long_term:
        long_list.append(each)
      terms.append(long_list)
      long_term = ''
      long_list = []
      in_long_term = False
      continue
    if not in_long_term and char == delimiter:
      in_long_term = True
      continue
    if in_long_term:
      long_term = long_term + char
    else:
      terms.append(char)
  if in_long_term and long_term:
    for char in long_term:
      long_list.append(char)
    terms.append(long_list)
  return terms

def decode(data, **params):
  if not isinstance(data, str):
    raise TypeError('"data" needs to be a str().')
  decoded = bytearray()
  data = data.replace(double_delimiter, delimiter+delimiter)
  if params.get('make_table'):
    make_table = params['make_table']
  else:
    make_table = default_make_table
  if params.get('charset'):
    charset = params['charset']
  else:
    charset = default_charset
  table = make_table(charset)
  terms = parser(data)
  for each in terms:
    n = 0
    if isinstance(each, str) and len(each) == 1:
      n = table[each]
      decoded.append(n)
    if isinstance(each, list):
      n = 0
      for num in each:
        n = n + table[num]
      decoded.append(n)
  return bytes(decoded)

def __switch(number):
  return number-number-number

def __slice(bytearr, parts):
  eachqnt = len(bytearr)//parts
  rest = len(bytearr)-eachqnt*parts
  slices = []
  item = bytearray()
  for each in bytearr:
    item.append(each)
    if len(item) == eachqnt:
      slices.append(item)
      item = bytearray()
  if rest != 0:
    last = len(slices)-1
    slices[last] = slices[last] + item
  return slices

def encode(data, **params):
  if not isinstance(data, bytes) and not isinstance(data, bytearray):
    raise TypeError('"data" needs to be a bytes().')
  encoded = ''
  if params.get('make_table'):
    make_table = params['make_table']
  else:
    make_table = default_make_table
  if params.get('charset'):
    charset = params['charset']
  else:
    charset = default_charset
  table = make_table(default_charset)
  for each in data:
    term = table.get(each)
    if each > table['biggest']:
      long_term = ''
      while 1:
        if each > table['biggest']:
          each = each - table['biggest']
          long_term = long_term + table[table['biggest']]
        else:
          long_term = long_term + table[each]
          break
      term = '=' + long_term + '='
    encoded = encoded + term
  return encoded.replace(delimiter+delimiter, double_delimiter)

def fast_encode(data, thread_quantity=35, func=encode):
  if not isinstance(data, bytes):
    raise TypeError('"data" needs to be a bytes().')
  thread_list = []
  data_list = __slice(data, thread_quantity)
  for l in range(thread_quantity):
    thread_list.append(Encoder())
    thread_list[l].data = data_list[l]
    thread_list[l].func = func
    thread_list[l].finished = False
    thread_list[l].start()
  while 1:
    finished = True
    for each in thread_list:
      if not each.finished:
        finished = False
        break
    if finished:
      data_encoded = ''
      for each in thread_list:
        data_encoded = data_encoded + each.encoded
      return data_encoded.replace(delimiter+delimiter, double_delimiter)