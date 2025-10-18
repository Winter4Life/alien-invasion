import random

class Settings:
    """A class to store all settings for Alien Invasion"""
    
    def __init__(self):
        """Initialize the game's settings"""
        # Screen settings
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_stars = (255, 255, 255)
        self.bg_color = (0, 0, 0)
        
        NUM_STARS = 80
        # Generating stars
        self.stars = []
        for _ in range(NUM_STARS):
            x = random.randint(0, 1200)
            y = random.randint(0, 800)
            self.stars.append((x, y))
            
        # Ship settings
        ship_width = 50
        ship_height = 50
        self.ship_size = (ship_width, ship_height)
        self.ship_speed = 2.5
        self.ship_limit = 3
        
        # Bullet settings
        bullet_width = 15
        bullet_height = 30
        self.bullet_size = (bullet_width, bullet_height)
        self.bullet_speed = 2.0
        self.bullets_allowed = 10
        
        # Alien settings
        alien_width = 30
        alien_height = 30
        self.alien_size = (alien_width, alien_height)
        self.alien_speed = 1.0
        self.fleet_drop_speed = 30
        self.fleet_direction = 1 # Moves right
        
        # Pause settings
        self.pause_button_spacing = 80
        self.pause_menu_offset_y = -40