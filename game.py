"""
Crossy Road Recreation - Game State
Main game logic, player management, and rendering
"""
import pygame
from utils import *
from player import Player
from terrain import TerrainManager
from obstacles import ObstacleManager


class Game:
    """Main game state"""
    
    def __init__(self):
        """Initialize the game"""
        # Player - start in middle of screen on grass
        start_y = GRID_HEIGHT // 2
        
        # Terrain with camera-based system
        self.terrain_manager = TerrainManager()
        
        # Find a grass tile to start on (avoid water)
        for check_y in range(start_y - 5, start_y + 5):
            tile = self.terrain_manager.get_tile_at(GRID_WIDTH // 2, check_y)
            if tile and tile.type in ["grass", "sidewalk"]:
                start_y = check_y
                break
        
        self.player = Player(start_y=start_y)
        
        # Obstacles
        self.obstacle_manager = ObstacleManager()
        
        # Spawn obstacles for all initial terrain
        for row_y, tiles in self.terrain_manager.rows.items():
            if tiles:
                terrain_type = tiles[0].type
                self.obstacle_manager.spawn_obstacles_for_row(row_y, terrain_type)
        
        # Input handling
        self.keys_pressed = set()
        self.last_move_time = 0
        self.move_cooldown = 0.15  # Seconds between moves
        
        # Game state
        self.running = True
        self.time = 0
        self.score = 0  # Score based on forward progress
        self.max_forward_progress = int(self.player.grid_y)  # Track furthest forward
        self.game_over = False
        
        # UI fonts
        self.font = load_font(24)
        self.small_font = load_font(18)
    
    def handle_event(self, event):
        """Handle game events"""
        if event.type == pygame.KEYDOWN:
            # Track which keys are pressed
            if event.key in [pygame.K_UP, pygame.K_w]:
                self.keys_pressed.add('up')
            elif event.key in [pygame.K_DOWN, pygame.K_s]:
                self.keys_pressed.add('down')
            elif event.key in [pygame.K_LEFT, pygame.K_a]:
                self.keys_pressed.add('left')
            elif event.key in [pygame.K_RIGHT, pygame.K_d]:
                self.keys_pressed.add('right')
            elif event.key == pygame.K_ESCAPE:
                # Pause will be implemented in Stage 7
                return STATE_MENU
        
        elif event.type == pygame.KEYUP:
            # Remove keys when released
            if event.key in [pygame.K_UP, pygame.K_w]:
                self.keys_pressed.discard('up')
            elif event.key in [pygame.K_DOWN, pygame.K_s]:
                self.keys_pressed.discard('down')
            elif event.key in [pygame.K_LEFT, pygame.K_a]:
                self.keys_pressed.discard('left')
            elif event.key in [pygame.K_RIGHT, pygame.K_d]:
                self.keys_pressed.discard('right')
        
        return None
    
    def update(self, dt):
        """Update game state"""
        if self.game_over:
            return  # Don't update if game is over
        
        self.time += dt
        
        # Handle player movement with cooldown
        if self.time - self.last_move_time >= self.move_cooldown:
            moved = False
            
            # Priority order: up, down, left, right
            if 'up' in self.keys_pressed:
                moved = self.player.move('up')
            elif 'down' in self.keys_pressed:
                moved = self.player.move('down')
            elif 'left' in self.keys_pressed:
                moved = self.player.move('left')
            elif 'right' in self.keys_pressed:
                moved = self.player.move('right')
            
            if moved:
                self.last_move_time = self.time
        
        # Update player
        self.player.update(dt)
        
        # Check if player is riding a log
        if not self.player.moving:
            log = self.obstacle_manager.get_log_at_position(self.player.grid_x, self.player.grid_y)
            if log:
                # Player is on a log - drift with it!
                self.player.grid_x += log.speed * dt * (1 if log.direction == 'right' else -1)
                self.player.update_screen_position()
                
                # Check if drifted off screen edges
                if self.player.grid_x < 0 or self.player.grid_x >= GRID_WIDTH:
                    # Fell off the side - die!
                    if not self.player.squished:
                        self.player.take_hit()
        
        # Update terrain based on player (camera) position
        new_rows = self.terrain_manager.update(dt, int(self.player.grid_y))
        
        # Spawn obstacles for new terrain rows
        for row_y, terrain_type in new_rows:
            self.obstacle_manager.spawn_obstacles_for_row(row_y, terrain_type)
        
        # Update obstacles
        self.obstacle_manager.update(dt)
        
        # Check if player is on water without a log (only after movement completes)
        if not self.player.moving:
            player_tile = self.terrain_manager.get_tile_at(int(self.player.grid_x), int(self.player.grid_y))
            if player_tile and player_tile.type == "water":
                # Check if standing on a log
                log = self.obstacle_manager.get_log_at_position(self.player.grid_x, self.player.grid_y)
                if log is None:
                    # Not on a log - drown!
                    if not self.player.squished:
                        self.player.take_hit()
        
        # Check collisions with cars/trains
        if not self.player.squished and self.obstacle_manager.check_collision(self.player):
            self.player.take_hit()
            # Game over will be triggered when squish animation completes
        
        # Check if player died
        if not self.player.alive:
            self.game_over = True
        
        # Track score based on forward progress (lower grid_y = further forward)
        # Use integer position to avoid float precision issues
        player_y_int = int(self.player.grid_y)
        if player_y_int < self.max_forward_progress:
            # Player moved forward
            progress = self.max_forward_progress - player_y_int
            self.score += progress
            self.max_forward_progress = player_y_int
    
    def draw(self, screen):
        """Draw the game"""
        # Clear screen with sky color
        screen.fill(SKY_BLUE)
        
        # Draw terrain based on player (camera) position
        camera_y = int(self.player.grid_y)
        self.terrain_manager.draw(screen, camera_y)
        
        # Calculate scroll offset for rendering
        scroll_offset = self.terrain_manager.get_scroll_offset(camera_y)
        
        # Draw obstacles
        self.obstacle_manager.draw(screen, scroll_offset)
        
        # Draw player at fixed screen position (camera follows player)
        self.player.draw(screen, scroll_offset)
        
        # Draw UI
        self.draw_ui(screen)
        
        # Draw game over screen if needed
        if self.game_over:
            self.draw_game_over(screen)
    
    def draw_ui(self, screen):
        """Draw UI elements"""
        # Draw controls reminder
        controls_text = "Arrow Keys/WASD to move | ESC to menu"
        text_surface = self.small_font.render(controls_text, True, WHITE)
        text_rect = text_surface.get_rect(center=(SCREEN_WIDTH // 2, 20))
        
        # Draw shadow
        shadow_surface = self.small_font.render(controls_text, True, BLACK)
        shadow_rect = shadow_surface.get_rect(center=(SCREEN_WIDTH // 2 + 2, 22))
        screen.blit(shadow_surface, shadow_rect)
        screen.blit(text_surface, text_rect)
        
        # Draw score
        score_text = f"Score: {self.score}"
        score_surface = self.font.render(score_text, True, WHITE)
        score_rect = score_surface.get_rect(topleft=(10, 10))
        
        # Shadow for score
        score_shadow = self.font.render(score_text, True, BLACK)
        shadow_rect = score_shadow.get_rect(topleft=(12, 12))
        screen.blit(score_shadow, shadow_rect)
        screen.blit(score_surface, score_rect)
        
        # Draw player position (for debugging)
        debug_text = f"Position: ({self.player.grid_x:.1f}, {self.player.grid_y:.1f})"
        debug_surface = self.small_font.render(debug_text, True, WHITE)
        debug_rect = debug_surface.get_rect(topleft=(10, SCREEN_HEIGHT - 30))
        screen.blit(debug_surface, debug_rect)
    
    def draw_game_over(self, screen):
        """Draw game over overlay"""
        # Semi-transparent overlay
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.set_alpha(180)
        overlay.fill((0, 0, 0))
        screen.blit(overlay, (0, 0))
        
        # Game Over text
        game_over_font = load_font(72, bold=True)
        game_over_text = game_over_font.render("GAME OVER", True, (255, 50, 50))
        game_over_rect = game_over_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 80))
        
        # Shadow
        shadow_text = game_over_font.render("GAME OVER", True, BLACK)
        shadow_rect = shadow_text.get_rect(center=(SCREEN_WIDTH // 2 + 4, SCREEN_HEIGHT // 2 - 76))
        screen.blit(shadow_text, shadow_rect)
        screen.blit(game_over_text, game_over_rect)
        
        # Final score
        score_text = f"Final Score: {self.score}"
        score_surface = load_font(36).render(score_text, True, TEXT_ACCENT)
        score_rect = score_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        
        score_shadow = load_font(36).render(score_text, True, BLACK)
        shadow_rect = score_shadow.get_rect(center=(SCREEN_WIDTH // 2 + 3, SCREEN_HEIGHT // 2 + 3))
        screen.blit(score_shadow, shadow_rect)
        screen.blit(score_surface, score_rect)
        
        # Instructions
        restart_text = "Press ESC to return to menu"
        restart_surface = self.font.render(restart_text, True, WHITE)
        restart_rect = restart_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 80))
        screen.blit(restart_surface, restart_rect)