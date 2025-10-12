import pygame
from pygame.sprite import Sprite

class Alien(Sprite):
    """A class to represent a single alien in a fleet"""
    
    def __init__(self, ai_game):
        """Initializing the alien and its starting position"""
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        
        # Loading alien image
        self.alien_green_img = pygame.image.load("images/alien_green.png")
        self.alien_green_rect = self.alien_green_img.get_rect()
        self.alien_red_img = pygame.image.load("images/alien_red.png")
        self.alien_red_rect = self.alien_red_img.get_rect()
        
        # Resizing image
        self.alien_green_img = pygame.transform.scale(self.alien_green_img, self.settings.alien_size)
        self.alien_red_img = pygame.transform.scale(self.alien_red_img, self.settings.alien_size)
        
        # Pixel perfect
        self.mask = pygame.mask.from_surface(self.alien_green_img)
        self.mask = pygame.mask.from_surface(self.alien_red_img)
        
        # Start each new alien near the top left of the screen
        self.alien_green_rect.x = self.alien_green_rect.width
        self.alien_green_rect.y = self.alien_green_rect.height
        
        self.alien_red_rect.x = self.alien_green_rect.x + self.alien_green_rect.width + 10 
        self.alien_red_rect.y = self.alien_green_rect.y 
        
        # Store exact position
        self.x = float(self.alien_green_rect.x)
        self.x = float(self.alien_red_rect.x)
        
    def draw_alien(self):
        """Draw the bullet to the screen"""
        self.screen.blit(self.alien_green_img, self.alien_green_rect)
        self.screen.blit(self.alien_red_img, self.alien_red_rect)