import sys
import pygame
import random

from settings import Settings
from ship import Ship

class AlienInvasion:
    """Overall class to manage game assets and behavior"""
    
    def __init__(self):
        """Initialize the game, and create game resources"""
        pygame.init()
        self.clock = pygame.time.Clock()    # Frame rate
        self.settings = Settings()
        
        self.screen = pygame.display.set_mode(
            (self.settings.screen_width, self.settings.screen_length))  # Dimensions
        pygame.display.set_caption("Alien Invasion")    # Screen title
        
        self.ship = Ship(self)  # Init ship
        
    def run_game(self):
        """Start the main loop for the game"""
        while True:
            self._check_events()
            self.ship.update()
            self._update_screen()
            self.clock.tick(60)
            
    def _check_events(self):
        """Respond to keypresses and mouse events"""
        # Returns a list of recent events since func call
        for event in pygame.event.get():  
                if event.type == pygame.QUIT:
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    self._check_keydown_events(event)
                        
                elif event.type == pygame.KEYUP:
                    self._check_keyup_events(event)
                        
    def _check_keydown_events(self, event):
        """Response to keypresses"""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = True
        elif  event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        
    def _check_keyup_events(self, event):
        """Response to keyreleases"""
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif  event.key == pygame.K_LEFT:
            self.ship.moving_left = False
                    
    def _update_screen(self):
        """Update images on the screen, and flip to the new screen"""
        # Redraw the screen during each pass through loop
        self.screen.fill(self.settings.bg_color)
        for star_pos in self.settings.stars:  # Draw stars
            self.screen.set_at(star_pos, self.settings.bg_stars)  # Sets a single pixel
            
        self.ship.blitme()  # Draw ship
                
        # Make the most recently drawn screen variable
        pygame.display.flip()
                
if __name__ == '__main__':
    # Make a game instance, and run the game
    ai = AlienInvasion()
    ai.run_game()