'''
Author: Kazaryan Sargis
Автор: Казарян Саргис Артурович

Description: This module contains 12 functions:
	engrus # layout from English into Russian
	ruseng # layout from Russian into English
	ameng # layout from Armenian to English
	engam # layout from English into Armenian
	amrus # layout from Armenian into Russian
	rusam # layout from Russian into Armenian
	The above - Returns the change, the incoming text in a different language keyboard layout, for example engrus - from English into Russian
The following return transcription incoming text, symbols of another language, such as engrust - from English into Russian
	engrust # Transcription from English into Russian
	rusengt # transcription from Russian into English
	amengt # transcription from Armenian to English
	engamt # Transcription from English into Armenian
	amrust # transcription from Armenian into Russian
	rusamt # transcription from Russian into Armenian
Описание: Данный модуль содержит 12 функций:
	engrus #раскладка с английского на русский
	ruseng #раскладка с русского на английский
	ameng #раскладка с армянского на английский
	engam #раскладка с английского на армянский
	amrus #раскладка с армянского на русский
	rusam #раскладка с русского на армянский
Вышеперечисленные - возвращают измененный, входящий текст в раскладке клавиатуры другого языка, например engrus - с английского на русский 
Нижеперечисленные возвращают транскрипцию входящего текста, символами другого языка, например engrust - с английского на русский 
	engrust #транскрипция с английского на русский
	rusengt #транскрипция с русского на английский
	amengt #транскрипция с армянского на английский
	engamt #транскрипция с английского на армянский
	amrust #транскрипция с армянского на русский
	rusamt #транскрипция с русского на армянский

	
Примеры: 

import keyw
keyw.engrus('ghbdtn vbh')
>>>привет мир

keyw.engrust('hello world')
>>>ХЕЛЛО ВОРЛД

Examples:

import keyw
keyw.ruseng('руддщ цщкдв')
>>>hello world
keyw.rusengt('Привет мир')
>>>privet mir

E-mail: basandbuddy@mail.ru
WWW: http://onepersonblog.ru/api/keyw
'''


