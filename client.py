from game import *
from socket import *
from multiprocessing import Process

class Client(object):
    Port=2466
    def __init__(self, MyHost):
        self.MyHost=MyHost
        self.kpIp=""

    def initial(self, SGID, ip, Port=2466):
        #send HELO MyHost and Get game, presume you don't have the game
        SGID=str(SGID)
        ClientSocket=socket(AF_INET,SOCK_STREAM)
        ClientSocket.connect((ip,Port))
        ClientSocket.send(("HELO " + self.MyHost.Me).encode('utf-8'))
        Message=ClientSocket.recv(1024)
        if Message[:2]=='OK':
            self.MyHost.Players[Message[3:]]=Player.loadFromList([Message[3:],ip])
            MyHost.savePlayers()
        ClientSocket.send("GET GAME "+SGID)
        Message=ClientSocket.recv(1024)
        if Message[:2]=="OK":
            with open("data/game%s.json"%SGID, "wb") as pFp:
                Message=ClientSocket.recv(4096)
                while(Message):
                    pFp.write(Message)
                    Message=ClientSocket.recv(4096)
        MyHost.loadGame(SGID)
        if MyHost.Games[SGID].kp not in MyHost.Players:
            ClientSocket.settimeout(5.0)
            Message=ClientSocket.recv(1024)
            ClientSocket.settimeout(None)
            if Message[:6]=="PLAYER":
                MyHost.Players[Message.split(" ")[1]]=Player.loadFromList(Message.split(" ")[1:])
                print("Retrieved the game and the kp information!")
            else:
                print("Retrieved the game but don't have kp information!")

        print("Retrieved the game and we already have the kp information!")

    def listen(self, Port=2466):
        SS=socket(AF_INET,SOCK_STREAM)
        SS.bind(('',Port))
        SS.listen(10)
        while True:
            CS, Addr=SS.accept()
            Message=SS.recv(4096)
            print (Message)
            SM=Messages.split(" ")
            if SM[0]=="HELO":
                CS.send(("OK "+ MyHost.Me).encode("utf-8"))
            elif SM[0]=="GET" and SM[1]=="GAME":
                if SM[3] in MyHost.Games:
                    CS.send("OK")
                    MyHost.saveGame(SM[3])
                    with open("data/game%s.json"%SM[3], "rb") as pFp:
                        Message=pFp.read(4096)
                        while Message:
                            CS.send(Message)
                            Message.read(4096)
                    if MyHost.Games[SM[3]].kp in MyHost.Players:
                        CS.send("PLAYER %s %s"%(MyHost.Games[SM[3]].kp,MyHost.Players[MyHost.Games[SM[3]].kp].ip))
                else:
                    CS.send("NO")


