import sys
import pygame
import random
from time import sleep

from settings import Settings
from ship import Ship
from bullet import Bullet
from alien import Alien
from game_stats import GameStats

class AlienInvasion:
    """Overall class to manage game assets and behavior"""
    
    def __init__(self):
        """Initialize the game, and create game resources"""
        pygame.init()
        self.clock = pygame.time.Clock()    # Frame rate
        self.settings = Settings()
        
        self.screen = pygame.display.set_mode(
            (self.settings.screen_width, self.settings.screen_height))  # Dimensions
        pygame.display.set_caption("Alien Invasion")    # Screen title
        
        self.stats = GameStats(self)
        
        self.ship = Ship(self)  
        self.bullets = pygame.sprite.Group() 
        self.aliens = pygame.sprite.Group()
        
        self._create_fleet()
        
        self.game_active = True
        
    def run_game(self):
        """Start the main loop for the game"""
        while True:
            self._check_events()
            
            if self.game_active:
                self.ship.update()
                self._update_bullets()
                self._update_aliens()
                
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
            self.bullets.add(new_bullet)
        
    def _update_bullets(self):
        """Update position of bullets and remove bullets that have gone off-screen"""
        # Update all bullets (calls each bullet's update method)
        self.bullets.update()
        
        # Remove bullets that have gone off-screen (extra safety)
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                bullet.kill()
        
        self._check_bullet_alien_collision()
        
    def _check_bullet_alien_collision(self):
        """Respond to bullet-alien collisions"""
        # If bullets hit an alien, remove the bullet and alien
        collisions = pygame.sprite.groupcollide(
            self.bullets, self.aliens, True, True,
            collided=pygame.sprite.collide_mask
        )
        
        if not self.aliens:
            # Destroy existing bullets and create new fleet
            self.bullets.empty()
            self._create_fleet()
                    
    def _update_screen(self):
        """Update images on the screen, and flip to the new screen"""
        # Redraw the screen during each pass through loop
        self.screen.fill(self.settings.bg_color)
        for star_pos in self.settings.stars:  # Draw stars
            self.screen.set_at(star_pos, self.settings.bg_stars)  # Sets a single pixel
        # Redraw the bullets
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()       
        self.ship.blitme()  # Draw ship
        # Draw aliens
        for alien in self.aliens.sprites():
            alien.draw_alien()
        
        # Make the most recently drawn screen variable
        pygame.display.flip()
    
    def _create_fleet(self):
        """Create a fleet of aliens"""
        # Creates an instance of a alien
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        
        aliens_per_row = 8
        num_rows = 5
        
        # Define the width and height of the fleet (its own screen)
        total_fleet_width = aliens_per_row * (alien_width * 2)
        total_fleet_height = num_rows * (alien_height * 2)
                
        start_x = (self.settings.screen_width - (aliens_per_row * (alien_width * 2))) // 2
        start_y = 100  # some top padding

        for row in range(num_rows):
            for col in range(aliens_per_row):
                color = random.choices(["green", "red"], weights = [.6, .4])[0]  # 60/40 chance
                self._create_alien(start_x + col * (alien_width * 2),
                                start_y + row * (alien_height * 2),
                                color)
    
    def _create_alien(self, x, y, color):
        alien = Alien(self, color_type=color)
        alien.rect.x = x
        alien.rect.y = y
        alien.x = float(x)
        self.aliens.add(alien)
        
    def _check_fleet_edges(self):
        """If alien fleet hits an edge, change direction and drop"""
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break
            
    def _change_fleet_direction(self):
        """Drop entire fleet and change direction"""
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1
        
    def _check_aliens_bottom(self):
        """Check if any aliens have reached the bottom of the screen"""
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= self.settings.screen_height:
                # Treat this the same as if the ship gets hit
                self._ship_hit()
                break
        
    def _update_aliens(self):
        """Update the positions of all aliens in the fleet"""
        self._check_fleet_edges()
        self.aliens.update()
        
        # Looks for alien-ship collisions
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            #print("Ship hit")
            self._ship_hit()
            
        # Looks for aliens reaching the bottom of the screen
        self._check_aliens_bottom()
        
    def _ship_hit(self):
        """Responds to the ship being hit"""
        if self.stats.ships_left > 0:
            # Decrement ships_left
            self.stats.ships_left -= 1
            # Delete remaining bullets and recreate fleet and ship
            self.bullets.empty()
            self.aliens.empty()
            self._create_fleet()
            self.ship.center_ship()
            
            # Pause
            sleep(.5)
        else:
            self.game_active = False
            
if __name__ == '__main__':
    # Make a game instance, and run the game
    ai = AlienInvasion()
    ai.run_game()