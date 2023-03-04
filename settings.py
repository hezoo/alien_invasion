class Settings:
    """存储游戏《外星人入侵》中所有设置的类"""

    def __init__(self):
        """初始化游戏的设置。"""
        # 屏幕设置
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (255, 255, 255)

        #剩余飞船
        self.ship_limit = 1

        # 子弹设置
        self.bullet_width = 200
        self.bullet_height = 30
        self.bullet_color = (60, 60, 60)
        self.bullets_allowed = 3

        self.fleet_drop_speed = 30

        #计分   
        self.alien_points = 50

        #加快节奏的速度
        self.speedup_scale = 1.5

        #加快节奏的难度
        self.diffcult_scale = 3

        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self):
        """初始化随游戏进行而变化的设置。"""
        self.ship_speed = 1.5
        self.bullet_speed = 3.0
        self.alien_speed = 0.5

        # fleet_direction为1表示向右，为-1表示向左。
        self.fleet_direction = 1

    def increase_speed(self):
        """提高速度设置"""
        self.ship_speed *= self.speedup_scale
        self.bullet_speed *= self.speedup_scale
        self.alien_speed *= self.speedup_scale

    def increase_diffcult(self):
        """提高难度设置"""
        self.ship_speed *= self.diffcult_scale
        self.bullet_speed *= self.diffcult_scale
        self.alien_speed *= self.diffcult_scale
                