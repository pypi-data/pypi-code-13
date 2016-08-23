#!/usr/bin/env python3
import sys,os
#sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)),'CRTT_lib'))
from CRTT.PyLog2html import *
from CRTT.config import CONF
app_name=CONF.LOG.app_name
Keyword_Italic=CONF.LOG.Keyword_Italic
Keyword_FontSize=CONF.LOG.Keyword_FontSize
Keyword_tag_start=CONF.LOG.Keyword_tag_start
Keyword_tag_end=CONF.LOG.Keyword_tag_end
msg_color=CONF.LOG.color
log_format=CONF.LOG.log_format
root_level=CONF.LOG.root_level
fh_level=CONF.LOG.fh_level
ch_level=CONF.LOG.ch_level
HtmlmaxBytes=CONF.LOG.HtmlmaxBytes
console_log=CONF.LOG.console_log
html_title=CONF.LOG.title
html_filename=CONF.LOG.logfilename
Html_Rotating=CONF.LOG.Html_Rotating
Html_backupCount=CONF.LOG.Html_backupCount
filemode=CONF.LOG.mode

logger=PyLogger(name=app_name, html_filename=html_filename, mode=filemode,
    html_title=html_title,root_level=root_level,fh_level=fh_level,ch_level=ch_level,
    HtmlmaxBytes=HtmlmaxBytes, encoding=None, delay=False,
    html_format=log_format, msg_color=msg_color,
    Keyword_Italic=Keyword_Italic,Keyword_FontSize=Keyword_FontSize,
	Keyword_tag_start=Keyword_tag_start,
    Keyword_tag_end=Keyword_tag_end,console_log=console_log, 
	Html_Rotating=False,Html_backupCount=5)

if __name__=="__main__":
	for i in range(1):
		logger.debug('This is debug')
		#logger.info('This is info')
		#logger.warning("This is <hl>warning</hl>")
		#logger.error('This is <hl>error</hl> xxx')
		#logger.info('_____________')
