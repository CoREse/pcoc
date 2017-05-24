from client import *

H=Host()
me=Player("CRE","127.0.0.1")
H.Players.update({me.PLID:me});
H.setMe(me)
H.saveHost()

AC=Client(H)

AC.initial("CRE", "127.0.0.1")

