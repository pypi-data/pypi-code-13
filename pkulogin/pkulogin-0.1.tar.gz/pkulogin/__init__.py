from urllib import request,parse,response
import requests
import getpass
def main():

    user = input('Username:')
    pwd = getpass.getpass('Password:')
    ipr = input("iprange (yes/no):")
    login_data = parse.urlencode([
        ('username', user),
        ('password', pwd),
        ('iprange',ipr)
    ])
    req = request.Request('https://its.pku.edu.cn/cas/webLogin',method='POST')
    req.add_header('Origin', 'https://its.pku.edu.cn')
    req.add_header('User-Agent', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36')
    req.add_header('Referer', 'https://its.pku.edu.cn')
    with request.urlopen(req,data=login_data.encode('utf-8')) as f:
        print('Status:',f.status, f.reason)
        #for k,v in f.getheaders():
        #    print('%s: %s' % (k,v))
        print("login...")
        data=f.read().decode('utf-8')
    #
    #with open('its.html','w') as file:
    #    file.write(data)
    #    file.close()
    re=requests.post('https://its.pku.edu.cn/cas/webLogin',data=login_data.encode('utf-8'))
    print(re.__dict__)
