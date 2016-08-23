#!/usr/bin/env python3
from oslo.config import cfg
import os.path
import re

conf_list=['CRTT.conf','crtt.conf','../CRTT.conf','../crtt.conf',\
		'../../CRTT.conf','../../crtt.conf']
def find_cfg_file():
	for conf_file in conf_list:
		if os.path.isfile(conf_file):
			return conf_file
###############################################################
rest_group = cfg.OptGroup(
	name='REST', 
	title='RESTful group options'
)
rest_cfg_opts = [
	cfg.StrOpt(
		name='root_node',
		default=None,
		help='The node url that we start to scan from'),

	cfg.StrOpt(
		name='client_name',
		default='redfish',
		help='Client app name that communicates with resetful'),

	cfg.StrOpt(
		name='host',
		default='10.204.29.244',
		help='The IP address of the resetful Server'),

	cfg.IntOpt(
		name='bind_port',
		default=8888,
		help='Port number the server listens on.'),

	cfg.ListOpt(
		name='ver_support',
		default=['1'],
		help='The ver of Redfish this app supports.'),

	cfg.ListOpt(
		name='subnode_keys',
		default=['@odata.id'],
		help='The key to find child sub nodes'),

	cfg.StrOpt(
		name='client_app_ver',
		default='1',
		help='The version of Client app.')
]
###############################################################
main_group = cfg.OptGroup(
	name='MAIN', 
	title='MAIN group options'
)
main_cfg_opts = [
	cfg.StrOpt(
         name='value_file',
         default='Value_Check/url_dict.conf',
         help='Path of comparing file'),
     cfg.IntOpt(
         name='cycle',
         default=2,
         help='cycle to execute.'),
     cfg.IntOpt(
         name='processes',
         default=2,
         help='How many processes do we have.')
]
##########################################################3
log_group = cfg.OptGroup(
	name='LOG', 
	title='LOG group options'
)

log_cfg_opts = [

	cfg.StrOpt(
	name='app_name',
	default='redfish_test',
	help='APP name showed in Log'),

	cfg.StrOpt(
	name='logfilename',
	default='./redfish.log',
	help='Log file path.'),

	cfg.StrOpt(
	name='mode',
	default='a',
	help='specifies the mode in which the file is opened'),

	cfg.StrOpt(
	name='log_format',
	default=None,
	help='Log format in log file.'),

	cfg.IntOpt(
	name='root_level',
	default=10,
	help='Log level for global.'),

	cfg.IntOpt(
	name='ch_level',
	default=10,
	help='Log level for console stream.'),

	cfg.IntOpt(
	name='fh_level',
	default=20,
	help='Log level for file stream.'),

	cfg.StrOpt(
	name='html_color',
	default='color_1',
	help='Choose one in LOG_COLOR, color_1 or color_2'),

	cfg.DictOpt(
	name='color',
	default={},
	help='The main color cheme for html log, generally \
		keep it emtpy'),

	cfg.DictOpt(
	name="color_1",
	default={"err_color": "magenta",
			"warn_color": "yellow",
			"info_color": "white",
			"dbg_color": "white"},
	help='The html color scheme option1'),

	cfg.DictOpt(
	name="color_2",
	default={"err_color": "red",
			"warn_color": "orange",
			"info_color": "white",
			"dbg_color": "blue"},
	help='The html color scheme option2'),
	
	cfg.BoolOpt(
	name="Keyword_Italic",
	default=True,
	help='Whether the key work need to be italic in html log'),

	cfg.IntOpt(
	name='Keyword_FontSize',
	default=5,
	help='How is the font size for keyword in html log.'),

	cfg.StrOpt(
	name='Keyword_tag_start',
	default='<hl>',
	help='start tag to mark the keyword to be it'),

	cfg.StrOpt(
	name='Keyword_tag_end',
	default='</hl>',
	help='end tag to mark the keyword to be it'),
	
	cfg.StrOpt(
	name='title',
	default='default_title',
	help='The title of the html log file'),

	cfg.IntOpt(
	name='HtmlmaxBytes',
	default=5*1024*1024,
	help='The size of the html file, keep it small\
		otherwise, it takes long time to open it in brower'),

	cfg.BoolOpt(
	name="console_log",
	default=False,
	help='Whether to print log to console'),

	cfg.BoolOpt(
	name="Html_Rotating",
	default=True,
	help='Whether to rotate the log file if it over the HtmlmaxBytes'),

	cfg.IntOpt(
	name='Html_backupCount',
	default=5,
	help='If the "Html_Rotating" is open, \
		Count of html file will be used to backup'),

]
##########################################################3
request_group = cfg.OptGroup(
	name='REQUEST',
	title='Request options'
)
req_fail_opts = [
	cfg.FloatOpt(
	name='http_time_warn',
	default= 0.4,
	help='The limit of request time'),

	cfg.FloatOpt(
	name='http_time_error',
	default= 1.0,
	help='The limit of request time'),

	cfg.FloatOpt(
	name='timeout',
	default= 2.0,
	help='Timeout to request an URL'),

	cfg.IntOpt(
	name='retries',
	default=4,
	help='How many times will retry after failure'),

	cfg.FloatOpt(
	name='delay',
	default= 1.5,
	help='How long will execute the next retry'),

	cfg.IntOpt(
	name='backoff',
	default= 2,
	help='backoff times will retry'),

	cfg.BoolOpt(
	name='failonerror',
	default=False,
	help="whether we need stop if occor error")
]
##########################################################3
cli_group=cfg.OptGroup(
	name="CLI",
	title = 'Cli options'
)

