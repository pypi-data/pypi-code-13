# -*- coding: utf-8 -*-

def print_lol(the_list, indent=False, level=0):	# indent=false, level=0, 리스트 반복 출력 함수 print_lol 정의

	for each_item in the_list:	# each_item 값을 the_list 에 들어있는 개수만큼 반복
		if isinstance(each_item, list):	# each_item 이 리스트가 맞는지 확인 # 
			print_lol(each_item, indent, level+1)	# indent=true 맞으면 each_item 값이 다시 리스트가 맞는지 반복
													# 리스트 묶음이 출력되면 level에 값을 1씩 증가
		else:
			if indent:
				for tab_stop in range(level):	# 아니라면 level 인자값만큼 tap_stop 을 반복하고
					print("\t", end="")	# \t로 level에 들어온 숫자만큼 탭을 프린트
			print(each_item) # each_item 이 리스트가 아니면 해당 값을 프린트


