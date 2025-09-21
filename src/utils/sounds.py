import pygame
import os


class Sounds:
    die: pygame.mixer.Sound
    hit: pygame.mixer.Sound
    point: pygame.mixer.Sound
    swoosh: pygame.mixer.Sound
    wing: pygame.mixer.Sound

    def __init__(self) -> None:
        self.die = pygame.mixer.Sound("assets/audio/die.wav")
        self.hit = pygame.mixer.Sound("assets/audio/hit.wav")
        self.point = pygame.mixer.Sound("assets/audio/point.wav")
        self.swoosh = pygame.mixer.Sound("assets/audio/swoosh.wav")
        self.wing = pygame.mixer.Sound("assets/audio/wing.wav")
        
        # Background music support
        self.bgm_playing = False
        self.death_bgm_path = "assets/audio/death_bgm.wav"  # You can add this file
        
    def play_death_bgm(self) -> None:
        """Play death background music"""
        try:
            if os.path.exists(self.death_bgm_path):
                pygame.mixer.music.load(self.death_bgm_path)
                pygame.mixer.music.play(-1)  # Loop indefinitely
                self.bgm_playing = True
                print("Playing death BGM")
            else:
                print(f"Death BGM file not found: {self.death_bgm_path}")
                # Play death sound longer as fallback
                self.die.play()
        except Exception as e:
            print(f"Error playing death BGM: {e}")
            self.die.play()
    
    def stop_bgm(self) -> None:
        """Stop background music"""
        if self.bgm_playing:
            pygame.mixer.music.stop()
            self.bgm_playing = False
            print("Stopped BGM")

    def stop_all(self) -> None:
        """Stop all currently playing sounds"""
        pygame.mixer.stop()
        self.stop_bgm()
        
    def stop_sound(self, sound_name: str) -> None:
        """Stop a specific sound"""
        sound = getattr(self, sound_name, None)
        if sound:
            sound.stop()
