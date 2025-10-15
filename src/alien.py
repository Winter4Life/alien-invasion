import pygame
from pygame.sprite import Sprite

class Alien(Sprite):
    """A class to represent a single alien in a fleet"""
    
    def __init__(self, ai_game, color_type="green"):
        """Initializing the alien and its starting position"""
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.color_type = color_type # green or red
        
        # Loading alien image
        if self.color_type == "green":
            self.alien_image = pygame.image.load("images/alien_green.png").convert_alpha()
        else:
            self.alien_image = pygame.image.load("images/alien_red.png").convert_alpha()
        
        self.alien_image = pygame.transform.scale(self.alien_image, self.settings.alien_size)
        self.alien_rect = self.alien_image.get_rect()
        
        # Start each new alien near the top left of the screen
        self.alien_rect.x = self.alien_rect.width
        self.alien_rect.y = self.alien_rect.height
        
        # Store exact position
        self.x = float(self.alien_rect.x)
        
    def draw_alien(self):
        """Draw the alien to the screen"""
        self.screen.blit(self.alien_image, self.alien_rect)