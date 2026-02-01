"""
Crossy Road Recreation - Utility Functions and Constants
"""
import pygame
import os

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60

# Grid settings
TILE_SIZE = 40
GRID_WIDTH = SCREEN_WIDTH // TILE_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // TILE_SIZE

# Colors - Matching Crossy Road's bright, vibrant palette
# Sky and UI
SKY_BLUE = (135, 206, 250)
MENU_BG = (100, 200, 255)

# Terrain colors
GRASS_COLOR = (76, 175, 80)
GRASS_DARK = (56, 142, 60)
ROAD_COLOR = (66, 66, 66)
ROAD_DARK = (50, 50, 50)
ROAD_LINE = (255, 215, 0)
WATER_COLOR = (33, 150, 243)
WATER_DARK = (25, 118, 210)
TRACK_COLOR = (121, 85, 72)
TRACK_DARK = (93, 64, 55)
SIDEWALK_COLOR = (189, 189, 189)
SIDEWALK_DARK = (158, 158, 158)

# Entity colors
PLAYER_COLOR = (255, 255, 255)
PLAYER_ACCENT = (255, 107, 129)
CAR_COLORS = [(244, 67, 54), (33, 150, 243), (255, 235, 59), (156, 39, 176)]
TRAIN_COLOR = (66, 66, 66)
LOG_COLOR = (121, 85, 72)
COIN_COLOR = (255, 215, 0)
COIN_SHINE = (255, 255, 200)

# UI colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BUTTON_COLOR = (255, 255, 255)
BUTTON_HOVER = (255, 235, 59)
BUTTON_TEXT = (33, 33, 33)
SHADOW_COLOR = (0, 0, 0, 100)

# Text colors
TEXT_PRIMARY = (255, 255, 255)
TEXT_SHADOW = (0, 0, 0)
TEXT_ACCENT = (255, 215, 0)

# Terrain types
TERRAIN_TYPES = ["grass", "road", "water", "tracks", "sidewalk"]

# Game states
STATE_MENU = "menu"
STATE_GAME = "game"
STATE_PAUSED = "paused"
STATE_GAME_OVER = "game_over"

# File paths
HIGH_SCORE_FILE = "highscore.txt"


def load_font(size, bold=False):
    """Load a font with the specified size"""
    try:
        # Try to load a fun, blocky font for that Crossy Road feel
        if bold:
            return pygame.font.Font(None, size + 10)
        return pygame.font.Font(None, size)
    except:
        return pygame.font.SysFont('arial', size, bold=bold)


def draw_text_with_shadow(surface, text, font, x, y, color=TEXT_PRIMARY, shadow_color=TEXT_SHADOW, shadow_offset=3):
    """Draw text with a shadow for better visibility"""
    # Draw shadow
    shadow_surface = font.render(text, True, shadow_color)
    surface.blit(shadow_surface, (x + shadow_offset, y + shadow_offset))
    
    # Draw main text
    text_surface = font.render(text, True, color)
    surface.blit(text_surface, (x, y))
    
    return text_surface.get_rect(topleft=(x, y))


def draw_button(surface, rect, text, font, is_hovered=False):
    """Draw a button with hover effect"""
    color = BUTTON_HOVER if is_hovered else BUTTON_COLOR
    
    # Draw shadow
    shadow_rect = rect.copy()
    shadow_rect.x += 4
    shadow_rect.y += 4
    pygame.draw.rect(surface, (0, 0, 0, 50), shadow_rect, border_radius=10)
    
    # Draw button
    pygame.draw.rect(surface, color, rect, border_radius=10)
    pygame.draw.rect(surface, BLACK, rect, width=3, border_radius=10)
    
    # Draw text
    text_surface = font.render(text, True, BUTTON_TEXT)
    text_rect = text_surface.get_rect(center=rect.center)
    surface.blit(text_surface, text_rect)


def load_high_score():
    """Load high score from file"""
    try:
        if os.path.exists(HIGH_SCORE_FILE):
            with open(HIGH_SCORE_FILE, 'r') as f:
                return int(f.read().strip())
    except:
        pass
    return 0


def save_high_score(score):
    """Save high score to file"""
    try:
        with open(HIGH_SCORE_FILE, 'w') as f:
            f.write(str(score))
    except:
        pass


def draw_isometric_tile(surface, x, y, width, height, color, dark_color=None):
    """Draw a simple isometric tile (diamond shape with 3D effect)"""
    if dark_color is None:
        dark_color = tuple(max(0, c - 30) for c in color)
    
    # Calculate diamond points
    top = (x + width // 2, y)
    right = (x + width, y + height // 2)
    bottom = (x + width // 2, y + height)
    left = (x, y + height // 2)
    
    # Draw the main face (lighter)
    pygame.draw.polygon(surface, color, [top, right, bottom, left])
    
    # Draw darker right face for 3D effect
    if dark_color:
        right_face = [
            (x + width // 2, y + height // 2),
            right,
            bottom
        ]
        pygame.draw.polygon(surface, dark_color, right_face)
    
    # Draw outline
    pygame.draw.polygon(surface, BLACK, [top, right, bottom, left], 2)