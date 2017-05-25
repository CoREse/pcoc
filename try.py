from client import *

I=Host()
me=Player("CRE","127.0.0.1")
I.Players.update({me.PLID:me});
I.setMe(me)
I.saveHost()

ACC=Client(I)

ACC.startServer()

ACC.initial("CRE", "127.0.0.1")
ACC.start("CRE")
