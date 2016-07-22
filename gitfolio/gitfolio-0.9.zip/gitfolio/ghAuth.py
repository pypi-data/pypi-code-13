import urllib.request as request
import json

def getAuth(useBrowser=False):
    if useBrowser:
        import webbrowser
        webbrowser.open("https://github.com/login/oauth/authorize?client_id=d518f1ee3b1cc76de248&redirect_uri=https://calderwhite.github.io/myGitFolio/register&scope=repo")
    else:
        print("Go to:\n\
        https://github.com/login/oauth/authorize?client_id=d518f1ee3b1cc76de248&redirect_uri=https://calderwhite.github.io/myGitFolio/register&scope=repo")
    code = input("enter code here:")
    
    auth_url = "https://github.com/login/oauth/access_token?client_id=d518f1ee3b1cc76de248&client_secret=91c59f92eb70efe00c40094ae71366dbf12ec77d&code=" + code
    
    req = request.Request(auth_url,headers={"Accept" : "application/json"})
    res = request.urlopen(req)
    jsonRes = json.loads(res.read().decode('utf-8'))
    if jsonRes.__contains__("access_token"):
        auth_token = jsonRes["access_token"]
        return auth_token
    else:
        print("An error occured with the api:")
        print(jsonRes["error_description"])
        raise Exception
        return jsonRes
if __name__ == '__main__':
    user_auth = getAuth()
    print(user_auth)
