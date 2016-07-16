# -*- coding: utf-8 -*-

import click
import yaml, markdown, os, json, sys, webbrowser, optparse, getpass
try:
    import SimpleHTTPServer
except:
    import http.server as SimpleHTTPServer
try:
    import SocketServer
except:
    import socketserver as SocketServer
import threading, time, socket
from jinja2 import Template, FileSystemLoader
from jinja2.environment import Environment
from bs4 import BeautifulSoup as bs
from cookiecutter.main import cookiecutter

@click.command()
@click.option('--openfile/--no_openfile', '-o/-n', default=False, help='Open in browser')
@click.option('--serve/--no_serve', '-s/-t', default=False, help='Serve up the file')
@click.option('--init/--no_init', '-i/-j', default=False, help='Initialize a wikicreator project')
def main(openfile, serve, init):
    if init:
        cookiecutter('https://MatanSilver@bitbucket.org/MatanSilver/cookiecutter-wikicreator.git')
    else:
        generate_files()
        if serve:
            url = "localhost:8080/output.html"
            server_thread = threading.Thread(target=server_worker)
            files_thread = threading.Thread(target=files_worker)
            server_thread.daemon = True
            files_thread.daemon = True
            server_thread.start()
            files_thread.start()
            if openfile:
                webbrowser.open_new_tab(url)
            try:
                while(True):
                    time.sleep(1)
            except KeyboardInterrupt:
                print ("Exiting")
                sys.exit(1)


if __name__ == "__main__":
    main()


def find_free_port():
    s = socket.socket()
    s.bind(('', 0))
    return s.getsockname()[1]

def create_tabpane(categories):
    tab_content = ""
    for category in categories:
        if category.get('file'):
            try:
                with open(category['file']) as f:
                    tab_body = markdown.markdown(f.read())
                    tab_content += '<div role="tabpanel" class="tab-pane' + (' active ' if 'active' in category and category['active'] == True else '') + '" id="' + category['file'].replace('/', '_').replace('.md', '') + '">' + tab_body + '</div>\n'
            except:
                print ("file " + category['file'] + " not found")
        if category.get('categories'):
            tab_content += create_tabpane(category['categories'])
    return tab_content

def create_sidebar(categories):
    sidebar_content=""
    for category in categories:
        if category.get('categories') and category.get('file'):
            sidebar_content += '\n<li><a role="button" data-toggle="collapse" href="#' + category['heading'].replace(' ', '_') + '_collapse" header-link="#' + category['file'].replace('/', '_').replace('.md', '') + '" aria-expanded="false" aria-controls="' + category['heading'].replace(' ', '_') + '_collapse"><i class="fa fa-chevron-right nav-chevron"></i>'
            sidebar_content += category['heading']
            sidebar_content += '</a></li>\n'
            sidebar_content += '<div class="collapse well" id="' + category['heading'].replace(' ', '_') + '_collapse">\n<ul class="nav nav-sidebar indented">\n'
            sidebar_content += create_sidebar(category['categories']) + '</ul>\n</div>'
        elif category.get('file'):
            sidebar_content += '<li role="navlinkelement"' + (' class="active" ' if 'active' in category and category['active'] == True else '') + '><a class="navlink" data-target="#'
            sidebar_content += category['file'].replace('/', '_').replace('.md', '') + '">'
            sidebar_content += category['heading'] + '</a></li>\n'
        elif category.get('categories'):
            sidebar_content += '\n<li><a role="button" data-toggle="collapse" href="#' + category['heading'].replace(' ', '_') + '_collapse" aria-expanded="false" aria-controls="' + category['heading'].replace(' ', '_') + '_collapse"><i class="fa fa-chevron-right nav-chevron"></i>'
            sidebar_content += category['heading']
            sidebar_content += '</a></li>\n'
            sidebar_content += '<div class="collapse well" id="' + category['heading'].replace(' ', '_') + '_collapse">\n<ul class="nav nav-sidebar indented">\n'
            sidebar_content += create_sidebar(category['categories']) + '</ul>\n</div>'
    return sidebar_content

def check_config(categories, active_exists):
    for category in categories:
        if active_exists == False and ('active' in category and category['active'] == True):
            active_exists = True
        elif not ('file' in category and category['file']) and not ('categories' in category and category['categories']):
            print ("Please use either a file or categories in config")
            return 1
        elif 'categories' in category and category['categories']:
            return check_config(category['categories'], active_exists)
    if active_exists == True:
        return 0
    else:
        print ("Please mark one category as active")
        return 1

def generate_files():
    config = open('config.yaml')
    dataMap = yaml.safe_load(config)
    config.close()
    if check_config(dataMap, False) == 0:
        env = Environment()
        env.loader = FileSystemLoader('.')
        wikitemplate = env.get_template('wikitemplate.html')
        tab_content = create_tabpane(dataMap)
        sidebar_content = create_sidebar(dataMap)
        htmlcontent = wikitemplate.render(sidebar_content=sidebar_content, tab_content=tab_content)
        soup=bs(htmlcontent, 'html.parser')  #make BeautifulSoup
        prettyHTML=soup.prettify()   #prettify the html
        output = open('output.html', 'w')
        output.write(prettyHTML)
        output.close()
        #print ("files generated")
    else:
        print("config check failed")
        return 1

def server_worker():
    """thread worker function"""
    PORT = find_free_port()
    Handler = SimpleHTTPServer.SimpleHTTPRequestHandler
    httpd = SocketServer.TCPServer(("", PORT), Handler)
    print ("serving at localhost:" + str(PORT) + "/output.html")
    httpd.serve_forever()
    pass
def files_worker():
    while(True):
        generate_files()
        time.sleep(1)
    pass
