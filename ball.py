import pygame
import math


class Ball(pygame.sprite.Sprite):
    """A class to manage the ball."""
    direction = 35

    def __init__(self, bo_game):
        """Initialize the ball and set its starting position."""
        super().__init__()
        self.screen = bo_game.screen
        self.settings = bo_game.settings
        self.screen_rect = bo_game.screen.get_rect()
        # Load the ball image and set its rect attribute.
        self.image = pygame.image.load('images/ball.png')
        self.image = pygame.transform.scale(self.image, (self.settings.ball_radius, self.settings.ball_radius))
        self.rect = self.image.get_rect()
        self.rect.center = self.screen_rect.center
        # Store values of ball position
        self.x = float(self.rect.x)
        self.y = float(self.rect.y)

    def update(self):
        """Move the ball."""
        direction_radians = math.radians(self.direction)

        self.x += self.settings.ball_speed * math.sin(direction_radians)
        self.y += self.settings.ball_speed * math.cos(direction_radians)
        # Bounce off left side
        if self.x <= 0:
            self.direction = (360 - self.direction) % 360
            self.x = 1
        # Bounce off right side
        if self.x >= self.screen_rect.right:
            self.direction = (360 - self.direction) % 360
        # Bounce off top
        if self.y <= self.screen_rect.top:
            self.bounce(0)
        self.rect.x = self.x
        self.rect.y = self.y

    def bounce(self, diff):
        """Bounce the ball in a direction."""
        self.direction = (180 - self.direction) % 360
        self.direction -= diff

    def blitme(self):
        """Draw the ball at its current location."""
        self.screen.blit(self.image, self.rect)

    def center_ball(self):
        """Center the ball on the screen."""
        self.rect.center = self.screen_rect.center
