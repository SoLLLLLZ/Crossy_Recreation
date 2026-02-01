"""
Crossy Road Recreation - Menu System
Landing page with animated elements and interactive buttons
"""
import pygame
import math
from utils import *


class Menu:
    def __init__(self):
        """Initialize the menu with animated elements"""
        self.title_font = load_font(80, bold=True)
        self.subtitle_font = load_font(24)
        self.button_font = load_font(40, bold=True)
        self.instruction_font = load_font(20)
        
        # Button setup
        self.play_button = pygame.Rect(
            SCREEN_WIDTH // 2 - 120,
            SCREEN_HEIGHT // 2 + 50,
            240,
            70
        )
        
        # Animation variables
        self.time = 0
        self.title_bounce = 0
        self.hovered_button = None
        
        # Floating decorative elements (simple circles for now)
        self.decorations = []
        for i in range(8):
            self.decorations.append({
                'x': (i * 100 + 50) % SCREEN_WIDTH,
                'y': 100 + (i % 3) * 150,
                'size': 15 + (i % 3) * 5,
                'speed': 0.5 + (i % 3) * 0.3,
                'phase': i * 0.5
            })
    
    def handle_event(self, event):
        """Handle menu events and return state change if needed"""
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Left click
                if self.play_button.collidepoint(event.pos):
                    return STATE_GAME
        
        return None
    
    def update(self, dt):
        """Update animation timers"""
        self.time += dt
        self.title_bounce = math.sin(self.time * 2) * 10
        
        # Update floating decorations
        for dec in self.decorations:
            dec['y'] = 100 + (dec['y'] - 100 + dec['speed']) % 400
    
    def draw(self, screen):
        """Draw the landing page"""
        # Draw animated gradient background
        for y in range(SCREEN_HEIGHT):
            progress = y / SCREEN_HEIGHT
            r = int(100 + progress * 50)
            g = int(200 - progress * 50)
            b = int(255 - progress * 30)
            pygame.draw.line(screen, (r, g, b), (0, y), (SCREEN_WIDTH, y))
        
        # Draw floating decorations
        for dec in self.decorations:
            float_offset = math.sin(self.time * 2 + dec['phase']) * 5
            y_pos = dec['y'] + float_offset
            
            # Draw small isometric cubes as decoration
            tile_x = dec['x'] - dec['size'] // 2
            tile_y = int(y_pos - dec['size'] // 2)
            
            # Alternate colors
            if dec['size'] > 20:
                color = GRASS_COLOR
            elif dec['size'] > 15:
                color = ROAD_LINE
            else:
                color = PLAYER_ACCENT
            
            pygame.draw.rect(screen, color, 
                           (tile_x, tile_y, dec['size'], dec['size']), 
                           border_radius=3)
            pygame.draw.rect(screen, BLACK, 
                           (tile_x, tile_y, dec['size'], dec['size']), 
                           width=2, border_radius=3)
        
        # Draw title with bounce animation
        title_y = 100 + self.title_bounce
        
        # Title shadow
        title_text = "CROSSY"
        shadow = self.title_font.render(title_text, True, BLACK)
        shadow_rect = shadow.get_rect(center=(SCREEN_WIDTH // 2 + 5, title_y + 5))
        screen.blit(shadow, shadow_rect)
        
        # Title main text
        title_surface = self.title_font.render(title_text, True, WHITE)
        title_rect = title_surface.get_rect(center=(SCREEN_WIDTH // 2, title_y))
        screen.blit(title_surface, title_rect)
        
        # Second line of title
        title_text2 = "ROAD"
        shadow2 = self.title_font.render(title_text2, True, BLACK)
        shadow_rect2 = shadow2.get_rect(center=(SCREEN_WIDTH // 2 + 5, title_y + 75))
        screen.blit(shadow2, shadow_rect2)
        
        title_surface2 = self.title_font.render(title_text2, True, TEXT_ACCENT)
        title_rect2 = title_surface2.get_rect(center=(SCREEN_WIDTH // 2, title_y + 70))
        screen.blit(title_surface2, title_rect2)
        
        # Draw subtitle
        subtitle = "RECREATION"
        subtitle_surface = self.subtitle_font.render(subtitle, True, WHITE)
        subtitle_rect = subtitle_surface.get_rect(center=(SCREEN_WIDTH // 2, title_y + 130))
        screen.blit(subtitle_surface, subtitle_rect)
        
        # Draw instructions
        instructions = [
            "Use ARROW KEYS or WASD to move",
            "Avoid cars and trains!",
            "Collect coins for points!"
        ]
        
        instruction_y = SCREEN_HEIGHT // 2 - 60
        for instruction in instructions:
            inst_surface = self.instruction_font.render(instruction, True, WHITE)
            inst_rect = inst_surface.get_rect(center=(SCREEN_WIDTH // 2, instruction_y))
            
            # Small shadow for instructions
            shadow_surface = self.instruction_font.render(instruction, True, (0, 0, 0, 128))
            shadow_rect = shadow_surface.get_rect(center=(SCREEN_WIDTH // 2 + 2, instruction_y + 2))
            screen.blit(shadow_surface, shadow_rect)
            
            screen.blit(inst_surface, inst_rect)
            instruction_y += 30
        
        # Check if mouse is hovering over button
        mouse_pos = pygame.mouse.get_pos()
        is_hovered = self.play_button.collidepoint(mouse_pos)
        
        # Add pulse effect when hovered
        button_rect = self.play_button.copy()
        if is_hovered:
            pulse = math.sin(self.time * 8) * 3
            button_rect.inflate_ip(pulse, pulse)
        
        # Draw play button
        draw_button(screen, button_rect, "PLAY", self.button_font, is_hovered)
        
        # Draw footer text
        footer = "Press ESC to pause during game"
        footer_surface = self.instruction_font.render(footer, True, (200, 200, 200))
        footer_rect = footer_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 30))
        screen.blit(footer_surface, footer_rect)