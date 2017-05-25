from game import *
from socket import *
from multiprocessing import Process
import time

class Client(object):
    Port=2466
    def __init__(self, MyHost):
        self.MyHost=MyHost
        self.kpIp=""
        self.CG=None#Current game CS

    def initial(self, SGID, ip, Port=2466):
        #send HELO MyHost and Get game, presume you don't have the game
        SGID=str(SGID)
        ClientSocket=socket(AF_INET,SOCK_STREAM)
        ClientSocket.connect((ip,Port))
        self.helo(ClientSocket)
        ClientSocket.send(("GET GAME "+SGID).encode("utf-8"))
        Message=ClientSocket.recv(1024).decode("utf-8")
        if Message=="OK":
            self.recvFile("data/game%s.json"%SGID, ClientSocket)
            self.MyHost.loadGame(SGID)
        else:
            print("Can't retrieve the game %s!"%SGID)
            ClientSocket.shutdown(SHUT_RDWR)
            return
        if self.MyHost.Games[SGID].kp!='' and (self.MyHost.Games[SGID].kp not in self.MyHost.Players):
            ClientSocket.send(("GET PLAYER %s"%self.MyHost.Games[SGID].kp).encode("utf-8"))
            #ClientSocket.settimeout(5.0)
            Message=ClientSocket.recv(1024).decode("utf-8")
            #ClientSocket.settimeout(None)
            SM=Message.split(" ")
            if SM[0]=="PLAYER":
                self.MyHost.Players[SM[1]]=Player.loadFromList(SM[1:])
                print("Retrieved the game and the kp information!")
            else:
                print("Retrieved the game but don't have kp information!")

        elif self.MyHost.Games[SGID].kp=='':
            print("Retrieved the game but this game(%s) has no kp!"%SGID);
        else:
            print("Retrieved the game and we have the kp information!")
        ClientSocket.shutdown(SHUT_RDWR)

    def helo(self, CS):
        CS.send(("HELO " + self.MyHost.Me).encode('utf-8'))
        Message=CS.recv(1024).decode("utf-8")
        if Message[:2]=='OK':
            self.MyHost.Players[Message[3:]]=Player.loadFromList([Message[3:],CS.getpeername()[0]])
            self.MyHost.savePlayers()
 
    def getPlayer(self, PLID, CS):
        CS.send(("GET PLAYER %s"%PLID).encode("utf-8"))
        Message=CS.recv(1024).decode("utf-8")
        SM=Message.split(" ")
        if SM[0]=="PLAYER":
            self.MyHost.Players[SM[1]]=Player.loadFromList(SM[1:])
            self.MyHost.savePlayers()
            return True
        else:
            return False

    def close(self):
        if self.CG!=None:
            self.CG.shutdown(SHUT_RDWR)
            print("You've shutdown the game connection for %s."%self.CG[1])
            self.CG=None
        else:
            print("There is no current game connection.")

    def start(self, SGID):
        self.close()
        if SGID not in self.MyHost.Games:
            print("We don't have the game %s yet!"%SGID)
            return
        if self.MyHost.Games[SGID].kp=='':
            print("The game %s don't have a kp!"%SGID)
            return
        if self.MyHost.Games[SGID].kp not in self.MyHost.Players:
            print("We don't have the ip address of kp %s"%self.MyHost.Games[SGID].kp)
            return
        kp=self.MyHost.Games[SGID].kp
        ip=self.MyHost.Players[kp].ip
        CS=socket(AF_INET, SOCK_STREAM)
        CS.connect((ip,2466))
        self.helo(CS)
        print("You've successfully connected to the kp(PLID:%s, ip:%s) of game %s!"%(kp,ip,SGID))
        self.CG=[SGID,CS]
        return CS
    
    def startServer(self, Port=2466):
        P=Process(target=self.listen, args=())
        P.start()
        time.sleep(1)
        return P

    def listen(self, Port=2466):
        SS=socket(AF_INET,SOCK_STREAM)
        SS.bind(('',Port))
        SS.listen(10)
        while True:
            CS, Addr=SS.accept()
            while True:
                try:
                    Message=CS.recv(4096).decode("utf-8")
                except socket.error:
                    break
                if(Message):
                    print("server:%s"%Message)
                else:
                    break
                #print (Message)
                SM=Message.split(" ")
                if SM[0]=="HELO":
                    CS.send(("OK "+ self.MyHost.Me).encode("utf-8"))
                elif SM[0]=="GET" and SM[1]=="GAME":
                    if SM[2] in self.MyHost.Games:
                        CS.send("OK".encode("utf-8"))
                        self.MyHost.saveGame(SM[2])
                        self.sendFile("data/game%s.json"%SM[2], CS)
                    else:
                        CS.send("NO".encode("utf-8"))
                elif SM[0]=="GET" and SM[1]=="PLAYER":
                    if self.MyHost.Games[SM[2]].kp in self.MyHost.Players:
                            CS.send(("PLAYER %s %s"%(self.MyHost.Games[SM[2]].kp,self.MyHost.Players[self.MyHost.Games[SM[2]].kp].ip)).encode("utf-8"))
                    else:
                        CS.send("NO".encode("utf-8"))

    def sendFile(self, FileName, CS):
        with open(FileName, "rb") as pFp:
            Message=pFp.read(255)
            while Message:
                Message=bytes([len(Message)])+Message
                CS.send(Message)
                Message=pFp.read(255)
            CS.send(bytes([0]))

    def recvFile(self, FileName, CS):
        with open(FileName, "wb") as pFp:
            Message=CS.recv(1)
            while Message!=bytes([0]):
                Message=CS.recv(ord(Message))
                print("Message:%s"%Message)
                pFp.write(Message)
                Message=CS.recv(1)
            print("Message:%s"%Message)


