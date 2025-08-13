# ACM Catch Game - Flask Web Version

This is a web-based version of the ACM Catch Game, converted from pygame to run in web browsers using Flask and HTML5 Canvas.

## Features

- **Web-based gameplay**: Runs in any modern web browser
- **Real-time scoring**: Live score updates and statistics
- **Progressive difficulty**: Items spawn faster as the game progresses
- **Time limit**: 2-minute game sessions
- **Win condition**: Catch the person's face to complete the game
- **Responsive design**: Works on desktop and mobile devices

## Local Development

### Prerequisites
- Python 3.7+
- Flask

### Installation
```bash
pip install -r flask_requirements.txt
```

### Running the Game
```bash
python app.py
```

Then open your browser to `http://localhost:5000`

## Game Instructions

1. **Game 1 - Catch Challenge**: Catch falling items with your basket to score points
2. **Controls**: Move your mouse to control the basket position
3. **Scoring**:
   - 🍫 Chocolates: 2 points each (15 items)
   - 🍟 Chips: 3 points each (10 items)
   - 🍩 Donuts: 4 points each (8 items)
   - 🍕 Pizza: 5 points each (4 items)
   - 👤 Person's Face: 10 points (1 item - catch this to win!)
4. **Time Limit**: 2 minutes to catch as many items as possible
5. **Miss Limit**: Game ends if you miss 2 items - be careful!
6. **Win Condition**: Catch the person's face to complete Game 1 and reveal first answer part

7. **Game 2 - ACM Logo Puzzle**: Reconstruct the ACM logo by sliding tiles
8. **Controls**: Click tiles adjacent to empty space to move them
9. **Objective**: Arrange pieces to form the complete ACM logo (no numbers - use visual recognition!)
10. **Win Condition**: Complete the logo to reveal the second answer part

**Complete both games to discover the full secret message: "aCM_iS_tHe_GOaT"**

## File Structure

```
├── app.py                 # Main Flask application
├── wsgi.py               # WSGI configuration for deployment
├── flask_requirements.txt # Python dependencies
├── templates/
│   ├── index.html        # Home page
│   └── game.html         # Game page
├── *.png, *.jpg, *.webp  # Game assets (images)
└── DEPLOYMENT_GUIDE.md   # PythonAnywhere deployment instructions
```

## API Endpoints

- `GET /` - Home page
- `GET /game` - Game page
- `POST /api/start_game` - Initialize a new game session
- `POST /api/update_score` - Update score when item is caught
- `POST /api/miss_item` - Record when item is missed
- `POST /api/end_game` - End game and get final statistics
- `GET /static/<filename>` - Serve game assets

## Deployment

This game is designed to be deployed on PythonAnywhere's free tier. See `DEPLOYMENT_GUIDE.md` for detailed deployment instructions.

## Differences from Original pygame Version

- **No pygame dependency**: Uses HTML5 Canvas and JavaScript instead
- **Web-based**: Accessible from any device with a web browser
- **Session management**: Game state tracked server-side
- **Responsive**: Adapts to different screen sizes
- **Cross-platform**: Works on Windows, Mac, Linux, mobile devices

## Technical Details

- **Backend**: Flask (Python)
- **Frontend**: HTML5 Canvas, JavaScript
- **Images**: Served as static files
- **Game Loop**: JavaScript requestAnimationFrame for smooth animation
- **Collision Detection**: 2D bounding box collision detection
- **State Management**: RESTful API with session-based game state

## Browser Compatibility

- Chrome 60+
- Firefox 55+
- Safari 11+
- Edge 79+
- Mobile browsers (iOS Safari, Chrome Mobile)

Enjoy playing the ACM Catch Game!
