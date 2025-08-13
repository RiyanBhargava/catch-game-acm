import asyncio
import pygame
import random
import sys
import time
from pygame import gfxdraw
import os

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 700
FPS = 60
BASKET_SPEED = 8
FALL_SPEED_BASE = 5
FALL_SPEED_INCREMENT = 1.0
TIME_LIMIT = 120

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GRAY = (128, 128, 128)
LIGHT_GRAY = (200, 200, 200)

class FallingItem:
    def __init__(self, image_path, points, x=None, speed=None, is_final_item=False):
        self.image = pygame.image.load(image_path)
        self.image = pygame.transform.scale(self.image, (50, 50))
        self.rect = self.image.get_rect()
        self.rect.x = x if x is not None else random.randint(0, SCREEN_WIDTH - self.rect.width)
        self.rect.y = -self.rect.height
        
        # Set speed based on item type
        if is_final_item:
            self.speed = 2 + random.uniform(0, 1)
        else:
            if random.random() < 0.3:
                self.speed = 9 + random.uniform(0, 2)
            else:
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
        if self.rect.x < 0:
            self.rect.x = 0
        elif self.rect.x > SCREEN_WIDTH - self.rect.width:
            self.rect.x = SCREEN_WIDTH - self.rect.width
            
    def draw(self, screen):
        screen.blit(self.image, self.rect)

