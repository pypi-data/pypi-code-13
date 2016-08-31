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
        self.bVerbose = bVerbose
        TCmdStringSckP2PLayout.__init__(self,sHubId,sHostAndPort,sPairId,sSuffix,sAcctPwd,sClientInfo,bVerbose)
        PrintTimeMsg('TCmdStringSckP2PLayoutPipe.PipeServerIPPort=(%s:%s)' % (sPipeServerIP,iPipeServerPort))
        self.pipeServer = TCmdPipeServerTCBQ(iPipeServerPort,sPipeServerIP,self.HandlePipePushData)

    def HandlePipePushData(self, oData,iDealCount):
        if self.bVerbose:
            PrintTimeMsg('TCmdStringSckP2PLayoutPipe.HandlePipePushData.%d#.oData=%s=' % (iDealCount,oData))
        sRcv = '*'
        lsParam = [str(oData)]
        if type(oData)==list:
            sRcv = oData[0]
            lsParam = oData[1:]
        self.SendRequestP2PLayoutCmd(sRcv,lsParam,'sLogicParamPipe')
        # WeiYF.20160826 发送日志如下：
        # [2016-08-26 13:54:57.483]ReadCmdStrFromLink.CmdCnt=8={
        #   CmdStr[0].24=!P2PLayout.SendCmdToPeer=
        #   CmdStr[1].13=FeedIB.AskBid=
        #   CmdStr[2].1=*=
        #   CmdStr[3].4=Test=
        #   CmdStr[4].3=One=
        #   CmdStr[5].1=2=
        #   CmdStr[6].5=three=
        #   CmdStr[7].6=iCnt=4=
        # }
        # 可以看出，CmdStr[0]是固定命令，CmdStr[1]是发送者的sSuffix
        # CmdStr[2+]才是 TCmdPipeClient 填入的参数。
