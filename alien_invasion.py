import sys
import pygame

from settings import Settings
from ship import Ship
from bullet import Bullet


class AlienIvasion:
    """管理游戏内容"""
    def __init__(self) -> None:
        """初始化游戏"""
        pygame.init()

        self.settings = Settings()
        #self.screen = pygame.display.set_mode((self.settings.screen_width,self.settings.screen_height))
        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self.settings.screen_width = self.screen.get_rect().width
        self.settings.screen_height = self.screen.get_rect().height

        pygame.display.set_caption("Alien Invasion")

        self.ship = Ship(self)
        #创建子弹编组
        self.bullets = pygame.sprite.Group()

    def run_game(self):
        """开始游戏"""
        while True:
            #监视输入
            self._check_events()
            #刷新子弹
            self._update_bullets()
            #刷新屏幕
            self._update_screen()
            #飞船运动
            self.ship.update()

    def _update_bullets(self):
        """更新子弹的位置并删除消失的子弹。"""
        # 更新子弹的位置。
        self.bullets.update()
        # 删除消失的子弹。
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                 self.bullets.remove(bullet)
        #print(len(self.bullets))

    def _check_events(self):
        #监制输入
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)

    def _check_keydown_events(self, event): 
        """检查键盘按下"""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        elif event.key == pygame.K_q:
            sys.exit()
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()

    def _fire_bullet(self):
        """创建一个子弹加入编组"""
        if len(self.bullets) < self.settings.bullets_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet) 

    def _check_keyup_events(self, event): 
        """检查键盘松开"""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False      
    
    def _update_screen(self):
        """更新屏幕的图像"""
        #重绘背景
        self.screen.fill(self.settings.bg_color)
        #绘制飞船
        self.ship.blitme()
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        #刷新
        pygame.display.flip()
        
if __name__ == "__main__":
    #创建游戏实例并运行
    ai_game = AlienIvasion()
    ai_game.run_game()
