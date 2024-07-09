import image
import pygame
import data_object
from const import *
import sunflower
import peashooter
import zombiebase
import random
import time

from sound import *

class Game(object):
    def __init__(self, DS):
        self.DS = DS
        self.back = image.Image(PATH_BACK, 0,(0, 0), GAME_SIZE, 0)
        self.lose = image.Image(PATH_LOSE, 0,(0, 0), GAME_SIZE, 0)
        self.isGameOver = False
        self.sunlightCount = image.Image(SUNLIGHT_BACK, 0, (150, 0), (77, 87), 0)
        self.plants = []
        self.summons = []
        self.hasPlants = []
        self.zombies = []
        self.zombiesRow = {'0': 0, '1': 0, '2':0, '3': 0, '4': 0}
        self.sunLight = 10000
        self.sunLightFont = pygame.font.Font(None, 25)
        self.zombieGenerateTime = 0
        for i in range(GRID_COUNT[0]):
            cal = []
            for j in range(GRID_COUNT[1]):
                cal.append(0)
            self.hasPlants.append(cal)

        self.zombieScore = 0
        self.zombieFont = pygame.font.Font(None, 50)

    def checkSummonVSZombie(self):
        for summon in self.summons:
            if summon.id != 2:
                for zombie in self.zombies:
                    if summon.isCollide(zombie):
                        self.fight(summon, zombie)
                        beatSound.play()
                        if zombie.hp <= 0:
                            self.zombies.remove(zombie)
                            self.zombieScore += 1
                            self.zombiesRow[str(zombie.row)] -= 1
                        if summon.hp <= 0:
                            self.summons.remove(summon)
                        return

    def checkZombieVSPlant(self):
        for zombie in self.zombies:
            for plant in self.plants:
                if zombie.isCollide(plant):
                    self.fight(zombie, plant)
                    if plant.hp <= 0:
                        eatSound.play()
                        self.plants.remove(plant)
                        break

    def getIndexByPos(self, pos):
        x = (pos[0] - LEFT_TOP[0]) // GRID_SIZE[0]
        y = (pos[1] - LEFT_TOP[1]) // GRID_SIZE[1]
        return x, y

    # 绘制
    def draw(self):
        if self.isGameOver:
            return
        # 绘制背景
        self.DS.fill( (255, 255, 255) )
        self.back.draw(self.DS)
        self.sunlightCount.draw(self.DS)
        # 绘制植物
        for plant in self.plants:
            plant.draw(self.DS)
        # 绘制僵尸
        for zombie in self.zombies:
            zombie.draw(self.DS)
        # 绘制召唤
        for summon in self.summons:
            summon.draw(self.DS)
        # 渲染字体
        self.renderFont()

    # 绘制阳光数量
    def renderFont(self):
        # render函数将文字对象Font转换为图像(image)
        textImage = self.sunLightFont.render(str(self.sunLight), True, (255, 255, 255))
        self.DS.blit(textImage, (173, 68))
        textImage = self.sunLightFont.render(str(self.sunLight), True, (0, 0, 0))
        self.DS.blit(textImage, (170, 65))

        textImage = self.zombieFont.render('Score: ' + str(self.zombieScore), True, (0, 0, 0))
        self.DS.blit(textImage, (13, 23))
        textImage = self.zombieFont.render('Score: ' + str(self.zombieScore), True, (255, 255, 255))
        self.DS.blit(textImage, (10, 20))
        

    # 更新元素
    def update(self):
        # print(self.zombiesRow)
        if self.isGameOver:
            return
        self.back.update(self.DS, self.zombiesRow)
        for plant in self.plants:
            plant.update(self.zombiesRow)
            if plant.hasSummon():
                summ = plant.doSummon()
                self.summons.append(summ)
        for summon in self.summons:
            summon.update(self.zombiesRow)
        for zombie in self.zombies:
            zombie.update(self.zombiesRow)
        
        if time.time() - self.zombieGenerateTime > 5:
            self.zombieGenerateTime = time.time()
            if random.random() < 0.3:
                zombieSound.play()
            row = random.randint(0, 4)
            self.zombiesRow[str(row)] += 1
            self.addZombie(14, row)

        self.checkSummonVSZombie()
        self.checkZombieVSPlant()

        # 检查游戏是否结束
        for zombie in self.zombies:
            if zombie.getRect().x < LEFT_TOP[0]:
                self.isGameOver = True
                pygame.mixer.music.stop()
                loseSound.play()
                self.lose.draw(self.DS)

        # 防止内存泄漏
        for summon in self.summons:
            if summon.getRect().x > GAME_SIZE[0] or summon.getRect().y > GAME_SIZE[1]:
                self.summons.remove(summon)
                break
        # print(len(self.summons))

    # 添加向日葵
    def addSunFlower(self, x, y):
        self.plants.append(sunflower.SunFlower(SUNFLOWER_ID, (LEFT_TOP[0] + x * GRID_SIZE[0], LEFT_TOP[1] + y * GRID_SIZE[1])))

    # 添加豌豆射手
    def addPeaShooter(self, x, y):
        self.plants.append(peashooter.PeaShooter(PEASHOOTER_ID, (LEFT_TOP[0] + x * GRID_SIZE[0], LEFT_TOP[1] + y * GRID_SIZE[1])))

    def addZombie(self, x, y):
        self.zombies.append(zombiebase.ZombieBase(ZOMBIE_ID, (LEFT_TOP[0] + x * GRID_SIZE[0], LEFT_TOP[1] + y * GRID_SIZE[1]), y))

    def fight(self, a, b):
        while True:
            a.hp -= b.attack
            b.hp -= a.attack
            if b.hp <= 0:
                return True
            if a.hp <= 0:
                return False
        return False

    # 检查鼠标点击
    def checkLoot(self, mousePos):
        for summon in self.summons:
            if not summon.canLoot():
                continue
            rect = summon.getRect()
            if rect.collidepoint(mousePos):
                # 获取阳光
                self.summons.remove(summon)
                sunlightSound.play()
                self.sunLight += summon.getSunLight()
                return True
        return False

    # 判断添加植物
    def checkAddPlant(self, mousePos, objId):
        x, y = self.getIndexByPos(mousePos)
        if x < 0 or x >= GRID_COUNT[0] or y < 0 or y >= GRID_COUNT[1]:
            # print('out of range')
            return
        if self.sunLight < data_object.data[objId]['PRICE']:
            return
        if self.hasPlants[x][y] == 1:
            # print('already has plant')
            return
        else:
            self.hasPlants[x][y] = 1
            self.sunLight -= data_object.data[objId]['PRICE']
            if objId == SUNFLOWER_ID:
                self.addSunFlower(x, y)
            elif objId == PEASHOOTER_ID:
                self.addPeaShooter(x, y)
            plantSound.play()

    def checkDeletePlant(self, mousePos):
        x, y = self.getIndexByPos(mousePos)
        if x < 0 or x >= GRID_COUNT[0] or y < 0 or y >= GRID_COUNT[1]:
            return
        if self.hasPlants[x][y] == 1:
            pass
            

    # 鼠标点击事件
    def mouseClickHandler(self, btn):
        if self.isGameOver:
            return
        mousePos = pygame.mouse.get_pos()
        # print(mousePos)
        if self.checkLoot(mousePos):
            return
        if btn == 1:
            self.checkAddPlant(mousePos, SUNFLOWER_ID)
        elif btn == 3:
            self.checkAddPlant(mousePos, PEASHOOTER_ID)
        elif btn == 2:
            self.checkDeletePlant(mousePos)