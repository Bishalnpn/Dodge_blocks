import pygame
import random
import sys

# Initialize Pygame
pygame.init()

# Screen settings
WIDTH, HEIGHT = 600, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Dodge Blocks")
clock = pygame.time.Clock()

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (200, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 200, 0)
GRAY = (128, 128, 128)
DARK_GRAY = (64, 64, 64)
LIGHT_BLUE = (100, 150, 255)

# Font
font_large = pygame.font.Font(None, 48)
font_medium = pygame.font.Font(None, 36)
font_small = pygame.font.Font(None, 24)

# Game states
MENU = "menu"
PLAYING = "playing"
GAME_OVER = "game_over"
PAUSED = "paused"

class Button:
    def __init__(self, x, y, width, height, text, color, hover_color):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.hover_color = hover_color
        self.current_color = color
        self.font = font_medium
        
    def draw(self, surface):
        pygame.draw.rect(surface, self.current_color, self.rect)
        pygame.draw.rect(surface, BLACK, self.rect, 2)
        
        text_surface = self.font.render(self.text, True, BLACK)
        text_rect = text_surface.get_rect(center=self.rect.center)
        surface.blit(text_surface, text_rect)
        
    def handle_event(self, event):
        if event.type == pygame.MOUSEMOTION:
            if self.rect.collidepoint(event.pos):
                self.current_color = self.hover_color
            else:
                self.current_color = self.color
                
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                return True
        return False

