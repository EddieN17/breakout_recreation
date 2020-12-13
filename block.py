import pygame


class Block(pygame.sprite.Sprite):
    """A class to represent the blocks to be destroyed."""

    def __init__(self, color, width, height):
        """Initialize the blocks."""
        super().__init__()

        self.image = pygame.Surface([width, height])
        self.image.fill(color)
        pygame.draw.rect(self.image, color, [0, 0, width, height])
        self.rect = self.image.get_rect()
