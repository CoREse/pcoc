import random
class Dice(object):
    def __init__(self, S):
        self.Sides=S

    def d4():
        return Dice(4)

    def d10():
        return Dice(10)

    def d6():
        return Dice(6)

    def d20():
        return Dice(20)

    def d100():
        return Dice(100)

    def roll(self, Times=1):
        random.seed()
        Result=0
        for i in range(Times):
            Result+=random.randrange(self.Sides)+1#The dice has minimum value 1
        return Result
