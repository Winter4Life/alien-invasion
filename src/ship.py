import pygame

class Ship:
    """A class to manage the player ship"""
    
    def __init__(self, ai_game):
        """Initialize the ship and set its starting position"""
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.screen_rect = ai_game.screen.get_rect()
        
        # Load ship image
        self.image = pygame.image.load("images/ship.png").convert_alpha()
        self.ship_mask = pygame.mask.from_surface(self.image)    # Pixel-perfect
        
        # Resizing image
        self.image = pygame.transform.scale(self.image, self.settings.ship_size)
        
        self.rect = self.image.get_rect()   # Ship position
        
        # Start each new ship at the bottom center of the screen
        self.rect.midbottom = self.screen_rect.midbottom
        self.rect.y -= 50  # Padding from the bottom
        
        # Movement
        self.moving_right = False
        self.moving_left = False

        self.x = float(self.rect.x)    # Smoother movement
        
    def update(self):
        """Update the ships position based on movement flag"""
        if self.moving_right:
            self.x += self.settings.ship_speed
        if self.moving_left:
            self.x -= self.settings.ship_speed
        
        # Screen wrapping
        # If ship goes off right screen, appears on the left
        if self.x > self.screen_rect.width:
            self.x = -self.rect.width
        # If ship goes off left screen, appears on the right    
        elif self.x + self.rect.width < 0:
            self.x = self.screen_rect.width
        
        # Update position from float position
        self.rect.x = int(self.x)
        
    def blitme(self):
        """Draw the ship at its current location"""
        self.screen.blit(self.image, self.rect)
        
    def center_ship(self):
        """Center ship on the screen"""
        self.rect.midbottom = self.screen_rect.midbottom
        self.rect.y -= 50  # Padding from the bottom
        self.x = float(self.rect.x)