class Game:
    def __init__(self):
        self.state = MENU
        self.score = 0
        self.high_score = 0
        self.reset_game()
        
        # Menu buttons
        button_width = 200
        button_height = 50
        center_x = WIDTH // 2 - button_width // 2
        
        self.start_button = Button(center_x, 250, button_width, button_height, 
                                  "Start Game", GREEN, (0, 255, 0))
        self.restart_button = Button(center_x, 320, button_width, button_height, 
                                   "Restart Game", BLUE, LIGHT_BLUE)
        self.exit_button = Button(center_x, 390, button_width, button_height, 
                                "Exit Game", RED, (255, 100, 100))
        
    def reset_game(self):
        # Player settings
        self.player_size = 50
        self.player_x = WIDTH // 2
        self.player_y = HEIGHT - self.player_size - 50
        self.player_speed = 10
        
        # Block settings
        self.block_size = 50
        self.block_x = random.randint(0, WIDTH - self.block_size)
        self.block_y = 0 - self.block_size
        self.block_speed = 15
        
        # Game variables
        self.score = 0
        self.game_speed = 1.0
        
    def draw_menu(self):
        screen.fill(WHITE)
        
        # Title
        title = font_large.render("DODGE BLOCKS", True, BLACK)
        title_rect = title.get_rect(center=(WIDTH//2, 150))
        screen.blit(title, title_rect)
        
        # Subtitle
        subtitle = font_small.render("Avoid the falling blocks!", True, DARK_GRAY)
        subtitle_rect = subtitle.get_rect(center=(WIDTH//2, 200))
        screen.blit(subtitle, subtitle_rect)
        
        # High score
        if self.high_score > 0:
            high_score_text = font_small.render(f"High Score: {self.high_score}", True, DARK_GRAY)
            high_score_rect = high_score_text.get_rect(center=(WIDTH//2, 450))
            screen.blit(high_score_text, high_score_rect)
        
        # Draw buttons
        self.start_button.draw(screen)
        self.restart_button.draw(screen)
        self.exit_button.draw(screen)
        
    def draw_game(self):
        screen.fill(WHITE)
        
        # Draw player
        player_rect = pygame.Rect(self.player_x, self.player_y, self.player_size, self.player_size)
        pygame.draw.rect(screen, BLUE, player_rect)
        pygame.draw.rect(screen, BLACK, player_rect, 2)
        
        # Draw block
        block_rect = pygame.Rect(self.block_x, self.block_y, self.block_size, self.block_size)
        pygame.draw.rect(screen, RED, block_rect)
        pygame.draw.rect(screen, BLACK, block_rect, 2)
        
        # Draw score
        score_text = font_medium.render(f"Score: {self.score}", True, BLACK)
        screen.blit(score_text, (10, 10))
        
        # Draw pause instruction
        pause_text = font_small.render("Press P to pause", True, DARK_GRAY)
        screen.blit(pause_text, (10, 50))
        
    def draw_game_over(self):
        screen.fill(WHITE)
        
        # Game over text
        game_over_text = font_large.render("GAME OVER!", True, RED)
        game_over_rect = game_over_text.get_rect(center=(WIDTH//2, 200))
        screen.blit(game_over_text, game_over_rect)
        
        # Final score
        final_score_text = font_medium.render(f"Final Score: {self.score}", True, BLACK)
        final_score_rect = final_score_text.get_rect(center=(WIDTH//2, 250))
        screen.blit(final_score_text, final_score_rect)
        
        # High score update
        if self.score > self.high_score:
            self.high_score = self.score
            new_high_text = font_medium.render("NEW HIGH SCORE!", True, GREEN)
            new_high_rect = new_high_text.get_rect(center=(WIDTH//2, 300))
            screen.blit(new_high_text, new_high_rect)
        
        # Draw buttons
        self.restart_button.draw(screen)
        self.exit_button.draw(screen)
        
    def draw_pause(self):
        # Semi-transparent overlay
        overlay = pygame.Surface((WIDTH, HEIGHT))
        overlay.set_alpha(128)
        overlay.fill(BLACK)
        screen.blit(overlay, (0, 0))
        
        # Pause text
        pause_text = font_large.render("PAUSED", True, WHITE)
        pause_rect = pause_text.get_rect(center=(WIDTH//2, HEIGHT//2 - 50))
        screen.blit(pause_text, pause_rect)
        
        # Instructions
        resume_text = font_medium.render("Press P to resume", True, WHITE)
        resume_rect = resume_text.get_rect(center=(WIDTH//2, HEIGHT//2))
        screen.blit(resume_text, resume_rect)
        
        menu_text = font_medium.render("Press M for menu", True, WHITE)
        menu_rect = menu_text.get_rect(center=(WIDTH//2, HEIGHT//2 + 50))
        screen.blit(menu_text, menu_rect)
        
    def handle_menu_events(self, event):
        if self.start_button.handle_event(event):
            self.state = PLAYING
            self.reset_game()
        elif self.restart_button.handle_event(event):
            self.state = PLAYING
            self.reset_game()
        elif self.exit_button.handle_event(event):
            pygame.quit()
            sys.exit()
            
    def handle_game_events(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_p:
                self.state = PAUSED
                
    def handle_pause_events(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_p:
                self.state = PLAYING
            elif event.key == pygame.K_m:
                self.state = MENU
                
    def handle_game_over_events(self, event):
        if self.restart_button.handle_event(event):
            self.state = PLAYING
            self.reset_game()
        elif self.exit_button.handle_event(event):
            pygame.quit()
            sys.exit()
            
    def update_game(self):
        # Key control
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and self.player_x > 0:
            self.player_x -= self.player_speed
        if keys[pygame.K_RIGHT] and self.player_x < WIDTH - self.player_size:
            self.player_x += self.player_speed

        # Block movement
        self.block_y += self.block_speed * self.game_speed
        if self.block_y > HEIGHT:
            self.block_y = 0 - self.block_size
            self.block_x = random.randint(0, WIDTH - self.block_size)
            self.score += 1
            
            # Increase speed every 10 points
            if self.score % 10 == 0:
                self.game_speed += 0.1

        # Collision detection
        player_rect = pygame.Rect(self.player_x, self.player_y, self.player_size, self.player_size)
        block_rect = pygame.Rect(self.block_x, self.block_y, self.block_size, self.block_size)
        if player_rect.colliderect(block_rect):
            self.state = GAME_OVER

# Create game instance
game = Game()

# Main game loop
running = True
while running:
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
            
        if game.state == MENU:
            game.handle_menu_events(event)
        elif game.state == PLAYING:
            game.handle_game_events(event)
        elif game.state == PAUSED:
            game.handle_pause_events(event)
        elif game.state == GAME_OVER:
            game.handle_game_over_events(event)
    
    # Update game logic
    if game.state == PLAYING:
        game.update_game()
    
    # Draw based on current state
    if game.state == MENU:
        game.draw_menu()
    elif game.state == PLAYING:
        game.draw_game()
    elif game.state == GAME_OVER:
        game.draw_game_over()
    elif game.state == PAUSED:
        game.draw_game()  # Draw the game first
        game.draw_pause()  # Then overlay the pause screen
    
    pygame.display.flip()
    clock.tick(60)
