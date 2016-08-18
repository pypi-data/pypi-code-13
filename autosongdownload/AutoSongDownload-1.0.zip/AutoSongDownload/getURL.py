from youtubeAudio import download
import requests, subprocess, os, sys, pyperclip
from bs4 import BeautifulSoup as bs

'''What it does-
"Download song of your choice in audio format in two steps by just entering the name."


Usage - 4 ways:-
1. Run the program and enter the song name.
2. From cmd line or run enter "song <song name>". This is will give you top
    n results(n depends on you).
3. From cmd line or run enter "song /<song name>". First result will be automatically downloaded.
4. You can just copy the song name and run "song" command from cmd or run. No
    need to paste just copy. Note:-This will automatically download the first result by default. (You
    can change that too.)
5. You can create a keyboard shorcut to shorten the 4th way even more. Just copy the
    the song name and press that Keyboard shortcut. And the download will start.

MIT License-
Tushar Tripathi
tushutripathi@gmail.com
'''

path='D:\\DC++Share\\Songs\\pyDirect'

def check(tag): # Custom function to get the channel names through BeautifulSoup
    if tag.has_attr('class') and ('g-hovercard' in tag['class']) and tag.parent.name=='div':
        return True
    else:
        return False

# If auto is 1 it will not give options, directly send the first result.
# Function return video url and title.
def get(query, auto=0):
    base="https://www.youtube.com"
    search_url = "https://www.youtube.com/results"
    payload={'search_query':query, 'page':'', 'utm_source':'opensearch'}
    r=requests.get(search_url, params=payload)
    soup=bs(r.text, "html.parser")

    videos=soup.find_all("a", class_="yt-ui-ellipsis-2") #all a tags containing link
                                                         #has this in class name

    if auto==1:     # Automatically choses the first one to download.
        print ("File to download ",videos[0].string)
        return (base + videos[0]['href'], videos[0]['title'])

    else:
        count,cc=1,0    # cc=Channel Count-wiil be used to access the channel name
                                # from the channels array
        channels=soup.find_all(check) #Scraping channel names
        print ("Choose what you want. Just enter the corresponding number.")

        for video in videos:
            if 'g-hovercard' in video['class']: # Skipping over channels
                cc+=1
                continue
            try:
                print "%d. %s" %(count, video.string), # In case of playlist the code
                                                                            # will tell in the same line
                if 'list' in video['href']:    # If its a playlist
                    print " - A PLAYLIST",
                print ""

                channel=channels[cc]
                if video.parent.next_sibling.string=="YouTube":
                    print ("-Made by Youtube.")
                else:
                    try:        # Checking if its verified channel
                        p=channel.next_sibling.next_sibling
                        print "Channel - ", channel.string,"-Verified"
                    except:
                        print "Channel - ", channel.string  # Not verified
                    count+=1

                cc+=1

            except:
                pass

            if count==11 or cc==len(channels): #Change it to how many options you want(max value-21)
                break
            print ""
        choice=int(raw_input("\nNow enter your choice- "))
        print "You chose- ", videos[choice-1].string
        print "Download is starting..."
        return (base + videos[choice-1]['href'], videos[choice-1]['title'])


def openFile(title):
    #print "Opening the folder."
    #subprocess.Popen('explorer '+path)
    global path
    print "Opening the file."
    for ext in ['.webm', '.m4a', '.mp3']:
        name='"'+path+"\\"+title+ext+'"'
        try:
            p = subprocess.Popen(name, shell=True)
            # Closing the cmd window opened
            subprocess.Popen("TASKKILL /F /PID {pid}".format(pid=p.pid))
            break
        except:
            pass
    else:
        print "File can't be opened for some reasons."
        print "Opening the folder."
        path = '"'+path+'"'
        p = subprocess.Popen('explorer '+path)
        subprocess.Popen("TASKKILL /F /PID {pid}".format(pid=p.pid))
    sys.exit()


def main(query):

    file_open = True # Whether to open the file after download
    if query[-1]=='/':
        file_open = False

    if query[0]=='/':
        query = query[1:]
        url,title = get(query,1)
    else:
        url,title=get(query)

    print "Got the url",url
    for ext in ['.webm', '.m4a', '.mp3']:
        name = path+"\\"+title+ext
        if os.path.isfile(name):
            print "It's already downloaded."
            break
    else:
        print "Starting download..."
        download(url)
    if file_open:
        openFile(title)
    sys.exit()


if __name__=="__main__":
    try:
        sys.argv[1]         # Checks if cmd line argument is given
        query= " ".join(sys.argv[1:])
    except:
        if "idlelib" in sys.modules:
            query = raw_input("Enter the song's name. - ")
        else:
            query = "/"+pyperclip.paste()
    main(query)
