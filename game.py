from pc import pc
from dice import Dice
import time
import json

class Player(object):
    def __init__(self, ID, ip=""):
        self.PLID=ID+str(time.time())
        self.ip=ip

    def setIp(self, ip):
        self.ip=ip

    def toList(self):
        TheL=[self.PLID,self.ip]
        return TheL
    def fromList(self, TheL):
        self.PLID=TheL[0]
        self.ip=TheL[1]
    def loadFromList(TheL):
        Obj=Player("")
        Obj.fromList(TheL)
        return Obj

class Game(object):
    def __init__(self, SGID):
        self.GID=SGID+str(time.time())
        self.SGID=SGID
        self.pcs=[]#PID
        self.kp=""
    def toList(self):
        TheL=[self.GID,self.SGID,self.kp]
        TheL+=self.pcs
        return TheL
    def fromList(self, TheL):
        self.GID=TheL[0]
        self.SGID=TheL[1]
        self.kp=TheL[2]
        self.pcs=TheL[3:]
    def loadFromList(TheL):
        Obj=Game("")
        Obj.fromList(TheL)
        return Obj

class Host(object):
    def __init__(self):
        self.Players={}#p.PLID:p
        self.Games={}#g.SGID:g
        self.pcs={}#p.PID:p
        self.Me=""

    def saveHost(self):
        self.saveMe()
        self.savePlayers()
        self.saveGames()
        self.savePcs()

    def loadHost(self):
        self.loadMe()
        self.loadPlayers()
        self.loadGames()
        self.loadPcs()

    def setMe(self, Me):
        self.Me=Me.PLID

    def saveMe(self):
        with open('data/me.json', 'w' ) as pFp:
            json.dump({"MyPLID":self.Me}, pFp)
    def loadMe(self):
        with open('data/me.json', 'r') as pFp:
            Data=json.load(pFp)
            self.Me=Data["MyPLID"]
         
    def savePlayers(self):
        with open('data/players.json', 'w' ) as pFp:
            Players={}
            for pk in self.Players:
                Players[self.Players[pk].PLID]=self.Players[pk].toList()
            json.dump(Players, pFp)

    def saveGames(self):
        with open('data/games.json', 'w') as pFp:
            Games={}
            for gk in self.Games:
                Games[self.Games[gk].SGID]=self.Games[gk].toList()
            json.dump(Games,pFp)

    def savePcs(self):
        with open('data/pcs.json', 'w') as pFp:
            pcs={}
            for pk in self.pcs:
                pcs[self.pcs[pk].PID]=self.pcs[pk].toList()
            json.dump(pcs,pFp)

    def loadPlayers(self):
        with open('data/players.json', 'r') as pFp:
            Data=json.load(pFp)
            for k in Data:
                self.Players[k]=Player.loadFromList(Data[k])
    def loadGames(self):
        with open('data/games.json', 'r') as pFp:
            Data=json.load(pFp)
            for k in Data:
                self.Games[k]=Game.loadFromList(Data[k])
    def loadPcs(self):
        with open('data/pcs.json', 'r') as pFp:
            Data=json.load(pFp)
            for k in Data:
                self.pcs[k]=pc.loadFromList(Data[k])

    def savePlayer(self, PLID):
        with open("data/player%s.json"%PLID, 'w') as pFp:
            json.dump({PLID:self.Players[PLID].toList()}, pFp)
    def loadPlayer(self, PLID):
        with open("data/player%s.json"%PLID, 'r') as pFp:
            Data=json.load(pFp)
            self.Players[PLID]=Player.loadFromList(Data[PLID])
    def saveGame(self, SGID):
        with open("data/game%s.json"%SGID, 'w') as pFp:
            json.dump({SGID:self.Games[SGID].toList()}, pFp)
    def loadGame(self, PLID):
        with open("data/game%s.json"%SGID, 'r') as pFp:
            Data=json.load(pFp)
            self.Games[SGID]=Game.loadFromList(Data[SGID])
    def savePc(self, PID):
        with open("data/pc%s.json"%PID, 'w') as pFp:
            json.dump({PID:self.pcs[PID].toList()}, pFp)
    def loadPc(self, PID):
        with open("data/pc%s.json"%PID, 'r') as pFp:
            Data=json.load(pFp)
            self.pcs[PID]=pc.loadFromList(Data[PID])

"""
H=Host()
H.Games["CRE"]=Game("CRE")
me=Player("CRE","127.0.0.1")
H.Players.update({me.PLID:me});
apc=pc()
apc.genAtts()
apc.setAge(34)
H.pcs[apc.PID]=apc
H.setMe(me)
H.saveHost()
I=Host()
I.loadHost()
print(I.Me)
print(I.Players)
print(I.Games)
print(I.pcs)
for k in I.pcs:
    print (I.pcs[k])
"""
