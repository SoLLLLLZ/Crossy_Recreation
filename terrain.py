"""
Crossy Road Recreation - Terrain System
Isometric tile rendering and terrain management
"""
import pygame
from utils import *


class TerrainTile:
    """Individual terrain tile"""
    
    def __init__(self, grid_x, grid_y, terrain_type="grass"):
        """Initialize a terrain tile"""
        self.grid_x = grid_x
        self.grid_y = grid_y
        self.type = terrain_type
        
        # Visual properties
        self.width = TILE_SIZE
        self.height = TILE_SIZE
        
        # Get colors based on type
        self.color, self.dark_color = self.get_colors()
    
    def get_colors(self):
        """Get colors based on terrain type"""
        if self.type == "grass":
            return GRASS_COLOR, GRASS_DARK
        elif self.type == "road":
            return ROAD_COLOR, ROAD_DARK
        elif self.type == "water":
            return WATER_COLOR, WATER_DARK
        elif self.type == "tracks":
            return TRACK_COLOR, TRACK_DARK
        elif self.type == "sidewalk":
            return SIDEWALK_COLOR, SIDEWALK_DARK
        else:
            return GRASS_COLOR, GRASS_DARK
    
    def draw(self, screen, scroll_offset=0):
        """Draw the terrain tile in isometric style"""
        # Calculate screen position
        x = self.grid_x * self.width
        y = self.grid_y * self.height + scroll_offset
        
        # Don't draw if off screen
        if y < -self.height or y > SCREEN_HEIGHT + self.height:
            return
        
        # Draw the isometric tile
        self.draw_isometric_base(screen, x, y)
        
        # Draw terrain-specific details
        if self.type == "road":
            self.draw_road_details(screen, x, y)
        elif self.type == "water":
            self.draw_water_details(screen, x, y)
        elif self.type == "tracks":
            self.draw_track_details(screen, x, y)
        elif self.type == "sidewalk":
            self.draw_sidewalk_details(screen, x, y)
        elif self.type == "grass":
            self.draw_grass_details(screen, x, y)
    
    def draw_isometric_base(self, screen, x, y):
        """Draw the base isometric tile shape"""
        # Simple rectangular tile with 3D effect
        # Top face (main surface)
        tile_rect = pygame.Rect(x, y, self.width, self.height)
        pygame.draw.rect(screen, self.color, tile_rect)
        
        # Right edge (darker for depth)
        right_edge = pygame.Rect(x + self.width - 3, y + 3, 3, self.height - 3)
        pygame.draw.rect(screen, self.dark_color, right_edge)
        
        # Bottom edge (darker for depth)
        bottom_edge = pygame.Rect(x + 3, y + self.height - 3, self.width - 3, 3)
        pygame.draw.rect(screen, self.dark_color, bottom_edge)
        
        # Border
        pygame.draw.rect(screen, BLACK, tile_rect, 1)
    
    def draw_road_details(self, screen, x, y):
        """Draw road-specific details (yellow center line)"""
        # Dashed center line - make it more visible
        dash_length = 10
        gap_length = 6
        
        # Two center lanes
        for lane_offset in [-TILE_SIZE // 4, TILE_SIZE // 4]:
            line_x = x + TILE_SIZE // 2 + lane_offset
            
            # Draw dashed line vertically through tile
            current_y = y + 2
            while current_y < y + self.height - 2:
                end_y = min(current_y + dash_length, y + self.height - 2)
                pygame.draw.line(screen, ROAD_LINE, 
                               (line_x, current_y), 
                               (line_x, end_y), 
                               3)
                current_y += dash_length + gap_length
    
    def draw_water_details(self, screen, x, y):
        """Draw water-specific details (wave lines)"""
        # Multiple wave lines with animation-like offset
        wave_color = tuple(min(255, c + 40) for c in self.color)
        wave_dark = tuple(max(0, c - 20) for c in self.color)
        
        # Offset based on position for variation
        offset = (self.grid_x * 3 + self.grid_y * 5) % 10
        
        # Draw 3 wave lines
        for i in range(3):
            wave_y = y + (self.height // 4) * (i + 1) + offset - 5
            
            # Wavy line using small segments
            for segment_x in range(0, self.width - 4, 4):
                start_x = x + segment_x
                end_x = x + segment_x + 4
                wave_height = 2 if (segment_x // 4 + i) % 2 == 0 else 0
                
                pygame.draw.line(screen, wave_color if i % 2 == 0 else wave_dark,
                               (start_x, wave_y + wave_height),
                               (end_x, wave_y + wave_height),
                               2)
    
    def draw_track_details(self, screen, x, y):
        """Draw railroad track details"""
        # Two parallel rails
        rail_color = tuple(max(0, c - 50) for c in self.color)
        tie_color = (101, 67, 33)
        
        # Rails positioned
        rail_spacing = self.width // 3
        left_rail_x = x + rail_spacing
        right_rail_x = x + 2 * rail_spacing
        
        # Draw rails (vertical lines)
        pygame.draw.line(screen, rail_color,
                       (left_rail_x, y),
                       (left_rail_x, y + self.height),
                       3)
        pygame.draw.line(screen, rail_color,
                       (right_rail_x, y),
                       (right_rail_x, y + self.height),
                       3)
        
        # Ties (wooden planks) - horizontal
        tie_width = int(self.width * 0.8)
        tie_height = 4
        tie_x = x + (self.width - tie_width) // 2
        
        # Draw multiple ties
        num_ties = 4
        for i in range(num_ties):
            tie_y = y + (i + 1) * (self.height // (num_ties + 1))
            tie_rect = pygame.Rect(tie_x, tie_y - tie_height // 2, tie_width, tie_height)
            pygame.draw.rect(screen, tie_color, tie_rect)
            pygame.draw.rect(screen, BLACK, tie_rect, 1)
    
    def draw_sidewalk_details(self, screen, x, y):
        """Draw sidewalk grid pattern"""
        grid_color = tuple(max(0, c - 30) for c in self.color)
        
        # Grid pattern - more detailed
        # Vertical lines
        for i in range(1, 3):
            line_x = x + (self.width // 3) * i
            pygame.draw.line(screen, grid_color,
                           (line_x, y),
                           (line_x, y + self.height),
                           1)
        
        # Horizontal lines
        for i in range(1, 3):
            line_y = y + (self.height // 3) * i
            pygame.draw.line(screen, grid_color,
                           (x, line_y),
                           (x + self.width, line_y),
                           1)
        
        # Small dots at intersections for detail
        for i in range(1, 3):
            for j in range(1, 3):
                dot_x = x + (self.width // 3) * i
                dot_y = y + (self.height // 3) * j
                pygame.draw.circle(screen, grid_color, (dot_x, dot_y), 1)
    
    def draw_grass_details(self, screen, x, y):
        """Draw grass texture (small darker spots and lighter highlights)"""
        # Add some variation to grass
        import random
        random.seed(self.grid_x * 1000 + self.grid_y)  # Deterministic randomness
        
        # Dark grass spots
        for _ in range(4):
            spot_x = x + random.randint(3, self.width - 3)
            spot_y = y + random.randint(3, self.height - 3)
            spot_size = random.randint(1, 2)
            pygame.draw.circle(screen, self.dark_color, (spot_x, spot_y), spot_size)
        
        # Light grass highlights
        light_color = tuple(min(255, c + 20) for c in self.color)
        for _ in range(2):
            spot_x = x + random.randint(3, self.width - 3)
            spot_y = y + random.randint(3, self.height - 3)
            pygame.draw.circle(screen, light_color, (spot_x, spot_y), 1)


class TerrainManager:
    """Manages infinite scrolling terrain with dynamic row generation"""
    
    def __init__(self):
        """Initialize terrain manager with camera-based system"""
        self.tiles = []
        self.tile_size = TILE_SIZE
        
        # Camera system (follows player instead of auto-scroll)
        self.camera_y = 0  # Camera position in grid coordinates
        
        # Track which rows exist
        self.rows = {}  # grid_y: [list of tiles in that row]
        self.lowest_row = 0  # Highest grid_y value (bottom of screen)
        self.highest_row = 0  # Lowest grid_y value (top, furthest forward)
        
        # Terrain generation with patterns
        self.current_section_type = "grass"
        self.section_rows_remaining = 0
        self.last_terrain_types = []  # Track recent types to avoid repetition
        
        # Terrain type probabilities (weighted random)
        self.terrain_weights = {
            "grass": 0.35,      # Safe, common
            "road": 0.25,       # Dangerous, medium frequency
            "water": 0.15,      # Need logs, less common
            "tracks": 0.15,     # Very dangerous, less common
            "sidewalk": 0.10    # Safe, uncommon
        }
        
        # Section length ranges (rows per section)
        self.section_lengths = {
            "grass": (3, 6),
            "road": (2, 5),
            "water": (2, 4),
            "tracks": (1, 3),
            "sidewalk": (2, 4)
        }
        
        # Generate initial screen of terrain plus buffer
        self.generate_initial_grid()
    
    def generate_initial_grid(self):
        """Generate initial terrain to fill screen plus buffer"""
        # Generate enough rows to fill screen plus large buffer above and below
        rows_needed = GRID_HEIGHT + 30  # Increased from 20 to 30
        start_row = -15  # Start further above screen (was -10)
        
        # Initialize first section
        import random
        self.current_section_type = random.choice(list(self.terrain_weights.keys()))
        min_len, max_len = self.section_lengths[self.current_section_type]
        self.section_rows_remaining = random.randint(min_len, max_len)
        
        for grid_y in range(start_row, start_row + rows_needed):
            self.generate_row(grid_y)
        
        self.highest_row = start_row
        self.lowest_row = start_row + rows_needed - 1
    
    def generate_row(self, grid_y):
        """Generate a single row of terrain"""
        row_tiles = []
        
        # Determine terrain type for this row
        terrain_type = self.determine_terrain_type(grid_y)
        
        # Create tiles for this row
        for grid_x in range(GRID_WIDTH):
            tile = TerrainTile(grid_x, grid_y, terrain_type)
            row_tiles.append(tile)
            self.tiles.append(tile)
        
        # Store row
        self.rows[grid_y] = row_tiles
        
        # Return terrain type so obstacles can be spawned
        return terrain_type
    
    def determine_terrain_type(self, grid_y):
        """Determine what terrain type this row should be using sections"""
        import random
        
        # If we're in the middle of a section, continue it
        if self.section_rows_remaining > 0:
            self.section_rows_remaining -= 1
            return self.current_section_type
        
        # Start a new section
        # Choose terrain type with weighted randomness, avoiding recent repeats
        available_types = list(self.terrain_weights.keys())
        weights = list(self.terrain_weights.values())
        
        # Reduce weight for recently used types (variety)
        if len(self.last_terrain_types) >= 2:
            for i, terrain_type in enumerate(available_types):
                if terrain_type in self.last_terrain_types[-2:]:
                    weights[i] *= 0.3  # Much less likely to repeat
        
        # Normalize weights
        total_weight = sum(weights)
        weights = [w / total_weight for w in weights]
        
        # Choose terrain type
        chosen_type = random.choices(available_types, weights=weights, k=1)[0]
        
        # Determine section length
        min_length, max_length = self.section_lengths[chosen_type]
        section_length = random.randint(min_length, max_length)
        
        # Update state
        self.current_section_type = chosen_type
        self.section_rows_remaining = section_length - 1  # -1 because we're generating one row now
        
        # Track recent types
        self.last_terrain_types.append(chosen_type)
        if len(self.last_terrain_types) > 5:
            self.last_terrain_types.pop(0)
        
        return chosen_type
    
    def update(self, dt, camera_y):
        """Update terrain based on camera position (player position)"""
        self.camera_y = camera_y
        
        new_rows = []  # Track new rows for obstacle spawning
        
        # Generate new rows ahead of camera if needed
        # Keep a LARGER buffer of rows above visible area for fast movement
        camera_top = camera_y - 10  # Increased from 5 to 10 rows ahead
        
        while self.highest_row > camera_top:
            # Generate new row at the top
            new_row_y = self.highest_row - 1
            terrain_type = self.generate_row(new_row_y)
            new_rows.append((new_row_y, terrain_type))
            self.highest_row = new_row_y
        
        # Remove old rows behind camera if too far away
        camera_bottom = camera_y + GRID_HEIGHT + 10  # Increased buffer
        
        # Remove rows that are too far below camera
        rows_to_remove = []
        for row_y in self.rows.keys():
            if row_y > camera_bottom:
                rows_to_remove.append(row_y)
        
        for row_y in rows_to_remove:
            self.remove_row(row_y)
        
        return new_rows  # Return list of (grid_y, terrain_type) tuples
    
    def remove_row(self, grid_y):
        """Remove a row that's scrolled off screen"""
        if grid_y in self.rows:
            # Remove tiles from main list
            tiles_to_remove = self.rows[grid_y]
            for tile in tiles_to_remove:
                if tile in self.tiles:
                    self.tiles.remove(tile)
            
            # Remove row tracking
            del self.rows[grid_y]
            
            # Update lowest_row
            if grid_y == self.lowest_row:
                self.lowest_row = grid_y - 1
    
    def draw(self, screen, camera_y):
        """Draw all visible terrain tiles based on camera position"""
        # Calculate screen offset based on camera position
        # Camera at grid_y should appear at specific screen position
        # Keep player visible in center-ish of screen
        camera_screen_y = SCREEN_HEIGHT // 2  # Center camera position on screen
        
        for tile in self.tiles:
            # Calculate where this tile should appear on screen
            # Tile's position relative to camera
            tile_screen_y = (tile.grid_y - camera_y) * TILE_SIZE + camera_screen_y
            
            # Only draw if visible
            if -TILE_SIZE < tile_screen_y < SCREEN_HEIGHT + TILE_SIZE:
                # Draw at calculated screen position
                tile.draw(screen, tile_screen_y - tile.grid_y * TILE_SIZE)
    
    def get_scroll_offset(self, camera_y):
        """Get scroll offset for rendering based on camera position"""
        camera_screen_y = SCREEN_HEIGHT // 2
        return camera_screen_y - camera_y * TILE_SIZE
    
    def get_tile_at(self, grid_x, grid_y):
        """Get tile at grid position"""
        if grid_y in self.rows and 0 <= grid_x < GRID_WIDTH:
            return self.rows[grid_y][grid_x]
        return None