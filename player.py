"""
Crossy Road Recreation - Player Character
Grid-based movement with isometric rendering
"""
import pygame
from utils import *


class Player:
    """Player character with grid-based movement"""
    
    def __init__(self, start_x=None, start_y=None):
        """Initialize player at starting position"""
        # Grid position (in tile units)
        self.grid_x = start_x if start_x is not None else GRID_WIDTH // 2
        self.grid_y = start_y if start_y is not None else GRID_HEIGHT - 3
        
        # Screen position (pixels) - will be calculated from grid position
        self.x = 0
        self.y = 0
        
        # Visual properties
        self.width = TILE_SIZE
        self.height = TILE_SIZE
        self.color = PLAYER_COLOR
        self.accent_color = PLAYER_ACCENT
        
        # Movement properties
        self.moving = False
        self.move_progress = 0
        self.move_speed = 10  # Speed of movement animation (higher = faster)
        self.target_grid_x = self.grid_x
        self.target_grid_y = self.grid_y
        self.moved_forward = False  # Track if last move was forward
        
        # Animation
        self.hop_height = 0
        self.hop_progress = 0
        
        # State
        self.alive = True
        self.squished = False
        self.squish_timer = 0
        self.squish_duration = 0.5
        
        # Update screen position
        self.update_screen_position()
    
    def update_screen_position(self):
        """Calculate screen position from grid position"""
        # Center the player on the screen horizontally
        # Vertically, keep player in bottom portion for forward visibility
        self.x = self.grid_x * TILE_SIZE + TILE_SIZE // 2
        self.y = self.grid_y * TILE_SIZE + TILE_SIZE // 2
    
    def move(self, direction):
        """Attempt to move in a direction (grid-based)"""
        if self.moving or not self.alive or self.squished:
            return False
        
        # Calculate target grid position
        new_x = self.grid_x
        new_y = self.grid_y
        moved_forward = False
        
        if direction == "up":
            new_y -= 1
            moved_forward = True
        elif direction == "down":
            new_y += 1
        elif direction == "left":
            new_x -= 1
        elif direction == "right":
            new_x += 1
        
        # Check bounds (can't move left/right off screen)
        if new_x < 0 or new_x >= GRID_WIDTH:
            return False
        
        # Allow infinite forward movement (negative Y)
        # Only restrict backward movement
        if new_y >= GRID_HEIGHT:
            return False
        
        # Start movement
        self.target_grid_x = new_x
        self.target_grid_y = new_y
        self.moving = True
        self.move_progress = 0
        self.hop_progress = 0
        self.moved_forward = moved_forward
        
        return True
    
    def update(self, dt):
        """Update player state"""
        # Handle squish animation
        if self.squished:
            self.squish_timer += dt
            if self.squish_timer >= self.squish_duration:
                self.alive = False
            return
        
        # Handle movement animation
        if self.moving:
            self.move_progress += self.move_speed * dt
            self.hop_progress += self.move_speed * dt
            
            # Lerp to target position
            if self.move_progress >= 1.0:
                self.move_progress = 1.0
                self.grid_x = self.target_grid_x
                self.grid_y = self.target_grid_y
                self.moving = False
                self.hop_height = 0
                self.moved_forward = False  # Reset after move completes
            else:
                # Smooth interpolation
                self.grid_x = self.grid_x + (self.target_grid_x - self.grid_x) * min(self.move_progress, 1.0)
                self.grid_y = self.grid_y + (self.target_grid_y - self.grid_y) * min(self.move_progress, 1.0)
                
                # Hop animation (parabolic arc)
                import math
                self.hop_height = math.sin(self.hop_progress * math.pi) * 15
            
            self.update_screen_position()
    
    def take_hit(self):
        """Player gets hit by obstacle"""
        if not self.squished and self.alive:
            self.squished = True
            self.squish_timer = 0
    
    def get_rect(self):
        """Get collision rectangle"""
        # Smaller collision box for better gameplay feel
        padding = 5
        return pygame.Rect(
            self.x - self.width // 2 + padding,
            self.y - self.height // 2 + padding,
            self.width - padding * 2,
            self.height - padding * 2
        )
    
    def draw(self, screen, scroll_offset=0):
        """Draw the player character in isometric style"""
        # Apply scroll offset
        draw_y = self.y + scroll_offset
        
        # Don't draw if off screen
        if draw_y < -TILE_SIZE or draw_y > SCREEN_HEIGHT + TILE_SIZE:
            return
        
        # Apply hop animation
        draw_y -= self.hop_height
        
        if self.squished:
            # Draw squished/flattened character
            squish_factor = 1 - (self.squish_timer / self.squish_duration) * 0.7
            self.draw_character(screen, self.x, draw_y, squished=True, squish_factor=squish_factor)
        else:
            # Draw normal character
            self.draw_character(screen, self.x, draw_y)
    
    def draw_character(self, screen, x, y, squished=False, squish_factor=1.0):
        """Draw the character matching the uploaded chicken model"""
        if squished:
            # Keep existing squish code
            height = int(self.height * squish_factor * 0.3)
            width = int(self.width * 1.3)
            body_rect = pygame.Rect(x - width // 2, y - height // 2, width, height)
            pygame.draw.rect(screen, self.color, body_rect)
            pygame.draw.rect(screen, BLACK, body_rect, 2)
        else:
            # Custom chicken model based on your image
            
            # Colors from your model
            body_white = (240, 240, 240)
            body_light_gray = (200, 200, 200)
            body_dark_gray = (160, 160, 160)
            comb_red = (244, 67, 54)
            comb_dark_red = (198, 40, 40)
            beak_orange = (255, 152, 0)
            beak_dark_orange = (230, 120, 0)
            feet_orange = (255, 152, 0)
            feet_dark_orange = (230, 120, 0)
            eye_black = (33, 33, 33)
            
            char_size = TILE_SIZE
            
            # FEET (bottom)
            foot_height = 8
            foot_width = 12
            # Left foot
            self._draw_cube(screen, x - 10, y + char_size//2 - foot_height, 
                           foot_width, foot_height, feet_orange, feet_orange, feet_dark_orange)
            # Right foot
            self._draw_cube(screen, x + 4, y + char_size//2 - foot_height, 
                           foot_width, foot_height, feet_orange, feet_orange, feet_dark_orange)
            
            # BODY (main white cube)
            body_height = char_size * 0.7
            body_width = char_size * 0.8
            self._draw_cube(screen, x - body_width//2, y - body_height//2 + 5, 
                           body_width, body_height, body_white, body_light_gray, body_dark_gray)
            
            # HEAD (smaller white cube on top)
            head_size = char_size * 0.5
            head_y = y - char_size * 0.5
            self._draw_cube(screen, x - head_size//2, head_y - head_size//2, 
                           head_size, head_size, body_white, body_light_gray, body_dark_gray)
            
            # COMB (red rectangle on top of head)
            comb_width = 24
            comb_height = 12
            comb_y = head_y - head_size//2 - comb_height
            self._draw_cube(screen, x - comb_width//2, comb_y, 
                           comb_width, comb_height, comb_red, comb_red, comb_dark_red)
            
            # BEAK (orange cube on side of head)
            beak_size = 10
            beak_x = x - head_size//2 - beak_size
            beak_y = head_y
            self._draw_cube(screen, beak_x, beak_y - beak_size//2, 
                           beak_size, beak_size, beak_orange, beak_orange, beak_dark_orange)
            
            # EYE (black square)
            eye_size = 6
            eye_x = x + 8
            eye_y = head_y - 4
            pygame.draw.rect(screen, eye_black, (eye_x, eye_y, eye_size, eye_size))
    
    def _draw_cube(self, screen, x, y, width, height, front_color, top_color=None, right_color=None):
        """Helper to draw a 3D cube with three visible faces"""
        if top_color is None:
            top_color = front_color
        if right_color is None:
            right_color = tuple(max(0, c - 30) for c in front_color)
        
        depth = 6  # 3D depth effect
        
        # Front face
        front_rect = pygame.Rect(x, y, width, height)
        pygame.draw.rect(screen, front_color, front_rect)
        pygame.draw.rect(screen, BLACK, front_rect, 1)
        
        # Top face (parallelogram)
        top_points = [
            (x, y),
            (x + width, y),
            (x + width + depth, y - depth),
            (x + depth, y - depth)
        ]
        pygame.draw.polygon(screen, top_color, top_points)
        pygame.draw.polygon(screen, BLACK, top_points, 1)
        
        # Right face
        right_points = [
            (x + width, y),
            (x + width + depth, y - depth),
            (x + width + depth, y + height - depth),
            (x + width, y + height)
        ]
        pygame.draw.polygon(screen, right_color, right_points)
        pygame.draw.polygon(screen, BLACK, right_points, 1)