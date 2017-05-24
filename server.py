from client import *
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

AC=Client(H)
AC.listen()
#p=Process(target=AC.listen, args=())
#p.start()

#p.join()
