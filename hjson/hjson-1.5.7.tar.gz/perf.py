import hjson
import json
import time

data="""
{
 "description"                : "The firefox web browser.\\nNote: If you have a different version of firefox running already, you must launch firefox with the -new-instance command line argument."
 ,"maintainer"                : "Timothy Hobbs <timothyhobbs (at) seznam dot cz>"
 ,"last-update-time"          : "2014-02-12-12:59"
 ,"executable"                : "/usr/bin/firefox"
 ,"user-dirs"                 : ["Downloads"]
 ,"x11"                       : true
 ,"sound-card"                     : true
 ,"allow-network-access"      : true
 ,"basic-common-permissions" : true
}
"""

data2="""
{
  description:
    '''
    The firefox web browser.
    Note: If you have a different version of firefox running already, you must launch firefox with the -new-instance command line argument.
    '''
  maintainer: Timothy Hobbs <timothyhobbs (at) seznam dot cz>
  last-update-time: 2014-02-12-12:59
  executable: /usr/bin/firefox
  user-dirs:
  [
    Downloads
  ]
  x11: true
  sound-card: true
  allow-network-access: true
  basic-common-permissions: true
}
"""

#print(data)

#a = hjson.loads(data)
#print hjson.dumps(a)

reps=1000

t1 = time.time()
for i in range(0, reps):
  a = hjson.loads(data2)
diff = int((time.time() - t1) * 1000)
print("hjson:"+str(diff))


t1 = time.time()
for i in range(0, reps):
  a = json.loads(data)
diff = int((time.time() - t1) * 1000)
print("json:"+str(diff))


