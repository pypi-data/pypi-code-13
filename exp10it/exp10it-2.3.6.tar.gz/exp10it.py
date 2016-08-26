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
    #将文件中的一行字符串用多行字符串替换，调用时要将"多行字符串的参数(第二个参数)"中的换行符设置为\n
    tmpstr=nline.replace('\n','\\\n')
    os.system("sed '/%s/c\\\n%s' %s > /tmp/1" % (oneline,tmpstr,file_abs_path))
    os.system("cat /tmp/1 > %s && rm /tmp/1" % file_abs_path)
    pass

def lin2win(file_abs_path):
    #将linux下的文件中的\n换行符换成win下的\n\n换行符
    import sys
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
    #exp_list为空时，得到目录下的所有文件名,不返回空文件夹名
    #返回结果为文件名列表，不是完全绝对路径名
    #eg.folder="/root"时，当/root目录下有一个文件夹a，一个文件2.txt,a中有一个文件1.txt
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
        #如果本地local_resp_path存在，且文件夹中有.git,当local_resp_path文件夹中的文件与远程github仓库中的文件不一致时，
        #且远程仓库有本地仓库没有的文件，选择合并本地和远程仓库并入远程仓库,所以这里采用一并重新合并的处理方法，
        #(与上一个if中的情况相比，多了一个合并前先删除本地仓库中的.git文件夹的动作),
        #虽然当远程仓库中不含本地仓库没有的文件时，不用这么做，但是这样做也可以处理那种情况
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
    import platform
    return platform.system()


#below code are the function about tab key complete with file path
#------------------------start-of-tab_complete_file_path--------------------------------
def tab_complete_file_path():
    #this is a function make system support Tab key complete file_path
    #works on linux,it seems windows not support readline module
    def tab_complete_for_file_path():
        import glob
        import sys
        import os
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

def get_response_key_value_from_uri(uri):
    #得到uri响应的关键参数的值
    #包括:响应状态码,uri的title,响应的html内容
    #返回结果为一个字典,有三个键值对:code,title,content
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
        br.set_handle_gzip(True)
        br.set_handle_redirect(True)
        br.set_handle_referer(True)
        br.set_handle_robots(False)
        br.set_handle_refresh(mechanize._http.HTTPRefreshProcessor(), max_time=1)
        br.addheaders = [('User-agent', 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008071615 Fedora/3.0.1-1.fc9 Firefox/3.0.1')]
        br.open(uri)
        code=br.response().code
        title=br.title()
        content=br.response().read()
    except mechanize.URLError as e:
        code=e.code
        content=e.read()
        from bs4 import BeautifulSoup
        soup=BeautifulSoup(content,"lxml")
        title=soup.title.string

    return {'code':'%s' % code,'title':'%s' % title,'content':'%s' % content}


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
        title=get_title_from_uri(http_domain)
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


#------------------below code is for func newscript--------------------#
import time
import os
import datetime
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

                    insert_code_header_to_file(file_abs_path,function,date,author,blog)

                    break
            print "please input the script function:)"
            function=raw_input()
            date=datetime.date.today()
            author="quanyechavshuo"
            blog="https://3xp10it.github.io"
            if os.path.basename(file_abs_path)!="newscript.py" and "exp10it.py"!=os.path.basename(file_abs_path):
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

#--------------------------newscript-end-------------------------------#


def blog():
    #便捷写博客(jekyll+github)函数
    import datetime
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
    #改变md5函数，简单的cmd命令达到混淆效果，可用于上传百度网盘
    #只适用于windows平台
    import os
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
    import os
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

def check_webshell_uri(uri):
    #检测uri是否为webshell,并检测是webshell需要用html中搜索到的表单爆破还是用一句话类型爆破方式爆破
    #返回结果为一个字典,有2个键值对,第一个键为是否是webshell,用y1表示,y1为True或者False
    #第二个键为webshell爆破方式,用y2表示
    #y2的值可能是
    #1>"biaodan_bao"(根据搜到的表单爆)
    #2>"direct_bao"(直接爆)
    #3>""(空字符串,对应uri不是webshell)
    #4>"bypass"(对应uri是一个webshll,且该webshell不用输入密码即可控制)

    y1=False
    belong2github=False
    y2=""

    response_dict=get_response_key_value_from_uri(uri)
    code=response_dict['code']
    title=response_dict['title']
    content=response_dict['content']

    #过滤掉github.com里面的文件
    from urlparse import urlparse
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
    if re.search(strange_title_pattern,title) and belong2github==False and len(content)<8000:
        y1=True

    #根据返回的html内容中是否有关键字以及返回内容大小判断是否为webshell
    strang_filecontent_pattern=re.compile(r".*((shell)|(hack)|(h4ck)|(b374k)|(c99)|(spy)|(80sec)|(hat)|(black)|(90sec)|(blood)|(r57)|(b4che10r)|(X14ob-Sh3ll)|(server_sync)).*",re.I)
    if re.search(strang_filecontent_pattern,content) and len(content)<8000:
        y1=True

    #如果正常返回大小很小，说明有可能是一句话
    #1.返回结果为200且文件内容少且有关键字的为大马
    #2.返回结果为200且文件内容少且没有关键字的为一句话小马
    if y1==True and str(200)==code:
        webshell_flag=re.compile(r"(c:)|(/home)|(/var)|(/phpstudy)",re.I)
        if len(content)<8000 and re.search(r'''method=('|")post('|")''',content):
            y2="biaodan_bao"
        if len(content)==0:
            y2="direct_bao"
        if len(content)>8000 and re.search(r'''method=('|")post('|")''',content) and re.search(webshell_flag,content):
            y2="bypass"

    #如果返回码为404且返回内容大小较小但是返回结果中没有uri中的文件名,判定为404伪装小马
    if str(404)==code and len(content)<400:
        uri=re.sub(r"(\s)$","",uri)
        webshell_file_name=uri.split("/")[-1]
        pattern=re.compile(r"%s")
        if re.search(pattern,content):
            y1=False
            y2=""
        else:
            if re.search(r'''method=('|")post('|")''',content) is None:
                y1=True
                y2="direct_bao"
            else:
                y1=True
                y2="biaodan_bao"

    return {'y1':y1,'y2':'%s' % y2}


def get_webshell_suffix_type(uri):
    #获取uri所在的webshell的真实后缀类型,结果为asp|php|aspx|jsp
    from urlparse import urlparse
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
    from urlparse import urlparse
    parsed=urlparse(uri)
    http_domain_value=parsed.scheme+"://"+parsed.netloc
    print http_domain_value
    return http_domain_value

