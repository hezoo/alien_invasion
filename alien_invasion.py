import sys
import pygame

from settings import Settings
from ship import Ship
from bullet import Bullet
from alien import Alien


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
        #创建外星人编组
        self.aliens = pygame.sprite.Group()

        self._creat_fleet()

    def run_game(self):
        """开始游戏"""
        while True:
            #监视输入
            self._check_events()
            #更新子弹状态
            self._update_bullets()
            #更新外星人
            self._update_aliens()
            #刷新屏幕
            self._update_screen()
            #飞船运动
            self.ship.update()

    def _creat_fleet(self):
        """创建外星人群。"""

        # 创建一个外星人并计算一行可容纳多少个外星人。
        # 外星人的间距为外星人宽度。
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        available_space_x = self.settings.screen_width - (2 * alien_width)
        number_aliens_x = available_space_x // (2 * alien_width)

        #计算屏幕可容纳多少行外星人。
        ship_height = self.ship.rect.height
        available_space_y = (self.settings.screen_height -
                                   (3 * alien_height) - ship_height)
        number_rows = available_space_y // (2 * alien_height)

        # 创建外星人群。
        for row_number in range(number_rows):
            for alien_number in range(number_aliens_x):
                self._create_alien(alien_number, row_number)

    def _create_alien(self, alien_number, row_number):
        """创建一个外星人，并将其放在当前行。"""
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        alien.x = alien_width + 2 * alien_width * alien_number
        alien.rect.x = alien.x
        alien.rect.y = alien_height + 2 * alien_height * row_number
        self.aliens.add(alien)


    def _check_fleet_edges(self):
        """有外星人到达边缘时采取相应的措施。"""
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break

    def _change_fleet_direction(self):
        """将整群外星人下移，并改变它们的方向。"""
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1

    def _update_aliens(self):
        """更新外星人群中所有外星人的位置。"""

        self._check_fleet_edges()
        self.aliens.update()       

    def _check_events(self):
        """监制输入"""
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

    def _update_bullets(self):
        """更新子弹的位置并删除消失的子弹。"""
        # 更新子弹的位置。
        self.bullets.update()
        # 删除消失的子弹。
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                 self.bullets.remove(bullet)
        #print(len(self.bullets))

        # 检查是否有子弹击中了外星人。
        #  如果是，就删除相应的子弹和外星人。
        collisions = pygame.sprite.groupcollide(
                self.bullets, self.aliens, False, True)


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
        #绘制子弹
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        #绘制外星人
        self.aliens.draw(self.screen)
        #刷新
        pygame.display.flip()
        
if __name__ == "__main__":
    #创建游戏实例并运行
    ai_game = AlienIvasion()
    ai_game.run_game()
