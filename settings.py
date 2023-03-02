class Settings:
    """存储游戏《外星人入侵》中所有设置的类"""

    def __init__(self):
        """初始化游戏的设置。"""
        # 屏幕设置
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (255, 255, 255)

        #速度
        self.ship_speed = 1
        self.ship_limit = 3

        # 子弹设置
        self.bullet_speed = 2.0
        self.bullet_width = 200
        self.bullet_height = 30
        self.bullet_color = (60, 60, 60)
        self.bullets_allowed = 3

        # 外星人设置
        self.alien_speed = 0.5

        self.fleet_drop_speed = 50
        # fleet_direction为1表示向右移，为-1表示向左移。
        self.fleet_direction = 1