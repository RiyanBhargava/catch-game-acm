import pygame
import random
import sys
import time
from pygame import gfxdraw

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH = 1000  # Increased from 800
SCREEN_HEIGHT = 700  # Increased from 600
FPS = 60
BASKET_SPEED = 8
FALL_SPEED_BASE = 5  # Reduced from 9 to 5
FALL_SPEED_INCREMENT = 1.0
TIME_LIMIT = 120  # 2 minutes

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

class FallingItem:
    def __init__(self, image_path, points, x=None, speed=None, is_final_item=False):
        self.image = pygame.image.load(image_path)
        self.image = pygame.transform.scale(self.image, (50, 50))
        self.rect = self.image.get_rect()
        self.rect.x = x if x is not None else random.randint(0, SCREEN_WIDTH - self.rect.width)
        self.rect.y = -self.rect.height
        
        # Set speed based on item type
        if is_final_item:  # Person's face - keep it slow
            self.speed = 2 + random.uniform(0, 1)
        else:
            # Other items - mix of normal (5) and some fast (9) speeds
            if random.random() < 0.3:  # 30% chance for fast items
                self.speed = 9 + random.uniform(0, 2)
            else:  # 70% chance for normal speed
                self.speed = 5 + random.uniform(0, 1)
        
        self.points = points
        self.is_final_item = is_final_item
        
    def update(self):
        self.rect.y += self.speed
        
    def draw(self, screen):
        screen.blit(self.image, self.rect)
        
    def is_off_screen(self):
        return self.rect.y > SCREEN_HEIGHT

