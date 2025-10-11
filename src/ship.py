import pygame

class Ship:
    """A class to manage the player ship"""
    
    def __init__(self, ai_game):
        """Initialize the ship and set its starting position"""
        self.screen = ai_game.screen
        self.screen_rect = ai_game.screen.get_rect()
        
        # Load ship image
        self.ship_img = pygame.image.load("images/ship.png").convert_alpha()
        self.ship_mask = pygame.mask.from_surface(self.ship_img)    # Pixel-perfect
        
        # Resizing image
        width = 50
        height = 50
        size = (width, height)
        self.ship_img = pygame.transform.scale(self.ship_img, size)
        
        self.ship_rect = self.ship_img.get_rect()   # Ship position
        
        # Start each new ship at the bottom center of the screen
        self.ship_rect.midbottom = self.screen_rect.midbottom
        self.ship_rect.y -= 50  # Padding from the bottom
        
    def blitme(self):
        """Draw the ship at its current location"""
        self.screen.blit(self.ship_img, self.ship_rect)