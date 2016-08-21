#!/usr/bin/python2.7
import requests
import urllib2
import os
import pwd
import json
import sys

def main():
   if len(sys.argv) < 2 or len(sys.argv) > 4:
      print "Usage: python YoutubetoMp3.py URL [path] [filename]"
      exit(0)
   url = sys.argv[1]
   r = requests.post("http://www.listentoyoutube.com/cc/conversioncloud.php",data={"mediaurl": url, "client_urlmap": "none"})
   try:
      statusurl = eval(r.text)['statusurl'].replace('\\/','/') + '&json'
   except:
      print eval(r.text)['error']
      time.sleep(1)
   while True:
      try:
         resp = eval(requests.get(statusurl).text)
         if 'downloadurl' in resp:
            downloadurl = resp['downloadurl'].replace('\\/','/')
            title = resp['file']
            break
         time.sleep(1)
      except Exception:
         pass
   path = os.path.join('/home',pwd.getpwuid(os.getuid()).pw_name,'Music')
   filename = title
   if len(sys.argv) == 3:
      path = sys.argv[2]
   elif len(sys.argv) == 4:
      path = sys.argv[2]
      filename = sys.argv[3]
   print "Downloading %s" % (title)
   mp3file = urllib2.urlopen(downloadurl)
   with open(os.path.join(path,filename), 'wb') as output:
      output.write(mp3file.read())
   print "File Successfully downloaded to : %s\nFilename : %s" % (path,filename)

if __name__ == "__main__":
    main()