sl1=[['ё','`'],['Ё','~'],['"','@'],['№','#'],[';','$'],[',','^'],['?','&'],['й','q'],['Й','Q'],['ц','w'],['Ц','W'],['У','E'],['у','e'],['К','R'],['к','r'],['Е','T'],['е','t'],['Н','Y'],['н','y'],['Г','U'],['г','u'],['Ш','I'],['ш','i'],['Щ','O'],['щ','o'],['З','P'],['з','p'],['Х','{'],['х','['],['ъ','}'],['Ъ','}'],['/','|'],['/','\\'],['Ф','A'],['ф','a'],['Ы','S'],['ы','s'],['В','D'],['в','d'],['А','F'],['а','f'],['П','G'],['п','g'],['Р','H'],['р','h'],['О','J'],['о','j'],['Л','K'],['л','k'],['Д','L'],['д','l'],['Ж',','],['ж',';'],['Э','"'],['э','\''],['Я','Z'],['я','z'],['Ч','X'],['ч','x'],['С','C'],['с','c'],['М','V'],['м','v'],['И','B'],['и','b'],['Т','N'],['т','n'],['Ь','M'],['ь','m'],['Б','<'],['б',','],['Ю','>'],['ю','.'],['.','?'],[',','/']]
sl2=[['՝', '`' ], ['՜', '~'], ['Ձ', '@' ], ['ձ', '2'], ['յ', '3'], ['Ձ', '#'], ['օ', '0'], ['Օ', ')' ], ['ռ', '-'],	 ['Ռ', '_'], ['ժ', '=' ], ['Ժ', '+' ],	 ['Խ', 'q' ], ['խ', 'Q' ], ['ւ', 'w' ], ['Ւ', 'W' ], ['Է', 'E' ], ['է', 'e' ], ['Ր', 'R' ], ['ր', 'r' ], ['Տ', 'T' ], ['տ', 't' ], ['Ե', 'Y' ], ['ե', 'y' ], ['Ը', 'U'], ['ը', 'u'], ['Ի', 'I'], ['ի', 'i' ], ['Ո', 'O'], ['ո', 'o' ], ['Պ', 'P' ], ['պ', 'p' ], ['Չ', '{'], ['չ', '['], ['Ջ', '}'], ['ջ', ']' ], ['՞', '|' ], ['\'', '\\' ], ['Ա', 'A' ], ['ա', 'a' ], ['Ս', 'S'], ['ս', 's'], ['Դ', 'D' ], ['դ', 'd' ], ['Ֆ', 'F'], ['ֆ', 'f'], ['Ք', 'G' ], ['ք', 'g' ], ['Հ' 'H' ], ['հ', 'h' ], ['Ճ', 'J'], ['ճ', 'j'], ['Կ', 'K'], ['կ', 'k'], [ 'Լ', 'L' ], ['լ', 'l' ], ['Թ', ':' ], ['թ', ';' ], ['Փ','"'], ['փ',"'" ], ['Զ','Z'], ['զ','z'], ['Ց','X'], ['ց','x'], ['Գ', 'C' ], ['գ','c'], ['Վ','V'], ['վ','v' ], ['Բ', 'B' ], ['բ','b' ], ['Ն', 'N' ], ['ն','n' ], ['Մ', 'M' ], ['մ','m' ], ['Շ','<' ], ['շ', ',' ], ['Ղ','>' ], ['ղ','.'], ['Ծ','?' ], ['ծ', '/']]  
sl3=[['ё','yo'],['Ё','Yo'],['№','#'],['Й','Y'],['й','y'],['ц','c'],['Ц','C'],['У','U'],['у','u'],['К','Q'],['к','q'],['К','K'],['к','k'],['Н','N'],['н','n'],['Г','G'],['г','g'],['Ш','Sh'],['ш','sh'],['Щ','Sch'],['щ','sch'],['З','Z'],['з','z'],['Х','H'],['х','h'],['ъ',''],['Ъ',''],['Ф','F'],['ф','f'],['Ы','Y'],['ы','y'],['Я','Ya'],['я','ya'],['В','W'],['в','w'],['В','V'],['в','v'],['А','A'],['а','a'],['П','P'],['п','p'],['Р','R'],['р','r'],['О','O'],['о','o'],['Л','L'],['л','l'],['Д','D'],['д','d'],['Ж','Zh'],['ж','zh'],['Э','E'],['э','e'],['Ч','Ch'],['ч','ch'],['С','S'],['с','s'],['М','M'],['м','m'],['И','I'],['и','i'],['Т','T'],['т','t'],['Ь',''],['ь',''],['Б','B'],['б','b'],['Ю','Yu'],['ю','yu'],['Е','E'],['е','e'],['Кс','X'],['кс','x'],['Дж','j'],['дж','j']]
sl4=[['Ձ', 'Dz' ], ['ձ', 'dz'], ['յ', 'j'], ['Ձ', 'J'], ['օ', 'o'], ['Օ', 'O' ], ['ռ', 'r'],	 ['Ռ', 'R'], ['ժ', 'Zh' ], ['Ժ', 'zh' ],	 ['Խ', 'H' ], ['խ', 'h' ],  ['Է', 'E' ], ['է', 'e' ], ['Ր', 'R' ], ['ր', 'r' ], ['Տ', 'T' ], ['տ', 't' ], ['Ե', 'Y' ], ['ե', 'y' ], ['Ը', 'U'], ['ը', 'u'], ['Ի', 'I'], ['ի', 'i' ], ['Ո', 'O'], ['ո', 'o' ], ['Պ', 'P' ], ['պ', 'p' ], ['Չ', 'Ch'], ['չ', 'ch'], ['Ջ', 'J'], ['ջ', 'j' ],  ['Ա', 'A' ], ['ա', 'a' ], ['Ս', 'S'], ['ս', 's'], ['Դ', 'D' ], ['դ', 'd' ], ['Ֆ', 'F'], ['ֆ', 'f'], ['Ք', 'Q' ], ['ք', 'q' ], ['Հ' 'H' ], ['հ', 'h' ], ['Ճ', 'Tch'], ['ճ', 'Tch'], ['Կ', 'K'], ['կ', 'k'], [ 'Լ', 'L' ], ['լ', 'l' ], ['Թ', 'T' ], ['թ', 't' ], ['Փ','P'], ['փ',"p" ], ['Զ','Z'], ['զ','z'], ['Ց','C'], ['ց','c'], ['Գ', 'G' ], ['գ','g'], ['Վ','V'], ['վ','v' ], ['Բ', 'B' ], ['բ','b' ], ['Ն', 'N' ], ['ն','n' ], ['Մ', 'M' ], ['մ','m' ], ['Շ','Sh' ], ['շ', 'sh' ], ['Ղ','Gh' ], ['ղ','gh'], ['Ծ','Tz' ], ['ծ', 'tz'],['ու', 'u' ], ['ՈՒ', 'U' ],['Ու', 'U' ],['վ', 'w' ], ['Վ', 'W' ],['կս', 'x' ], ['Կս', 'X' ]]    

