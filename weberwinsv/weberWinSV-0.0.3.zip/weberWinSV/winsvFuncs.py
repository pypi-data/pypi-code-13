#!/usr/local/bin/python
# -*- coding:utf-8 -*-
"""
    2016/7/20  WeiYanfeng
    提供了 WinSV 需要一些公共函数。

-------- 依赖包
pip install psutil
pip install import_file

"""

import sys
from weberFuncs import PrintTimeMsg, PrettyPrintStr


def ReadTailLines(sFileName, iNum=5):
    # 读取文件尾部几行
    import linecache
    linecache.checkcache(sFileName)
    lsText = linecache.getlines(sFileName)[-iNum:]
    linecache.clearcache()
    return lsText

def TerminateByPid(pid):
    # 根据 pid 结束进程
    import psutil
    # process = psutil.Popen('TASKKILL /PID '+str(pid)+' /F')
    # process = os.popen('TASKKILL /PID '+str(pid)+' /F')
    # PrintTimeMsg("TerminateByPid.terminate(%s)=%s=" % (pid,str(process)))
    # return
    p = psutil.Process(pid)
    sCmd = p.cmdline()
    ret = p.terminate()
    # PrintTimeMsg("TerminateByPid.terminate(%s)=%s=" % (pid,ret))
    ret = p.wait(timeout=3)
    # PrintTimeMsg("TerminateByPid.wait(%s)=%s=" % (pid,ret))
    PrintTimeMsg("TerminateByPid(pid=%s)=(%s)" % (pid,sCmd))

def ImportPythonClassOrVar(sPythonFileName, sClassOrVar):
    # 从python源码文件动态import
    try:
        from import_file import import_file
        imp = import_file(sPythonFileName)
        return getattr(imp,sClassOrVar)
    except Exception, e:
        import traceback
        traceback.print_exc()
        PrintTimeMsg('ImportPythonClassOrVar.Exception.e=(%s)' % (str(e)))

def LoadWinSVConfigFmDict(dictConfigByGroupId, sLongIdStr):
    # 从 dictConfigByGroupId 加载WinSV配置参数到列表
    #   sLongIdStr 英文逗号分隔的<groupId.programId>
    #   单项中，若 programId 不存在，则包含整个程序组
    # 正常返回 命令行程序配置参数列表，出错返回空列表
    lsReturn = []
    for sId in sLongIdStr.split(','):
        if sId=='': continue
        groupId,cSep,programId = sId.partition('.')
        if groupId=='': #
            PrintTimeMsg("LoadWinSVConfigFmDict.sLongIdStr=(%s)Error!" % (sLongIdStr))
            return []
        else:
            dictGroup = dictConfigByGroupId.get(groupId,{})
            if dictGroup:
                def getDictFmGrp(programId):
                    dictProgram = dictGroup.get(programId,{})
                    dictParam = {}
                    dictParam['groupId'] = groupId
                    dictParam['programId'] = programId
                    dictParam['cmdExec'] = dictProgram.get('cmdExec','')
                    dictParam['cmdTitle'] = dictProgram.get('cmdTitle','')
                    dictParam['shellPopen'] = dictProgram.get('shellPopen',False)
                    def getParamFmGrp(sKey):
                        sValue = dictProgram.get(sKey,'')
                        if sValue=='':  sValue = dictGroup.get(sKey,'')
                        return sValue
                    dictParam['workDir'] = getParamFmGrp('workDir')
                    dictParam['logDir'] = getParamFmGrp('logDir')
                    err2out = getParamFmGrp('err2out')
                    if err2out=='':  err2out = False
                    dictParam['err2out'] = err2out
                    return dictParam
                if programId!='':
                    lsReturn.append(getDictFmGrp(programId))
                else:
                    for k,v in dictGroup.items():
                        if type(v)==dict:
                            lsReturn.append(getDictFmGrp(k))
    return lsReturn

def LoadWinSVConfigFmFile(sPythonFileName, sDictVarName, sLongIdStr):
    # 从指定 Python 源码文件中加载WinSV配置
    dictConfigByGroupId = ImportPythonClassOrVar(sPythonFileName, sDictVarName)
    return LoadWinSVConfigFmDict(dictConfigByGroupId, sLongIdStr)

#--------------------------------------
def testMain():
    print LoadWinSVConfigFmFile('demoSettingsWinSV.py','gDictConfigByGroupId',
                          'groupExample.programQQ,groupExample.programJC,')
    return
    # from demoSettingsWinSV import gDictConfigByGroupId
    from import_file import import_file
    # gDictConfigByGroupId= ImportModuleClass('demoSettingsWinSV','gDictConfigByGroupId')
    imp = import_file('demoSettingsWinSV.py')
    print dir(imp)
    gDictConfigByGroupId = getattr(imp,'gDictConfigByGroupId')
    print gDictConfigByGroupId
    print PrettyPrintStr(LoadWinSVConfigFmDict(gDictConfigByGroupId, 'groupExample.programQQ,groupExample.programJC,'))
    pass

#--------------------------------------
if __name__=='__main__':
    testMain()