class CatchGame:
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
            ("chocolates.jpg", 2, 15),
            ("chips.jpg", 3, 10),
            ("donuts.jpg", 4, 8),
            ("pizza.jpg", 5, 4),
            ("persons_face.png", 10, 1)
        ]
        
        self.current_item_index = 0
        self.current_item_count = 0
        self.spawn_timer = 0
        self.spawn_delay = 60
        
        self.total_items_to_catch = sum(item[2] for item in self.items_to_spawn)
    
    def blur_surface(self, surface, blur_radius):
        blurred = surface.copy()
        for _ in range(blur_radius):
            small = pygame.transform.smoothscale(blurred, (SCREEN_WIDTH//4, SCREEN_HEIGHT//4))
            blurred = pygame.transform.smoothscale(small, (SCREEN_WIDTH, SCREEN_HEIGHT))
        return blurred
    
    def spawn_item(self):
        if self.current_item_index < len(self.items_to_spawn):
            item_info = self.items_to_spawn[self.current_item_index]
            filename, points, total_count = item_info
            
            if self.current_item_count < total_count:
                is_final_item = (filename == "persons_face.png")
                new_item = FallingItem(filename, points, is_final_item=is_final_item)
                self.falling_items.append(new_item)
                self.current_item_count += 1
                self.total_items_spawned += 1
                
                self.spawn_delay = max(20, 60 - (self.current_item_index * 10))
            else:
                self.current_item_index += 1
                self.current_item_count = 0
                if self.current_item_index < len(self.items_to_spawn):
                    self.spawn_delay = 40
    
    def update(self):
        if self.game_over or self.won:
            return
            
        elapsed_time = time.time() - self.start_time
        if elapsed_time > TIME_LIMIT:
            self.game_over = True
            self.show_try_again = True
            return
            
        mouse_x, _ = pygame.mouse.get_pos()
        self.basket.update(mouse_x)
        
        self.spawn_timer += 1
        if self.spawn_timer >= self.spawn_delay:
            self.spawn_item()
            self.spawn_timer = 0
        
        for item in self.falling_items[:]:
            item.update()
            
            if self.basket.rect.colliderect(item.rect):
                self.score += item.points
                self.items_caught += 1
                self.falling_items.remove(item)
                
                if self.items_caught >= self.total_items_to_catch:
                    self.won = True
                    
            elif item.is_off_screen():
                self.items_missed += 1
                self.falling_items.remove(item)
                self.game_over = True
                self.show_try_again = True
                return
    
    def draw(self):
        self.screen.blit(self.background, (0, 0))
        
        if not self.game_over and not self.won:
            self.basket.draw(self.screen)
            for item in self.falling_items:
                item.draw(self.screen)
            
            score_text = self.font.render(f"Score: {self.score}", True, BLACK)
            self.screen.blit(score_text, (10, 10))
            
            caught_text = self.font.render(f"Caught: {self.items_caught}/{self.total_items_to_catch}", True, BLACK)
            self.screen.blit(caught_text, (10, 50))
            
            elapsed_time = time.time() - self.start_time
            remaining_time = max(0, TIME_LIMIT - elapsed_time)
            time_text = self.font.render(f"Time: {int(remaining_time)}s", True, BLACK)
            self.screen.blit(time_text, (10, 90))
            
            if self.current_item_index < len(self.items_to_spawn):
                item_name = self.items_to_spawn[self.current_item_index][0].split('.')[0]
                current_text = self.font.render(f"Catching: {item_name.title()}", True, BLACK)
                self.screen.blit(current_text, (SCREEN_WIDTH - 250, 10))
            
            warning_text = self.font.render("Don't miss ANY item!", True, RED)
            self.screen.blit(warning_text, (SCREEN_WIDTH - 250, 50))
        
        elif self.won:
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
                return "quit"
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return "quit"
                elif event.key == pygame.K_SPACE:
                    if self.game_over or self.won:
                        self.__init__()
                        return "restart"
                elif event.key == pygame.K_RETURN:
                    if self.won:
                        return "start_slide_puzzle"
        return "continue"

class SlidePuzzle:
    def __init__(self):
        self.screen = pygame.display.get_surface()
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 36)
        self.big_font = pygame.font.Font(None, 72)
        
        # Create ACM logo tiles
        self.create_tiles()
        
        # Game state
        self.grid = list(range(9))
        self.empty_pos = 8
        self.solved = False
        self.moves = 0
        
        # Shuffle the puzzle
        self.shuffle_puzzle()
        
    def create_tiles(self):
        if not os.path.exists("acm.png"):
            self.create_simple_acm_logo()
            
        try:
            acm_image = pygame.image.load("acm.png")
        except:
            self.create_simple_acm_logo()
            acm_image = pygame.image.load("acm.png")
            
        total_size = 3 * 150
        acm_image = pygame.transform.scale(acm_image, (total_size, total_size))
        
        self.tiles = []
        for i in range(3):
            for j in range(3):
                if i * 3 + j < 8:
                    tile_rect = pygame.Rect(j * 150, i * 150, 150, 150)
                    tile_surface = pygame.Surface((150, 150))
                    tile_surface.blit(acm_image, (0, 0), tile_rect)
                    
                    pygame.draw.rect(tile_surface, BLACK, (0, 0, 150, 150), 3)
                    
                    number_text = self.font.render(str(i * 3 + j + 1), True, WHITE)
                    number_rect = number_text.get_rect()
                    number_rect.topleft = (5, 5)
                    tile_surface.blit(number_text, number_rect)
                    
                    self.tiles.append(tile_surface)
    
    def create_simple_acm_logo(self):
        logo_surface = pygame.Surface((450, 450))
        logo_surface.fill((30, 60, 120))
        
        font = pygame.font.Font(None, 100)
        text = font.render("ACM", True, WHITE)
        text_rect = text.get_rect(center=(225, 150))
        logo_surface.blit(text, text_rect)
        
        small_font = pygame.font.Font(None, 40)
        subtitle = small_font.render("Association for", True, WHITE)
        subtitle_rect = subtitle.get_rect(center=(225, 250))
        logo_surface.blit(subtitle, subtitle_rect)
        
        subtitle2 = small_font.render("Computing Machinery", True, WHITE)
        subtitle2_rect = subtitle2.get_rect(center=(225, 290))
        logo_surface.blit(subtitle2, subtitle2_rect)
        
        pygame.draw.rect(logo_surface, WHITE, (20, 20, 410, 410), 8)
        
        pygame.image.save(logo_surface, "acm.png")
    
    def shuffle_puzzle(self):
        self.solved = False
        self.moves = 0
        
        for _ in range(2000):
            self.make_random_move_without_counting()
        
        self.moves = 0
        
        while self.is_solved_state():
            for _ in range(100):
                self.make_random_move_without_counting()
        
        self.moves = 0
    
    def make_random_move_without_counting(self):
        valid_moves = self.get_valid_moves()
        if valid_moves:
            move = random.choice(valid_moves)
            self.grid[self.empty_pos], self.grid[move] = self.grid[move], self.grid[self.empty_pos]
            self.empty_pos = move
    
    def is_solved_state(self):
        for i in range(8):
            if self.grid[i] != i:
                return False
        return True
    
    def get_valid_moves(self):
        valid_moves = []
        empty_row, empty_col = divmod(self.empty_pos, 3)
        
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        for dr, dc in directions:
            new_row, new_col = empty_row + dr, empty_col + dc
            if 0 <= new_row < 3 and 0 <= new_col < 3:
                valid_moves.append(new_row * 3 + new_col)
        
        return valid_moves
    
    def move_tile(self, tile_pos):
        if tile_pos in self.get_valid_moves():
            self.grid[self.empty_pos], self.grid[tile_pos] = self.grid[tile_pos], self.grid[self.empty_pos]
            self.empty_pos = tile_pos
            self.moves += 1
            
            self.check_solved()
    
    def check_solved(self):
        if self.is_solved_state():
            self.solved = True
            return True
        return False
    
    def get_tile_at_pos(self, mouse_pos):
        mouse_x, mouse_y = mouse_pos
        
        grid_offset_x = (SCREEN_WIDTH - 3 * 150) // 2
        grid_offset_y = (SCREEN_HEIGHT - 3 * 150) // 2 + 50
        
        if (grid_offset_x <= mouse_x < grid_offset_x + 3 * 150 and
            grid_offset_y <= mouse_y < grid_offset_y + 3 * 150):
            
            grid_x = (mouse_x - grid_offset_x) // 150
            grid_y = (mouse_y - grid_offset_y) // 150
            
            return grid_y * 3 + grid_x
        
        return None
    
    def draw(self):
        self.screen.fill(LIGHT_GRAY)
        
        grid_offset_x = (SCREEN_WIDTH - 3 * 150) // 2
        grid_offset_y = (SCREEN_HEIGHT - 3 * 150) // 2 + 50
        
        if not self.solved:
            title_text = self.big_font.render("ACM Slide Puzzle", True, BLACK)
            title_rect = title_text.get_rect(center=(SCREEN_WIDTH//2, 40))
            self.screen.blit(title_text, title_rect)
            
            subtitle_text = self.font.render("Second Half", True, BLUE)
            subtitle_rect = subtitle_text.get_rect(center=(SCREEN_WIDTH//2, 80))
            self.screen.blit(subtitle_text, subtitle_rect)
            
            instruction_text = self.font.render("Click on tiles next to empty space to move them", True, BLACK)
            instruction_rect = instruction_text.get_rect(center=(SCREEN_WIDTH//2, 120))
            self.screen.blit(instruction_text, instruction_rect)
            
            goal_text = self.font.render("Goal: Arrange tiles to form the complete ACM logo", True, BLACK)
            goal_rect = goal_text.get_rect(center=(SCREEN_WIDTH//2, 150))
            self.screen.blit(goal_text, goal_rect)
            
            moves_text = self.font.render(f"Moves: {self.moves}", True, BLACK)
            self.screen.blit(moves_text, (50, 250))
            
            progress_text = self.font.render("Progress:", True, BLACK)
            self.screen.blit(progress_text, (SCREEN_WIDTH - 200, 250))
            
            correct_tiles = sum(1 for i in range(8) if self.grid[i] == i)
            progress_bar_width = 150
            progress_bar_height = 20
            progress_x = SCREEN_WIDTH - 200
            progress_y = 280
            
            pygame.draw.rect(self.screen, WHITE, (progress_x, progress_y, progress_bar_width, progress_bar_height))
            pygame.draw.rect(self.screen, BLACK, (progress_x, progress_y, progress_bar_width, progress_bar_height), 2)
            
            fill_width = int((correct_tiles / 8) * progress_bar_width)
            if fill_width > 0:
                pygame.draw.rect(self.screen, GREEN, (progress_x, progress_y, fill_width, progress_bar_height))
            
            percentage = int((correct_tiles / 8) * 100)
            percent_text = self.font.render(f"{percentage}%", True, BLACK)
            self.screen.blit(percent_text, (progress_x, progress_y + 25))
            
            for i in range(3):
                for j in range(3):
                    pos = i * 3 + j
                    tile_x = grid_offset_x + j * 150
                    tile_y = grid_offset_y + i * 150
                    
                    if pos == self.empty_pos:
                        pygame.draw.rect(self.screen, GRAY, (tile_x, tile_y, 150, 150))
                        pygame.draw.rect(self.screen, BLACK, (tile_x, tile_y, 150, 150), 3)
                        
                        empty_text = self.font.render("EMPTY", True, BLACK)
                        empty_rect = empty_text.get_rect(center=(tile_x + 75, tile_y + 75))
                        self.screen.blit(empty_text, empty_rect)
                    else:
                        tile_num = self.grid[pos]
                        if tile_num < len(self.tiles):
                            self.screen.blit(self.tiles[tile_num], (tile_x, tile_y))
                            
                            if pos in self.get_valid_moves():
                                pygame.draw.rect(self.screen, GREEN, (tile_x, tile_y, 150, 150), 4)
            
            hint_text = self.font.render("Green borders show movable tiles", True, BLACK)
            hint_rect = hint_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT - 60))
            self.screen.blit(hint_text, hint_rect)
            
        else:
            win_text = self.big_font.render("SECOND HALF COMPLETE!", True, GREEN)
            win_rect = win_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 - 200))
            self.screen.blit(win_text, win_rect)
            
            complete_text = self.font.render('Second half answer is: "tHe_gOaT"', True, GREEN)
            complete_rect = complete_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 - 140))
            self.screen.blit(complete_text, complete_rect)
            
            full_answer_text = self.big_font.render('Complete answer: "AcM_is_tHe_gOaT"', True, BLUE)
            full_answer_rect = full_answer_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 - 80))
            self.screen.blit(full_answer_text, full_answer_rect)
            
            moves_text = self.font.render(f"Puzzle completed in {self.moves} moves!", True, BLACK)
            moves_rect = moves_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 - 20))
            self.screen.blit(moves_text, moves_rect)
            
            congrats_text = self.font.render("🎉 Congratulations! You completed both halves! 🎉", True, BLACK)
            congrats_rect = congrats_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 + 40))
            self.screen.blit(congrats_text, congrats_rect)
            
            challenge_text = self.font.render("You have successfully solved the ACM Challenge!", True, BLACK)
            challenge_rect = challenge_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 + 80))
            self.screen.blit(challenge_text, challenge_rect)
            
            restart_text = self.font.render("Press SPACE to restart puzzle or ESC to quit", True, BLACK)
            restart_rect = restart_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 + 140))
            self.screen.blit(restart_text, restart_rect)
        
        pygame.display.flip()
    
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return "quit"
                elif event.key == pygame.K_SPACE and self.solved:
                    self.__init__()
                    return "restart"
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if not self.solved and event.button == 1:
                    tile_pos = self.get_tile_at_pos(event.pos)
                    if tile_pos is not None:
                        self.move_tile(tile_pos)
        return "continue"

class WebGameController:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("ACM Challenge - Two Part Game")
        self.clock = pygame.time.Clock()
        
        self.current_game = "catch"
        self.catch_game = CatchGame()
        self.slide_puzzle = None
        
    async def run(self):
        running = True
        while running:
            if self.current_game == "catch":
                result = self.catch_game.handle_events()
                if result == "quit":
                    running = False
                elif result == "start_slide_puzzle":
                    self.current_game = "slide"
                    self.slide_puzzle = SlidePuzzle()
                
                self.catch_game.update()
                self.catch_game.draw()
                
            elif self.current_game == "slide":
                result = self.slide_puzzle.handle_events()
                if result == "quit":
                    running = False
                
                self.slide_puzzle.draw()
            
            self.clock.tick(FPS)
            await asyncio.sleep(0)
        
        pygame.quit()

async def main():
    game = WebGameController()
    await game.run()

if __name__ == "__main__":
    asyncio.run(main())
