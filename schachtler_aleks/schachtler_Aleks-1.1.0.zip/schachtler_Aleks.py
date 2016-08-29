Python 3.5.2 (v3.5.2:4def2a2901a5, Jun 25 2016, 22:01:18) [MSC v.1900 32 bit (Intel)] on win32
Type "copyright", "credits" or "license()" for more information.
>>> def print_lvl(liste):
	"""Dies ist das Modul "schachtler_Aleks.py". Es stellt eine Funktion namens print_lvl(), die eine Liste mit beliebiger vielen eingebautten Lsiten ausgibt. Die Funktion selbst -> Diese Funktion erwartet ein positionelles Argument namens "liste", das eine beliebige Python-Liste (mit eventuellen eingebauten Listen) ist. Jedes Element der Liste wird (rekursiv) auf dem Bildschirm auf einer eigenen Zeile ausgegeben."""
	for element in liste:
		if isinstance(element, list):
			print_lvl(element)
		else:
			print(element)

			
>>> filme = ["Die Ritter der Kokosnuss", 1975, "Terry Jones & Terry Gilliam", 91, ["Graham Chapman", ["Michael Palin", "John Cleese", "Terry Gilliam", "Eric Idle", "Terry Jones"]]]
>>> print_lvl(filme)
Die Ritter der Kokosnuss
1975
Terry Jones & Terry Gilliam
91
Graham Chapman
Michael Palin
John Cleese
Terry Gilliam
Eric Idle
Terry Jones
>>> 

