import asyncio
import sys

import pygame
from pygame.locals import K_ESCAPE, K_SPACE, K_UP, KEYDOWN, QUIT

from .entities import (
    Background,
    Floor,
    GameOver,
    DarkGameOver,
    Pipes,
    Player,
    PlayerMode,
    Score,
    WelcomeMessage,
    DarkWelcomeMessage,
    VideoPlayer,
)
from .utils import GameConfig, Images, Sounds, Window, DarkTheme


class Flappy:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Flappy Bird - Dark Web Edition")
        window = Window(288, 512)
        screen = pygame.display.set_mode((window.width, window.height))
        
        # Initialize with no bird selection initially
        self.selected_bird_index = None
        
        # Detect if running on web
        self.is_web = self.detect_web_environment()
        
        self.config = GameConfig(
            screen=screen,
            clock=pygame.time.Clock(),
            fps=30,
            window=window,
            images=None,  # Will be set after bird selection
            sounds=Sounds(),
        )

    def detect_web_environment(self):
        """Detect if running in a web environment"""
        try:
            import platform
            import sys
            
            # Check for pygbag/web environment indicators
            if 'pygbag' in sys.modules:
                return True
            if platform.system() == 'Emscripten':
                return True
            if hasattr(sys, 'platform') and 'emscripten' in sys.platform:
                return True
        except:
            pass
        return False

    async def start(self):
        # Only one bird available (blue), so skip selection screen
        self.selected_bird_index = 0
        
        while True:
            # Stop all sounds when starting a new game
            self.config.sounds.stop_all()
            
            # Create images with selected bird
            self.config.images = Images(self.selected_bird_index)
            
            self.background = Background(self.config)
            self.floor = Floor(self.config)
            self.player = Player(self.config)
            
            # Use dark theme welcome message for web, regular for desktop
            if self.is_web:
                self.welcome_message = DarkWelcomeMessage(self.config)
                self.game_over_message = DarkGameOver(self.config)
            else:
                self.welcome_message = WelcomeMessage(self.config)
                self.game_over_message = GameOver(self.config)
            self.pipes = Pipes(self.config)
            self.score = Score(self.config)
            await self.splash()
            await self.play()
            await self.game_over()

    async def splash(self):
        """Shows welcome splash screen animation of flappy bird"""

        self.player.set_mode(PlayerMode.SHM)

        while True:
            for event in pygame.event.get():
                self.check_quit_event(event)
                
                # Check for dark welcome message input if using web mode
                if self.is_web and hasattr(self.welcome_message, 'handle_input'):
                    if self.welcome_message.handle_input(event):
                        return
                elif self.is_tap_event(event):
                    return

            self.background.tick()
            self.floor.tick()
            self.player.tick()
            self.welcome_message.tick()

            pygame.display.update()
            await asyncio.sleep(0)
            self.config.tick()

    def check_quit_event(self, event):
        if event.type == QUIT or (
            event.type == KEYDOWN and event.key == K_ESCAPE
        ):
            pygame.quit()
            sys.exit()

    def is_tap_event(self, event):
        m_left, _, _ = pygame.mouse.get_pressed()
        space_or_up = event.type == KEYDOWN and (
            event.key == K_SPACE or event.key == K_UP
        )
        screen_tap = event.type == pygame.FINGERDOWN
        return m_left or space_or_up or screen_tap

    async def play(self):
        self.score.reset()
        self.player.set_mode(PlayerMode.NORMAL)

        while True:
            if self.player.collided(self.pipes, self.floor):
                return

            for i, pipe in enumerate(self.pipes.upper):
                if self.player.crossed(pipe):
                    self.score.add()

            for event in pygame.event.get():
                self.check_quit_event(event)
                if self.is_tap_event(event):
                    self.player.flap()

            self.background.tick()
            self.floor.tick()
            self.pipes.tick()
            self.score.tick()
            self.player.tick()

            pygame.display.update()
            await asyncio.sleep(0)
            self.config.tick()

    async def game_over(self):
        """crashes the player down and shows gameover image"""

        self.player.set_mode(PlayerMode.CRASH)
        self.pipes.stop()
        self.floor.stop()

        # Wait for player to hit the ground
        while True:
            for event in pygame.event.get():
                self.check_quit_event(event)
                if self.is_tap_event(event):
                    if self.player.y + self.player.h >= self.floor.y - 1:
                        break

            self.background.tick()
            self.floor.tick()
            self.pipes.tick()
            self.score.tick()
            self.player.tick()
            self.game_over_message.tick()

            self.config.tick()
            pygame.display.update()
            await asyncio.sleep(0)
            
            if self.player.y + self.player.h >= self.floor.y - 1:
                break

        # Stop any remaining sounds before video
        self.config.sounds.stop_all()
        
        # Show video after crash
        await self.show_game_over_video()

    async def show_game_over_video(self):
        """Show game over video with skip option"""
        import os
        
        # Stop all ongoing sounds before video
        self.config.sounds.stop_all()
        
        # Try to find a video file
        video_paths = [
            "assets/videos/gameover.mp4",
            "assets/videos/gameover.avi", 
            "assets/videos/gameover.mov"
        ]
        
        video_path = None
        for path in video_paths:
            if os.path.exists(path):
                video_path = path
                break
        
        if not video_path:
            video_path = "assets/videos/gameover.mp4"  # Use default path for placeholder
        
        # Create video player
        video_player = VideoPlayer(self.config, video_path)
        video_player.play()
        
        # Video playback loop
        video_start_time = pygame.time.get_ticks()
        max_video_duration = 10000  # 10 seconds max
        
        while True:
            current_time = pygame.time.get_ticks()
            video_elapsed = current_time - video_start_time
            
            # Check for skip input
            for event in pygame.event.get():
                self.check_quit_event(event)
                if self.is_tap_event(event):
                    video_player.stop()
                    video_player.cleanup()
                    return
            
            # Auto-skip after max duration
            if video_elapsed >= max_video_duration:
                video_player.stop()
                video_player.cleanup()
                return
                
            # Check if video finished naturally
            if video_player.is_finished():
                video_player.cleanup()
                return
            
            # Clear screen and draw video
            self.config.screen.fill((0, 0, 0))
            video_player.tick()
            video_player.draw(self.config.screen)
            
            pygame.display.update()
            await asyncio.sleep(0)
            self.config.tick()
