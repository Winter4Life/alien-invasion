import pygame
from pygame.sprite import Sprite

class Bullet(Sprite):
    """A class to manage bullets fired from the ship"""
    
    def __init__(self, ai_game):
        """Create the bullet at the ship's current location"""
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        
        # Load bullet image
        self.bullet_img = pygame.image.load("images/bullet.png").convert_alpha()
        
        # Resizing image
        self.bullet_img = pygame.transform.scale(self.bullet_img, self.settings.bullet_size)
        
        # Setting correct position
        self.bullet_rect = self.bullet_img.get_rect()
        self.bullet_rect.midtop = ai_game.ship.ship_rect.midtop
        
        # Create a mask for collisions (only the core counts)
        self.mask = pygame.mask.from_surface(self.bullet_img)
        
        self.y = float(self.bullet_rect.y)
        
    def update(self):
        """Move the bullet up the screen"""
        self.y -= self.settings.bullet_speed
        self.bullet_rect.y = int(self.y)
        
    def draw_bullet(self):
        """Draw the bullet to the screen"""
        self.screen.blit(self.bullet_img, self.bullet_rect)