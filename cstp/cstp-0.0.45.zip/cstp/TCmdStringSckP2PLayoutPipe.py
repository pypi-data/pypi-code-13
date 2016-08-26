#!/usr/local/bin/python
# -*- coding:utf-8 -*-
"""
    2016/8/26  WeiYanfeng
    实现了 TCmdPipeServer 和 P2PLayout模式下Peer端的对接。
"""

import sys

from weberFuncs import PrintTimeMsg
from TCmdStringSckP2PLayout import TCmdStringSckP2PLayout
from TCmdPipeServerTCBQ import TCmdPipeServerTCBQ

class TCmdStringSckP2PLayoutPipe(TCmdStringSckP2PLayout):
    def __init__(self, sHubId,sHostAndPort,sPairId,sSuffix,sAcctPwd,sClientInfo,
                 iPipeServerPort,sPipeServerIP='127.0.0.1', bVerbose=False):
        TCmdStringSckP2PLayout.__init__(self,sHubId,sHostAndPort,sPairId,sSuffix,sAcctPwd,sClientInfo)
        PrintTimeMsg('TCmdStringSckP2PLayoutPipe.PipeServerIPPort=(%s:%s)' % (sPipeServerIP,iPipeServerPort))
        self.pipeServer = TCmdPipeServerTCBQ(iPipeServerPort,sPipeServerIP,self.HandlePipePushData)

    def HandlePipePushData(self, oData,iDealCount):
        if bVerbose:
            PrintTimeMsg('TCmdStringSckP2PLayoutPipe.HandlePipePushData.%d#.oData=%s=' % (iDealCount,oData))
        sRcv = '*'
        lsParam = [str(oData)]
        if type(oData)==list:
            sRcv = oData[0]
            lsParam = oData[1:]
        self.SendRequestP2PLayoutCmd(sRcv,lsParam,'sLogicParamPipe')
