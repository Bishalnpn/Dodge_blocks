import pygame
import random
import sys

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
PLAYER_SIZE = 30
OBSTACLE_SIZE = 25
PLAYER_SPEED = 5
OBSTACLE_SPEED = 10
OBSTACLE_SPAWN_RATE = 100  # frames between obstacle spawns
ICON_SIZE = 60

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
GRAY = (128, 128, 128)
YELLOW = (255, 255, 0)
LIGHT_BLUE = (100, 150, 255)
DARK_RED = (150, 0, 0)

# Display setup
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Dodge Blocks!")
clock = pygame.time.Clock()

class Menu:
    def __init__(self):
        self.font_large = pygame.font.Font(None, 72)
        self.font_medium = pygame.font.Font(None, 48)
        self.font_small = pygame.font.Font(None, 36)
        self.selected_option = 0
        self.options = ["Play", "Exit"]
        
    def draw(self):
        screen.fill(BLACK)
        
        # Draw title
        title_text = self.font_large.render("DODGE BLOCKS!", True, YELLOW)
        title_rect = title_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//4))
        screen.blit(title_text, title_rect)
        
        # Draw options
        for i, option in enumerate(self.options):
            color = GREEN if i == self.selected_option else WHITE
            text = self.font_medium.render(option, True, color)
            text_rect = text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 + i * 60))
            screen.blit(text, text_rect)
            
        # Draw instructions
        instruction_text = self.font_small.render("Use UP/DOWN arrows to navigate, ENTER to select", True, GRAY)
        instruction_rect = instruction_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT - 50))
        screen.blit(instruction_text, instruction_rect)
        
    def handle_input(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                self.selected_option = (self.selected_option - 1) % len(self.options)
            elif event.key == pygame.K_DOWN:
                self.selected_option = (self.selected_option + 1) % len(self.options)
            elif event.key == pygame.K_RETURN:
                return self.options[self.selected_option]
        return None

class PauseMenu:
    def __init__(self):
        self.font_large = pygame.font.Font(None, 72)
        self.font_medium = pygame.font.Font(None, 48)
        self.font_small = pygame.font.Font(None, 36)
        self.selected_option = 0
        self.options = ["Resume", "Restart", "Exit"]
        
    def draw_pause_icon(self, x, y, size, color):
        # Draw pause icon (two vertical bars)
        bar_width = size // 6
        bar_height = size // 2
        bar_spacing = size // 4
        
        pygame.draw.rect(screen, color, (x + bar_spacing, y + (size - bar_height)//2, bar_width, bar_height))
        pygame.draw.rect(screen, color, (x + size - bar_spacing - bar_width, y + (size - bar_height)//2, bar_width, bar_height))
        
    def draw_restart_icon(self, x, y, size, color):
        # Draw restart icon (circular arrow)
        center_x, center_y = x + size//2, y + size//2
        radius = size//3
        
        # Draw circle
        pygame.draw.circle(screen, color, (center_x, center_y), radius, 3)
        
        # Draw arrow head
        arrow_points = [
            (center_x + radius//2, center_y - radius//2),
            (center_x + radius//2 + 8, center_y - radius//2),
            (center_x + radius//2 + 4, center_y - radius//2 - 8)
        ]
        pygame.draw.polygon(screen, color, arrow_points)
        
    def draw_exit_icon(self, x, y, size, color):
        # Draw exit icon (X)
        margin = size // 4
        pygame.draw.line(screen, color, (x + margin, y + margin), (x + size - margin, y + size - margin), 4)
        pygame.draw.line(screen, color, (x + size - margin, y + margin), (x + margin, y + size - margin), 4)
        
    def draw(self, game_surface):
        # Draw the game state in the background
        screen.blit(game_surface, (0, 0))
        
        # Create a semi-transparent overlay
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.set_alpha(128)
        overlay.fill(BLACK)
        screen.blit(overlay, (0, 0))
        
        # Draw pause title
        title_text = self.font_large.render("PAUSED", True, YELLOW)
        title_rect = title_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//4))
        screen.blit(title_text, title_rect)
        
        # Draw icons with labels vertically
        icon_x = SCREEN_WIDTH//2 - ICON_SIZE//2
        start_y = SCREEN_HEIGHT//2 - 80
        spacing = 100
        
        # Resume icon
        resume_y = start_y
        resume_color = GREEN if self.selected_option == 0 else WHITE
        self.draw_pause_icon(icon_x, resume_y, ICON_SIZE, resume_color)
        resume_text = self.font_small.render("Resume", True, resume_color)
        resume_text_rect = resume_text.get_rect(center=(SCREEN_WIDTH//2, resume_y + ICON_SIZE + 15))
        screen.blit(resume_text, resume_text_rect)
        
        # Restart icon
        restart_y = start_y + spacing
        restart_color = GREEN if self.selected_option == 1 else WHITE
        self.draw_restart_icon(icon_x, restart_y, ICON_SIZE, restart_color)
        restart_text = self.font_small.render("Restart", True, restart_color)
        restart_text_rect = restart_text.get_rect(center=(SCREEN_WIDTH//2, restart_y + ICON_SIZE + 15))
        screen.blit(restart_text, restart_text_rect)
        
        # Exit icon
        exit_y = start_y + spacing * 2
        exit_color = GREEN if self.selected_option == 2 else WHITE
        self.draw_exit_icon(icon_x, exit_y, ICON_SIZE, exit_color)
        exit_text = self.font_small.render("Exit", True, exit_color)
        exit_text_rect = exit_text.get_rect(center=(SCREEN_WIDTH//2, exit_y + ICON_SIZE + 15))
        screen.blit(exit_text, exit_text_rect)
        
        # Draw navigation hint
        hint_text = self.font_small.render("Use ↑ ↓ arrows to navigate, ENTER to select", True, GRAY)
        hint_rect = hint_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT - 50))
        screen.blit(hint_text, hint_rect)
        
    def handle_input(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                self.selected_option = (self.selected_option - 1) % len(self.options)
            elif event.key == pygame.K_DOWN:
                self.selected_option = (self.selected_option + 1) % len(self.options)
            elif event.key == pygame.K_RETURN:
                return self.options[self.selected_option]
        return None

class Player:
    def __init__(self):
        self.x = SCREEN_WIDTH // 2
        self.y = SCREEN_HEIGHT - 50
        self.size = PLAYER_SIZE
        self.speed = PLAYER_SPEED
        
    def move(self, direction):
        if direction == "left" and self.x > 0:
            self.x -= self.speed
        if direction == "right" and self.x < SCREEN_WIDTH - self.size:
            self.x += self.speed
            
    def draw(self):
        pygame.draw.rect(screen, BLUE, (self.x, self.y, self.size, self.size))
        # Small black box added to make it more 3D
        pygame.draw.rect(screen, (100, 100, 255), (self.x + 2, self.y + 2, self.size - 4, self.size - 4))

class Obstacle:
    def __init__(self, x):
        self.x = x
        self.y = -OBSTACLE_SIZE
        self.size = OBSTACLE_SIZE
        self.speed = OBSTACLE_SPEED
        
    def move(self):
        self.y += self.speed
        
    def draw(self):
        pygame.draw.rect(screen, RED, (self.x, self.y, self.size, self.size))
        pygame.draw.rect(screen, (200, 0, 0), (self.x + 2, self.y + 2, self.size - 4, self.size - 4))
        
    def is_off_screen(self):
        return self.y > SCREEN_HEIGHT
        
    def collides_with(self, player):
        return (self.x < player.x + player.size and
                self.x + self.size > player.x and
                self.y < player.y + player.size and
                self.y + self.size > player.y)  

class Game:
    def __init__(self):
        self.player = Player()
        self.obstacles = []
        self.score = 0
        self.game_over = False
        self.spawn_counter = 0
        self.font = pygame.font.Font(None, 36)
        self.font_small = pygame.font.Font(None, 24)
        self.game_over_selection = 0  # 0 for restart, 1 for exit
        
    def spawn_obstacle(self):
        x = random.randint(0, SCREEN_WIDTH - OBSTACLE_SIZE)
        self.obstacles.append(Obstacle(x))
        
    def update(self):
        if self.game_over:
            return
            
        # Spawn obstacles
        self.spawn_counter += 1
        if self.spawn_counter >= OBSTACLE_SPAWN_RATE:
            self.spawn_obstacle()
            self.spawn_counter = 0
            
        # Update obstacles
        for obstacle in self.obstacles[:]:
            obstacle.move()
            if obstacle.is_off_screen():
                self.obstacles.remove(obstacle)
                self.score += 1
            elif obstacle.collides_with(self.player):
                self.game_over = True
                
    def draw(self):
        screen.fill(BLACK)
        
        # Draw player
        self.player.draw()
        
        # Draw obstacles
        for obstacle in self.obstacles:
            obstacle.draw()
            
        # Draw score
        score_text = self.font.render(f"Score: {self.score}", True, WHITE)
        screen.blit(score_text, (10, 10))
        
        # Draw pause icon in top right
        pause_icon_size = 30
        pause_x = SCREEN_WIDTH - pause_icon_size - 10
        pause_y = 10
        
        # Draw pause icon background
        pygame.draw.rect(screen, LIGHT_BLUE, (pause_x - 5, pause_y - 5, pause_icon_size + 10, pause_icon_size + 10))
        pygame.draw.rect(screen, BLACK, (pause_x - 3, pause_y - 3, pause_icon_size + 6, pause_icon_size + 6))
        
        # Draw pause bars
        bar_width = 4
        bar_height = 20
        bar_spacing = 6
        
        pygame.draw.rect(screen, WHITE, (pause_x + bar_spacing, pause_y + 5, bar_width, bar_height))
        pygame.draw.rect(screen, WHITE, (pause_x + pause_icon_size - bar_spacing - bar_width, pause_y + 5, bar_width, bar_height))
        
        # Draw game over screen
        if self.game_over:
            game_over_text = self.font.render("GAME OVER!", True, RED)
            final_score_text = self.font.render(f"Final Score: {self.score}", True, GREEN)
            
            screen.blit(game_over_text, (SCREEN_WIDTH//2 - game_over_text.get_width()//2, SCREEN_HEIGHT//2 - 80))
            screen.blit(final_score_text, (SCREEN_WIDTH//2 - final_score_text.get_width()//2, SCREEN_HEIGHT//2 - 40))
            
            # Draw restart and exit icons
            icon_x = SCREEN_WIDTH//2 - ICON_SIZE//2
            icon_y = SCREEN_HEIGHT//2 + 20
            spacing = 120
            
            # Restart icon
            restart_x = icon_x - spacing//2
            restart_color = GREEN if self.game_over_selection == 0 else WHITE
            pygame.draw.circle(screen, restart_color, (restart_x + ICON_SIZE//2, icon_y + ICON_SIZE//2), ICON_SIZE//3, 3)
            arrow_points = [
                (restart_x + ICON_SIZE//2 + 8, icon_y + ICON_SIZE//2 - 8),
                (restart_x + ICON_SIZE//2 + 16, icon_y + ICON_SIZE//2 - 8),
                (restart_x + ICON_SIZE//2 + 12, icon_y + ICON_SIZE//2 - 16)
            ]
            pygame.draw.polygon(screen, restart_color, arrow_points)
            restart_text = self.font_small.render("Restart", True, restart_color)
            restart_text_rect = restart_text.get_rect(center=(restart_x + ICON_SIZE//2, icon_y + ICON_SIZE + 15))
            screen.blit(restart_text, restart_text_rect)
            
            # Exit icon
            exit_x = icon_x + spacing//2
            exit_color = GREEN if self.game_over_selection == 1 else WHITE
            margin = ICON_SIZE // 4
            pygame.draw.line(screen, exit_color, (exit_x + margin, icon_y + margin), (exit_x + ICON_SIZE - margin, icon_y + ICON_SIZE - margin), 4)
            pygame.draw.line(screen, exit_color, (exit_x + ICON_SIZE - margin, icon_y + margin), (exit_x + margin, icon_y + ICON_SIZE - margin), 4)
            exit_text = self.font_small.render("Exit", True, exit_color)
            exit_text_rect = exit_text.get_rect(center=(exit_x + ICON_SIZE//2, icon_y + ICON_SIZE + 15))
            screen.blit(exit_text, exit_text_rect)
            
            # Draw navigation hint
            hint_text = self.font_small.render("Use ← → arrows to navigate, ENTER to select", True, GRAY)
            hint_rect = hint_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT - 50))
            screen.blit(hint_text, hint_rect)
            
    def reset(self):
        self.player = Player()
        self.obstacles = []
        self.score = 0
        self.game_over = False
        self.spawn_counter = 0
        self.game_over_selection = 0
        
    def handle_game_over_input(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                self.game_over_selection = (self.game_over_selection - 1) % 2
            elif event.key == pygame.K_RIGHT:
                self.game_over_selection = (self.game_over_selection + 1) % 2
            elif event.key == pygame.K_RETURN:
                if self.game_over_selection == 0:  # Restart
                    return "restart"
                elif self.game_over_selection == 1:  # Exit
                    return "exit"
        return None

def main():
    menu = Menu()
    pause_menu = PauseMenu()
    game = Game()
    current_state = "menu"  # "menu", "game", "pause", "game_over"
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if current_state == "menu":
                    selection = menu.handle_input(event)
                    if selection == "Play":
                        current_state = "game"
                        game.reset()
                    elif selection == "Exit":
                        pygame.quit()
                        sys.exit()
                elif current_state == "game":
                    if event.key == pygame.K_p and not game.game_over:
                        current_state = "pause"
                    elif game.game_over:
                        game_over_action = game.handle_game_over_input(event)
                        if game_over_action == "restart":
                            current_state = "menu"
                        elif game_over_action == "exit":
                            pygame.quit()
                            sys.exit()
                elif current_state == "pause":
                    selection = pause_menu.handle_input(event)
                    if selection == "Resume":
                        current_state = "game"
                    elif selection == "Restart":
                        current_state = "game"
                        game.reset()
                    elif selection == "Exit":
                        pygame.quit()
                        sys.exit()
        
        if current_state == "menu":
            menu.draw()
        elif current_state == "game":
            if not game.game_over:
                # Handle player movement
                keys = pygame.key.get_pressed()
                if keys[pygame.K_LEFT] or keys[pygame.K_a]:
                    game.player.move("left")
                if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
                    game.player.move("right")
                    
                game.update()
                
            game.draw()
        elif current_state == "pause":
            # Capture the current game state for background
            game_surface = screen.copy()
            game.draw()
            pause_menu.draw(game_surface)
            
        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    main()

