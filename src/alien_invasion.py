import sys
import pygame

from settings import Settings
from ship import Ship
from bullet import Bullet

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
        self.bullets = [] # Init bullet
        
    def run_game(self):
        """Start the main loop for the game"""
        while True:
            self._check_events()
            self.ship.update()
            self._update_bullets()
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
        if event.key == pygame.K_d:
            self.ship.moving_right = True
        elif event.key == pygame.K_a:
            self.ship.moving_left = True
        elif event.key == pygame.K_UP:
            self._fire_bullet()
        
    def _check_keyup_events(self, event):
        """Response to keyreleases"""
        if event.key == pygame.K_d:
            self.ship.moving_right = False
        elif event.key == pygame.K_a:
            self.ship.moving_left = False
            
    def _fire_bullet(self):
        """Create a new bullet"""
        if len(self.bullets) < self.settings.bullets_allowed:
            new_bullet = Bullet(self)
            self.bullets.append(new_bullet)
        
    def _update_bullets(self):
        """Update position of bullets and remove bullets that have gone off-screen"""
        for bullet in self.bullets[:]:  # Iterate over a copy of the list
            bullet.update()
            if bullet.bullet_rect.bottom < 0:
                self.bullets.remove(bullet)
                    
    def _update_screen(self):
        """Update images on the screen, and flip to the new screen"""
        # Redraw the screen during each pass through loop
        self.screen.fill(self.settings.bg_color)
        for star_pos in self.settings.stars:  # Draw stars
            self.screen.set_at(star_pos, self.settings.bg_stars)  # Sets a single pixel
        # Redraw the bullets
        for bullet in self.bullets:
            bullet.draw_bullet()
                
        self.ship.blitme()  # Draw ship
                
        # Make the most recently drawn screen variable
        pygame.display.flip()
                
if __name__ == '__main__':
    # Make a game instance, and run the game
    ai = AlienInvasion()
    ai.run_game()