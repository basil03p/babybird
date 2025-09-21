import pygame
import os
from pygame.locals import K_SPACE, K_ESCAPE, KEYDOWN

# Try to import OpenCV, fall back to placeholder if not available (web compatibility)
try:
    import cv2
    import numpy as np
    CV2_AVAILABLE = True
except ImportError:
    CV2_AVAILABLE = False

from ..utils import GameConfig, DarkTheme
from .entity import Entity


class VideoPlayer(Entity):
    def __init__(self, config: GameConfig, video_path: str) -> None:
        # Create a placeholder surface initially
        image = pygame.Surface((1, 1))
        super().__init__(config, image, 0, 0)
        
        self.video_path = video_path
        self.cap = None
        self.fps = 30
        self.frame_duration = 1000 / self.fps  # milliseconds per frame
        self.last_frame_time = 0
        self.current_frame = None
        self.video_ended = False
        self.video_loaded = False
        self.is_playing = False
        self.web_mode = not CV2_AVAILABLE
        
        # Try to load the video
        self.load_video()
        
    def load_video(self):
        """Load video file using OpenCV or create web-compatible placeholder"""
        if not CV2_AVAILABLE:
            print("OpenCV not available (web mode), using enhanced placeholder")
            self.create_web_placeholder()
            return True
        if not os.path.exists(self.video_path):
            print(f"Video file not found: {self.video_path}")
            self.create_web_placeholder()
            return False
            
        try:
            self.cap = cv2.VideoCapture(self.video_path)
            if not self.cap.isOpened():
                print(f"Could not open video: {self.video_path}")
                self.create_web_placeholder()
                return False
                
            # Get video properties
            self.fps = self.cap.get(cv2.CAP_PROP_FPS) or 30
            self.frame_duration = 1000 / self.fps
            
            print(f"Video loaded successfully: {self.video_path}")
            print(f"FPS: {self.fps}")
            self.video_loaded = True
            return True
            
        except Exception as e:
            print(f"Error loading video: {e}")
            self.create_web_placeholder()
            return False
    
    def create_web_placeholder(self):
        """Create an enhanced web-compatible placeholder"""
        width, height = 400, 300
        self.current_frame = DarkTheme.create_dark_surface(width, height)
        
        # Add dark theme styling
        gradient = DarkTheme.create_gradient_surface(
            width, height,
            DarkTheme.BACKGROUND_DARK,
            DarkTheme.BACKGROUND_MEDIUM
        )
        self.current_frame.blit(gradient, (0, 0))
        
        # Add border
        pygame.draw.rect(self.current_frame, DarkTheme.BORDER_COLOR, 
                        self.current_frame.get_rect(), 2)
        
        # Create fonts
        try:
            title_font = pygame.font.Font(None, 42)
            subtitle_font = pygame.font.Font(None, 24)
            small_font = pygame.font.Font(None, 18)
        except:
            title_font = pygame.font.SysFont('Arial', 42, bold=True)
            subtitle_font = pygame.font.SysFont('Arial', 24)
            small_font = pygame.font.SysFont('Arial', 18)
        
        # Title with glow effect
        title_text = "GAME OVER"
        title_surface = title_font.render(title_text, True, DarkTheme.ACCENT_PURPLE)
        title_rect = title_surface.get_rect(centerx=width//2, y=80)
        
        # Add glow
        glow_surface = title_font.render(title_text, True, (*DarkTheme.ACCENT_PURPLE, 100))
        for offset in [(2, 2), (-2, -2), (2, -2), (-2, 2)]:
            glow_rect = title_rect.move(offset)
            self.current_frame.blit(glow_surface, glow_rect)
        
        self.current_frame.blit(title_surface, title_rect)
        
        # Subtitle
        if self.web_mode:
            subtitle_text = "🌐 Web Mode - Enhanced Experience"
            color = DarkTheme.ACCENT_BLUE
        else:
            subtitle_text = "Video not available"
            color = DarkTheme.TEXT_SECONDARY
            
        subtitle_surface = subtitle_font.render(subtitle_text, True, color)
        subtitle_rect = subtitle_surface.get_rect(centerx=width//2, y=title_rect.bottom + 20)
        self.current_frame.blit(subtitle_surface, subtitle_rect)
        
        # Instructions
        instructions = [
            "✨ Dark theme optimized",
            "🎮 Responsive controls", 
            "📱 Mobile friendly",
            "",
            "Press SPACE to continue"
        ]
        
        y_start = subtitle_rect.bottom + 30
        for i, instruction in enumerate(instructions):
            if instruction:
                color = DarkTheme.ACCENT_GREEN if instruction.startswith("✨") else DarkTheme.TEXT_MUTED
                if instruction.startswith("Press"):
                    color = DarkTheme.TEXT_PRIMARY
                text_surface = small_font.render(instruction, True, color)
                text_rect = text_surface.get_rect(centerx=width//2, y=y_start + i * 20)
                self.current_frame.blit(text_surface, text_rect)

    def create_placeholder(self):
        """Create a placeholder when video cannot be loaded"""
        width, height = 400, 300
        self.current_frame = pygame.Surface((width, height))
        self.current_frame.fill((50, 50, 50))
        
        # Add text
        font = pygame.font.Font(None, 36)
        small_font = pygame.font.Font(None, 24)
        
        title = font.render("Game Over", True, (255, 255, 255))
        info = small_font.render("Video not available", True, (200, 200, 200))
        skip = small_font.render("Press SPACE to continue", True, (255, 255, 0))
        
        # Center text
        title_rect = title.get_rect(center=(width//2, height//2 - 40))
        info_rect = info.get_rect(center=(width//2, height//2))
        skip_rect = skip.get_rect(center=(width//2, height//2 + 40))
        
        self.current_frame.blit(title, title_rect)
        self.current_frame.blit(info, info_rect)
        self.current_frame.blit(skip, skip_rect)
    
    def get_next_frame(self):
        """Get the next frame from the video"""
        if not self.video_loaded or not self.cap:
            return None
            
        ret, frame = self.cap.read()
        if not ret:
            self.video_ended = True
            return None
            
        # Convert BGR to RGB (OpenCV uses BGR, pygame uses RGB)
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        
        # Convert to pygame surface
        frame = np.rot90(frame)  # Rotate for pygame
        frame = np.flipud(frame)  # Flip for pygame
        surface = pygame.surfarray.make_surface(frame)
        
        # Scale to fit screen while maintaining aspect ratio
        screen_width = self.config.window.width
        screen_height = self.config.window.height
        
        # Get original frame dimensions
        frame_width, frame_height = surface.get_size()
        
        # Calculate scaling to fit screen
        scale_x = screen_width / frame_width
        scale_y = screen_height / frame_height
        scale = min(scale_x, scale_y) * 0.8  # 80% of screen size
        
        new_width = int(frame_width * scale)
        new_height = int(frame_height * scale)
        
        scaled_surface = pygame.transform.scale(surface, (new_width, new_height))
        return scaled_surface
    
    def play(self):
        """Start video playback"""
        self.is_playing = True
        if not self.video_loaded:
            self.create_placeholder()
    
    def stop(self):
        """Stop video playback"""
        self.is_playing = False
    
    def update_animation(self):
        """Update video frame based on timing"""
        if not self.is_playing:
            return
            
        if self.video_loaded and not self.video_ended:
            current_time = pygame.time.get_ticks()
            if current_time - self.last_frame_time >= self.frame_duration:
                self.current_frame = self.get_next_frame()
                self.last_frame_time = current_time
    
    def tick(self):
        """Update the video player"""
        self.update_animation()
        super().tick()
    
    def draw(self, screen):
        """Draw the current video frame"""
        if self.current_frame:
            # Center the video on screen
            screen_rect = screen.get_rect()
            video_rect = self.current_frame.get_rect()
            video_rect.center = screen_rect.center
            
            screen.blit(self.current_frame, video_rect)
            
        # Draw skip instruction
        font = pygame.font.Font(None, 24)
        skip_text = font.render("Press SPACE to skip", True, (255, 255, 255))
        text_rect = skip_text.get_rect()
        text_rect.bottomright = (screen.get_width() - 10, screen.get_height() - 10)
        
        # Draw background for text
        bg_rect = text_rect.inflate(10, 5)
        pygame.draw.rect(screen, (0, 0, 0, 128), bg_rect)
        screen.blit(skip_text, text_rect)
    
    def handle_input(self, event):
        """Handle input events during video playback"""
        if event.type == KEYDOWN:
            if event.key == K_SPACE or event.key == K_ESCAPE:
                return "skip"
        return None
    
    def is_finished(self):
        """Check if video has ended"""
        return self.video_ended or not self.video_loaded
    
    def cleanup(self):
        """Clean up video resources"""
        if self.cap:
            self.cap.release()
            self.cap = None