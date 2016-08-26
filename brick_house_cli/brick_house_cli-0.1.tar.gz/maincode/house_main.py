

houseSq = House(10, 10, 3)
houseSq.win_door(1, 2, 1.5, 2.5)
kladka = 1.5
houseSq.squareForBricks(kladka)
print('Площадь дома = ', houseSq.square)
print('Площадь одного кирпича = %2.2f'%(houseSq.brSq.br.square))
print('Количество кирпичей при кладке '+ str(kladka) + ' = %5.1f'%(houseSq.brickQty))
