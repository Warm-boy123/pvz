import objectbase
import peabullet
import time
from const import *

from sound import *

class PeaShooter(objectbase.ObjectBase):
    def __init__(self, id, pos):
        super(PeaShooter, self).__init__(id, pos)
        self.hasShoot = False   # 是否需要射击
        self.hasPeabullet = False   # 是否到达射击帧
        self.pathIndex = 9
        self.shootFlag = 1

    def preSummon(self, zombiesRow: dict):
        if zombiesRow[str(int((self.pos[1] - LEFT_TOP[1]) / GRID_SIZE[1]))] > 0:
            self.hasShoot = True
            self.pathIndex = 0
            self.shootFlag = 1
            peaSound.play()

    def hasSummon(self):
        return self.hasPeabullet
    
    def doSummon(self):
        if self.hasSummon():
            self.hasPeabullet = False
            return peabullet.PeaBullet(0, (self.pos[0] + self.size[0] - 10, self.pos[1] + 40))

    def checkImageIndex(self):
        CD = self.getImageIndexCD()
        if time.time() - self.preIndexTime <= CD:
            return
        self.preIndexTime = time.time()
        if self.shootFlag == 1:
            idx = self.pathIndex + 1
            if idx == 8 and self.hasShoot:
                self.hasPeabullet = True
            if idx > 14:
                idx = 14
                self.shootFlag = -1
        elif self.shootFlag == -1:
            idx = self.pathIndex - 1
            if idx < 9:
                idx = 9
                self.shootFlag = 1
        self.updateIndex(idx)