# -*- coding: utf-8 -*-

import pygame
#导入pygame库
from sys import exit
#向sys模块借一个exit函数用来退出程序
import random

pygame.init()
#初始化pygame,为使用硬件做准备

screen = pygame.display.set_mode((540, 961), 0, 32)
#创建了一个窗口,窗口大小和背景图片大小一样

pygame.display.set_caption("Hello, World!")
#设置窗口标题

bg1 = pygame.image.load('bg.jpg')
bg2 = pygame.image.load('bg2.jpg')
#读取图片并保存，以后不用再次读取
background = bg2.convert()
#加载并转换图像
# plane = pygame.image.load('plane.jpg').convert()
#加载飞机图像
# bullet = pygame.image.load('bullet.jpg').convert_alpha()
print(pygame.font.get_fonts())
# 所有可用的系统字体
count = 0
#设置一个计数器
score = 0
# 分数
highest = 0
#最高分

font = pygame.font.SysFont('couriernew', 22)#pygame.font.Font(sysfont, 32)
# 要显示的分数
font2 = pygame.font.SysFont('couriernew', 22)#pygame.font.Font(sysfont, 32)
# 要显示的最高分

def chbg():
#定义一个change background的函数，用于点击鼠标后改变背景图片
    if event.type == pygame.MOUSEBUTTONDOWN:
        #接收到鼠标按下事件后更换背景
        if count % 2 == 0:
            background = bg2.convert()
        else:
            background = bg1.convert()
        count += 1
        # 计数器加1，改变奇偶性

class Plane:
    def restart(self):
        self.x = 200
        self.y = 600     

    def __init__(self):
        self.restart()
        self.image = pygame.image.load('plane.png').convert_alpha()

    def move(self):
        x, y = pygame.mouse.get_pos()
        x-= self.image.get_width() / 2
        y-= self.image.get_height() / 2
        self.x = x
        self.y = y

class Bullet:
#定义一个Bullet类，封装子弹相关的数据和方法
    def __init__(self):
        #初始化成员变量，x，y，image
        self.x = 0
        self.y = -1
        self.image = pygame.image.load('bullet.jpg').convert_alpha()
        #默认不激活
        self.active = False
        
    def move(self):
        #处理子弹的运动
        # if self.y < 0:
            # mouseX, mouseY = pygame.mouse.get_pos()
            # self.x = mouseX - self.image.get_width() / 2
            # self.y = mouseY - self.image.get_height() / 2
        # else:
            # self.y -= 1
        if self.active:
        #激活状态下，向上移动
            self.y -= 3
        if self.y < 0:
        #当飞出屏幕，就设为不激活
            self.active = False

    def restart(self):
        #重置子弹位置
        mouseX, mouseY = pygame.mouse.get_pos()
        self.x = mouseX - self.image.get_width() / 2
        self.y = mouseY - self.image.get_height() / 2
        #激活子弹
        self.active = True
        
#定义一个Enemy类
class Enemy:
    def __init__(self):
        # self.x = 540/2-178/2
        # self.y = -50
        self.restart()
        self.image = pygame.image.load('enemy.png').convert_alpha()
        
    def move(self):
        if self.y < 961:
            self.y += self.speed
            # self.y += 0.3
        else:
            # self.y = -50
            self.restart()
            
    def restart(self):
        self.x = random.randint(50, 400)
        self.y = random.randint(-200, -50)
        self.speed = random.random()*0.3 + 0.1
        # print self.speed

def checkHit(enemy, bullet):
#判断子弹是否击中enemy
    if (bullet.x > enemy.x and bullet.x < enemy.x + enemy.image.get_width()) and (bullet.y > enemy.y and bullet.y < enemy.y + enemy.image.get_height()):
        enemy.restart()
        bullet.active = False
        return True
        # 发生碰撞
    return False

def checkCrash(enemy, plane):
    if (plane.x + 0.7*plane.image.get_width() > enemy.x) and (plane.x + 0.3*plane.image.get_width() < enemy.x + enemy.image.get_width()) and (plane.y + 0.7*plane.image.get_height() > enemy.y) and (plane.y + 0.3*plane.image.get_height() < enemy.y + enemy.image.get_height()):
        return True
    return False
    
enemies = []
for i in range(5):
    enemies.append(Enemy())

bullets = []
#创建子弹的list
for i in range(5):
#向list中添加5发子弹
    bullets.append(Bullet())

plane = Plane()

count_b = len(bullets)
#子弹总数
index_b = 0
#即将激活的子弹序号
interval_b = 0
#发射子弹的间隔
gameover = False

while True:
#游戏主循环

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            #接收到退出事件后退出程序
            pygame.quit()
            exit()
        # chbg()

    screen.blit(background, (0, 0))
    #将背景图画上去
    
    if gameover and event.type == pygame.MOUSEBUTTONUP:
        #重置游戏
        
        plane.restart()
        for e in enemies:
            e.restart()

        for b in bullets:
            b.active = False

        score = 0
        gameover = False
    
    if not gameover:
    
        #发射间隔递减
        interval_b -= 1

        #当间隔小于0时，激活一发子弹
        if interval_b < 0:
            bullets[index_b].restart()
            interval_b = 100
            #重置间隔时间
            index_b = (index_b + 1) % count_b
            #子弹序号周期性递增

        for b in bullets:
        #判断每个子弹的状态
            if b.active:
                for e in enemies:
                    if checkHit(e, b):
                    #击中敌机后，分数加100
                        score += 100
                b.move()
                screen.blit(b.image, (b.x, b.y))
                #处于激活状态的子弹，移动位置并绘制

        x, y = pygame.mouse.get_pos()
        #获取鼠标位置

        for e in enemies:
        #检测敌人的运动并画到屏幕上
            if checkCrash(e, plane):
            #如果撞上敌机，设gameover为True
                gameover = True
            e.move()
            screen.blit(e.image, (e.x, e.y))

        plane.move()
        screen.blit(plane.image, (plane.x, plane.y))
        #把飞机画到屏幕上
        
        text = font.render("Score: %d" % score, 1, (255, 255, 255))
        screen.blit(text, (0, 0))
        # 把分数画到屏幕上
    
    else:
        if score > highest:
            highest = score
            #记录最高分
        text = font.render("Score: %d" % score, 1, (255, 255, 255))
        screen.blit(text, (540/2-100, 961/2-100))
        # 把分数画到屏幕上
        text2 = font2.render("Highest Score: %d" % highest, 1, (255, 255, 255))
        screen.blit(text2, (540/2-100, 961/2-80))
        # 把最高分画到屏幕上
        
    pygame.display.update()
    #刷新一下画面