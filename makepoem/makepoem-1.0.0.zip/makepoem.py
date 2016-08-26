import random
a=input("아무말이나 입력하세요")
s = a.split()
print(s)
b = len(s)
print(b)
c = 0
while c<=b:
	r = random.randint(0, b-1)	
	c = c+1
	print(s[r])

	
