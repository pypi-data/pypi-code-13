import json, base64, sys, os
sys.path.append(os.getcwd() + "ghAuth.py")
sys.path.append(os.getcwd() + "summarize_v2.py")
from mygitfolio import ghAuth
from mygitfolio import summarize_v2
import urllib.request as request

def get_sorted_repos(token,order="date",private=True):
    repoUrl = "https://api.github.com/user/repos?access_token=" + token + "&visibility="
    public = request.urlopen(repoUrl + "public")
    repos = []
    if private:
        allRepo = request.urlopen(repoUrl + "all")
        repoAll = json.loads(allRepo.read().decode('utf-8'))
        repos = repoAll
    else:
        repoPu = json.loads(public.read().decode('utf-8'))
        for i in repoPu:
            repos.append(i)
    if len(repos) < 1:
        # no repos to gather!
        raise Exception
    if order == "date":
        repos.sort(key=lambda r: r["created_at"],reverse=True)
        # you have to revese the sort, since by default it sorts oldest to newest
    elif order == "stars":
        repos.sort(key=lambda r: r["stargazers_count"],reverse=True)
    elif order == "watchers":
        repos.sort(key=lambda r: r["watchers_count"])
    else:
        # no known order string was passed in
        raise Exception
    return repos

def build_summary(repoUrl,token,repoJson,auth=True):
    global err
    err = False
    try:
        global readme_req
        global readme
        if auth:
            readme_req = request.urlopen(repoUrl + "/readme?access_token=" + token)
        else:
            readme_req = request.urlopen(repoUrl + "/readme")
        readme = readme_req.read()
    except:
        print("ERROR: got bad http code")
        # too lazy to check for other errors, or to make sure the object is in fact the correct one -_-
        err = True
    if err:
        decoded_contents = None
    else:
        readme = json.loads(readme.decode('utf-8'))
        ending = readme["name"].split(".")[-1]
        if ending.lower() != "md":
            decoded_contents = False
            print("ERROR: bad file type: " + ending)
        else:
            b64encoded_contents = readme["content"]
            encoded_contents = base64.b64decode(b64encoded_contents)
            #encoded_contents = str(encoded_contents)[2:len(str(encoded_contents)) - 1]
            decoded_contents = encoded_contents.decode('utf-8')
    summary = summarize_v2.summary(decoded_contents,repoJson)
    return summary
def build(oauth_token,myOrder="date",privateRepos=True):
    print("retrieving repositories...")
    repoList = get_sorted_repos(oauth_token,order=myOrder,private=privateRepos)
    summaries = []
    print("building summaries...")
    for i in repoList:
        x = build_summary(i["url"],oauth_token,i)
        summary_package = {
            "name" : i["name"],
            "fork" : i["fork"],
            "summary" : x
            }
        summaries.append(summary_package)
        print("summary " + str(repoList.index(i) + 1) + "/" + str(len(repoList)) + " is complete.")
    print(summaries)
def custom_build(api_url,private,oauth_token=None):
    if private:
        if oauth_token == None:
            raise Exception("The repository is private, but no oauth_token was provided.\n  Example for private repository: mySummary = builder.custom_build(<fileType>,<repository url for github api>,True,<oauth token (long hash)>")
        else:
            Rjson = request.urlopen(api_url + "?oauth_token=" + oauth_token).read().decode('utf-8')
            Rjson = json.loads(Rjson)
            summ = build_summary(api_url,oauth_token,Rjson,auth=True)
            summary_package = {
                "name" : Rjson["name"],
                "fork" : Rjson["fork"],
                "summary" : summ
                }
            return summary_package
    else:
        Rjson = request.urlopen(api_url).read().decode('utf-8')
        Rjson = json.loads(Rjson)
        summ = build_summary(api_url,oauth_token,Rjson,auth=False)
        summary_package = {
            "name" : Rjson["name"],
            "fork" : Rjson["fork"],
            "summary" : summ
            }
        return summary_package
def custom_group_build(name,oauth_token=None):
    # this function works for orginizations and users
    # remember, capital letters matter in the name!
    if oauth_token != None:
        api_url = "https://api.github.com/users/" + name + "/repos?oauth_token=" + oauth_token + "&visibility=all"
    else:
        api_url = "https://api.github.com/users/" + name + "/repos"
    repos = request.urlopen(api_url).read().decode('utf-8')
    Jrepos = json.loads(repos)
    summs = []
    for i in Jrepos:
        if oauth_token != None:
            summ = build_summary(i["url"],oauth_token,i,auth=True)
        else:
            summ = build_summary(i["url"],None,i,auth=False)
        summary_package = {
            "name" : i["name"],
            "fork" : i["fork"],
            "summary" : summ
            }
        summs.append(summary_package)
        print("repo " + str(Jrepos.index(i) + 1) + "/" + str(len(Jrepos)) + " is done.")
    return summs
def build_auth(useWebBrowser=False):
    r = open("userData.json",'r')
    rj = json.loads(r.read())
    r.close()
    if rj.__contains__("oauth_token"):
        print("already authenticated.")
        oauth_token = rj["oauth_token"]
    else:
        oauth_token = ghAuth.getAuth(useBrowser=useWebBrowser)
        jBuild = {}
        jBuild["oauth_token"] = oauth_token
        jstr = json.dumps(jBuild,indent=4)
        w = open("userData.json", 'w')
        w.write(jstr)
        w.close()
        print("--------------")

if __name__ == '__main__':
    print("authenticating....")
    r = open("userData.json",'r')
    rj = json.loads(r.read())
    r.close()
    if rj.__contains__("oauth_token"):
        oauth_token = rj["oauth_token"]
    else:
        oauth_token = ghAuth.getAuth()
        jBuild = {}
        jBuild["oauth_token"] = oauth_token
        jstr = json.dumps(jBuild,indent=4)
        w = open("userData.json", 'w')
        w.write(jstr)
        w.close()
        print("--------------")
    buildFile(oauth_token)

