"""
Crossy Road Recreation - Obstacles System
Cars, trains, logs, and collision detection
"""
import pygame
import random
from utils import *


class Obstacle:
    """Base obstacle class"""
    
    def __init__(self, grid_x, grid_y, direction, speed):
        """Initialize obstacle"""
        self.grid_x = grid_x
        self.grid_y = grid_y
        self.direction = direction  # 'left' or 'right'
        self.speed = speed  # Tiles per second
        
        # Visual properties
        self.width = TILE_SIZE
        self.height = TILE_SIZE
        
        # State
        self.active = True
    
    def update(self, dt):
        """Update obstacle position"""
        if self.direction == 'left':
            self.grid_x -= self.speed * dt
        else:
            self.grid_x += self.speed * dt
        
        # Mark as inactive if off screen
        if self.grid_x < -2 or self.grid_x > GRID_WIDTH + 2:
            self.active = False
    
    def get_rect(self):
        """Get collision rectangle"""
        # Convert grid position to screen position
        x = self.grid_x * TILE_SIZE
        y = self.grid_y * TILE_SIZE
        
        # Add some padding for better collision feel
        padding = 3
        return pygame.Rect(
            x + padding,
            y + padding,
            self.width - padding * 2,
            self.height - padding * 2
        )
    
    def draw(self, screen, scroll_offset):
        """Draw the obstacle - override in subclasses"""
        pass


class Car(Obstacle):
    """Car obstacle on roads"""
    
    def __init__(self, grid_x, grid_y, direction, speed=2.5):
        """Initialize car"""
        super().__init__(grid_x, grid_y, direction, speed)
        
        # Car dimensions
        self.width = TILE_SIZE * 0.9
        self.height = TILE_SIZE * 0.6
        
        # Random car color
        self.color = random.choice(CAR_COLORS)
        self.dark_color = tuple(max(0, c - 40) for c in self.color)
    
    def draw(self, screen, scroll_offset):
        """Draw the car in 3D isometric style"""
        # Calculate screen position
        x = self.grid_x * TILE_SIZE
        y = self.grid_y * TILE_SIZE + scroll_offset
        
        # Don't draw if off screen
        if y < -TILE_SIZE or y > SCREEN_HEIGHT + TILE_SIZE:
            return
        
        # Car body
        car_width = int(self.width)
        car_height = int(self.height)
        
        # Main body (rectangle)
        body_rect = pygame.Rect(
            x + TILE_SIZE // 2 - car_width // 2,
            y + TILE_SIZE // 2 - car_height // 2,
            car_width,
            car_height
        )
        
        # Draw body with 3D effect
        pygame.draw.rect(screen, self.color, body_rect, border_radius=3)
        
        # Draw top (lighter)
        top_color = tuple(min(255, c + 30) for c in self.color)
        top_rect = pygame.Rect(
            body_rect.x + 5,
            body_rect.y + 3,
            body_rect.width - 10,
            body_rect.height // 2
        )
        pygame.draw.rect(screen, top_color, top_rect, border_radius=2)
        
        # Draw windows (dark)
        window_color = (50, 50, 70)
        window_width = car_width // 3
        window_height = car_height // 3
        
        # Front window
        if self.direction == 'right':
            window_x = body_rect.x + car_width - window_width - 5
        else:
            window_x = body_rect.x + 5
        
        window_rect = pygame.Rect(
            window_x,
            body_rect.y + car_height // 4,
            window_width,
            window_height
        )
        pygame.draw.rect(screen, window_color, window_rect, border_radius=2)
        
        # Outline
        pygame.draw.rect(screen, BLACK, body_rect, width=2, border_radius=3)


