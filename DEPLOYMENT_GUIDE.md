# Flask Deployment Guide for PythonAnywhere

## Files Overview
- `app.py` - Main Flask application with both games
- `templates/index.html` - Home page
- `templates/game.html` - Catch game page
- `templates/puzzle.html` - Slide puzzle game page
- `flask_requirements.txt` - Flask dependencies
- `wsgi.py` - WSGI configuration for PythonAnywhere
- `static/` folder - All game assets (images)

## Local Testing

1. Install Flask dependencies:
```bash
pip install -r flask_requirements.txt
```

2. Run the Flask app locally:
```bash
python app.py
```

3. Open your browser to `http://localhost:5000`

## PythonAnywhere Deployment

### Step 1: Upload Files
1. Log into your PythonAnywhere account
2. Go to "Files" and navigate to `/home/yourusername/mysite/`
3. Upload all the Flask files:
   - `app.py`
   - `wsgi.py`
   - `flask_requirements.txt`
   - `templates/` folder with both HTML files
   - All image files (acm.png, basket.png, background_image.webp, chocolates.jpg, chips.jpg, donuts.jpg, pizza.jpg, persons_face.png)

### Step 2: Install Dependencies
1. Go to "Tasks" → "Consoles" → "Bash"
2. Run: `pip3.10 install --user -r flask_requirements.txt`

### Step 3: Configure Web App
1. Go to "Web" tab
2. Click "Add a new web app"
3. Choose "Manual configuration" and Python 3.10
4. In the "Code" section:
   - Source code: `/home/yourusername/mysite/`
   - Working directory: `/home/yourusername/mysite/`
5. Edit the WSGI configuration file:
   - Replace the content with the `wsgi.py` file content
   - Update the path to match your username: `/home/yourusername/mysite`

### Step 4: Static Files (Important!)
In the "Static files" section, add:
- URL: `/static/`
- Directory: `/home/yourusername/mysite/`

This ensures your game images are served correctly.

### Step 5: Reload and Test
1. Click "Reload" button in the Web tab
2. Visit your app at `https://yourusername.pythonanywhere.com`

## Game Features
- **Two-part challenge**: Catch game followed by slide puzzle
- **Web-based**: No pygame required, runs in any browser
- **Miss detection**: Game ends if too many items are missed
- **Answer revelation**: First part revealed after catch game, second part after puzzle
- **Score tracking**: Real-time score updates
- **Time limit**: 2-minute game sessions
- **Progressive difficulty**: Items spawn faster as game progresses
- **Secret message**: Complete both parts to reveal "aCM_iS_tHe_GOaT"

## Troubleshooting
- If images don't load, check the static files configuration
- If the game doesn't start, check the browser console for JavaScript errors
- Ensure all image files are uploaded to the correct directory

## Game Controls
- Move mouse to control the basket
- Catch falling items to score points
- Catch the person's face to win the game

## Scoring System
- Chocolates: 2 points (15 items)
- Chips: 3 points (10 items)  
- Donuts: 4 points (8 items)
- Pizza: 5 points (4 items)
- Person's Face: 10 points (1 item - win condition)

The Flask version maintains the same game mechanics as your original pygame version but runs in a web browser, making it perfect for PythonAnywhere deployment!
