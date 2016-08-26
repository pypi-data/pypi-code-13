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

class TCmdSckPipeP2PLayout(TCmdStringSckP2PLayout):
    def __init__(self, sHubId,sHostAndPort,sPairId,sSuffix,sAcctPwd,sClientInfo,iPipeServerPort,sPipeServerIP):
        TCmdStringSckP2PLayout.__init__(self,sHubId,sHostAndPort,sPairId,sSuffix,sAcctPwd,sClientInfo)
        PrintTimeMsg('TCmdSckPipeP2PLayout.PipeServerIPPort=(%s:%s)' % (sPipeServerIP,iPipeServerPort))
        self.pipeServer = CPipeServerRelayToPeer(iPipeServerPort,sPipeServerIP,self.HandlePipePushData)

    def HandlePipePushData(self, oData,iDealCount):
        PrintTimeMsg('TCmdSckPipeP2PLayout.HandlePipePushData.%d#.oData=%s=' % (iDealCount,oData))
