class GameStats:
    """Track statistics for Breakout."""

    def __init__(self, bo_game):
        """Initialize statistics."""
        self.settings = bo_game.settings
        self.reset_stats()

        # Start game in an inactive state.
        self.game_active = False

        # High score should never be reset.
        self.high_score = 0

    def reset_stats(self):
        """Initialize statistics that can change during the game."""
        self.lives_left = self.settings.lives_limit
        self.score = 0
        self.level = 1
