import pygame

class Image(pygame.sprite.Sprite):
    # (self, 路径格式， 路径索引， 位置， 图片大小， 路径索引数量）
    def __init__(self, pathFmt, pathIndex, pos, size = None, pathIndexCount = 0):
        super().__init__()
        self.pathFmt = pathFmt
        self.pathIndex = pathIndex
        self.pos = list(pos)
        self.size = size
        self.pathIndexCount = pathIndexCount
        self.updateImage()

    def updateImage(self):
        path = self.pathFmt
        if self.pathIndexCount != 0:
            path = path % self.pathIndex
        self.image = pygame.image.load(path)
        if self.size:
            self.image = pygame.transform.scale(self.image, self.size)

    def updateSize(self, size):
        self.size = size
        self.updateImage()

    def updateIndex(self, pathIndex):
        self.pathIndex = pathIndex
        self.updateImage()

    def getRect(self):
        rect = self.image.get_rect()
        rect.x, rect.y = self.pos
        return rect

    def doLeft(self):
        self.pos[0] -= 0.1

    def draw(self, screen):
        screen.blit(self.image, self.getRect())