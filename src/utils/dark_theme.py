"""
Dark Theme Configuration for Flappy Bird Web Version
"""
import pygame

class DarkTheme:
    """Dark theme colors and styling for the web version"""
    
    # Dark color palette
    BACKGROUND_DARK = (18, 18, 25)      # Very dark blue-gray
    BACKGROUND_MEDIUM = (25, 25, 35)    # Medium dark
    BACKGROUND_LIGHT = (35, 35, 45)     # Light dark
    
    # Accent colors
    ACCENT_BLUE = (64, 145, 255)        # Bright blue
    ACCENT_PURPLE = (138, 43, 226)      # Purple
    ACCENT_GREEN = (0, 255, 127)        # Bright green
    
    # Text colors
    TEXT_PRIMARY = (255, 255, 255)      # White
    TEXT_SECONDARY = (180, 180, 190)    # Light gray
    TEXT_MUTED = (120, 120, 130)        # Muted gray
    
    # UI colors
    BORDER_COLOR = (60, 60, 80)         # Dark border
    SHADOW_COLOR = (0, 0, 0, 100)       # Semi-transparent black
    
    @classmethod
    def create_dark_surface(cls, width, height, alpha=255):
        """Create a dark themed surface"""
        surface = pygame.Surface((width, height), pygame.SRCALPHA)
        surface.fill((*cls.BACKGROUND_DARK, alpha))
        return surface
    
    @classmethod
    def create_gradient_surface(cls, width, height, color1, color2, vertical=True):
        """Create a gradient surface between two colors"""
        surface = pygame.Surface((width, height))
        
        if vertical:
            for y in range(height):
                ratio = y / height
                r = int(color1[0] * (1 - ratio) + color2[0] * ratio)
                g = int(color1[1] * (1 - ratio) + color2[1] * ratio)
                b = int(color1[2] * (1 - ratio) + color2[2] * ratio)
                pygame.draw.line(surface, (r, g, b), (0, y), (width, y))
        else:
            for x in range(width):
                ratio = x / width
                r = int(color1[0] * (1 - ratio) + color2[0] * ratio)
                g = int(color1[1] * (1 - ratio) + color2[1] * ratio)
                b = int(color1[2] * (1 - ratio) + color2[2] * ratio)
                pygame.draw.line(surface, (r, g, b), (x, 0), (x, height))
        
        return surface
    
    @classmethod
    def draw_dark_button(cls, surface, rect, text, font, hover=False):
        """Draw a dark themed button"""
        # Button background
        bg_color = cls.ACCENT_BLUE if hover else cls.BACKGROUND_MEDIUM
        border_color = cls.ACCENT_BLUE if hover else cls.BORDER_COLOR
        
        # Draw button with rounded corners effect
        pygame.draw.rect(surface, bg_color, rect)
        pygame.draw.rect(surface, border_color, rect, 2)
        
        # Add inner glow effect
        inner_rect = rect.inflate(-4, -4)
        pygame.draw.rect(surface, (*cls.ACCENT_BLUE, 30), inner_rect)
        
        # Draw text
        text_color = cls.TEXT_PRIMARY
        text_surface = font.render(text, True, text_color)
        text_rect = text_surface.get_rect(center=rect.center)
        surface.blit(text_surface, text_rect)
    
    @classmethod
    def draw_dark_panel(cls, surface, rect, title=None, font=None):
        """Draw a dark themed panel"""
        # Panel background with gradient
        gradient = cls.create_gradient_surface(
            rect.width, rect.height, 
            cls.BACKGROUND_MEDIUM, cls.BACKGROUND_DARK
        )
        surface.blit(gradient, rect)
        
        # Border
        pygame.draw.rect(surface, cls.BORDER_COLOR, rect, 2)
        
        # Title if provided
        if title and font:
            title_surface = font.render(title, True, cls.TEXT_PRIMARY)
            title_rect = title_surface.get_rect(centerx=rect.centerx, y=rect.y + 10)
            surface.blit(title_surface, title_rect)
    
    @classmethod
    def apply_dark_overlay(cls, surface, alpha=128):
        """Apply a dark overlay to make backgrounds darker"""
        overlay = pygame.Surface(surface.get_size(), pygame.SRCALPHA)
        overlay.fill((*cls.BACKGROUND_DARK, alpha))
        surface.blit(overlay, (0, 0))