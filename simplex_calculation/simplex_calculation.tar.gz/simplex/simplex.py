"""
 The objective function and all other  constraints
 must be specified in all degree of variable unitl
 the highest one if it has no particular  variable
 then 0 must be specified as it's coefficient.
 Example z-3x1-4x2-0x3
	 1x1-1x2-0x3<=45
	 1x1+33x2+4x3<=6
"""
obj=raw_input("Enter the objective function\n")
n=int(raw_input("Enter the number of constraints\n"))
#This function is used to determine the lowest value in the objective function
def lowest_value(v):
	temp=[]
	for i in range(1,len(v)-1):
		temp.append(int(v[i]))
	temp1=min(temp)
	for i in range(0,len(temp)):
		if temp1==temp[i]:
			return i+1
def evaluate_the_simple(v,d):
	z=lowest_value(v)
	if int(v[z])>=0:
		return z
	else:
		#This is for finding the value of RHS/leastcolumn
		temp2=[]
		for i in range(0,len(d)):
			temp2.append(float(d[i][-1])/float(d[i][z]))
		#This is for finding the minimum ratio
		hope=min(temp2)
		if hope<=0:
			temp2.remove(hope)
			hope=min(temp2)
		for i in range(0, len(temp2)):
			if hope==temp2[i]:
				hope=i
		d[hope][0]="x"+str(z)	
		#Dividing the pivot row by pivot element
		m=float(d[hope][z])
		for i in range(1,len(d[hope])):
			d[hope][i]=float(d[hope][i])/m
		#hope is row and z is column	
		for i in range(0,len(d)):
			if i==hope:
				continue
			element=d[i][z]
			element=-float(element)
			for j in range(1,len(d[i])):
				d[i][j]=float(d[i][j])+float(d[hope][j])*element
		element=float(v[z])
		element=-float(element)
		for i in range(1,len(v)):
			v[i]=float(v[i])+float(d[hope][i])*element
		evaluate_the_simple(v,d) 
#The below process is carried out to create a virtual table like representation
list=[]
for i in range(0,n):
	list.append(raw_input())
d = { x:y for x,y in zip(range(0,n), list) }
m=int(obj[-1])
for i in range(1,m+1):
	obj=obj.replace('x'+str(i) , '')
b=''
for i in range(0, len(d)):
	b='s'+str(i)
	(b1,b2)=d[i].split("<=")
	m=int(b1[-1])
	for j in range(1,m+1):
		b1=b1.replace("x"+str(j), '')
	if b1[0] != '-':
		b1="+"+b1
	if b2[0] != '-':
		b2="+"+b2
	b=b+b1+b2
	d[i]=b
	b=''
obj=obj+(n+1)*"+0"
obj=obj.replace('z', 'z0')
b=''
for i in range(0, len(d)):
	b=(i)*'0'+'1'+(n-1-i)*'0'
	k=''
	for j in range(0, len(b)):
		k=k+'+'+b[j]
	c=''
	count=-1
	while(d[i][count]!='+' and d[i][count]!='-'):
		c=d[i][count]+c
		count=count-1
	c=d[i][count]+c
	count=-(count)
	d[i]=d[i].__getslice__(0,len(d[i])-count)
	d[i]=d[i]+k+c
c=''
#Virtual table completed
v=[] #Contains the objective function
for i in range(0, len(obj)):
	if obj[i]=='+' or obj[i]=='-':
		v.append(c)
		c=obj[i]
	else:
		c=c+obj[i]
v.append(c)
#This below code is used to convert the string in the form of list
for j in range(0,len(d)):
	c=''
	x=[]
	for i in range(0, len(d[j])):
		if d[j][i]=='+' or d[j][i]=='-':
			x.append(c)
			c=d[j][i]
		else:
			c=c+d[j][i]
	x.append(c)
	d[j]=x
b=evaluate_the_simple(v,d)
print "Objective Function Value"+str(v[-1])
for i in range(0,len(d)):
	print str(d[i][0])+" "+str(d[i][-1])
	
