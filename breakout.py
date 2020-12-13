# Eddie Noyes
# Breakout
# 12-1-2020
# 12-12-2020 Version 1.0

import sys
import pygame
from settings import Settings
from paddle import Paddle
from button import Button
from game_stats import GameStats
from ball import Ball
from scoreboard import Scoreboard
from block import Block
from time import sleep
clock = pygame.time.Clock()  # Function to cap frame rate

# Defined Colors for Blocks
LIGHT_BLUE = (0, 175, 255)
RED = (255, 0, 0)
ORANGE = (255, 165, 0)
LIME_GREEN = (0, 255, 0)
DARK_BLUE = (0, 0, 255)


class Breakout:
    """Overall class to manage game assets and behaviors."""

    def __init__(self):
        """Initialize the game, and create game resources."""
        pygame.init()
        self.settings = Settings()
        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self.settings.screen_width = self.screen.get_rect().width
        self.settings.screen_height = self.screen.get_rect().height
        pygame.display.set_caption("Breakout")

        self.stats = GameStats(self)
        self.sb = Scoreboard(self)
        self.paddle = Paddle(self)
        self.ball = Ball(self)
        self.all_sprites_list = pygame.sprite.Group()
        self.blocks = pygame.sprite.Group()

        self.play_button = Button(self, "Play")
        self.games_ran = 0

    def run_game(self):
        """Start the main loop for the game."""
        while True:
            clock.tick(60)
            self._check_events()

            if self.stats.game_active:
                self.paddle.update()
                self.paddle_collision()
                self.ball.update()
                self.check_ball_block_collision()
                self.check_ball_bottom()

            self._update_screen()

    def _check_events(self):
        """Respond to keypresses and mouse events."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self._check_play_button(mouse_pos)

    def _check_keydown_events(self, event):
        """Respond to keypresses."""
        # Exit game if 'ESCAPE' key is pressed
        if event.key == pygame.K_ESCAPE:
            sys.exit()

    def _check_play_button(self, mouse_pos):
        """Start a new game when the player clicks Play."""
        button_clicked = self.play_button.rect.collidepoint(mouse_pos)
        if button_clicked and not self.stats.game_active:
            # Reset the game settings.
            self.games_ran += 1
            self.settings.initialize_dynamic_settings()
            # Reset the game statistics.
            self.stats.reset_stats()
            if self.games_ran == 1:
                # Fixes bug where the first ran game had an extra life
                self.stats.lives_left = 2
            self.stats.game_active = True
            self.sb.prep_score()
            self.sb.prep_level()
            self.sb.prep_balls()

            # Create a new row and center the ball
            self.create_row()
            self.ball.center_ball()

            # Hide the mouse cursor.
            pygame.mouse.set_visible(False)

    def paddle_collision(self):
        """Formulas to make the ball bounce off the paddle in a predictable fashion."""
        if self.ball.rect.colliderect(self.paddle):
            diff = (self.paddle.rect.x + self.settings.paddle_width / 2) - (self.ball.rect.x + self.settings.ball_radius / 2)
            self.ball.rect.y = self.screen.get_rect().height - self.settings.paddle_height - self.settings.ball_radius - 1
            self.ball.bounce(diff)

    def create_row(self):
        """Create the row of blocks."""
        for i in range(14):
            block = Block(LIGHT_BLUE, 105, 30)
            block.rect.x = 10 + i* 110
            block.rect.y = 60
            self.all_sprites_list.add(block)
            self.blocks.add(block)
        for i in range(14):
            block = Block(RED, 105, 30)
            block.rect.x = 10 + i* 110
            block.rect.y = 100
            self.all_sprites_list.add(block)
            self.blocks.add(block)
        for i in range(14):
            block = Block(ORANGE, 105, 30)
            block.rect.x = 10 + i* 110
            block.rect.y = 140
            self.all_sprites_list.add(block)
            self.blocks.add(block)
        for i in range(14):
            block = Block(LIME_GREEN, 105, 30)
            block.rect.x = 10 + i* 110
            block.rect.y = 180
            self.all_sprites_list.add(block)
            self.blocks.add(block)
        for i in range(14):
            block = Block(DARK_BLUE, 105, 30)
            block.rect.x = 10 + i* 110
            block.rect.y = 220
            self.all_sprites_list.add(block)
            self.blocks.add(block)

    def check_ball_block_collision(self):
        """Respond to ball-block collisions."""
        for block in self.blocks:
            if self.ball.rect.colliderect(block):
                self.ball.bounce(0)
                self.blocks.remove(block)
                self.stats.score += self.settings.block_points
                self.sb.prep_score()
                self.sb.check_high_score()
                # Change ball speed in correlation with block color
                if block.rect.y == 220:
                    self.settings.ball_speed = 12
                elif block.rect.y == 180:
                    self.settings.ball_speed = 14
                elif block.rect.y == 140:
                    self.settings.ball_speed = 16
                elif block.rect.y == 100:
                    self.settings.ball_speed = 18
                elif block.rect.y == 60:
                    self.settings.ball_speed = 20
        if not self.blocks:
            # Remake game and make it a new level
            self.stats.level += 1
            self.sb.prep_level()
            self.sb.prep_balls()
            self.ball.center_ball()
            sleep(1)
            self.ball.__init__(self)
            self.settings.ball_speed = 10
            self.create_row()
            self.ball.bounce(0)

    def check_ball_bottom(self):
        """Check if any ball have reached the bottom of the screen."""
        screen_rect = self.screen.get_rect()
        if self.ball.rect.bottom >= screen_rect.bottom:
            # Treat this the same as if the ship got hit.
            self.ball_lost()

    def ball_lost(self):
        """Respond to the ball hitting the bottom of the screen."""
        if self.stats.lives_left > 0:
            self.stats.lives_left -= 1
            self.sb.prep_balls()
            self.ball.center_ball()
            sleep(1)
            self.ball.__init__(self)
            self.settings.ball_speed = 10
        else:
            # End game if no lives are left
            self.stats.game_active = False
            self.blocks.empty()
            self.settings.ball_speed = 10
            pygame.mouse.set_visible(True)

    def _update_screen(self):
        """Update images on the screen and flip to the updated screen."""
        self.screen.fill(self.settings.bg_color)
        self.paddle.blitme()
        self.ball.blitme()
        self.blocks.draw(self.screen)
        self.sb.show_score()

        if not self.stats.game_active:
            self.play_button.draw_button()
        pygame.display.flip()

if __name__ == '__main__':
    # Make a game instance and run the game.
    bo = Breakout()
    bo.run_game()
