import pygame
import sys
import os

# Import both game modules
from catch_game import Game as CatchGame
from slide_puzzle import SlidePuzzle

class GameController:
    def __init__(self):
        pygame.init()
        
    def run_full_game(self):
        """Run the complete two-part game"""
        print("Starting ACM Challenge - Two Part Game!")
        print("First Half: Catch Game")
        print("Second Half: Slide Puzzle")
        print("-" * 50)
        
        # Run first half (catch game)
        catch_game = CatchGame()
        result = catch_game.run()
        
        if result == "start_slide_puzzle":
            print("First half completed! Starting second half...")
            
            # Run second half (slide puzzle)
            slide_puzzle = SlidePuzzle()
            slide_puzzle.run()
        
        print("Game completed! Thanks for playing!")

if __name__ == "__main__":
    controller = GameController()
    controller.run_full_game()
