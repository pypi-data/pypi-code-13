#!/usr/local/bin/python
# -*- coding:utf-8 -*-
"""
    2016/8/5  WeiYanfeng
    基于串列表的命名管道（借助 socket 实现）客户端。

"""

import sys
import os
import socket
from weberFuncs import GetCurrentTime,PrintTimeMsg,PrintAndSleep
from CSockReadWrite import CSockReadWrite

#--------------------------------------
class TCmdPipeClient:
    def __init__(self, sServerIPPort):

        self.sServerIP = '127.0.0.1'
        self.iServerPort = 8888
        lsServer = sServerIPPort.split(':')
        if len(lsServer)>=2:
            if lsServer[0]: self.sServerIP = lsServer[0]
            self.iServerPort = int(lsServer[1])
        self.sServerIPPort = '%s:%s' % (self.sServerIP,self.iServerPort)

        self.clientsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        self.sockRW = None

        self.ConnectToServer()

    def __del__(self):
        pass

    def ConnectToServer(self):
        self.clientsocket.connect((self.sServerIP,self.iServerPort))
        self.sockRW = CSockReadWrite(self.clientsocket,'C')
        self.sockRW.SetObjIPPort(self.sServerIPPort)
        PrintTimeMsg("ConnectToServer(%s).pid=(%s)" % (self.sServerIPPort,os.getpid()))

    def CloseSocket(self):
        self.sockRW.sock.close()
        PrintTimeMsg("CloseSocket(%s).pid=(%s)" % (self.sServerIPPort,os.getpid()))
        self.sockRW = None

    def SendPipeRequest(self, CmdStr):
        if self.sockRW==None:
            self.ConnectToServer()
        dwCmdId = 1225
        bResult = self.sockRW.WriteCmdStrToLink(dwCmdId,CmdStr)
        if not bResult:
            self.CloseSocket()
        return bResult

def testTCmdPipeClient():
    c = TCmdPipeClient('127.0.0.1:8805')
    iCnt = 0
    while iCnt<5:
        bRet = c.SendPipeRequest(['Test','One','2','three','iCnt=%d' % iCnt])
        if not bRet:
            PrintTimeMsg("testTCmdPipeClient.SendPipeRequest.Error.iCnt=%d" % (iCnt))
            break
        PrintAndSleep(6,'testTCmdPipeClient.iCnt=%d' % iCnt)
        iCnt += 1

#--------------------------------------
if __name__ == '__main__':
    testTCmdPipeClient()
