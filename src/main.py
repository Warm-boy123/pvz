import sys
import pygame
# from pygame.locals import *
from const import *
import game
import time
import image

pygame.init()

# 设置窗口标题
pygame.display.set_caption(GAME_NAME)
# 加载图标
logo = pygame.image.load(LOGO_PATH)
# 设置窗口图标
pygame.display.set_icon(logo)

DS = pygame.display.set_mode(GAME_SIZE)
DS.fill( (255, 255, 255) )

game = game.Game(DS)

# 加载封面
coverTime = time.time() - 3
cover = image.Image(COVER_PATH, 0, (0, 0), GAME_SIZE, 0)

# 加载动画
while True:
    if time.time() - coverTime < 2:
        cover.draw(DS)
        cover.update(DS)
        pygame.display.update()
        continue
    break

# 加载背景音乐文件
pygame.mixer.music.load(MORNING_BGM)
# 设置背景音乐的音量（范围0.0到1.0）
pygame.mixer.music.set_volume(1.0)
# 播放背景音乐
pygame.mixer.music.play(-1)

# 游戏场景
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            game.mouseClickHandler(event.button)
    game.update()
    game.draw()
    pygame.display.update()