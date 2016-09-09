#!/usr/bin/env python
'''
Copyright (c) 2016, Nigcomsat I&D
All rights reserved.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met:
1. Redistributions of source code must retain the above copyright
   notice, this list of conditions and the following disclaimer.
2. Redistributions in binary form must reproduce the above copyright
   notice, this list of conditions and the following disclaimer in the
   documentation and/or other materials provided with the distribution.
3. All advertising materials mentioning features or use of this software
   must display the following acknowledgement:
   This product includes software developed by Nigcomsat I&D.
4. Neither the name of Nigcomsat I&D nor the
   names of its contributors may be used to endorse or promote products
   derived from this software without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY Nigcomsat I&D ''AS IS'' AND ANY
EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL Nigcomsat I&D BE LIABLE FOR ANY
DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
(INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
(INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
'''
import time
from socket import *
from libopeniot import IoTComm
from openiot import myeval
import thread
import sys
import re
import configparser

class whendo():
    def __init__(self, when, do):
        self.when = when
        self.do = do

class ScripingEnging():
    def __init__(self, comm):
        self.whendos = []
        self.variables = {}
        self.comm = comm

    def reset(self):
        del self.variables[:]
        del self.whendos[:]

    def engine_process(self, script):
        if ' do ' in script:
            parts = script.split(' do ')
            when, do = parts[0].replace('when ',''), parts[1]
            whendo1 = whendo(when, do)
            self.whendos.append(whendo1)
        elif '=' in script:
            self.evaluate(script)
        elif script.strip() != '':
            return myeval.eval_expr(self.substitute(script))

    def engine_execution_loop(self): #todo event driven execution
        for whendo in self.whendos:
            if self.evaluate(whendo.when):
                if ';' in whendo.do:
                    dos = whendo.do.split(';')
                    for do in dos:
                        self.evaluate(do)
                else:
                    self.evaluate(whendo.do)
            time.sleep(0.3)

    def evaluate(self, exp):
        if ' or ' in exp:
            exps = exp.split(' or ')
            for ex in exps:
                if self.evaluate(ex):
                    return True
            return False
        elif ' and ' in exp:
            exps = exp.split(' and ')
            for ex in exps:
                if not self.evaluate(ex):
                    return False
            return True
        else:
            if '==' in exp:
                exps = exp.split('==')
                lhs, rhs = exps[0].strip(), exps[1].strip()
                return myeval.eval_expr(self.substitute(lhs)) == myeval.eval_expr(self.substitute(rhs))
            elif '!=' in exp:
                exps = exp.split('!=')
                lhs, rhs = exps[0].strip(), exps[1].strip()
                return myeval.eval_expr(self.substitute(lhs)) != myeval.eval_expr(self.substitute(rhs))
            elif '>=' in exp:
                exps = exp.split('>=')
                lhs, rhs = exps[0].strip(), exps[1].strip()
                return myeval.eval_expr(self.substitute(lhs)) >= myeval.eval_expr(self.substitute(rhs))
            elif '<=' in exp:
                exps = exp.split('<=')
                lhs, rhs = exps[0].strip(), exps[1].strip()
                return myeval.eval_expr(self.substitute(lhs)) <= myeval.eval_expr(self.substitute(rhs))
            elif '>' in exp:
                exps = exp.split('>')
                lhs, rhs = exps[0].strip(), exps[1].strip()
                return myeval.eval_expr(self.substitute(lhs)) > myeval.eval_expr(self.substitute(rhs))
            elif '<' in exp:
                exps = exp.split('<')
                lhs, rhs = exps[0].strip(), exps[1].strip()
                return myeval.eval_expr(self.substitute(lhs)) < myeval.eval_expr(self.substitute(rhs))
            elif '=' in exp:
                exps = exp.split('=')
                lhs, rhs = exps[0].strip(), exps[1].strip()
                if lhs == 'remote':
                    if '[' in rhs:
                        ll = rhs.split('[')
                        node = ll[0]
                        index = ll[1][:-1]
                        if index.startswith("'"):
                            comm.send(node, 'get' + index.strip("'")) #  ,' remote'
                        else:
                            comm.send(node, 'getportvalue', index) # + ' remote')
                elif '[' in lhs:
                    ll = lhs.split('[')
                    node = ll[0]
                    index = ll[1][:-1]
                    if not index.startswith("'"):
                        comm.send(node, 'setportvalue', index, str(myeval.eval_expr(self.substitute(rhs)))) # + ' remote')
                    return self.assign(lhs, myeval.eval_expr(self.substitute(rhs)))
                else:
                    return self.assign(lhs, myeval.eval_expr(self.substitute(rhs)))

    def assign(self, variable, value):
        self.variables[variable] = value
        return value

    def substitute(self, exp):
        #print exp
        words = re.split(r'([+-/*])',exp)
        for word in words:
            word = word.strip()
            if word == 'time':
                exp = exp.replace(word, str(time.time()))
            elif '[' in word:
                ll = word.split('[')
                node = ll[0]
                index = ll[1][:-1]
                '''
                if index.startswith("'"):
                    comm.send(node, 'get' + index.strip("'")) #  ,' remote'
                else:
                    comm.send(node, 'getportvalue', index) # + ' remote')
                '''
                if word in self.variables.keys():
                    exp = exp.replace(word, str(self.variables[word]))
                elif node == 'time':
                    index = index.strip("'")
                    if index == 'hour':
                        exp = exp.replace(word, str(time.localtime(time.time()).tm_hour))
                    elif index == 'minute':
                        exp = exp.replace(word, str(time.localtime(time.time()).tm_min))
                    elif index == 'second':
                        exp = exp.replace(word, str(time.localtime(time.time()).tm_sec))
                    elif index == 'year':
                        exp = exp.replace(word, str(time.localtime(time.time()).tm_year))
                    elif index == 'month':
                        exp = exp.replace(word, str(time.localtime(time.time()).tm_mon))
                    elif index == 'mday':
                        exp = exp.replace(word, str(time.localtime(time.time()).tm_mday))
                    elif index == 'wday':
                        exp = exp.replace(word, str(time.localtime(time.time()).tm_wday))
                    elif index == 'yday':
                        exp = exp.replace(word, str(time.localtime(time.time()).tm_yday))
                else:
                    pass
                    # exp = exp.replace(word, 0)
            elif word in self.variables.keys():
                exp = exp.replace(word, str(self.variables[word]))
        return exp


    def addscript(self, script):
        for line in script.splitlines():
            self.engine_process(line)

    def addinteractive(self, line):
        return self.engine_process(line)

    def ProcessCommand(self, cmd):
        try:
            Command = cmd['command']
            Params = cmd['params']
            Sender = cmd['sender']

            if Command == 'portvalue':
               self.variables[Sender + '[' + Params[0] + ']'] = Params[1]
            elif Command == 'temperature' or Command == 'humidity':
                self.variables[Sender + "['" + Command +"']"] = Params[0]
            elif len(Params)==1:
                self.variables[Sender + "['" + Command +"']"] = Params[0]
        except:
            pass


