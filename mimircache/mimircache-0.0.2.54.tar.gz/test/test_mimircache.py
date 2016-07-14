

from mimircache import *


reader = csvReader('../mimircache/data/trace.csv', init_params={"header" :True, 'label_column' :4, 'delimiter' :','})

# reader = csvReader('../mimircache/data/test.dat', init_params={'label_column': 0})
# reader = plainReader('../mimircache/data/test.dat')
# c = c_cacheReader.read_one_element(reader.cReader)
# count = 1
# while(c):
#     print(c)
#     count += 1
#     c = c_cacheReader.read_one_element(reader.cReader)
# print(count)
p = cGeneralProfiler(reader, "FIFO", cache_size=2000, num_of_threads=1)
# reader = csvReader('../mimircache/data/trace.csv', init_params={"header": True, "label_column": 4})
# p = LRUProfiler(reader)

# hr = p.get_hit_rate()

# p.get_reuse_distance()
hr = p.get_hit_count()
print(hr)


# hr = p.get_hit_rate()
# hc = p.get_hit_count()
# mr = p.get_miss_rate()
