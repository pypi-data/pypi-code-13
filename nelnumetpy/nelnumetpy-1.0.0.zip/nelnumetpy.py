"""
Module nelnumetpy provides various numerical methods implemented in Python.
It doesn't intend to be an alternative to numpy or to any other professional
implementation of numerical methods either.  It's just an implementation for
study and for fun.  Enjoy!
"""


def raizquadrada(numero,erro):
    """
    This function calculates the square root of a number.
"""
    if numero < 0:
        print("Este número não tem raiz quadrada real")
    else:
       if numero > 1:
           chute=numero/2
       else:
            chute = numero*2
       raiz=chute
       erroc=erro+1
       while erroc > erro:
            raiz = (raiz+numero/raiz)/2
            erroc = abs(raiz**2-numero)

    print(raiz)