class Basket:
    def __init__(self):
        self.image = pygame.image.load("basket.png")
        self.image = pygame.transform.scale(self.image, (80, 60))
        self.rect = self.image.get_rect()
        self.rect.x = SCREEN_WIDTH // 2 - self.rect.width // 2
        self.rect.y = SCREEN_HEIGHT - self.rect.height - 10
        
    def update(self, mouse_x):
        self.rect.x = mouse_x - self.rect.width // 2
        # Keep basket on screen
        if self.rect.x < 0:
            self.rect.x = 0
        elif self.rect.x > SCREEN_WIDTH - self.rect.width:
            self.rect.x = SCREEN_WIDTH - self.rect.width
            
    def draw(self, screen):
        screen.blit(self.image, self.rect)

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("ACM Catch Game")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 36)
        self.big_font = pygame.font.Font(None, 72)
        
        # Load and blur background
        self.original_background = pygame.image.load("background_image.webp")
        self.original_background = pygame.transform.scale(self.original_background, (SCREEN_WIDTH, SCREEN_HEIGHT))
        self.background = self.blur_surface(self.original_background, 5)
        
        # Game objects
        self.basket = Basket()
        self.falling_items = []
        
        # Game state
        self.score = 0
        self.items_caught = 0
        self.items_missed = 0
        self.total_items_spawned = 0
        self.start_time = time.time()
        self.game_over = False
        self.won = False
        self.show_try_again = False
        
        # Item counts and queue
        self.items_to_spawn = [
            ("chocolates.jpg", 2, 15),  # (filename, points, count)
            ("chips.jpg", 3, 10),
            ("donuts.jpg", 4, 8),
            ("pizza.jpg", 5, 4),
            ("persons_face.png", 10, 1)  # Final item
        ]
        
        self.current_item_index = 0
        self.current_item_count = 0
        self.spawn_timer = 0
        self.spawn_delay = 60  # frames between spawns
        
        # Calculate total items for win condition
        self.total_items_to_catch = sum(item[2] for item in self.items_to_spawn)
    
    def blur_surface(self, surface, blur_radius):
        """Apply a simple blur effect to a surface"""
        # Create a copy of the surface
        blurred = surface.copy()
        
        # Apply multiple passes of averaging for blur effect
        for _ in range(blur_radius):
            # Scale down and up to create blur effect
            small = pygame.transform.smoothscale(blurred, (SCREEN_WIDTH//4, SCREEN_HEIGHT//4))
            blurred = pygame.transform.smoothscale(small, (SCREEN_WIDTH, SCREEN_HEIGHT))
        
        return blurred
        
    def spawn_item(self):
        if self.current_item_index < len(self.items_to_spawn):
            item_info = self.items_to_spawn[self.current_item_index]
            filename, points, total_count = item_info
            
            if self.current_item_count < total_count:
                # Check if this is the final item (person's face)
                is_final_item = (filename == "persons_face.png")
                
                new_item = FallingItem(filename, points, is_final_item=is_final_item)
                self.falling_items.append(new_item)
                self.current_item_count += 1
                self.total_items_spawned += 1
                
                # Decrease spawn delay as game progresses (increase difficulty)
                self.spawn_delay = max(20, 60 - (self.current_item_index * 10))
            else:
                # Move to next item type
                self.current_item_index += 1
                self.current_item_count = 0
                if self.current_item_index < len(self.items_to_spawn):
                    self.spawn_delay = 40  # Brief pause between item types
    
    def update(self):
        if self.game_over or self.won:
            return
            
        # Check time limit
        elapsed_time = time.time() - self.start_time
        if elapsed_time > TIME_LIMIT:
            self.game_over = True
            self.show_try_again = True
            return
            
        # Update basket position with mouse
        mouse_x, _ = pygame.mouse.get_pos()
        self.basket.update(mouse_x)
        
        # Spawn items
        self.spawn_timer += 1
        if self.spawn_timer >= self.spawn_delay:
            self.spawn_item()
            self.spawn_timer = 0
        
        # Update falling items
        for item in self.falling_items[:]:
            item.update()
            
            # Check collision with basket
            if self.basket.rect.colliderect(item.rect):
                self.score += item.points
                self.items_caught += 1
                self.falling_items.remove(item)
                
                # Check win condition - must catch ALL items
                if self.items_caught >= self.total_items_to_catch:
                    self.won = True
                    
            # Check if item falls off screen - IMMEDIATE LOSS
            elif item.is_off_screen():
                self.items_missed += 1
                self.falling_items.remove(item)
                # Immediate game over if any item is missed
                self.game_over = True
                self.show_try_again = True
                return
    
    def draw(self):
        self.screen.blit(self.background, (0, 0))
        
        if not self.game_over and not self.won:
            # Draw game objects
            self.basket.draw(self.screen)
            for item in self.falling_items:
                item.draw(self.screen)
            
            # Draw UI with black text
            score_text = self.font.render(f"Score: {self.score}", True, BLACK)
            self.screen.blit(score_text, (10, 10))
            
            caught_text = self.font.render(f"Caught: {self.items_caught}/{self.total_items_to_catch}", True, BLACK)
            self.screen.blit(caught_text, (10, 50))
            
            elapsed_time = time.time() - self.start_time
            remaining_time = max(0, TIME_LIMIT - elapsed_time)
            time_text = self.font.render(f"Time: {int(remaining_time)}s", True, BLACK)
            self.screen.blit(time_text, (10, 90))
            
            # Show current item type
            if self.current_item_index < len(self.items_to_spawn):
                item_name = self.items_to_spawn[self.current_item_index][0].split('.')[0]
                current_text = self.font.render(f"Catching: {item_name.title()}", True, BLACK)
                self.screen.blit(current_text, (SCREEN_WIDTH - 250, 10))
            
            # Warning message
            warning_text = self.font.render("Don't miss ANY item!", True, RED)
            self.screen.blit(warning_text, (SCREEN_WIDTH - 250, 50))
        
        elif self.won:
            # Victory screen
            win_text = self.big_font.render("FIRST HALF COMPLETE!", True, GREEN)
            win_rect = win_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 - 120))
            self.screen.blit(win_text, win_rect)
            
            answer_text = self.font.render('First half answer is: "AcM_is_"', True, GREEN)
            answer_rect = answer_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 - 70))
            self.screen.blit(answer_text, answer_rect)
            
            score_text = self.font.render(f"Final Score: {self.score}", True, BLACK)
            score_rect = score_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 - 30))
            self.screen.blit(score_text, score_rect)
            
            perfect_text = self.font.render("Perfect Game! All items caught!", True, BLACK)
            perfect_rect = perfect_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 + 10))
            self.screen.blit(perfect_text, perfect_rect)
            
            continue_text = self.font.render("Press ENTER to continue to second half", True, BLUE)
            continue_rect = continue_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 + 50))
            self.screen.blit(continue_text, continue_rect)
            
            restart_text = self.font.render("Press SPACE to restart or ESC to quit", True, BLACK)
            restart_rect = restart_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 + 90))
            self.screen.blit(restart_text, restart_rect)
            
        elif self.show_try_again:
            # Game over screen
            game_over_text = self.big_font.render("GAME OVER", True, RED)
            game_over_rect = game_over_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 - 100))
            self.screen.blit(game_over_text, game_over_rect)
            
            reason_text = self.font.render("You missed an item!", True, RED)
            reason_rect = reason_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 - 60))
            self.screen.blit(reason_text, reason_rect)
            
            score_text = self.font.render(f"Final Score: {self.score}", True, BLACK)
            score_rect = score_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 - 20))
            self.screen.blit(score_text, score_rect)
            
            caught_text = self.font.render(f"Items Caught: {self.items_caught}/{self.total_items_to_catch}", True, BLACK)
            caught_rect = caught_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 + 20))
            self.screen.blit(caught_text, caught_rect)
            
            try_again_text = self.font.render("Press SPACE to try again or ESC to quit", True, BLACK)
            try_again_rect = try_again_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 + 60))
            self.screen.blit(try_again_text, try_again_rect)
        
        pygame.display.flip()
    
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return False
                elif event.key == pygame.K_SPACE:
                    if self.game_over or self.won:
                        self.restart_game()
                elif event.key == pygame.K_RETURN:
                    if self.won:
                        # Start second half (slide puzzle)
                        return "start_slide_puzzle"
        return True
    
    def restart_game(self):
        self.__init__()
    
    def run(self):
        running = True
        while running:
            result = self.handle_events()
            if result == "start_slide_puzzle":
                return "start_slide_puzzle"
            elif result == False:
                running = False
            self.update()
            self.draw()
            self.clock.tick(FPS)
        
        pygame.quit()
        return "quit"

if __name__ == "__main__":
    game = Game()
    result = game.run()
    if result == "start_slide_puzzle":
        print("Starting second half...")
        # This will be handled by main_game.py
