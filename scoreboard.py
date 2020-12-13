import pygame.font
from pygame.sprite import Group
from ball import Ball


class Scoreboard:
    """A class to report scoring information."""

    def __init__(self, bo_game):
        """Initialize scorekeeping attributes."""
        self.bo_game = bo_game
        self.screen = bo_game.screen
        self.screen_rect = self.screen.get_rect()
        self.settings = bo_game.settings
        self.stats = bo_game.stats

        # Font settings for scoring information.
        self.text_color = (255, 255, 255)
        self.font = pygame.font.SysFont('freesansbold', 48)

        # Prepare the initial score images.
        self.prep_score()
        self.prep_high_score()
        self.prep_level()
        self.prep_balls()

    def prep_score(self):
        """Turn the score into a rendered image."""
        rounded_score = self.stats.score
        score_str = "{:,}".format(rounded_score)
        self.score_image = self.font.render(score_str, True,
                                            self.text_color, self.settings.bg_color)

        # Display the score at the top right of the screen.
        self.score_rect = self.score_image.get_rect()
        self.score_rect.right = self.screen_rect.right - 20
        self.score_rect.top = 20

    def prep_high_score(self):
        """Turn the high score into a rendered image."""
        high_score = self.stats.high_score
        high_score_str = "{:,}".format(high_score)
        self.high_score_image = self.font.render(high_score_str, True,
                                                 self.text_color, self.settings.bg_color)

        # Center the high score at the top of the screen.
        self.high_score_rect = self.high_score_image.get_rect()
        self.high_score_rect.centerx = self.screen_rect.centerx
        self.high_score_rect.top = self.score_rect.top

    def prep_level(self):
        """Turn the level into a rendered image."""
        level_str = str(self.stats.level)
        self.level_image = self.font.render(level_str, True,
                                            self.text_color, self.settings.bg_color)

        # Position the level below the score.
        self.level_rect = self.level_image.get_rect()
        self.level_rect.x = 100
        self.level_rect.top = 20

    def prep_balls(self):
        """Show how many balls are left."""
        self.balls = Group()
        for ball_number in range(self.stats.lives_left):
            ball = Ball(self.bo_game)
            ball.rect.x = 10 + ball_number * ball.rect.width * 2
            ball.rect.y = 10
            self.balls.add(ball)

    def check_high_score(self):
        """Check to see if there's a new high score."""
        if self.stats.score > self.stats.high_score:
            self.stats.high_score = self.stats.score
            self.prep_high_score()

    def show_score(self):
        """Draw scores, level, and ships to the screen."""
        self.screen.blit(self.score_image, self.score_rect)
        self.screen.blit(self.high_score_image, self.high_score_rect)
        self.screen.blit(self.level_image, self.level_rect)
        self.balls.draw(self.screen)
