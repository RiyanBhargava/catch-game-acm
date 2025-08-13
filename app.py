from flask import Flask, render_template, request, jsonify, send_from_directory
import os
import json
import time
from config import config

app = Flask(__name__)
app.config.from_object(config['development'])

# Game configuration
GAME_CONFIG = {
    'SCREEN_WIDTH': 1000,
    'SCREEN_HEIGHT': 700,
    'BASKET_SPEED': 8,
    'TIME_LIMIT': 120,  # 2 minutes
    'items_to_spawn': [
        {"filename": "chocolates.jpg", "points": 2, "count": 15},
        {"filename": "chips.jpg", "points": 3, "count": 10},
        {"filename": "donuts.jpg", "points": 4, "count": 8},
        {"filename": "pizza.jpg", "points": 5, "count": 4},
        {"filename": "persons_face.png", "points": 10, "count": 1}
    ],
    'PUZZLE_SIZE': 3,
    'TILE_SIZE': 150
}

# Store game sessions (in production, use a database)
game_sessions = {}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/game')
def game():
    return render_template('game.html', config=GAME_CONFIG)

@app.route('/puzzle')
def puzzle():
    return render_template('puzzle.html', config=GAME_CONFIG)

@app.route('/api/start_game', methods=['POST'])
def start_game():
    """Initialize a new game session"""
    session_id = str(int(time.time() * 1000))  # Simple session ID
    
    game_sessions[session_id] = {
        'score': 0,
        'items_caught': 0,
        'items_missed': 0,
        'start_time': time.time(),
        'game_over': False,
        'won': False
    }
    
    return jsonify({
        'session_id': session_id,
        'config': GAME_CONFIG
    })

@app.route('/api/update_score', methods=['POST'])
def update_score():
    """Update game score when an item is caught"""
    data = request.get_json()
    session_id = data.get('session_id')
    points = data.get('points', 0)
    
    if session_id in game_sessions:
        session = game_sessions[session_id]
        session['score'] += points
        session['items_caught'] += 1
        
        return jsonify({
            'success': True,
            'score': session['score'],
            'items_caught': session['items_caught']
        })
    
    return jsonify({'success': False, 'error': 'Invalid session'})

@app.route('/api/miss_item', methods=['POST'])
def miss_item():
    """Record when an item is missed"""
    data = request.get_json()
    session_id = data.get('session_id')
    
    if session_id in game_sessions:
        session = game_sessions[session_id]
        session['items_missed'] += 1
        
        return jsonify({
            'success': True,
            'items_missed': session['items_missed']
        })
    
    return jsonify({'success': False, 'error': 'Invalid session'})

@app.route('/api/end_game', methods=['POST'])
def end_game():
    """End game and return final stats"""
    data = request.get_json()
    session_id = data.get('session_id')
    won = data.get('won', False)
    missed_final_item = data.get('missed_final_item', False)
    
    if session_id in game_sessions:
        session = game_sessions[session_id]
        session['game_over'] = True
        session['won'] = won
        session['missed_final_item'] = missed_final_item
        session['end_time'] = time.time()
        session['duration'] = session['end_time'] - session['start_time']
        
        # Set the first part of the answer if won
        if won:
            session['first_answer_part'] = "aCM_iS_"
        
        return jsonify({
            'success': True,
            'final_score': session['score'],
            'items_caught': session['items_caught'],
            'items_missed': session['items_missed'],
            'duration': session['duration'],
            'won': won,
            'missed_final_item': missed_final_item,
            'first_answer_part': session.get('first_answer_part', '') if won else ''
        })
    
    return jsonify({'success': False, 'error': 'Invalid session'})

@app.route('/api/start_puzzle', methods=['POST'])
def start_puzzle():
    """Initialize puzzle game"""
    data = request.get_json()
    session_id = data.get('session_id')
    
    if session_id in game_sessions:
        session = game_sessions[session_id]
        session['puzzle_moves'] = 0
        session['puzzle_completed'] = False
        session['puzzle_start_time'] = time.time()
        
        # Generate shuffled puzzle state
        puzzle_state = list(range(9))  # 0-8, where 8 is empty
        import random
        
        # Shuffle by making random valid moves
        empty_pos = 8
        for _ in range(1000):
            valid_moves = []
            row, col = empty_pos // 3, empty_pos % 3
            
            # Check all 4 directions
            for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                new_row, new_col = row + dr, col + dc
                if 0 <= new_row < 3 and 0 <= new_col < 3:
                    valid_moves.append(new_row * 3 + new_col)
            
            if valid_moves:
                move_pos = random.choice(valid_moves)
                # Swap empty space with the chosen position
                puzzle_state[empty_pos], puzzle_state[move_pos] = puzzle_state[move_pos], puzzle_state[empty_pos]
                empty_pos = move_pos
        
        session['puzzle_state'] = puzzle_state
        session['empty_pos'] = empty_pos
        
        return jsonify({
            'success': True,
            'puzzle_state': puzzle_state,
            'empty_pos': empty_pos
        })
    
    return jsonify({'success': False, 'error': 'Invalid session'})

@app.route('/api/move_tile', methods=['POST'])
def move_tile():
    """Move a tile in the puzzle"""
    data = request.get_json()
    session_id = data.get('session_id')
    tile_pos = data.get('tile_pos')
    
    if session_id in game_sessions:
        session = game_sessions[session_id]
        puzzle_state = session['puzzle_state']
        empty_pos = session['empty_pos']
        
        # Check if move is valid (adjacent to empty space)
        empty_row, empty_col = empty_pos // 3, empty_pos % 3
        tile_row, tile_col = tile_pos // 3, tile_pos % 3
        
        if abs(empty_row - tile_row) + abs(empty_col - tile_col) == 1:
            # Valid move - swap tile with empty space
            puzzle_state[empty_pos], puzzle_state[tile_pos] = puzzle_state[tile_pos], puzzle_state[empty_pos]
            session['empty_pos'] = tile_pos
            session['puzzle_moves'] += 1
            
            # Check if solved
            solved = puzzle_state == list(range(9))
            if solved:
                session['puzzle_completed'] = True
                session['puzzle_end_time'] = time.time()
                session['second_answer_part'] = "tHe_GOaT"
                session['full_answer'] = "aCM_iS_tHe_GOaT"
            
            return jsonify({
                'success': True,
                'puzzle_state': puzzle_state,
                'empty_pos': session['empty_pos'],
                'moves': session['puzzle_moves'],
                'solved': solved,
                'second_answer_part': session.get('second_answer_part', '') if solved else '',
                'full_answer': session.get('full_answer', '') if solved else ''
            })
        else:
            return jsonify({'success': False, 'error': 'Invalid move'})
    
    return jsonify({'success': False, 'error': 'Invalid session'})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
