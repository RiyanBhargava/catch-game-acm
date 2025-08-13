import pygame
import random
import sys
import os

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH = 1000  # Increased from 800
SCREEN_HEIGHT = 700  # Increased from 600
GRID_SIZE = 3
TILE_SIZE = 150
GRID_OFFSET_X = (SCREEN_WIDTH - GRID_SIZE * TILE_SIZE) // 2
GRID_OFFSET_Y = (SCREEN_HEIGHT - GRID_SIZE * TILE_SIZE) // 2 + 50  # Moved down to make room for UI
FPS = 60

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GRAY = (128, 128, 128)
LIGHT_GRAY = (200, 200, 200)

class SlidePuzzle:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("ACM Slide Puzzle - Second Half")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 36)
        self.big_font = pygame.font.Font(None, 72)
        
        # Create ACM logo tiles
        self.create_tiles()
        
        # Game state
        self.grid = list(range(9))  # 0-8, where 8 is empty space
        self.empty_pos = 8  # Position of empty space
        self.solved = False
        self.moves = 0
        
        # Shuffle the puzzle
        self.shuffle_puzzle()
        
    def create_tiles(self):
        """Create 9 tiles from ACM logo image"""
        # Check if acm.png exists, if not create a placeholder
        if not os.path.exists("acm.png"):
            self.create_placeholder_acm_logo()
        
        # Load and resize the ACM logo
        try:
            acm_image = pygame.image.load("acm.png")
        except:
            # Create a simple ACM logo if file doesn't exist
            self.create_simple_acm_logo()
            acm_image = pygame.image.load("acm_logo.png")
            
        # Resize to fit the grid
        total_size = GRID_SIZE * TILE_SIZE
        acm_image = pygame.transform.scale(acm_image, (total_size, total_size))
        
        # Split into 9 tiles
        self.tiles = []
        for i in range(GRID_SIZE):
            for j in range(GRID_SIZE):
                if i * GRID_SIZE + j < 8:  # Don't create tile for empty space
                    tile_rect = pygame.Rect(j * TILE_SIZE, i * TILE_SIZE, TILE_SIZE, TILE_SIZE)
                    tile_surface = pygame.Surface((TILE_SIZE, TILE_SIZE))
                    tile_surface.blit(acm_image, (0, 0), tile_rect)
                    
                    # Add border to tile
                    pygame.draw.rect(tile_surface, BLACK, (0, 0, TILE_SIZE, TILE_SIZE), 3)
                    
                    # Add tile number for reference
                    number_text = self.font.render(str(i * GRID_SIZE + j + 1), True, WHITE)
                    number_rect = number_text.get_rect()
                    number_rect.topleft = (5, 5)
                    tile_surface.blit(number_text, number_rect)
                    
                    self.tiles.append(tile_surface)
    
    def create_simple_acm_logo(self):
        """Create a simple ACM logo if the file doesn't exist"""
        logo_surface = pygame.Surface((450, 450))
        logo_surface.fill(BLUE)
        
        # Draw simple ACM text
        font = pygame.font.Font(None, 120)
        text = font.render("ACM", True, WHITE)
        text_rect = text.get_rect(center=(225, 225))
        logo_surface.blit(text, text_rect)
        
        # Add some decorative elements
        pygame.draw.circle(logo_surface, WHITE, (225, 225), 200, 5)
        pygame.draw.rect(logo_surface, WHITE, (50, 50, 350, 350), 5)
        
        pygame.image.save(logo_surface, "acm_logo.png")
    
    def create_placeholder_acm_logo(self):
        """Create a placeholder ACM logo"""
        logo_surface = pygame.Surface((450, 450))
        logo_surface.fill((30, 60, 120))  # ACM blue
        
        # Draw ACM text
        font = pygame.font.Font(None, 100)
        text = font.render("ACM", True, WHITE)
        text_rect = text.get_rect(center=(225, 150))
        logo_surface.blit(text, text_rect)
        
        # Add subtitle
        small_font = pygame.font.Font(None, 40)
        subtitle = small_font.render("Association for", True, WHITE)
        subtitle_rect = subtitle.get_rect(center=(225, 250))
        logo_surface.blit(subtitle, subtitle_rect)
        
        subtitle2 = small_font.render("Computing Machinery", True, WHITE)
        subtitle2_rect = subtitle2.get_rect(center=(225, 290))
        logo_surface.blit(subtitle2, subtitle2_rect)
        
        # Add decorative border
        pygame.draw.rect(logo_surface, WHITE, (20, 20, 410, 410), 8)
        
        pygame.image.save(logo_surface, "acm.png")
    
    def shuffle_puzzle(self):
        """Shuffle the puzzle by making random valid moves"""
        # Reset solved state and moves before shuffling
        self.solved = False
        self.moves = 0
        
        # Make many random moves to scramble the puzzle
        for _ in range(2000):  # Increased shuffling moves
            self.make_random_move_without_counting()
        
        # Reset moves counter after shuffling
        self.moves = 0
        
        # Ensure puzzle is not in solved state after shuffling
        while self.is_solved_state():
            for _ in range(100):
                self.make_random_move_without_counting()
        
        self.moves = 0  # Reset moves counter again
    
    def make_random_move_without_counting(self):
        """Make a random valid move without incrementing move counter"""
        valid_moves = self.get_valid_moves()
        if valid_moves:
            move = random.choice(valid_moves)
            # Swap tile with empty space without incrementing moves
            self.grid[self.empty_pos], self.grid[move] = self.grid[move], self.grid[self.empty_pos]
            self.empty_pos = move
    
    def is_solved_state(self):
        """Check if puzzle is in solved state without setting solved flag"""
        for i in range(8):
            if self.grid[i] != i:
                return False
        return True
    
    def make_random_move(self):
        """Make a random valid move"""
        valid_moves = self.get_valid_moves()
        if valid_moves:
            move = random.choice(valid_moves)
            self.move_tile(move)
    
    def get_valid_moves(self):
        """Get list of tiles that can be moved"""
        valid_moves = []
        empty_row, empty_col = divmod(self.empty_pos, GRID_SIZE)
        
        # Check all four directions
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        for dr, dc in directions:
            new_row, new_col = empty_row + dr, empty_col + dc
            if 0 <= new_row < GRID_SIZE and 0 <= new_col < GRID_SIZE:
                valid_moves.append(new_row * GRID_SIZE + new_col)
        
        return valid_moves
    
    def move_tile(self, tile_pos):
        """Move a tile to the empty space"""
        if tile_pos in self.get_valid_moves():
            # Swap tile with empty space
            self.grid[self.empty_pos], self.grid[tile_pos] = self.grid[tile_pos], self.grid[self.empty_pos]
            self.empty_pos = tile_pos
            self.moves += 1
            
            # Check if puzzle is solved only after a player move
            self.check_solved()
    
    def check_solved(self):
        """Check if the puzzle is solved"""
        if self.is_solved_state():
            self.solved = True
            return True
        return False
    
    def get_tile_at_pos(self, mouse_pos):
        """Get the tile position at mouse coordinates"""
        mouse_x, mouse_y = mouse_pos
        
        # Check if click is within the grid
        if (GRID_OFFSET_X <= mouse_x < GRID_OFFSET_X + GRID_SIZE * TILE_SIZE and
            GRID_OFFSET_Y <= mouse_y < GRID_OFFSET_Y + GRID_SIZE * TILE_SIZE):
            
            grid_x = (mouse_x - GRID_OFFSET_X) // TILE_SIZE
            grid_y = (mouse_y - GRID_OFFSET_Y) // TILE_SIZE
            
            return grid_y * GRID_SIZE + grid_x
        
        return None
    
    def draw(self):
        self.screen.fill(LIGHT_GRAY)
        
        if not self.solved:
            # Draw title at the top
            title_text = self.big_font.render("ACM Slide Puzzle", True, BLACK)
            title_rect = title_text.get_rect(center=(SCREEN_WIDTH//2, 40))
            self.screen.blit(title_text, title_rect)
            
            # Draw subtitle
            subtitle_text = self.font.render("Second Half", True, BLUE)
            subtitle_rect = subtitle_text.get_rect(center=(SCREEN_WIDTH//2, 80))
            self.screen.blit(subtitle_text, subtitle_rect)
            
            # Draw instructions
            instruction_text = self.font.render("Click on tiles next to empty space to move them", True, BLACK)
            instruction_rect = instruction_text.get_rect(center=(SCREEN_WIDTH//2, 120))
            self.screen.blit(instruction_text, instruction_rect)
            
            goal_text = self.font.render("Goal: Arrange tiles to form the complete ACM logo", True, BLACK)
            goal_rect = goal_text.get_rect(center=(SCREEN_WIDTH//2, 150))
            self.screen.blit(goal_text, goal_rect)
            
            # Draw move counter on the left side
            moves_text = self.font.render(f"Moves: {self.moves}", True, BLACK)
            self.screen.blit(moves_text, (50, 250))
            
            # Draw progress indicator on the right side
            progress_text = self.font.render("Progress:", True, BLACK)
            self.screen.blit(progress_text, (SCREEN_WIDTH - 200, 250))
            
            # Calculate how many tiles are in correct position
            correct_tiles = sum(1 for i in range(8) if self.grid[i] == i)
            progress_bar_width = 150
            progress_bar_height = 20
            progress_x = SCREEN_WIDTH - 200
            progress_y = 280
            
            # Draw progress bar background
            pygame.draw.rect(self.screen, WHITE, (progress_x, progress_y, progress_bar_width, progress_bar_height))
            pygame.draw.rect(self.screen, BLACK, (progress_x, progress_y, progress_bar_width, progress_bar_height), 2)
            
            # Draw progress bar fill
            fill_width = int((correct_tiles / 8) * progress_bar_width)
            if fill_width > 0:
                pygame.draw.rect(self.screen, GREEN, (progress_x, progress_y, fill_width, progress_bar_height))
            
            # Draw progress percentage
            percentage = int((correct_tiles / 8) * 100)
            percent_text = self.font.render(f"{percentage}%", True, BLACK)
            self.screen.blit(percent_text, (progress_x, progress_y + 25))
            
            # Draw the puzzle grid
            for i in range(GRID_SIZE):
                for j in range(GRID_SIZE):
                    pos = i * GRID_SIZE + j
                    tile_x = GRID_OFFSET_X + j * TILE_SIZE
                    tile_y = GRID_OFFSET_Y + i * TILE_SIZE
                    
                    if pos == self.empty_pos:
                        # Draw empty space
                        pygame.draw.rect(self.screen, GRAY, 
                                       (tile_x, tile_y, TILE_SIZE, TILE_SIZE))
                        pygame.draw.rect(self.screen, BLACK, 
                                       (tile_x, tile_y, TILE_SIZE, TILE_SIZE), 3)
                        
                        # Add "EMPTY" text in the empty space
                        empty_text = self.font.render("EMPTY", True, BLACK)
                        empty_rect = empty_text.get_rect(center=(tile_x + TILE_SIZE//2, tile_y + TILE_SIZE//2))
                        self.screen.blit(empty_text, empty_rect)
                    else:
                        # Draw tile
                        tile_num = self.grid[pos]
                        if tile_num < len(self.tiles):
                            self.screen.blit(self.tiles[tile_num], (tile_x, tile_y))
                            
                            # Highlight tiles that can be moved
                            if pos in self.get_valid_moves():
                                pygame.draw.rect(self.screen, GREEN, 
                                               (tile_x, tile_y, TILE_SIZE, TILE_SIZE), 4)
            
            # Draw hint at the bottom
            hint_text = self.font.render("Green borders show movable tiles", True, BLACK)
            hint_rect = hint_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT - 60))
            self.screen.blit(hint_text, hint_rect)
            
        else:
            # Victory screen - better spacing
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
                return False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return False
                elif event.key == pygame.K_SPACE and self.solved:
                    self.restart_puzzle()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if not self.solved and event.button == 1:  # Left click
                    tile_pos = self.get_tile_at_pos(event.pos)
                    if tile_pos is not None:
                        self.move_tile(tile_pos)
        return True
    
    def restart_puzzle(self):
        """Restart the puzzle"""
        self.__init__()
    
    def run(self):
        running = True
        while running:
            running = self.handle_events()
            self.draw()
            self.clock.tick(FPS)
        
        pygame.quit()
        return "quit"

if __name__ == "__main__":
    puzzle = SlidePuzzle()
    puzzle.run()
