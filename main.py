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

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
GRAY = (128, 128, 128)
YELLOW = (255, 255, 0)

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
        
        # Draw game over screen
        if self.game_over:
            game_over_text = self.font.render("GAME OVER!", True, RED)
            restart_text = self.font.render("Press R to restart or Q to quit", True, WHITE)
            final_score_text = self.font.render(f"Final Score: {self.score}", True, GREEN)
            
            screen.blit(game_over_text, (SCREEN_WIDTH//2 - game_over_text.get_width()//2, SCREEN_HEIGHT//2 - 60))
            screen.blit(restart_text, (SCREEN_WIDTH//2 - restart_text.get_width()//2, SCREEN_HEIGHT//2))
            screen.blit(final_score_text, (SCREEN_WIDTH//2 - final_score_text.get_width()//2, SCREEN_HEIGHT//2 + 60))
            
    def reset(self):
        self.player = Player()
        self.obstacles = []
        self.score = 0
        self.game_over = False
        self.spawn_counter = 0

def main():
    menu = Menu()
    game = Game()
    current_state = "menu"  # "menu", "game", "game_over"
    
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
                    if event.key == pygame.K_r and game.game_over:
                        current_state = "menu"
                    elif event.key == pygame.K_q and game.game_over:
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
            
        pygame.display.flip()
        clock.tick(60)

if __name__ == "__main__":
    main()

