import os
import pickle
with open("jan.txt") as jan:
    JAN = jan.readline()
    Jan = JAN.strip().split(",")
with open("jul.txt") as jul:
    JUL = jul.readline()
    Jul = JUL.strip().split(',')
with open("mik.txt") as mik:
    MIK = mik.readline()
    Mik = MIK.strip().split(',')
with open("sar.txt") as sar:
    SAR = sar.readline()
    Sar = SAR.strip().split(',')
print(Jan)
print(Jul)
print(Mik)
print(Sar)
print(sorted(Jan))
print(sorted(Jul))
print(sorted(Mik))
print(sorted(Sar))
