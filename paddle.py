import pygame
from pygame.sprite import Sprite


class Paddle(Sprite):
    """A class to represent the paddle."""

    def __init__(self, bo_game):
        """Initialize the paddle and set its starting position."""
        super().__init__()
        self.screen = bo_game.screen
        self.settings = bo_game.settings
        self.screen_rect = bo_game.screen.get_rect()
        # Load image and get rect
        self.image = pygame.image.load('images/paddle.png')
        self.image = pygame.transform.scale(self.image, (self.settings.paddle_width, self.settings.paddle_height))
        self.rect = self.image.get_rect()
        # Start paddle at the bottom center of screen
        self.rect.midbottom = self.screen_rect.midbottom
        # Store values of paddle position
        self.x = float(self.rect.x)
        self.rect.y = self.rect.height
        self.y = float(self.rect.y)

    def update(self):
        """Update the paddles position based on mouse cursors x position"""
        if pygame.mouse.get_pos()[0] <= (self.screen_rect.right - 40):
            self.rect.x = pygame.mouse.get_pos()[0]

    def blitme(self):
        """Draw the paddle at its current location."""
        self.screen.blit(self.image, self.rect)
        self.rect.y = (self.screen_rect.bottom - 50)

    def center_paddle(self):
        """Center the paddle on the screen."""
        self.rect.midbottom = self.screen_rect.midbottom
