#!/usr/bin/env python
Str= ['1950 0025',
'1950 0022',
'1950 0011',
'1949 0031',      
'1949 0111',
'1949 0078',
'1948 0023',
'1948 0019']
(last_key, tot_val, avg_val, ctr, cum_val) = (None, 0, 0, 0, 0)
for line in Str:
    (key, val) = line.strip().split(" ")
    if last_key and last_key != key:
       avg_val = float(cum_val/ctr)
       print(last_key, avg_val)
       (ctr, cum_val) = (1, 0)
       (last_key, tot_val) = (key, int(val))
       cum_val = cum_val + tot_val
    else:
       (last_key,tot_val) = (key,int(val))
       ctr = ctr + 1
       cum_val = cum_val + tot_val
       last_key = key
       #(last_key, tot_val) = (key, sum(int(val)))
if last_key:
   #ctr = ctr + 1
   avg_val = float(cum_val/ctr)
   print(last_key, avg_val)