class Train(Obstacle):
    """Train obstacle on tracks - longer and faster than cars"""
    
    def __init__(self, grid_x, grid_y, direction, speed=4.0):
        """Initialize train"""
        super().__init__(grid_x, grid_y, direction, speed)
        
        # Train dimensions (longer)
        self.width = TILE_SIZE * 2.0
        self.height = TILE_SIZE * 0.7
        
        # Train color
        self.color = TRAIN_COLOR
        self.dark_color = tuple(max(0, c - 30) for c in self.color)
    
    def draw(self, screen, scroll_offset):
        """Draw the train in 3D isometric style"""
        # Calculate screen position
        x = self.grid_x * TILE_SIZE
        y = self.grid_y * TILE_SIZE + scroll_offset
        
        # Don't draw if off screen
        if y < -TILE_SIZE or y > SCREEN_HEIGHT + TILE_SIZE:
            return
        
        # Train body (longer rectangle)
        train_width = int(self.width)
        train_height = int(self.height)
        
        body_rect = pygame.Rect(
            x + TILE_SIZE // 2 - train_width // 2,
            y + TILE_SIZE // 2 - train_height // 2,
            train_width,
            train_height
        )
        
        # Draw body
        pygame.draw.rect(screen, self.color, body_rect, border_radius=3)
        
        # Draw top stripe (yellow warning stripe)
        stripe_color = (255, 215, 0)
        stripe_rect = pygame.Rect(
            body_rect.x + 5,
            body_rect.y + 5,
            body_rect.width - 10,
            5
        )
        pygame.draw.rect(screen, stripe_color, stripe_rect)
        
        # Draw windows along the train
        window_color = (70, 100, 120)
        window_spacing = 15
        window_width = 10
        window_height = train_height - 18
        
        for i in range(int(train_width // window_spacing)):
            window_x = body_rect.x + 8 + i * window_spacing
            window_rect = pygame.Rect(
                window_x,
                body_rect.y + 10,
                window_width,
                window_height
            )
            pygame.draw.rect(screen, window_color, window_rect, border_radius=1)
        
        # Outline
        pygame.draw.rect(screen, BLACK, body_rect, width=2, border_radius=3)
        
        # Draw front (darker rectangle)
        if self.direction == 'right':
            front_x = body_rect.x + train_width - 8
        else:
            front_x = body_rect.x
        
        front_rect = pygame.Rect(front_x, body_rect.y, 8, train_height)
        pygame.draw.rect(screen, self.dark_color, front_rect, border_radius=2)


class Log(Obstacle):
    """Log obstacle on water - player can ride on logs"""
    
    def __init__(self, grid_x, grid_y, direction, speed=1.5):
        """Initialize log"""
        super().__init__(grid_x, grid_y, direction, speed)
        
        # Log dimensions
        self.width = TILE_SIZE * 1.5
        self.height = TILE_SIZE * 0.5
        
        # Log color
        self.color = LOG_COLOR
        self.dark_color = tuple(max(0, c - 30) for c in self.color)
    
    def draw(self, screen, scroll_offset):
        """Draw the log in 3D isometric style"""
        # Calculate screen position
        x = self.grid_x * TILE_SIZE
        y = self.grid_y * TILE_SIZE + scroll_offset
        
        # Don't draw if off screen
        if y < -TILE_SIZE or y > SCREEN_HEIGHT + TILE_SIZE:
            return
        
        # Log body (rounded rectangle)
        log_width = int(self.width)
        log_height = int(self.height)
        
        body_rect = pygame.Rect(
            x + TILE_SIZE // 2 - log_width // 2,
            y + TILE_SIZE // 2 - log_height // 2,
            log_width,
            log_height
        )
        
        # Draw main body
        pygame.draw.rect(screen, self.color, body_rect, border_radius=log_height // 2)
        
        # Draw top highlight
        highlight_color = tuple(min(255, c + 20) for c in self.color)
        highlight_rect = pygame.Rect(
            body_rect.x + 3,
            body_rect.y + 2,
            body_rect.width - 6,
            body_rect.height // 3
        )
        pygame.draw.rect(screen, highlight_color, highlight_rect, border_radius=log_height // 4)
        
        # Draw wood rings (circles on ends)
        ring_color = tuple(max(0, c - 20) for c in self.color)
        
        # Left end
        pygame.draw.circle(screen, ring_color, 
                         (body_rect.x + 5, body_rect.centery), 
                         log_height // 3)
        
        # Right end
        pygame.draw.circle(screen, ring_color, 
                         (body_rect.x + log_width - 5, body_rect.centery), 
                         log_height // 3)
        
        # Outline
        pygame.draw.rect(screen, self.dark_color, body_rect, width=2, border_radius=log_height // 2)


class ObstacleManager:
    """Manages all obstacles in the game"""
    
    def __init__(self):
        """Initialize obstacle manager"""
        self.obstacles = []
        
        # Spawn timing per row
        self.row_spawn_timers = {}  # grid_y: time until next spawn
        self.row_terrain_types = {}  # grid_y: terrain type
        
        # Track which rows have been initialized
        self.initialized_rows = set()
    
    def spawn_obstacles_for_row(self, grid_y, terrain_type):
        """Initialize obstacle spawning for a terrain row"""
        if grid_y in self.initialized_rows:
            return  # Already initialized
        
        self.initialized_rows.add(grid_y)
        self.row_terrain_types[grid_y] = terrain_type
        
        if terrain_type in ["road", "tracks", "water"]:
            # Set initial spawn timer
            self.row_spawn_timers[grid_y] = 0.5  # Spawn first obstacle soon
            
            # Spawn initial obstacles
            self._spawn_for_row(grid_y, terrain_type)
        
    def _spawn_for_row(self, grid_y, terrain_type):
        """Spawn obstacles for a specific row"""
        # Determine spawn parameters based on terrain type
        if terrain_type == "road":
            # Spawn 1-2 cars
            num_obstacles = random.randint(1, 2)
            direction = random.choice(['left', 'right'])
            speed = random.uniform(2.0, 3.5)
            
            for i in range(num_obstacles):
                # Space them out
                if direction == 'left':
                    start_x = GRID_WIDTH + 1 + i * 4
                else:
                    start_x = -2 - i * 4
                
                car = Car(start_x, grid_y, direction, speed)
                self.obstacles.append(car)
        
        elif terrain_type == "tracks":
            # Spawn 1 train
            direction = random.choice(['left', 'right'])
            speed = random.uniform(3.5, 5.0)
            
            if direction == 'left':
                start_x = GRID_WIDTH + 2
            else:
                start_x = -4
            
            train = Train(start_x, grid_y, direction, speed)
            self.obstacles.append(train)
        
        elif terrain_type == "water":
            # Spawn 4-5 logs with tighter spacing to ensure crossability
            # Logs are 1.5 tiles wide, so spacing of 3-3.5 ensures overlap
            num_logs = random.randint(4, 5)
            direction = random.choice(['left', 'right'])
            speed = random.uniform(1.0, 2.0)
            
            # Tighter spacing ensures always a log to hop to
            spacing = 3.5  # Tiles between log starts
            
            for i in range(num_logs):
                if direction == 'left':
                    start_x = GRID_WIDTH + 1 + i * spacing
                else:
                    start_x = -3 - i * spacing
                
                log = Log(start_x, grid_y, direction, speed)
                self.obstacles.append(log)
    
    def update(self, dt):
        """Update all obstacles and spawn new ones"""
        # Update spawn timers and spawn new obstacles
        for grid_y in list(self.row_spawn_timers.keys()):
            self.row_spawn_timers[grid_y] -= dt
            
            if self.row_spawn_timers[grid_y] <= 0:
                # Time to spawn new obstacle
                terrain_type = self.row_terrain_types.get(grid_y)
                if terrain_type:
                    self._spawn_for_row(grid_y, terrain_type)
                    
                    # Set next spawn time based on terrain type
                    if terrain_type == "road":
                        self.row_spawn_timers[grid_y] = random.uniform(3.0, 5.0)
                    elif terrain_type == "tracks":
                        self.row_spawn_timers[grid_y] = random.uniform(4.0, 7.0)
                    elif terrain_type == "water":
                        # Spawn logs more frequently to ensure crossability
                        self.row_spawn_timers[grid_y] = random.uniform(3.0, 5.0)
        
        # Update obstacle positions
        for obstacle in self.obstacles:
            obstacle.update(dt)
        
        # Remove inactive obstacles
        self.obstacles = [obs for obs in self.obstacles if obs.active]
    
    def cleanup_row(self, grid_y):
        """Clean up spawning for a row that's no longer visible"""
        if grid_y in self.row_spawn_timers:
            del self.row_spawn_timers[grid_y]
        if grid_y in self.row_terrain_types:
            del self.row_terrain_types[grid_y]
        if grid_y in self.initialized_rows:
            self.initialized_rows.remove(grid_y)
    
    def draw(self, screen, scroll_offset):
        """Draw all obstacles"""
        for obstacle in self.obstacles:
            obstacle.draw(screen, scroll_offset)
    
    def check_collision(self, player):
        """Check if player collides with any obstacle"""
        player_rect = player.get_rect()
        
        for obstacle in self.obstacles:
            if isinstance(obstacle, Log):
                # Logs are safe to stand on (will handle in Stage 6)
                continue
            
            obstacle_rect = obstacle.get_rect()
            if player_rect.colliderect(obstacle_rect):
                return True
        
        return False
    
    def get_log_at_position(self, player_x, player_y):
        """Get log that player is standing on (for water riding)"""
        # Use generous collision detection for landing on logs
        player_rect = pygame.Rect(
            player_x * TILE_SIZE + 5,  # Small padding
            player_y * TILE_SIZE + 5,
            TILE_SIZE - 10,
            TILE_SIZE - 10
        )
        
        for obstacle in self.obstacles:
            if isinstance(obstacle, Log):
                # Check if log is at the same Y position
                if abs(obstacle.grid_y - player_y) < 0.5:  # Same row
                    obstacle_rect = obstacle.get_rect()
                    if player_rect.colliderect(obstacle_rect):
                        return obstacle
        
        return None