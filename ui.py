#!/usr/bin/python

from client import *
from game import *
from socket import *
import sys

MyHost=Host()
MyHost.loadHost()

C=Client(MyHost)

def getIp():
    S=socket(AF_INET, SOCK_DGRAM)
    try:
        S.connect(("www.baidu.com"), 80)
        IP=S.getsockname()[0]
    except:
        IP='127.0.0.1'
    finally:
        S.close()
    return IP

def createMe():
    print("Please create your player(not pc) by enter your name:")
    Name=input()
    Me=Player(Name,getIp())
    return Me

Server=None
try:
    while (True):
        if C.MyHost.Me=="":
            Me=createMe()
            C.MyHost.setMe(Me)
        if Server==None:
            Server=C.startServer()
        Command=input()
        SC=Command.split(" ")
        if Command=="help":
            printHelp()
        elif SC[0]=="exit":
            sys.exit()
        elif SC[0]=="!":
            exec(Command[1:])
        elif SC[0]=="show":
            if SC[1]=="pcs":
                if C.CG==None:
                    for k in C.MyHost.pcs:
                        print(C.MyHost.pcs[k])
                else:
                    pcs=C.MyHost.getPcs(C.CG[0])
                    for k in pcs:
                        print(pcs[k])

except (KeyboardInterrupt, SystemExit):
    if Server!=None:
        Server.terminate()
    sys.exit()

def printHelp():
    print("help:\tshow this text.\nexit:\texit.\n!command:\texecute python command")
