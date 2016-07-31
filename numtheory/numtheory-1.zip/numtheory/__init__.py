def reverse(num, base=10) :
	rev = 0
	while num :
		rev = rev * base + num % base
		num //= base
	return rev

def is_palindromic(num, base=10) :
	return num == reverse(num, base)