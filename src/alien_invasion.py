import sys
import pygame
import random

from settings import Settings

class AlienInvasion:
    """Overall class to manage game assets and behavior"""
    
    def __init__(self):
        """Initialize the game, and create game resources"""
        pygame.init()
        self.clock = pygame.time.Clock()    # frame rate
        self.settings = Settings()
        
        self.screen = pygame.display.set_mode(
            (self.settings.screen_width, self.settings.screen_length))  # Dimensions
        pygame.display.set_caption("Alien Invasion")    # Screen title
        
    def run_game(self):
        """Start the main loop for the game"""
        while True:
            # Watch for keyboard and mouse events
            # Returns a list of recent events since func call
            for event in pygame.event.get():  
                if event.type == pygame.QUIT:
                    sys.exit()
            
            # Redraw the screen during each pass through loop
            self.screen.fill(self.settings.bg_color)
            for star_pos in self.settings.stars:  # Draw stars
                self.screen.set_at(star_pos, self.settings.bg_stars)  # Sets a single pixel
                    
            # Make the most recently drawn screen variable
            pygame.display.flip()
            self.clock.tick(60)
                
if __name__ == '__main__':
    # Make a game instance, and run the game
    ai = AlienInvasion()
    ai.run_game()