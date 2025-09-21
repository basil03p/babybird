# Pygbag Configuration for Flappy Bird Web Deployment

# Required packages for web build
install_requires = [
    "pygame>=2.6.0",
    "pillow>=10.0.0",
    "opencv-python-headless>=4.8.0",  # Use headless version for web
]

# Pygbag specific settings
pygbag_config = {
    "width": 288,
    "height": 512,
    "name": "flappy-bird-dark",
    "title": "Flappy Bird - Dark Web Edition",
    "author": "Enhanced by AI",
    "description": "Classic Flappy Bird game with modern dark theme and web optimization",
    "template": "index.html",
    "icon": "flappy.ico",
    "cdn": "https://cdn.jsdelivr.net/pyodide/",
    "archive": False,
    "ume_block": 0,
    "cdn_python": "3.11",
    "optimize": True,
}

# Assets to include in web build
assets = [
    "assets/",
    "src/",
    "flappy.ico",
    "main.py",
]

# Files to exclude from web build
exclude = [
    "*.backup",
    "__pycache__/",
    "*.pyc",
    ".git/",
    ".venv/",
    "resize_sprites.py",
    "video_player_old.py",
]