import pygame
from pygame.locals import K_ESCAPE, K_SPACE, K_UP, K_LEFT, K_RIGHT, KEYDOWN

from ..utils import GameConfig, PLAYERS
from .entity import Entity


class BirdSelection(Entity):
    def __init__(self, config: GameConfig) -> None:
        # Use a placeholder image initially
        image = pygame.Surface((100, 50))
        image.fill((0, 0, 0))
        super().__init__(config, image, 0, 0)
        
        self.selected_bird = 0  # Index of currently selected bird
        self.bird_count = len(PLAYERS)
        self.bird_previews = []
        self.selection_confirmed = False
        
        # Load all bird preview images
        self.load_bird_previews()
        
        # UI positioning
        self.title_y = 50
        self.birds_y = 200
        self.birds_spacing = 80
        self.instruction_y = 400
        
    def load_bird_previews(self):
        """Load preview images for all bird types"""
        for i, bird_sprites in enumerate(PLAYERS):
            try:
                # Use the mid-flap sprite for preview
                preview_image = pygame.image.load(bird_sprites[1]).convert_alpha()
                self.bird_previews.append(preview_image)
            except (pygame.error, FileNotFoundError) as e:
                print(f"Warning: Could not load bird {i} sprites: {e}")
                # Create a placeholder image for missing bird
                placeholder = pygame.Surface((34, 24), pygame.SRCALPHA)
                placeholder.fill((200, 100, 100, 128))  # Semi-transparent red
                
                # Draw text on placeholder
                font = pygame.font.Font(None, 16)
                text = font.render("MISSING", True, (255, 255, 255))
                text_rect = text.get_rect(center=(17, 12))
                placeholder.blit(text, text_rect)
                
                self.bird_previews.append(placeholder)
        
        # Update bird count to only include successfully loaded birds
        self.bird_count = len(self.bird_previews)
    
    def handle_input(self, event):
        """Handle input for bird selection"""
        if event.type == KEYDOWN:
            if event.key == K_LEFT:
                self.selected_bird = (self.selected_bird - 1) % self.bird_count
                self.config.sounds.swoosh.play()
                return False
            elif event.key == K_RIGHT:
                self.selected_bird = (self.selected_bird + 1) % self.bird_count
                self.config.sounds.swoosh.play()
                return False
            elif event.key == K_SPACE or event.key == K_UP:
                self.selection_confirmed = True
                self.config.sounds.wing.play()
                return True
            elif event.key == K_ESCAPE:
                return "quit"
        
        # Mouse click handling
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left click
                mouse_x, mouse_y = pygame.mouse.get_pos()
                
                # Check if clicked on a bird
                for i in range(self.bird_count):
                    bird_x = self.get_bird_x_position(i)
                    bird_rect = pygame.Rect(
                        bird_x - 25, self.birds_y - 25, 50, 50
                    )
                    if bird_rect.collidepoint(mouse_x, mouse_y):
                        if i == self.selected_bird:
                            # Double click on same bird - confirm selection
                            self.selection_confirmed = True
                            self.config.sounds.wing.play()
                            return True
                        else:
                            # Select different bird
                            self.selected_bird = i
                            self.config.sounds.swoosh.play()
                            return False
        
        return False
    
    def get_bird_x_position(self, bird_index):
        """Calculate X position for bird at given index"""
        total_width = (self.bird_count - 1) * self.birds_spacing
        start_x = (self.config.window.width - total_width) // 2
        return start_x + bird_index * self.birds_spacing
    
    def tick(self):
        """Draw the bird selection screen"""
        self.draw()
    
    def draw(self):
        """Render the bird selection screen"""
        # Clear screen with background color
        self.config.screen.fill((135, 206, 235))  # Sky blue
        
        print("Drawing bird selection screen...")  # Debug
        
        # Draw title
        try:
            title_font = pygame.font.Font(None, 48)
            title_text = title_font.render("Choose Your Bird", True, (255, 255, 255))
            title_rect = title_text.get_rect(center=(self.config.window.width // 2, self.title_y))
            self.config.screen.blit(title_text, title_rect)
            print("Title drawn successfully")  # Debug
        except Exception as e:
            print(f"Error drawing title: {e}")
            # Fallback without custom font
            title_font = pygame.font.SysFont('Arial', 48)
            title_text = title_font.render("Choose Your Bird", True, (0, 0, 0))
            title_rect = title_text.get_rect(center=(self.config.window.width // 2, self.title_y))
            self.config.screen.blit(title_text, title_rect)
        
        # Draw bird options
        print(f"Drawing {len(self.bird_previews)} birds...")  # Debug
        for i, bird_preview in enumerate(self.bird_previews):
            bird_x = self.get_bird_x_position(i)
            bird_y = self.birds_y
            
            print(f"Drawing bird {i} at position ({bird_x}, {bird_y})")  # Debug
            
            # Scale up the bird image for better visibility
            scaled_bird = pygame.transform.scale(bird_preview, (50, 36))
            bird_rect = scaled_bird.get_rect(center=(bird_x, bird_y))
            
            # Draw selection highlight
            if i == self.selected_bird:
                print(f"Bird {i} is selected - drawing highlight")  # Debug
                # Draw selection border
                highlight_rect = pygame.Rect(bird_x - 35, bird_y - 35, 70, 70)
                pygame.draw.rect(self.config.screen, (255, 255, 0), highlight_rect, 3)
                
                # Draw selection arrow
                arrow_y = bird_y - 50
                pygame.draw.polygon(self.config.screen, (255, 255, 0), [
                    (bird_x - 10, arrow_y),
                    (bird_x + 10, arrow_y),
                    (bird_x, arrow_y + 15)
                ])
            
            # Draw the bird
            self.config.screen.blit(scaled_bird, bird_rect)
            
            # Draw bird type label
            bird_names = ["Red Bird", "Blue Bird", "Yellow Bird", "Custom Bird"]
            # Extend with generic names if more birds exist
            while len(bird_names) < len(PLAYERS):
                bird_names.append(f"Bird {len(bird_names) + 1}")
                
            if i < len(bird_names):
                label_font = pygame.font.Font(None, 24)
                bird_name = bird_names[i]
                
                # Check if this bird's sprites are missing
                try:
                    pygame.image.load(PLAYERS[i][1])
                except (pygame.error, FileNotFoundError):
                    bird_name += " (Missing)"
                    
                label_text = label_font.render(bird_name, True, (255, 255, 255))
                label_rect = label_text.get_rect(center=(bird_x, bird_y + 40))
                self.config.screen.blit(label_text, label_rect)
        
        # Draw instructions
        instruction_font = pygame.font.Font(None, 32)
        instructions = [
            "Use LEFT/RIGHT arrows or click to select",
            "Press SPACE or click twice to confirm",
            "Press ESC to quit"
        ]
        
        for i, instruction in enumerate(instructions):
            instruction_text = instruction_font.render(instruction, True, (255, 255, 255))
            instruction_rect = instruction_text.get_rect(
                center=(self.config.window.width // 2, self.instruction_y + i * 30)
            )
            self.config.screen.blit(instruction_text, instruction_rect)
    
    def get_selected_bird(self):
        """Return the index of the selected bird"""
        return self.selected_bird