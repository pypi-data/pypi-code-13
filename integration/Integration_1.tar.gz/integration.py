def integration(a,b,expr):
	a=float(a)
	b=float(b)
	expr=expr.replace('^', '**')
	h=(b-a)/6
	c=[]
	d=[]
	for b in range(0,7):
		c.append(a)
		a=a+h
	
	for b in range(0,7):
		c[b]=str(c[b])
		d.append(expr.replace("x", c[b]))
	
	for b in range(0,7):
		c[b]=eval(d[b])
	
	ans=(3*h)/10
	ans=ans*(c[0]+5*c[1]+c[2]+6*c[3]+c[4]+5*c[5]+c[6])
	print( ans )