sl5=[['J', 'ДЖ'],  ['X', 'КС'],  ['B', 'Б'], ['T', 'Т'], ['T', 'Т'], ['I', 'АЙ'], ['M', 'М'], ['S', 'С'], ['E', 'Э'], ['D', 'Д'], ['L', 'Л'],  ['O', 'О'], ['R', 'Р'],  ['P', 'П'], ['A', 'А'],  ['V', 'В'], ['W', 'В'],  ['Y', 'Ы'], ['F', 'Ф'], ['', 'Ъ'], ['H', 'Х'],  ['Z', 'З'], ['G', 'Г'],  ['N', 'Н'], ['K', 'К'], ['Q', 'К'], ['U', 'У'],  ['C', 'Ц'], ['Y', 'Й'],  ['YA', 'Я'], ['CK', 'К'],  ['KN', 'Н'],['GH', 'К'],  ['TH', 'Д'], ['WH', 'В'],  ['YA', 'Я'], ['SH', 'Ш'],  ['CH', 'Ч'], ['YU', 'Ю'],  ['E', 'Е'], ['MY', 'МАЙ'], ['EE', 'И'], ['EA', 'И'],  ['OU', 'АУ'], ['CA', 'КА'],  ['OO', 'У'], ['JH', 'ДЖ'],  ['YO', 'Ё'],  ['ZH', 'Ж'],['WR','Р'],['GHT','Т']]
sl6=[['J', 'Ջ'],  ['X', 'ԿՍ'],  ['B', 'Բ'], ['T', 'Տ'],  ['I', 'Ի'], ['M', 'Մ'], ['S', 'Ս'], ['E', 'Ե'], ['D', 'Դ'], ['L', 'Լ'],  ['O', 'O'], ['R', 'Ր'],  ['P', 'Պ'], ['A', 'Ա'],  ['V', 'Վ'], ['W', 'Վ'],  ['Y', 'Ձ'], ['F', 'Ֆ'], ['', 'Ъ'], ['H', 'Հ'],  ['Z', 'Զ'], ['G', 'Գ'],  ['N', 'Ն'], ['K', 'Կ'], ['Q', 'Կ'], ['U', 'ՈՒ'],  ['C', 'Ց'], ['Y', 'Ձ'],  ['YA', 'ՁԱ'], ['CK', 'Կ'],  ['KN', 'Ն'],['GH', 'Ղ'],  ['TH', 'Դ'], ['WH', 'Վ'],  ['SH', 'Շ'],  ['CH', 'Չ'], ['YU', 'ՁՈՒ'],   ['MY', 'ՄԱՁ'], ['EE', 'Ի'], ['EA', 'Ի'],  ['OU', 'ԱՈՒ'], ['CA', 'ԿԱ'],  ['OO', 'ՈՒ'], ['JH', 'Ջ'],    ['ZH', 'ժ'],['WR','Ր'],['GHT','Տ'],['DZ','Ձ'],['TZ','Ծ']]
sl7=[['Ձ', 'Дз' ], ['ձ', 'дз'], ['յ', 'й'], ['Ձ', 'Й'], ['օ', 'о'], ['Օ', 'О' ], ['ռ', 'р'],	 ['Ռ', 'Р'], ['ժ', 'Ж' ], ['Ժ', 'Ж' ],	 ['Խ', 'х' ], ['խ', 'Х' ],  ['Է', 'Э' ], ['է', 'э' ], ['Ր', 'Р' ], ['ր', 'р' ], ['Տ', 'Т' ], ['տ', 'т' ], ['Ե', 'Е' ], ['ե', 'е' ], ['Ը', 'Ы'], ['ը', 'ы'], ['Ի', 'И'], ['ի', 'и' ], ['Ո', 'О'], ['ո', 'о' ], ['Պ', 'П' ], ['պ', 'п' ], ['Չ', 'Ч'], ['չ', 'ч'], ['Ջ', 'Дж'], ['ջ', 'дж' ],  ['Ա', 'А' ], ['ա', 'а' ], ['Ս', 'С'], ['ս', 'с'], ['Դ', 'Д' ], ['դ', 'д' ], ['Ֆ', 'Ф'], ['ֆ', 'ф'], ['Ք', 'К' ], ['ք', 'к' ], ['Հ' 'Х' ], ['Հ', 'Х' ], ['Ճ', 'Тч'], ['ճ', 'тч'], ['Կ', 'К'], ['կ', 'к'], [ 'Լ', 'Л' ], ['լ', 'л' ], ['Թ', 'Т' ], ['թ', 'т' ], ['Փ','П'], ['փ',"п" ], ['Զ','З'], ['զ','з'], ['Ց','Ц'], ['ց','ц'], ['Գ', 'Г' ], ['գ','г'], ['Վ','В'], ['վ','в' ], ['Բ', 'Б' ], ['բ','б' ], ['Ն', 'Н' ], ['ն','н' ], ['Մ', 'М' ], ['մ','м' ], ['Շ','Ш' ], ['շ', 'ш' ], ['Ղ','Х' ], ['ղ','х'], ['Ծ','Тз' ], ['ծ', 'тз'],['ու', 'у' ], ['ՈՒ', 'У' ],['Ու', 'у' ],['ՁԱ','Я'],['ՁՈՒ','Ю']]    


