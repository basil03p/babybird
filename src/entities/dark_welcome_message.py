import pygame
from pygame.locals import K_SPACE, K_UP, KEYDOWN, MOUSEBUTTONDOWN

from ..utils import GameConfig, DarkTheme
from .entity import Entity


class DarkWelcomeMessage(Entity):
    def __init__(self, config: GameConfig) -> None:
        # Create a larger dark-themed welcome screen
        width = config.window.width
        height = config.window.height
        
        # Create dark background
        image = DarkTheme.create_dark_surface(width, height)
        super().__init__(config, image, 0, 0)
        
        self.config = config
        self.create_dark_welcome()
        
        # Animation properties
        self.pulse_timer = 0
        self.glow_intensity = 0
        
    def create_dark_welcome(self):
        """Create a modern dark-themed welcome screen"""
        width = self.config.window.width
        height = self.config.window.height
        
        # Clear with dark gradient background
        gradient_bg = DarkTheme.create_gradient_surface(
            width, height,
            DarkTheme.BACKGROUND_DARK,
            DarkTheme.BACKGROUND_MEDIUM
        )
        self.image.blit(gradient_bg, (0, 0))
        
        # Create fonts
        try:
            title_font = pygame.font.Font(None, 48)
            subtitle_font = pygame.font.Font(None, 32) 
            instruction_font = pygame.font.Font(None, 24)
            small_font = pygame.font.Font(None, 18)
        except:
            title_font = pygame.font.SysFont('Arial', 48, bold=True)
            subtitle_font = pygame.font.SysFont('Arial', 32)
            instruction_font = pygame.font.SysFont('Arial', 24)
            small_font = pygame.font.SysFont('Arial', 18)
        
        # Main title with glow effect
        title_text = "FLAPPY BIRD"
        title_surface = title_font.render(title_text, True, DarkTheme.ACCENT_BLUE)
        
        # Create glow effect for title
        glow_surface = title_font.render(title_text, True, (*DarkTheme.ACCENT_BLUE, 100))
        title_rect = title_surface.get_rect(centerx=width//2, y=80)
        
        # Draw multiple glow layers
        for offset in [(2, 2), (-2, -2), (2, -2), (-2, 2)]:
            glow_rect = title_rect.move(offset)
            self.image.blit(glow_surface, glow_rect)
        
        self.image.blit(title_surface, title_rect)
        
        # Subtitle
        subtitle_text = "Dark Web Edition"
        subtitle_surface = subtitle_font.render(subtitle_text, True, DarkTheme.TEXT_SECONDARY)
        subtitle_rect = subtitle_surface.get_rect(centerx=width//2, y=title_rect.bottom + 10)
        self.image.blit(subtitle_surface, subtitle_rect)
        
        # Central panel with game instructions
        panel_rect = pygame.Rect(width//2 - 120, height//2 - 80, 240, 160)
        DarkTheme.draw_dark_panel(self.image, panel_rect, "HOW TO PLAY", instruction_font)
        
        # Game instructions
        instructions = [
            "🎮 SPACE or UP to flap",
            "🎯 Avoid the pipes", 
            "🏆 Score as high as you can",
            "",
            "✨ Enhanced with:",
            "• Dark UI theme",
            "• Death background music",
            "• Bigger blue bird",
            "• Real video playback"
        ]
        
        y_offset = panel_rect.y + 40
        for instruction in instructions:
            if instruction:
                color = DarkTheme.ACCENT_GREEN if instruction.startswith("✨") else DarkTheme.TEXT_SECONDARY
                if instruction.startswith("•"):
                    color = DarkTheme.TEXT_MUTED
                    instruction_surface = small_font.render(instruction, True, color)
                else:
                    instruction_surface = small_font.render(instruction, True, color)
                
                instruction_rect = instruction_surface.get_rect(centerx=width//2, y=y_offset)
                self.image.blit(instruction_surface, instruction_rect)
            y_offset += 16
        
        # Start button
        button_rect = pygame.Rect(width//2 - 80, height - 100, 160, 40)
        DarkTheme.draw_dark_button(self.image, button_rect, "PRESS SPACE TO START", instruction_font)
        
        # Web deployment info
        web_text = "🌐 Deployed with pygbag • Optimized for web"
        web_surface = small_font.render(web_text, True, DarkTheme.TEXT_MUTED)
        web_rect = web_surface.get_rect(centerx=width//2, y=height - 20)
        self.image.blit(web_surface, web_rect)
        
        # Add some decorative elements
        self.add_decorative_elements()
    
    def add_decorative_elements(self):
        """Add decorative elements to make the UI more appealing"""
        width = self.config.window.width
        height = self.config.window.height
        
        # Corner decorations
        corner_size = 20
        for x, y in [(0, 0), (width-corner_size, 0), (0, height-corner_size), (width-corner_size, height-corner_size)]:
            corner_rect = pygame.Rect(x, y, corner_size, corner_size)
            pygame.draw.rect(self.image, DarkTheme.ACCENT_PURPLE, corner_rect)
            
        # Side accent lines
        pygame.draw.rect(self.image, DarkTheme.ACCENT_BLUE, (0, 0, 3, height))
        pygame.draw.rect(self.image, DarkTheme.ACCENT_BLUE, (width-3, 0, 3, height))
    
    def update_animation(self):
        """Update pulsing animations"""
        self.pulse_timer += self.config.clock.get_time()
        
        # Recreate the welcome screen with updated animation
        if self.pulse_timer >= 100:  # Update every 100ms
            self.create_dark_welcome()
            self.pulse_timer = 0
    
    def tick(self):
        """Update the welcome message"""
        self.update_animation()
        super().tick()
    
    def handle_input(self, event):
        """Handle input events"""
        if event.type == KEYDOWN:
            if event.key in [K_SPACE, K_UP]:
                return True
        elif event.type == MOUSEBUTTONDOWN:
            return True
        return False