class Settings:
    """A class to store all settings for Breakout."""

    def __init__(self):
        """Initialize the game's static settings."""
        self.screen_width = 1800
        self.screen_height = 1000
        self.bg_color = (0, 0, 0)

        self.lives_limit = 3

        self.ball_speed = 10

        self.paddle_width = 75
        self.paddle_height = 25

        self.ball_radius = 15

        self.block_count = 11
        self.block_width = 100
        self.block_height = 40

        self.block_points = 1

    def initialize_dynamic_settings(self):
        """Initialize settings that change throughout the game."""
        self.ball_speed = 5
        self.paddle_width = 75
        self.ball_radius = 15
