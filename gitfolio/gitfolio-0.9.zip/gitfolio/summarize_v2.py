import mistune, json
from bs4 import BeautifulSoup as bs4
import urllib.request as request

def summary(markdown,repoJson):
    desc = "Error loading description"
    if markdown == None or markdown == "":
        desc = "No description available"
    elif markdown == False:
        desc = "Bad file type"
    else:
        # convert md text into beautifulSoup class
        htmlMD = mistune.markdown(markdown)
        tree = bs4(htmlMD,"html.parser")
        wantedTags = ["h1","h2","h3","h4","h5","h6","hr"]
        textTags = ["p","li"]
        hasTags = False
        Htags = []
        for i in wantedTags:
            if len(tree.findAll(i)) > 0:
                hasTags = True
                for j in tree.findAll(i):
                    Htags.append(j)
        if hasTags == False:
            #if there are no headers
            hasText = False
            for i in textTags:
                if len(tree.findAll(i)) > 0:
                    hasText = True
                    dText = tree.findAll(i)[0]
                    break
            if hasText == False:
                desc = "No description available (no text tags or headers)."
            else:
                dText = dText.text
                if len(dText) > 130:
                    desc = dText[0:130] + "..."
                else:
                    desc = dText
        elif len(Htags) == 1:
            # really we do the same thing as if there were no heading tags
            hasText = False
            for i in textTags:
                if len(tree.findAll(i)) > 0:
                    hasText = True
                    dText = tree.findAll(i)[0]
                    break
            if hasText == False:
                desc = "No description available (no text tags)."
            else:
                dText = dText.text
                if len(dText) > 130:
                    desc = dText[0:130] + "..."
                else:
                    desc = dText
        elif len(Htags) >= 2:
            betterTags = []
            hasText = False
            TTags = []
            for i in textTags:
                if len(tree.findAll(i)) > 0:
                    hasText = True
                    for j in tree.findAll(i):
                        TTags.append(j)
                    break
            if hasText == False:
                desc = "No description available (no text tags)."
            else:
                for i in TTags:
                    if i.text.find(repoJson["name"]) > -1 or i.text.lower().find(repoJson["name"].lower()) > -1:
                        betterTags.append(i)
                # -------------
                if len(betterTags) > 1:
                    if len(betterTags[0].text) > 130:
                        desc = betterTags[0].text[0:130] + "..."
                    else:
                        desc = betterTags[0].text
                else:
                    dTag = TTags[0]
                    if len(dTag.text) > 130:
                        desc = TTags[0].text[0:130] + "..."
                    else:
                        desc = TTags[0].text
    # now eliminate some descriptions we don't want
    badDescs = {
        "-" : "No description available.",
        "" : "No description available (got empty summary string)."
        }
    for i in badDescs:
        if desc == i:
            desc = badDescs[i]
            break
    return desc

if __name__ == '__main__':
    tc = request.urlopen("https://raw.githubusercontent.com/bbatsov/rubocop/master/README.md").read().decode('utf-8')
    rj = request.urlopen("https://api.github.com/repos/bbatsov/rubocop").read().decode('utf-8')
    rj = json.loads(rj)
    summ = summary(tc,rj)
    print("[\n" + summ + "\n]")
