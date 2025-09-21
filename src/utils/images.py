import random
from typing import List, Tuple

import pygame

from .constants import BACKGROUNDS, PIPES, PLAYERS


class Images:
    numbers: List[pygame.Surface]
    game_over: pygame.Surface
    welcome_message: pygame.Surface
    base: pygame.Surface
    background: pygame.Surface
    player: Tuple[pygame.Surface]
    pipe: Tuple[pygame.Surface]

    def __init__(self, selected_bird_index: int = None) -> None:
        self.numbers = list(
            (
                pygame.image.load(f"assets/sprites/{num}.png").convert_alpha()
                for num in range(10)
            )
        )

        # game over sprite
        self.game_over = pygame.image.load(
            "assets/sprites/gameover.png"
        ).convert_alpha()
        # welcome_message sprite for welcome screen
        self.welcome_message = pygame.image.load(
            "assets/sprites/message.png"
        ).convert_alpha()
        # base (ground) sprite
        self.base = pygame.image.load("assets/sprites/base.png").convert_alpha()
        self.randomize(selected_bird_index)

    def randomize(self, selected_bird_index: int = None):
        # select random background sprites
        rand_bg = random.randint(0, len(BACKGROUNDS) - 1)
        
        # select player sprites - use selected bird or random
        if selected_bird_index is not None:
            rand_player = selected_bird_index
        else:
            rand_player = random.randint(0, len(PLAYERS) - 1)
            
        # Ensure the selected bird index is valid
        if rand_player >= len(PLAYERS):
            rand_player = 0  # Fallback to first bird
            
        # select random pipe sprites
        rand_pipe = random.randint(0, len(PIPES) - 1)

        self.background = pygame.image.load(BACKGROUNDS[rand_bg]).convert()
        
        # Try to load the selected player sprites, fallback to first bird if failed
        try:
            self.player = (
                pygame.image.load(PLAYERS[rand_player][0]).convert_alpha(),
                pygame.image.load(PLAYERS[rand_player][1]).convert_alpha(),
                pygame.image.load(PLAYERS[rand_player][2]).convert_alpha(),
            )
        except (pygame.error, FileNotFoundError) as e:
            print(f"Warning: Could not load bird sprites for bird {rand_player}: {e}")
            print("Falling back to first bird (Red Bird)")
            # Fallback to the first bird (red bird)
            self.player = (
                pygame.image.load(PLAYERS[0][0]).convert_alpha(),
                pygame.image.load(PLAYERS[0][1]).convert_alpha(),
                pygame.image.load(PLAYERS[0][2]).convert_alpha(),
            )
            
        self.pipe = (
            pygame.transform.flip(
                pygame.image.load(PIPES[rand_pipe]).convert_alpha(),
                False,
                True,
            ),
            pygame.image.load(PIPES[rand_pipe]).convert_alpha(),
        )
