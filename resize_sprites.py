#!/usr/bin/env python3
"""
Image Resizer for Flappy Bird Sprites
Resizes custom bird images to match the original game's dimensions
"""

import os
import sys
from PIL import Image, ImageOps

def get_target_size(sprite_name):
    """Get the expected size for different sprite types"""
    # Define expected sizes for different game assets
    sprite_sizes = {
        # Bird sprites (making blue bird bigger)
        'bird': (45, 32),  # Increased from (34, 24) - 32% larger
        
        # UI elements  
        'message.png': (184, 267),      # Welcome message
        'gameover.png': (204, 54),      # Game over text
        
        # Numbers (0-9)
        'number': (24, 36),
        
        # Background and ground
        'background-day.png': (288, 512),
        'background-night.png': (288, 512),
        'base.png': (336, 112),
        
        # Pipes
        'pipe-green.png': (52, 320),
        'pipe-red.png': (52, 320),
    }
    
    # Check for specific files
    if sprite_name in sprite_sizes:
        return sprite_sizes[sprite_name]
    
    # Check for bird sprites
    if 'bird' in sprite_name and any(pos in sprite_name for pos in ['upflap', 'midflap', 'downflap']):
        return sprite_sizes['bird']
    
    # Check for number sprites
    if sprite_name in [f'{i}.png' for i in range(10)]:
        return sprite_sizes['number']
    
    # Default fallback
    return None

def resize_image(input_path, output_path, target_size):
    """Resize an image to target size while maintaining aspect ratio"""
    try:
        with Image.open(input_path) as img:
            # Convert to RGBA if not already (for transparency)
            if img.mode != 'RGBA':
                img = img.convert('RGBA')
            
            # Resize while maintaining aspect ratio
            img.thumbnail(target_size, Image.Resampling.LANCZOS)
            
            # Create a new image with the exact target size and transparent background
            final_img = Image.new('RGBA', target_size, (0, 0, 0, 0))
            
            # Center the resized image
            paste_x = (target_size[0] - img.width) // 2
            paste_y = (target_size[1] - img.height) // 2
            final_img.paste(img, (paste_x, paste_y), img)
            
            # Save the result
            final_img.save(output_path, 'PNG', optimize=True)
            print(f"[OK] Resized {input_path} -> {output_path} ({img.size} -> {target_size})")
            return True
            
    except Exception as e:
        print(f"Error resizing {input_path}: {e}")
        return False

def main():
    """Main function to resize all game sprites"""
    print("Flappy Bird Sprite Resizer")
    print("=" * 40)
    
    sprites_dir = "assets/sprites"
    if not os.path.exists(sprites_dir):
        print(f"[ERROR] Directory {sprites_dir} not found!")
        return
    
    # List of all sprites to check and resize
    all_sprites = [
        # Bird sprites
        "bluebird-downflap.png", "bluebird-midflap.png", "bluebird-upflap.png",
        "redbird-downflap.png", "redbird-midflap.png", "redbird-upflap.png",
        "yellowbird-downflap.png", "yellowbird-midflap.png", "yellowbird-upflap.png",
        "custombird-downflap.png", "custombird-midflap.png", "custombird-upflap.png",
        
        # UI elements
        "message.png", "gameover.png",
        
        # Numbers
        "0.png", "1.png", "2.png", "3.png", "4.png", "5.png", "6.png", "7.png", "8.png", "9.png",
        
        # Environment
        "background-day.png", "background-night.png", "base.png",
        "pipe-green.png", "pipe-red.png"
    ]
    
    resized_count = 0
    
    for sprite_name in all_sprites:
        sprite_path = os.path.join(sprites_dir, sprite_name)
        
        if os.path.exists(sprite_path):
            # Get the target size for this specific sprite
            target_size = get_target_size(sprite_name)
            
            if target_size is None:
                print(f"[WARNING] {sprite_name} - No target size defined, skipping")
                continue
                
            try:
                with Image.open(sprite_path) as img:
                    current_size = img.size
                    file_size = os.path.getsize(sprite_path)
                    
                    print(f"\n[FILE] {sprite_name}")
                    print(f"   Current: {current_size[0]}x{current_size[1]} ({file_size:,} bytes)")
                    print(f"   Target:  {target_size[0]}x{target_size[1]}")
                    
                    # Check if resize is needed
                    size_wrong = current_size != target_size
                    file_too_big = file_size > 100000  # If bigger than 100KB, probably needs resize
                    
                    if size_wrong or file_too_big:
                        backup_path = sprite_path + ".backup"
                        
                        # Create backup
                        if not os.path.exists(backup_path):
                            img.save(backup_path, 'PNG')
                            print(f"   [BACKUP] Backup saved as {sprite_name}.backup")
                        
                        # Resize
                        if resize_image(sprite_path, sprite_path, target_size):
                            resized_count += 1
                            new_size = os.path.getsize(sprite_path)
                            print(f"   [SIZE] Reduced from {file_size:,} to {new_size:,} bytes")
                    else:
                        print(f"   [OK] Already correct size")
                        
            except Exception as e:
                print(f"   [ERROR] Error checking {sprite_name}: {e}")
        else:
            if "custombird" not in sprite_name:  # Don't warn about missing custom birds
                print(f"[WARNING] {sprite_name} not found")
    
    print(f"\nSummary: Resized {resized_count} sprites")
    print("Your sprites are now optimized for Flappy Bird!")
    
    if resized_count > 0:
        print("\nTips:")
        print("- Original files backed up as .backup")
        print("- Run the game to test the changes")
        print("- If needed, restore from .backup files")

if __name__ == "__main__":
    main()