def div_list(a=[]):
    '''多层嵌套列表的拆解'''
    for outs in a:
        if isinstance(outs,list):
            div_list(outs) #使用递归调用解决！
        else:
            print(outs)
