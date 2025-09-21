import pygame
from ..utils import GameConfig
from .entity import Entity


class EnhancedGameOver(Entity):
    def __init__(self, config: GameConfig) -> None:
        super().__init__(
            config=config,
            image=config.images.game_over,
            x=(config.window.width - config.images.game_over.get_width()) // 2,
            y=int(config.window.height * 0.2),
        )
        
        # Create text surfaces for the try again message
        self.font_large = pygame.font.Font(None, 36)
        self.font_small = pygame.font.Font(None, 24)
        
        # Create "Try Again?" text
        self.try_again_text = self.font_large.render("Try Again?", True, (255, 255, 255))
        self.try_again_rect = self.try_again_text.get_rect(
            centerx=config.window.width // 2,
            y=self.y + self.image.get_height() + 30
        )
        
        # Create instruction text
        self.instruction_text = self.font_small.render("Press SPACE or tap to restart", True, (200, 200, 200))
        self.instruction_rect = self.instruction_text.get_rect(
            centerx=config.window.width // 2,
            y=self.try_again_rect.bottom + 15
        )
        
        # Animation variables
        self.blink_timer = 0
        self.show_try_again = True
        
    def tick(self) -> None:
        super().tick()
        
        # Animate the "Try Again?" text with blinking effect
        self.blink_timer += 1
        if self.blink_timer >= 30:  # Blink every 30 frames (about 0.5 seconds at 60 FPS)
            self.show_try_again = not self.show_try_again
            self.blink_timer = 0
        
        # Draw the game over image
        self.config.screen.blit(self.image, (self.x, self.y))
        
        # Draw the try again text (with blinking)
        if self.show_try_again:
            self.config.screen.blit(self.try_again_text, self.try_again_rect)
        
        # Always draw the instruction text
        self.config.screen.blit(self.instruction_text, self.instruction_rect)