from dice import Dice
import time
d4=Dice.d4()
d6=Dice.d6()
d10=Dice.d10()
d20=Dice.d20()
d100=Dice.d100()

class pc(object):
    def __init__(self, ID=""):
        self.PID=ID+str(time.time())
        self.Name=""
        self.Description=""
        self.Sex=""
        self.Age=0
        self.STR=0
        self.CON=0
        self.SIZ=0
        self.DEX=0
        self.APP=0
        self.INT=0
        self.POW=0
        self.EDU=0
        self.LUC=0
    
    def __str__(self):
        return "PID:%s\nName:%s\tSex:%s\tAge:%d\nDescription:%s\nSTR:%d\tCON:%d\tSIZ:%d\tDEX:%d\nAPP:%d\tINT:%d\tPOW:%d\tEDU:%d\nLUC:%d" % (self.PID,self.Name,self.Sex, self.Age, self.Description, self.STR,self.CON,self.SIZ,self.DEX, self.APP,self.INT,self.POW,self.EDU, self.LUC)

    def toList(self):
        return [self.PID,self.Name,self.Description, self.Sex, self.Age, self.STR, self.CON, self.SIZ, self.DEX, self.APP, self.INT, self.POW, self.EDU, self.LUC]
    def fromList(self,TheL):
        [self.PID,self.Name,self.Description, self.Sex, self.Age, self.STR, self.CON, self.SIZ, self.DEX, self.APP, self.INT, self.POW, self.EDU, self.LUC]=TheL
    def loadFromList(TheL):
        Obj=pc()
        Obj.fromList(TheL)
        return Obj

    def genSTR(self):
        self.STR=d6.roll(3)
        self.STR*=5
    def genCON(self):
        self.CON=d6.roll(3)
        self.CON*=5
    def genSIZ(self):
        self.SIZ=d6.roll(2)+6
        self.SIZ*=5
    def genDEX(self):
        self.DEX=d6.roll(3)
        self.DEX*=5
    def genAPP(self):
        self.APP=d6.roll(3)
        self.APP*=5
    def genINT(self):
        self.INT=d6.roll(2)+6
        self.INT*=5
    def genPOW(self):
        self.POW=d6.roll(3)
        self.POW*=5
    def genEDU(self):
        self.EDU=d6.roll(2)+6
        self.EDU*=5
    def genLUC(self):
        self.LUC=d6.roll(3)
        self.LUC*=5

    def genAtts(self):
        self.genSTR()
        self.genCON()
        self.genSIZ()
        self.genDEX()
        self.genAPP()
        self.genINT()
        self.genPOW()
        self.genEDU()
        self.genLUC()

    def educate(self,Times=1):
        for i in range(Times):
            if (d100.roll()>self.EDU):
                self.EDU+=d10.roll()
                if (self.EDU>99):
                    self.EDU=99

    def setAge(self, Age):
        if (Age in range(15,90)):
            self.Age=Age
            if (Age<20):
                self.STR-=5
                self.SIZ-=5
            elif (Age<40):
                self.educate()
            elif (Age<50):
                self.educate(2)
                self.APP-=5
            elif (Age<60):
                self.educate(3)
                self.APP-=10
            elif (Age<70):
                self.educate(4)
                self.APP-=15
            elif (Age<80):
                self.educate(4)
                self.APP-=20
            else:
                self.educate(4)
                self.APP-=25
