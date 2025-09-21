import pygame
import os


class Sounds:
    die: pygame.mixer.Sound
    hit: pygame.mixer.Sound
    point: pygame.mixer.Sound
    swoosh: pygame.mixer.Sound
    wing: pygame.mixer.Sound

    def __init__(self) -> None:
        # Initialize sounds
        self.die = pygame.mixer.Sound("assets/audio/die.wav")
        self.hit = pygame.mixer.Sound("assets/audio/hit.wav")
        self.point = pygame.mixer.Sound("assets/audio/point.wav")
        self.swoosh = pygame.mixer.Sound("assets/audio/swoosh.wav")
        self.wing = pygame.mixer.Sound("assets/audio/wing.wav")
        
        # Death sound tracking
        self.death_channel = None
        
    def play_death_bgm(self) -> None:
        """Play death sound and track its channel"""
        try:
            # Play the death sound effect and track its channel
            self.death_channel = self.die.play()
        except Exception as e:
            print(f"Error playing death sound: {e}")
    
    def is_death_sound_playing(self) -> bool:
        """Check if death sound is still playing"""
        if self.death_channel:
            return self.death_channel.get_busy()
        return False
    
    def stop_all(self) -> None:
        """Stop all currently playing sounds"""
        pygame.mixer.stop()
        
    def stop_sound(self, sound_name: str) -> None:
        """Stop a specific sound"""
        sound = getattr(self, sound_name, None)
        if sound:
            sound.stop()
