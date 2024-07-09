import pygame
from const import *

pygame.init()

# 加载音效文件
beatSound = pygame.mixer.Sound(BEAT_SOUND)

eatSound = pygame.mixer.Sound(EAT_SOUND)

loseSound = pygame.mixer.Sound(LOSE_SOUND)

peaSound = pygame.mixer.Sound(PEA_SOUND)

plantSound = pygame.mixer.Sound(PLANT_SOUND)

sunlightSound = pygame.mixer.Sound(SUNLIGHT_SOUND)

zombieSound = pygame.mixer.Sound(ZOMBIE_SOUND)