import random

class Settings:
    """A class to store all settings for Alien Invasion"""
    
    def __init__(self):
        """Initialize the game's settings"""
        # Screen settings
        self.screen_width = 1200
        self.screen_length = 800
        self.bg_stars = (255, 255, 255)
        self.bg_color = (0, 0, 0)
        
        NUM_STARS = 80
        # Generating stars
        self.stars = []
        for _ in range(NUM_STARS):
            x = random.randint(0, 1200)
            y = random.randint(0, 800)
            self.stars.append((x, y))