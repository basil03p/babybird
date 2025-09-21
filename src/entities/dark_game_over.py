import pygame
from pygame.locals import K_SPACE, K_UP, KEYDOWN, MOUSEBUTTONDOWN

from ..utils import GameConfig, DarkTheme
from .entity import Entity


class DarkGameOver(Entity):
    def __init__(self, config: GameConfig) -> None:
        # Create dark-themed game over screen
        width = config.window.width  
        height = config.window.height
        
        image = DarkTheme.create_dark_surface(width, height, 200)
        super().__init__(config, image, 0, 0)
        
        self.config = config
        self.animation_timer = 0
        self.create_dark_game_over()
        
    def create_dark_game_over(self):
        """Create a modern dark-themed game over screen"""
        width = self.config.window.width
        height = self.config.window.height
        
        # Clear with dark semi-transparent background
        self.image.fill((*DarkTheme.BACKGROUND_DARK, 180))
        
        # Create fonts
        try:
            title_font = pygame.font.Font(None, 56)
            subtitle_font = pygame.font.Font(None, 28)
            instruction_font = pygame.font.Font(None, 22)
        except:
            title_font = pygame.font.SysFont('Arial', 56, bold=True)
            subtitle_font = pygame.font.SysFont('Arial', 28)
            instruction_font = pygame.font.SysFont('Arial', 22)
        
        # Game Over title with glow effect
        title_text = "GAME OVER"
        title_surface = title_font.render(title_text, True, DarkTheme.ACCENT_PURPLE)
        
        # Create red glow for dramatic effect
        glow_color = (255, 100, 100)
        glow_surface = title_font.render(title_text, True, glow_color)
        title_rect = title_surface.get_rect(centerx=width//2, y=100)
        
        # Draw glow layers
        for offset in [(3, 3), (-3, -3), (3, -3), (-3, 3), (0, 3), (0, -3), (3, 0), (-3, 0)]:
            glow_rect = title_rect.move(offset)
            glow_alpha = pygame.Surface(glow_surface.get_size(), pygame.SRCALPHA)
            glow_alpha.blit(glow_surface, (0, 0))
            glow_alpha.set_alpha(30)
            self.image.blit(glow_alpha, glow_rect)
        
        self.image.blit(title_surface, title_rect)
        
        # Central panel for stats and restart info
        panel_rect = pygame.Rect(width//2 - 130, height//2 - 60, 260, 120)
        DarkTheme.draw_dark_panel(self.image, panel_rect)
        
        # Score display placeholder (will be updated by game)
        score_text = "Final Score: ---"
        score_surface = subtitle_font.render(score_text, True, DarkTheme.ACCENT_GREEN)
        score_rect = score_surface.get_rect(centerx=width//2, y=panel_rect.y + 30)
        self.image.blit(score_surface, score_rect)
        
        # Best score placeholder
        best_text = "Best Score: ---"
        best_surface = instruction_font.render(best_text, True, DarkTheme.TEXT_SECONDARY)
        best_rect = best_surface.get_rect(centerx=width//2, y=score_rect.bottom + 15)
        self.image.blit(best_surface, best_rect)
        
        # Restart instructions
        restart_text = "SPACE to play again • ESC to quit"
        restart_surface = instruction_font.render(restart_text, True, DarkTheme.TEXT_PRIMARY)
        restart_rect = restart_surface.get_rect(centerx=width//2, y=panel_rect.bottom + 20)
        self.image.blit(restart_surface, restart_rect)
        
        # Add some decorative elements
        self.add_game_over_decorations()
    
    def add_game_over_decorations(self):
        """Add decorative elements for game over screen"""
        width = self.config.window.width
        height = self.config.window.height
        
        # Corner X marks to indicate game over
        corner_size = 15
        line_width = 3
        
        # Top corners
        for x_pos in [20, width - 35]:
            # Draw X
            start1 = (x_pos, 20)
            end1 = (x_pos + corner_size, 20 + corner_size)
            start2 = (x_pos + corner_size, 20)
            end2 = (x_pos, 20 + corner_size)
            
            pygame.draw.line(self.image, DarkTheme.ACCENT_PURPLE, start1, end1, line_width)
            pygame.draw.line(self.image, DarkTheme.ACCENT_PURPLE, start2, end2, line_width)
        
        # Bottom accent line
        pygame.draw.rect(self.image, DarkTheme.ACCENT_PURPLE, (0, height-5, width, 5))
    
    def update_score_display(self, current_score, best_score):
        """Update the score display on the game over screen"""
        # Recreate the game over screen with updated scores
        self.create_dark_game_over()
        
        width = self.config.window.width
        
        try:
            subtitle_font = pygame.font.Font(None, 28)
            instruction_font = pygame.font.Font(None, 22)
        except:
            subtitle_font = pygame.font.SysFont('Arial', 28)
            instruction_font = pygame.font.SysFont('Arial', 22)
        
        # Update score display
        panel_rect = pygame.Rect(width//2 - 130, self.config.window.height//2 - 60, 260, 120)
        
        # Clear the score area and redraw with actual scores
        score_area = pygame.Rect(panel_rect.x + 10, panel_rect.y + 20, panel_rect.width - 20, 60)
        pygame.draw.rect(self.image, DarkTheme.BACKGROUND_MEDIUM, score_area)
        
        # Current score
        score_text = f"Final Score: {current_score}"
        score_surface = subtitle_font.render(score_text, True, DarkTheme.ACCENT_GREEN)
        score_rect = score_surface.get_rect(centerx=width//2, y=panel_rect.y + 30)
        self.image.blit(score_surface, score_rect)
        
        # Best score
        best_text = f"Best Score: {best_score}"
        best_color = DarkTheme.ACCENT_BLUE if current_score >= best_score else DarkTheme.TEXT_SECONDARY
        best_surface = instruction_font.render(best_text, True, best_color)
        best_rect = best_surface.get_rect(centerx=width//2, y=score_rect.bottom + 15)
        self.image.blit(best_surface, best_rect)
        
        # New record indicator
        if current_score >= best_score and best_score > 0:
            record_text = "🏆 NEW RECORD!"
            record_surface = instruction_font.render(record_text, True, DarkTheme.ACCENT_GREEN)
            record_rect = record_surface.get_rect(centerx=width//2, y=best_rect.bottom + 10)
            self.image.blit(record_surface, record_rect)
    
    def tick(self):
        """Update the game over screen with subtle animations"""
        self.animation_timer += self.config.clock.get_time()
        
        # Add subtle pulsing effect every 2 seconds
        if self.animation_timer >= 2000:
            self.animation_timer = 0
            # Could add subtle animation effects here
        
        super().tick()