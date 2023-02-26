import pygame

class Ship:  
    """管理飞船的类"""

    def __init__(self, ai_game):
        """初始化飞船并设置其初始位置。"""
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.screen_rect = ai_game.screen.get_rect()
        
        #移动标志
        self.moving_right = False
        self.moving_left = False

        # 加载飞船图像并获取其外接矩形。
        self.image = pygame.image.load('allien_invasion/images/ship.jpg')
        self.image = pygame.transform.scale(self.image,(50,50))
        self.rect = self.image.get_rect()
        # 对于每艘新飞船，都将其放在屏幕底部的中央。
        self.rect.midbottom = self.screen_rect.midbottom

        # 存储x的浮点值
        self.x = float(self.rect.x)
    def blitme(self):
        """在指定位置绘制飞船。"""
        self.screen.blit(self.image, self.rect)

    def update(self):
        """移动飞船"""
        if self.moving_right == True and self.rect.right < self.screen_rect.right :
            self.x += self.settings.ship_speed
        if self.moving_left == True and self.rect.left > 0 :
            self.x -= self.settings.ship_speed

        self.rect.x = self.x