def engrus(stroka):
	i=0;
	j=0;
	nsl=[]
	newstring='';
	newchar=''
	while i<len(stroka):
		j=0
		newchar=''
		while j<len(sl1):
			
			if sl1[j].count(stroka[i])>0:
				if sl1[j].index(stroka[i])==1:
					newchar=sl1[j][0]	
			j=j+1
		if newchar=='':
			newchar=stroka[i]
		newstring=newstring+newchar;
		i=i+1;
	return newstring
def ruseng(stroka):
	i=0;
	j=0;
	nsl=[]
	newstring='';
	newchar=''
	while i<len(stroka):
		j=0
		newchar=''
		while j<len(sl1):
			
			if sl1[j].count(stroka[i])>0:
				if sl1[j].index(stroka[i])==0:
					newchar=sl1[j][1]	
			j=j+1
		if newchar=='':
			newchar=stroka[i]
		newstring=newstring+newchar;
		i=i+1;
	return newstring
def ameng(stroka):
	i=0;
	j=0;
	nsl=[]
	newstring='';
	newchar=''
	while i<len(stroka):
		j=0
		newchar=''
		while j<len(sl2):
			
			if sl2[j].count(stroka[i])>0:
				if sl2[j].index(stroka[i])==0:
					newchar=sl2[j][1]	
			j=j+1
		if newchar=='':
			newchar=stroka[i]
		newstring=newstring+newchar;
		i=i+1;
	return newstring
def engam(stroka):
	i=0;
	j=0;
	nsl=[]
	newstring='';
	newchar=''
	while i<len(stroka):
		j=0
		newchar=''
		while j<len(sl2):
			
			if sl2[j].count(stroka[i])>0:
				if sl2[j].index(stroka[i])==1:
					newchar=sl2[j][0]	
			j=j+1
		if newchar=='':
			newchar=stroka[i]
		newstring=newstring+newchar;
		i=i+1;
	return newstring

def rusam(stroka):
	stroka1=ruseng(stroka)
	stroka1=engam(stroka1)
	return stroka1
def amrus(stroka):
	stroka1=ameng(stroka)
	stroka1=engrus(stroka1)
	return stroka1
	
