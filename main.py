import asyncio
import sys
import os

# Add pygbag support for web deployment
try:
    import pygbag
    PYGBAG_AVAILABLE = True
except ImportError:
    PYGBAG_AVAILABLE = False

from src.flappy import Flappy

async def main():
    """Main game entry point with web compatibility"""
    game = Flappy()
    await game.start()

if __name__ == "__main__":
    if PYGBAG_AVAILABLE:
        # Running on web with pygbag
        print("🌐 Running Flappy Bird in web mode")
        asyncio.run(main())
    else:
        # Running locally
        print("🎮 Running Flappy Bird locally")
        asyncio.run(main())
