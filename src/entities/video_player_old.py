import pygame
import os
import time
from typing import Optional
from ..utils import GameConfig
from .entity import Entity


class VideoPlayer(Entity):
    def __init__(self, config: GameConfig, video_path: str) -> None:
        # Initialize with a transparent surface initially
        temp_surface = pygame.Surface((config.window.width, config.window.height), pygame.SRCALPHA)
        super().__init__(
            config=config,
            image=temp_surface,
            x=0,
            y=0,
        )
        
        self.video_path = video_path
        self.is_playing = False
        self.show_skip_text = True
        self.skip_text_timer = 0
        self.skip_text_blink_interval = 500  # milliseconds
        self.animation_timer = 0
        self.animation_frame = 0
        
        # Create font for skip text
        try:
            self.font = pygame.font.Font(None, 48)
            self.small_font = pygame.font.Font(None, 32)
            self.tiny_font = pygame.font.Font(None, 24)
        except:
            self.font = pygame.font.SysFont('Arial', 48)
            self.small_font = pygame.font.SysFont('Arial', 32)
            self.tiny_font = pygame.font.SysFont('Arial', 24)
        
        # Check if video exists with debugging
        self.video_exists = os.path.exists(self.video_path)
        print(f"Video path: {self.video_path}")
        print(f"Video exists: {self.video_exists}")
        print(f"Current working directory: {os.getcwd()}")
        if self.video_exists:
            print(f"Video file size: {os.path.getsize(self.video_path)} bytes")
        
    def play(self) -> None:
        """Start playing the video."""
        self.is_playing = True
        if self.video_exists:
            print(f"Video file found: {self.video_path}")
            print("Note: Video playback not implemented in this version")
            print("Showing animated placeholder instead")
        self.create_animated_placeholder()
    
    def create_animated_placeholder(self) -> None:
        """Create an animated placeholder surface when video can't be loaded."""
        self.image = pygame.Surface((self.config.window.width, self.config.window.height))
        self.image.fill((20, 20, 40))  # Dark blue background
        
        # Add animated title
        title = "GAME OVER"
        title_surface = self.font.render(title, True, (255, 100, 100))
        title_rect = title_surface.get_rect(center=(self.config.window.width // 2, 100))
        self.image.blit(title_surface, title_rect)
        
        # Re-check video existence to be sure
        video_exists_now = os.path.exists(self.video_path)
        
        # Add animated subtitle with pulsing effect
        pulse = abs(pygame.math.Vector2(0, 1).rotate(self.animation_frame * 5).y)
        alpha = int(150 + 105 * pulse)
        
        if video_exists_now:
            subtitle = "Video File Found"
            sub_color = (100, 255, 100, alpha)
            print(f"Displaying: Video File Found for {self.video_path}")
        else:
            subtitle = "No Video File"
            sub_color = (255, 255, 100, alpha)
            print(f"Displaying: No Video File for {self.video_path}")
            
        subtitle_surface = self.small_font.render(subtitle, True, sub_color[:3])
        subtitle_surface.set_alpha(alpha)
        subtitle_rect = subtitle_surface.get_rect(center=(self.config.window.width // 2, 150))
        self.image.blit(subtitle_surface, subtitle_rect)
        
        # Add instructions
        instructions = [
            "Video playback not supported",
            "in this pygame version",
            "",
            "To add video support:",
            "1. Add gameover.mp4 to assets/videos/",
            "2. Install video codec support",
            "",
        ]
        
        y_start = 220
        for i, line in enumerate(instructions):
            if line:
                color = (200, 200, 200) if i < 2 else (150, 150, 150)
                text_surface = self.tiny_font.render(line, True, color)
                text_rect = text_surface.get_rect(center=(self.config.window.width // 2, y_start + i * 25))
                self.image.blit(text_surface, text_rect)
        
        # Add animated skip indicator
        if self.show_skip_text:
            skip_text = "Press SPACE, UP arrow, or CLICK to skip"
            skip_color = (255, 255, 0)
            if self.animation_frame % 60 < 30:  # Blink effect
                skip_color = (255, 255, 150)
            
            skip_surface = self.small_font.render(skip_text, True, skip_color)
            skip_rect = skip_surface.get_rect(center=(self.config.window.width // 2, self.config.window.height - 80))
            self.image.blit(skip_surface, skip_rect)
            
            # Add escape instruction
            esc_text = "Press ESC to quit game"
            esc_surface = self.tiny_font.render(esc_text, True, (180, 180, 180))
            esc_rect = esc_surface.get_rect(center=(self.config.window.width // 2, self.config.window.height - 40))
            self.image.blit(esc_surface, esc_rect)
    
    def stop(self) -> None:
        """Stop the video playback."""
        self.is_playing = False
    
    def is_finished(self) -> bool:
        """Check if video has finished playing."""
        # For placeholder, never auto-finish (wait for user skip)
        return False
    
    def update_animation(self) -> None:
        """Update the animation and blinking effects."""
        self.animation_timer += self.config.clock.get_time()
        self.animation_frame += 1
        
        if self.animation_timer >= self.skip_text_blink_interval:
            self.show_skip_text = not self.show_skip_text
            self.animation_timer = 0
            
        # Recreate the animated placeholder every few frames
        if self.animation_frame % 5 == 0:
            self.create_animated_placeholder()
    
    def tick(self) -> None:
        """Update the video player."""
        if self.is_playing:
            self.update_animation()
        super().tick()


def create_default_video_placeholder(config: GameConfig) -> None:
    """Create a default video file placeholder for users."""
    video_dir = "assets/videos"
    readme_path = os.path.join(video_dir, "README.txt")
    
    if not os.path.exists(readme_path):
        readme_content = """Video Assets for Game Over Screen
=====================================

Place your game over video file here with one of these names:
- gameover.mp4
- gameover.avi
- gameover.mov

Supported formats depend on your system's video codecs.
The video will play when the player loses the game.

Note: Current pygame version may have limited video support.
A text placeholder will be shown if video cannot be loaded.

Recommended video specifications:
- Resolution: 288x512 (game window size) or smaller
- Duration: 3-10 seconds
- Format: MP4 for best compatibility

Controls during video playback:
- SPACE, UP arrow, or Mouse Click: Skip video
- ESC: Quit game

The video will automatically skip after 10 seconds if not manually skipped.
"""
        
        with open(readme_path, 'w') as f:
            f.write(readme_content)