def engrust(stroka):
	i=0;
	j=0;
	nsl=[]
	newstring='';
	newchar=''
	stroka=stroka.upper()
	while i<len(stroka):
		j=0
		newchar=''
		while j<len(sl5):
			if i+1<len(stroka):
				if sl5[j].count(stroka[i]+stroka[i+1])>0:
					if sl5[j].index(stroka[i]+stroka[i+1])==0:
						newchar=sl5[j][1]	
						i=i+1
				else:
					if sl5[j].count(stroka[i])>0:
						if sl5[j].index(stroka[i])==0:
							newchar=sl5[j][1]
			else:
				if sl5[j].count(stroka[i])>0:
					if sl5[j].index(stroka[i])==0:
						newchar=sl5[j][1]				
			j=j+1
		if newchar=='':
			newchar=stroka[i]
		newstring=newstring+newchar;
		i=i+1;
	return newstring
def rusengt(stroka):
	i=0;
	j=0;
	nsl=[]
	newstring='';
	newchar=''
	while i<len(stroka):
		j=0
		newchar=''
		while j<len(sl3):
			
			if sl3[j].count(stroka[i])>0:
				if sl3[j].index(stroka[i])==0:
					newchar=sl3[j][1]	
			j=j+1
		if newchar=='':
			newchar=stroka[i]
		newstring=newstring+newchar;
		i=i+1;
	return newstring
def amengt(stroka):
	i=0;
	j=0;
	nsl=[]
	newstring='';
	newchar=''
	stroka=stroka.upper()
	while i<len(stroka):
		j=0
		newchar=''
		while j<len(sl4):
			if i+1<len(stroka):
				if sl4[j].count(stroka[i]+stroka[i+1])>0:
					if sl4[j].index(stroka[i]+stroka[i+1])==0:
						newchar=sl4[j][1]	
						i=i+1
				else:
					if sl4[j].count(stroka[i])>0:
						if sl4[j].index(stroka[i])==0:
							newchar=sl4[j][1]
			else:
				if sl4[j].count(stroka[i])>0:
					if sl4[j].index(stroka[i])==0:
						newchar=sl4[j][1]				
			j=j+1
		if newchar=='':
			newchar=stroka[i]
		newstring=newstring+newchar;
		i=i+1;
	return newstring
def engamt(stroka):
	i=0;
	j=0;
	nsl=[]
	newstring='';
	newchar=''
	stroka=stroka.upper()
	while i<len(stroka):
		j=0
		newchar=''
		while j<len(sl6):
			if i+1<len(stroka):
				if sl6[j].count(stroka[i]+stroka[i+1])>0:
					if sl6[j].index(stroka[i]+stroka[i+1])==0:
						newchar=sl6[j][1]	
						i=i+1
				else:
					if sl6[j].count(stroka[i])>0:
						if sl6[j].index(stroka[i])==0:
							newchar=sl6[j][1]
			else:
				if sl6[j].count(stroka[i])>0:
					if sl6[j].index(stroka[i])==0:
						newchar=sl6[j][1]				
			j=j+1
		if newchar=='':
			newchar=stroka[i]
		newstring=newstring+newchar;
		i=i+1;
	return newstring
def rusamt(stroka):
	stroka1=rusengt(stroka)
	stroka1=engamt(stroka1)
	return stroka1
def amrust(stroka):
	i=0;
	j=0;
	nsl=[]
	newstring='';
	newchar=''
	stroka=stroka.upper()
	while i<len(stroka):
		j=0
		newchar=''
		while j<len(sl7):
			if i+1<len(stroka):
				if sl7[j].count(stroka[i]+stroka[i+1])>0:
					if sl7[j].index(stroka[i]+stroka[i+1])==0:
						newchar=sl7[j][1]	
						i=i+1
				else:
					if sl7[j].count(stroka[i])>0:
						if sl7[j].index(stroka[i])==0:
							newchar=sl7[j][1]
			else:
				if sl7[j].count(stroka[i])>0:
					if sl7[j].index(stroka[i])==0:
						newchar=sl7[j][1]				
			j=j+1
		if newchar=='':
			newchar=stroka[i]
		newstring=newstring+newchar;
		i=i+1;
	return newstring
