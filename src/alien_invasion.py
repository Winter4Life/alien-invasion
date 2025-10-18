import sys
import pygame
import random
from time import sleep

from settings import Settings
from ship import Ship
from bullet import Bullet
from alien import Alien
from game_stats import GameStats
from button import Button

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
        
        self.game_active = False # Game state
        self.play_button = Button(self, "Play")
        
        self.game_paused = False
        self.pause_buttons = {
            "Continue": Button(self, "Continue"),
            "Restart": Button(self, "Restart"),
            "Quit": Button(self, "Quit Game")
        }
        center_x = self.settings.screen_width // 2
        center_y = self.settings.screen_height // 2
        spacing = self.settings.pause_button_spacing

        for i, (label, button) in enumerate(self.pause_buttons.items()):
            y = center_y - 80 + i * spacing  # adjust vertical offset
            button.set_center((center_x, y))

    def run_game(self):
        """Start the main loop for the game"""
        while True:
            self._check_events()
            
            if self.game_active and not self.game_paused:
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
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()

                if not self.game_active:
                    self._check_play_button(mouse_pos)
                elif self.game_paused:
                    self._check_pause_menu(mouse_pos)

                
    def _check_play_button(self, mouse_pos):
        """Start a new game when player clicks play"""
        if self.play_button.rect.collidepoint(mouse_pos):
            self.game_active = True
            pygame.mouse.set_visible(False)
            
    def _check_pause_menu(self, mouse_pos):
        """Handle clicks on pause menu buttons"""
        for label, button in self.pause_buttons.items():
            if button.rect.collidepoint(mouse_pos):
                if label == "Continue":
                    self.game_paused = False
                elif label == "Restart":
                    self._restart_game()
                    self.stats.reset_stats()
                elif label == "Quit":
                    sys.exit()
                    
    def _restart_game(self):
        """Restart the game from scratch"""
        self.stats.ships_left = 3
        self.bullets.empty()
        self.aliens.empty()
        self._create_fleet()
        self.ship.center_ship()
        self.game_paused = False

                        
    def _check_keydown_events(self, event):
        """Response to keypresses"""
        if event.key == pygame.K_d:
            self.ship.moving_right = True
        elif event.key == pygame.K_a:
            self.ship.moving_left = True
        elif event.key == pygame.K_UP:
            self._fire_bullet()
        elif event.key == pygame.K_ESCAPE:
            if self.game_active:
                self.game_paused = not self.game_paused
                pygame.mouse.set_visible(True)
        
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
        
        if not self.game_active:
            self.play_button.draw_button()
            
        if self.game_paused:
            panel_width = 400
            panel_height = 300
            panel_color = (60, 60, 60)      # dim grey
            border_color = (100, 100, 100)  # border
            border_thickness = 4
            
            panel_rect = pygame.Rect(0, 0, panel_width, panel_height)
            panel_rect.center = (self.settings.screen_width // 2, 
                                 self.settings.screen_height // 2)
            
            pygame.draw.rect(self.screen, border_color, panel_rect) # Border
            
            inner_rect = panel_rect.inflate(-border_thickness*2, -border_thickness*2) # Fill
            pygame.draw.rect(self.screen, panel_color, inner_rect)
            
            # Buttons
            for button in self.pause_buttons.values():
                button.draw_button()

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