from strupy import units as u

#!
'''
##*Obliczenie zbrojenia w przekroju zginanym prostokatnym*

>*(metoda maksymalnie uproszczona)*
'''

#! ###1.Wymiary przekroju
h = 1200 *   u.mm #<< - wysokosc przekoju
b = 400 * u.mm #<< - szerokosc przekroju

#! ###2.Obciazenie
Msd = 1200    *        u.kNm #<< - moment obliczeniowy

#! ###3.Material
materials = [300 * u.MPa, 400 * u.MPa, 500 * u.MPa]
fyd = materials[1] #<< - stal zbrojeniowa

#! ---

#%img PrzekZginany_fig_1.png

#! Ze wzoru:

As1 = Msd / (0.8 * h) * 1 / fyd #%tex


#! otrzymujemy wynik:

As1 = As1.asUnit(u.cm2) 
As1 #! - potrzebna powierzchnia zbrojenia

#!
'''
---
###Podsumowanie
Dla przekroju o wymiarach %(b)s x %(h)s (bxh) i obciazeniniu %(Msd)s 
potrzebne zbrojenie dolem %(As1)s
'''












