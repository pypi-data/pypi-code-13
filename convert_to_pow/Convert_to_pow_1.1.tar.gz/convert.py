def convert(str):
	def convert_to_pow(str):
		(b1,b2)=str.split('^',1)
		if b1[-1]!=')' and b2[0]!='(':
			count=-1
			c=''
			for i in range(0,len(b1)):
				if b1[count-i]=='+' or b1[count-i]=='-' or b1[count-i]=='*' or b1[count-i]=='/' or b1[count-i]=='^' or b1[count-i]=='(' or b1[count-i]==')':
					break;
				else:
					c=b1[count-i]+c	
			d=''
			for i in range(0,len(b2)):
				if b2[i]=='+' or b2[i]=='-' or b2[i]=='*' or b2[i]=='/' or b2[i]=='^' or b2[i]=='w' or b2[i]=='(' or b2[i]==')':
					break;
				else:
					d=d+b2[i]
			b1=b1.__getslice__(0,len(b1)-len(c))
			b2=b2.__getslice__(len(d),len(b2))
			b=b1+"pow("+c+","+d+")"+b2
			return b
		if b1[-1]!=')' and b2[0]=='(':
			count=-1
			c=''
			for i in range(0,len(b1)):
				if b1[count-i]=='+' or b1[count-i]=='-' or b1[count-i]=='*' or b1[count-i]=='/' or b1[count-i]=='^' or b1[count-i]=='w' or b1[count-i]=='n':
					break;
				else:
					c=b1[count-i]+c	
			d='('
			i=1
			level=1
			while(level!=0):
				if b2[i]=='(':
					level=level+1
				if b2[i]==')':
					level=level-1
				d=d+b2[i]		
				i=i+1
			b1=b1.__getslice__(0,len(b1)-len(c))
			b2=b2.__getslice__(len(d),len(b2))
			b=b1+"pow("+c+","+d+")"+b2
			return b
		if b1[-1]==')' and b2[0]!='(':
			c=')'
			i=-2
			level=1
			while(level!=0):
				if b1[i]==')':
					level=level+1
				if b1[i]=='(':
					level=level-1
				c=b1[i]+c		
				i=i-1
			d=''
			for i in range(0,len(b2)):
				if b2[i]=='+' or b2[i]=='-' or b2[i]=='*' or b2[i]=='/' or b2[i]=='s' or b2[i]=='p' or b2[i]=='w':
					break;
				else:
					d=d+b2[i]
			b1=b1.__getslice__(0,len(b1)-len(c))
			b2=b2.__getslice__(len(d),len(b2))
			b=b1+"pow("+c+","+d+")"+b2
			return b
		if b1[-1]==')' and b2[0]=='(':
			c=')'
			count=-1
			i=-2
			level=1
			while(level!=0):
				if b1[i]==')':
					level=level+1
				if b1[i]=='(':
					level=level-1
				c=b1[i]+c		
				i=i-1
			d='('
			i=1
			level=1
			while(level!=0):
				if b2[i]=='(':
					level=level+1
				if b2[i]==')':
					level=level-1
				d=d+b2[i]		
				i=i+1
			b1=b1.__getslice__(0,len(b1)-len(c))
			b2=b2.__getslice__(len(d),len(b2))
			b=b1+"pow("+c+","+d+")"+b2
			return b
	for i in range(0, len(str)-2):
		if '^' in str:
			str=convert_to_pow(str)
	print	(str) 
