import image
import time
import random
import data_object

class ObjectBase(image.Image):
    def __init__(self, id, pos):
        self.id = id
        self.preIndexTime = 0
        self.prePositionTime = 0
        self.preSummonTime = 0
        self.hp = self.getData()['HP']
        self.attack = self.getData()['ATT']
        super(ObjectBase, self).__init__(
            self.getData()['PATH'],
            0,
            pos,
            self.getData()['SIZE'],
            self.getData()['IMAGE_INDEX_MAX'])
        
    def getData(self):
        return data_object.data[self.id]

    def getPositionCD(self):
        return self.getData()['POSITION_CD']
    
    def getImageIndexCD(self):
        return self.getData()['IMAGE_INDEX_CD']
    
    def getSummonCD(self):
        return self.getData()['SUMMON_CD']
    
    def getSpeed(self):
        return self.getData()['SPEED']
    
    def canLoot(self):
        return self.getData()['CAN_LOOT']
    
    def getSunLight(self):
        return self.getData()['PRICE']
    
    def isCollide(self, other):
        return self.getRect().colliderect( other.getRect() )

    def update(self, zombiesRow: dict):
        self.checkSummon(zombiesRow)
        self.checkImageIndex()
        self.checkPosition()

    def checkSummon(self, zombiesRow: dict):
        CD = self.getSummonCD()
        if time.time() - self.preSummonTime <= CD:
            return
        self.preSummonTime = time.time()
        self.preSummon(zombiesRow)

    def checkImageIndex(self):
        CD = self.getImageIndexCD()
        if time.time() - self.preIndexTime <= CD:
            return
        self.preIndexTime = time.time()

        idx = self.pathIndex + 1
        if idx >= self.pathIndexCount:
            idx = 0
        self.updateIndex(idx)

    def checkPosition(self):
        CD = self.getPositionCD()
        if time.time() - self.prePositionTime <= CD:
            return False
        self.prePositionTime = time.time()
        speed = self.getSpeed()
        self.pos[0] += speed[0]
        self.pos[1] += speed[1]
        return True
    
    def preSummon(self, zombiesRow: dict):
        pass

    def hasSummon(self):
        pass

    def doSummon(self):
        pass