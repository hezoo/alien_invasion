import sys
from time import sleep

import pygame

from settings import Settings
from ship import Ship
from bullet import Bullet
from alien import Alien
from game_stats import GameStats
from button import Button,ButtonDiffcult
from scoreboard import Scoreboard


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
        
        #创建统计信息实例
        self.stats = GameStats(self)
        #创建飞船
        self.ship = Ship(self)
        #创建子弹编组
        self.bullets = pygame.sprite.Group()
        #创建外星人编组
        self.aliens = pygame.sprite.Group()
        self._creat_fleet()

        #play按钮
        self.play_button = Button(self,"play")
        self.play_button1 = ButtonDiffcult(self,"1")
        self.play_button2 = ButtonDiffcult(self,"2")
        #self.play_button3 = Button(self,"3")

        #记分牌
        self.score = Scoreboard(self)

    def run_game(self):
        """开始游戏"""
        while True:
            #监视输入
            self._check_events()
            if self.stats.game_active:
                #更新子弹状态
                self._update_bullets()
                #更新外星人
                self._update_aliens()
                #飞船运动
                self.ship.update()
            #刷新屏幕
            self._update_screen()

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

    def _ship_hit(self):
        """响应飞船被外星人撞到。"""

        if self.stats.ships_left > 0:
            # 将ships_left减1。
            self.stats.ships_left -= 1

            # 清空余下的外星人和子弹。
            self.aliens.empty()
            self.bullets.empty()

            # 创建一群新的外星人，并将飞船放到屏幕底端的中央。
            self._creat_fleet()
            self.ship.center_ship()
            # 暂停。
            sleep(0.5)      
        else:
            self.stats.game_active = False
            self.settings.initialize_dynamic_settings()
            pygame.mouse.set_visible(True)

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
        #检查外星人碰撞飞船
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            self._ship_hit()
        #检查外星人到底端
        self._check_aliens_bottom()

    def _check_aliens_bottom(self):
        """检查是否有外星人到达了屏幕底端。"""
        screen_rect = self.screen.get_rect()
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= screen_rect.bottom:
                # 像飞船被撞到一样处理。
                self._ship_hit()
                break

    def _check_events(self):
        """监视输入"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self._check_play_button(mouse_pos)

    def _check_play_button(self, mouse_pos):
        """在玩家单击Play按钮时开始新游戏。"""
        if self.play_button1.rect.collidepoint(mouse_pos):
            self.settings.increase_diffcult()

        if self.play_button.rect.collidepoint(mouse_pos) and not self.stats.game_active:
            #重置stats
            self.stats.reset_stats()
            self.score.prep_score()
            self.stats.game_active = True
            pygame.mouse.set_visible(False)
            # 清空余下的外星人和子弹。
            self.aliens.empty()
            self.bullets.empty()

            #创建一群新的外星人，并将飞船放到屏幕底端的中央。
            self._creat_fleet()
            self.ship.center_ship()


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
        self._check_bullet_alien_collisions()

    def _check_bullet_alien_collisions(self):
        # 检查是否有子弹击中了外星人。
        #  如果是，就删除相应的子弹和外星人。
        collisions = pygame.sprite.groupcollide(
                self.bullets, self.aliens, False, True)

        if collisions:
            for alien in collisions.values():
                self.stats.score += self.settings.alien_points*len(alien)
            self.score.prep_score()

        if not self.aliens:
            #删除现有子弹并新建一群外星人
            self.bullets.empty()
            self._creat_fleet() 
            self.settings.increase_speed()

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
        self.score.show_score()
        #绘制飞船
        self.ship.blitme()
        #绘制子弹
        if  self.stats.game_active:
            for bullet in self.bullets.sprites():
                bullet.draw_bullet()
        #绘制外星人
        self.aliens.draw(self.screen)
        if not self.stats.game_active:
            self.play_button.draw_button()
            self.play_button1.draw_button()
            self.play_button2.draw_button()
        #刷新
        pygame.display.flip()
        
if __name__ == "__main__":
    #创建游戏实例并运行
    ai_game = AlienIvasion()
    ai_game.run_game()
