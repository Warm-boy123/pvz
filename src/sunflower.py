import objectbase
import sunlight
import time
import random

from sound import *

class SunFlower(objectbase.ObjectBase):
    def __init__(self, id, pos):
        super(SunFlower, self).__init__(id, pos)
        self.hasSunlight = False
        # 使向日葵的第一个阳光达到随机效果
        self.preSummonTime = time.time() + random.random() * self.getSummonCD()

    def preSummon(self, zombiesRow: dict):
        self.hasSunlight = True

    def hasSummon(self):
        return self.hasSunlight
    
    def doSummon(self):
        if self.hasSummon():
            self.hasSunlight = False
            # sunlightSound.play()
            return sunlight.SunLight(2, (self.pos[0] + 20, self.pos[1] - 10))
