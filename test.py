import random


class test:
    def __init__(self):
        self.muddis = []
        self.muddis.append(test2(random.random()))
        self.muddis.append(test2(random.random()))
        self.muddis.append(test2(random.random()))


class test2:
    def __init__(self, prob):
        prob = prob


t = test()
print(t.muddis)

radius = 1
numberx = 3
numbery = 3
for i in range(numberx-radius, numberx+radius+1):
    for j in range(numbery-radius, numbery+radius+1):
        if(not(i < 0 or j < 0) and not (i == numberx and j == numbery)):
            print("x: "+str(i)+", y: "+str(j))
