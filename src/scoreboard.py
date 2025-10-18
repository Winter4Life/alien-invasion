import pygame.font
from pygame.sprite import Group

from ship import Ship

class Scoreboard:
    """Reporting scoring information"""
    
    def __init__(self, ai_game):
        """Scorekeeping attributes"""
        self.ai_game = ai_game
        self.screen = ai_game.screen
        self.screen_rect = self.screen.get_rect()
        self.settings = ai_game.settings
        self.stats = ai_game.stats
        
        # Font settings
        self.text_color = (255, 255, 255)
        self.font = pygame.font.SysFont(None, 48)
        
        self.prep_ships()
                
        # Current score
        self.prep_score()
        # Highest score
        self.prep_high_score()
        
    def prep_score(self):
        """Turn score into rendered image"""
        score_str = str(self.stats.score)
        self.score_image = self.font.render(score_str, True, 
                self.text_color, self.settings.bg_color)
        
        # Display the score
        self.score_rect = self.score_image.get_rect()
        self.score_rect.right = self.screen_rect.right - 20
        self.score_rect.top = 20
        
    def prep_high_score(self):
        "Highscore into rendered image"
        high_score_str = f"HighScore: {self.stats.high_score}"
        self.high_score_image = self.font.render(high_score_str, True, 
                self.text_color, self.settings.bg_color)
        
        # Display the score
        self.high_score_rect = self.high_score_image.get_rect()
        self.high_score_rect.left = self.screen_rect.left + 20
        self.high_score_rect.top = 20
        
    def check_high_score(self):
        """Check to see if there's a new high score"""
        if self.stats.score > self.stats.high_score:
            self.stats.high_score = self.stats.score
            self.prep_high_score()    
            
    def prep_ships(self):
        """Display Lives"""
        self.ships = Group()
        ship_width, ship_height = 30, 30  # Size

        for ship_number in range(self.stats.ships_left):
            ship = Ship(self.ai_game)

            # Scale down the ship image
            ship.image = pygame.transform.scale(ship.image, (ship_width, ship_height))
            ship.rect = ship.image.get_rect()

            # Position them in bottom-left corner
            ship.rect.x = 10 + ship_number * (ship_width + 5)  # 5 px spacing
            ship.rect.bottom = self.ai_game.settings.screen_height - 10  # 10 px padding from bottom

            self.ships.add(ship)
    
    def show_scores(self):
        """Draw score to the screen"""
        self.screen.blit(self.score_image, self.score_rect)
        self.screen.blit(self.high_score_image, self.high_score_rect)
        self.ships.draw(self.screen)