from gitfolio import builder
import sys, os, json
def gitfolio(cmds,dash,ddash):
    """main file\n--help for help"""
    sys.path.append(os.getcwd() + "gitfolio.py")
    from gitfolio import gitfolio_run as funcs
    from gitfolio import gitfolio_run as funcCalls
    funcs = dir(funcs)
    if len(ddash) > 0:
        if ddash[0] == "--help":
            funcs.pop(funcs.index("check_commands"))
            for i in funcs:
                if i[0:2] != "__" and i != "builder" and i != "os" and i != "sys" and i != "json":
                    print(i + ":")
                    print(" " + funcCalls.__getattribute__(i).__doc__)
                    print("----------")
        else:
            try:
                eval(cmds[0] + "(" + str(cmds[1:]) + "," + str(dash) + "," + str(ddash) + ")")
            except NameError:
                raise Exception("No such command as " + cmds[0])
    else:
        try:
            eval(cmds[0] + "(" + str(cmds[1:]) + "," + str(dash) + "," + str(ddash) + ")")
        except NameError:
            raise Exception("No such command as " + cmds[0])     
def build_package(cmds,dash,ddash):
    """by default, this will build for the current user's oauth_token only\n
    format:\n
    <your python 3> gitfolio.py build_package <name of organization or user> <auth code (if private) > <options>
    options:\n
    --private : custom build activated, custom build requires a full api url and oauth token (when --private)
    """
    if len(ddash) > 0:
        for i in ddash:
            if i == "--private":
                if len(cmds) < 1:
                    print("not enough arguments given!")
                else:
                    print("building...")
                    print(builder.custom_group_build(cmds[0],oauth_token=cmds[1]))
    else:
        print("building...")
        print(builder.custom_group_build(cmds[0]))
    pass
def authenticate(cmds,dash,ddash):
    """this will retrive your oauth_token, so you may run gitfolio commands"""
    if os.path.exists(os.getcwd() + "\\mygitfolio"):
        os.chdir(os.getcwd() + "\\mygitfolio")
    # this is just so when the program is compiled we don't run into any errors
    builder.build_auth(useWebBrowser=True)
    pass
def unauthenticate(cmds,dash,ddash):
    """delete your authentication information.\n
    this way you can authenticate for a different user:
    <your python 3> gitfolio.py unauthenticate
    <your python 3> gitfolio.py authenticate
    """
    if os.path.exists(os.getcwd() + "\\mygitfolio"):
        os.chdir(os.getcwd() + "\\mygitfolio")
    # this is just so when the program is compiled we don't run into any errors
    
def auto_build_package(cmds,dash,ddash):
    """this command will build a summary package for whatever\n
    user's oauth_token is in userData.json (hence the name auto)\n
    options:\n
    --public : only build for public repos
    --all : DEFAULT, build for all repositories, including private
    """
    if os.path.exists(os.getcwd() + "\\mygitfolio"):
        os.chdir(os.getcwd() + "\\mygitfolio")
    # this is just so when the program is compiled we don't run into any errors
    print("grabbing authentication info...")
    r = open("userData.json",'r')
    rj = json.loads(r.read())
    r.close()
    private = True
    for i in ddash:
        if i == "--public":
            private = False
    if rj.__contains__("oauth_token"):
        oauth_token = rj["oauth_token"]
        builder.build(oauth_token,privateRepos=private)
    else:
        raise Exception("Not authenticated!\nto authenticate/integrate your github account type the following\ncommand, and then follow its instructions: <your python 3> gitfolio.py authenticate")
def check_commands(args):
    commands = []
    options1 = []
    options2 = []
    for i in args:
        if i.find("--") > -1:
            options2.append(i)
        elif i.find("-") > -1:
            options1.append(i)
        else:
            commands.append(i)
    try:
        eval(commands[0] + "(" + str(commands[1:]) + "," + str(options1) + "," + str(options2) + ")")
    except NameError:
        raise Exception("No such command as " + commands[0])
if __name__ == '__main__':
    args = [sys.argv[0].split(".")[0]]
    for i in sys.argv[1:]:
        args.append(i)
    check_commands(args)