script = '''var = time
when time - var > 10 do NODE04[3]=0; var=time
'''

'''
alarm = 0
delay = time
when NODE001[17]==1 do alarm=1
when alarm==1 do NODE002[4]=1; delay=time; alarm = 0
when alarm==1 and time['second']>10 and time['second']<20 do NODE002[0]=1; delay=time; alarm = 0
when time-delay > 2 do NODE002[4]=0
'''

'''
myvar = time
humidwait = time
var = 0
temp = 0
port3Ondone = 0
port3Offdone = 0
when time - myvar >= 30 do temp = LOCK001['temperature']; myvar = time
when time - humidwait >= 5 do var = LOCK001[2]; humidwait = time
when var == 1 do remote = LOCK001['humidity']; LOCK001[2] = 0; var = 0
when port3Ondone == 0 and temp >= 34 do LOCK001[3] = 1; port3Ondone = 1; port3Offdone = 0
when port3Offdone == 0 and temp < 34 do LOCK001[3] = 0; port3Ondone = 0; port3Offdone = 1
'''


'''
myvar = time
when time - myvar >= 10 do remote = LOCK001['temperature']; myvar = time
when LOCK001[2] == 1 do remote = LOCK001['humidity']; LOCK001[2] = 0
when LOCK001['temperature'] >= 35 and LOCK001[3] == 0 do LOCK001[3] = 1
when LOCK001['temperature'] < 35 and LOCK001[3]==1 do LOCK001[3] = 0
'''

#Handles LAN
def local_server():
    #local server
    myHost = ''  # server machine, '' means local host
    myPort = 10002  # listen on a non-reserved port number

    sockobj = socket(AF_INET, SOCK_STREAM)  # make a TCP socket object
    sockobj.bind((myHost, myPort))  # bind it to server port number
    sockobj.listen(5)  # allow up to 5 pending connects
    dispatcher(sockobj)

def handleClient(connection,addr): # in spawned thread: reply
    connection.sendall('Welcome to IoTScript\n>>')
    while True:
        try:
            command = connection.recv(1024)
            #print('tcp:'+command)
            if command.strip() == 'quit':
                break
            else:
                resp = se.addinteractive(command)
                if resp != None:
                    connection.send(str(resp))
                connection.sendall('\n>>')
        except Exception as error:
            print(error)
            connection.sendall(str(error) + '\n')

    connection.close()


def dispatcher(sockobj): # listen until process killed
    print('starting local TCP server ... \n')
    while True: # wait for next connection,
        connection, address = sockobj.accept() # pass to thread for service

        if len(sys.argv) >= 2 and sys.argv[1] == 'Secure':
            connection = ssl.wrap_socket(connection,
                                         certfile="cert.pem",
                                         ssl_version=ssl.PROTOCOL_SSLv23,
                                         server_side=True)

        thread.start_new_thread(handleClient, (connection, address,))

config = configparser.RawConfigParser()
config.read('cp.cfg')
user = str(config.get('user', 'account_name'))
password = str(config.get('user', 'password'))

comm = IoTComm(account=user, password=password)
comm.debug = True
se = ScripingEnging(comm)
comm.process = se.ProcessCommand
comm.address = 'remote'
comm.startMqttListener()
se.addscript(script)
thread.start_new_thread(local_server, ())
while True:
    try:
        se.engine_execution_loop()
    except:
        pass
    #time.sleep(0.2)