"""
Crossy Road Recreation - Main Entry Point
Handles game loop, state management, and pygame initialization
"""
import pygame
import sys
from utils import *
from menu import Menu
from game import Game


class GameManager:
    """Main game manager handling state transitions and the game loop"""
    
    def __init__(self):
        """Initialize pygame and game states"""
        pygame.init()
        
        # Create game window
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Crossy Road Recreation")
        
        # Clock for FPS control
        self.clock = pygame.time.Clock()
        
        # State management
        self.state = STATE_MENU
        self.running = True
        
        # Initialize menu
        self.menu = Menu()
        
        # Game will be initialized later
        self.game = None
        
        # Delta time
        self.dt = 0
    
    def handle_events(self):
        """Handle pygame events"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            
            # Pass events to current state
            if self.state == STATE_MENU:
                new_state = self.menu.handle_event(event)
                if new_state == STATE_GAME:
                    self.transition_to_game()
            
            elif self.state == STATE_GAME:
                # Game event handling
                if self.game:
                    new_state = self.game.handle_event(event)
                    if new_state == STATE_MENU:
                        self.state = STATE_MENU
    
    def transition_to_game(self):
        """Transition from menu to game state"""
        self.state = STATE_GAME
        self.game = Game()
        print("Game started!")
    
    def update(self):
        """Update current state"""
        if self.state == STATE_MENU:
            self.menu.update(self.dt)
        
        elif self.state == STATE_GAME:
            # Game update
            if self.game:
                self.game.update(self.dt)
    
    def draw(self):
        """Draw current state"""
        if self.state == STATE_MENU:
            self.menu.draw(self.screen)
        
        elif self.state == STATE_GAME:
            # Game drawing
            if self.game:
                self.game.draw(self.screen)
        
        # Update display
        pygame.display.flip()
    
    def run(self):
        """Main game loop"""
        while self.running:
            # Calculate delta time
            self.dt = self.clock.tick(FPS) / 1000.0
            
            # Handle events
            self.handle_events()
            
            # Update game state
            self.update()
            
            # Draw everything
            self.draw()
        
        # Cleanup
        pygame.quit()
        sys.exit()


def main():
    """Entry point for the game"""
    game_manager = GameManager()
    game_manager.run()


if __name__ == "__main__":
    main()