cli_opts = [
	cfg.IntOpt(
		name='retry',
		positional=False,
    	help='How many times retryies after failure'),
	cfg.StrOpt(
		name='logname',
		positional=False,
    	help='Location for the execution log'),
	cfg.StrOpt(
		name='check_file',
		positional=False,
    	help='The url response data check file'),
	cfg.IntOpt(
		name='cycles',
		positional=False,
    	help='How many times we scan the nodes'),
	cfg.StrOpt(
		name='time_to_stop',
		positional=False,
    	help="The datetime we stop testing.\nFormat: 2016-06-21 12:00:59")

]

CONF = cfg.CONF
CONF.register_group(rest_group)
CONF.register_opts(rest_cfg_opts, rest_group)

CONF.register_group(main_group)
CONF.register_opts(main_cfg_opts, main_group)

CONF.register_group(log_group)
CONF.register_opts(log_cfg_opts, log_group)

CONF.register_group(request_group)
CONF.register_opts(req_fail_opts, request_group)

CONF.register_group(cli_group)
CONF.register_cli_opts(cli_opts, cli_group)
try:
	CONF(default_config_files=[find_cfg_file()])
except AttributeError:
	print("Can not find a proper config file, check") 

#This following condition is to: find the proper color 
#which defines in CONF.LOG.color
if CONF.LOG.html_color=='color_1':
	#Don't use shallow copying here
	CONF.LOG.color.update(CONF.LOG.color_1)
elif CONF.LOG.html_color=='color_2':
	CONF.LOG.color.update(CONF.LOG.color_2)

#This following condition is to: keep the user typed are working.
if CONF.CLI.retry:
	CONF.REQUEST.retries= CONF.CLI.retry
if CONF.CLI.logname:
	CONF.LOG.logfilename=CONF.CLI.logname
if CONF.CLI.check_file:
	CONF.MAIN.value_file= CONF.CLI.check_file
if CONF.CLI.cycles:
	CONF.MAIN.cycle= CONF.CLI.cycles
if CONF.CLI.time_to_stop:
	if not re.search(r'(20\d\d)-(\d\d)-(\d\d) (\d\d):(\d\d):(\d\d)', \
				CONF.CLI.time_to_stop):
		msg="The date time you entered is not in the corrent format, as: 2014-12-12 08:30:59"
		raise ValueError(msg) 


if __name__ =="__main__":
	print('CONF.value_file',CONF.MAIN.value_file)
	print('CONF.MAIN.cycle',CONF.MAIN.cycle)
	print('CONF.root_node:',CONF.REST.root_node)
	print('CONF.client_name:',CONF.REST.client_name)
	print('CONF.bind_port:',CONF.REST.bind_port)
	print('CONF.ver_support:',CONF.REST.ver_support)
	print('CONF.LOG.app_name:',CONF.LOG.app_name)
	print('CONF.LOG.logfilename:',CONF.LOG.logfilename)
	print('CONF.LOG.log_format:',CONF.LOG.log_format)
	print('CONF.LOG.root_level:',CONF.LOG.root_level)
	print('CONF.LOG.ch_level:',CONF.LOG.ch_level)
	print('CONF.LOG.fh_level:',CONF.LOG.fh_level)
	print('CONF.REQUEST.http_time_error:',CONF.REQUEST.http_time_error)
	print('CONF.REQUEST.http_time_warn:',CONF.REQUEST.http_time_warn)
	print('CONF.REQUEST.retries:',CONF.REQUEST.retries)
	print('CONF.REQUEST.delay:',CONF.REQUEST.delay)
	print('CONF.REQUEST.backoff:',CONF.REQUEST.backoff)
	print('CONF.REQUEST.failonerror:',CONF.REQUEST.failonerror)
	print('CONF.CLI.time_to_stop:',CONF.CLI.time_to_stop)
	print("""CONF.LOG.color:""",CONF.LOG.color)
