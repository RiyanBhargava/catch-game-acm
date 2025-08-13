# 🎮 ACM Challenge - Two Part Game

A thrilling two-part interactive game designed to test your reflexes and puzzle-solving skills while revealing a secret ACM message!

## 🌐 Play Online

**Live Demo:** [https://riyanvhargava.github.io/catch-game-acm](https://riyanvhargava.github.io/catch-game-acm)

## 🎯 Game Overview

### Part 1: Catch Game 🎯
- **Objective:** Catch all falling items without missing any
- **Controls:** Move your mouse to control the basket
- **Challenge:** Must catch ALL 38 items (15 chocolates, 10 chips, 8 donuts, 4 pizza, 1 person's face)
- **Difficulty:** Items fall at varying speeds - some normal, some very fast!
- **Rule:** Miss even ONE item and you lose!

### Part 2: Slide Puzzle 🧩
- **Objective:** Rearrange ACM logo tiles to form the complete image
- **Controls:** Click on tiles adjacent to empty space to move them
- **Challenge:** Solve the 3x3 sliding puzzle
- **Goal:** Arrange tiles in correct order to reveal the ACM logo

## 🏆 The Secret Mission

Complete both parts to discover the hidden ACM message! Each part reveals a portion of the answer.

## 🚀 How to Run Locally

### Prerequisites
- Python 3.7+
- pip package manager

### Installation
1. **Clone the repository:**
   ```bash
   git clone https://github.com/RiyanBhargava/catch-game-acm.git
   cd catch-game-acm
   ```

2. **Install required packages:**
   ```bash
   pip install pygame Pillow
   ```

3. **Create the ACM logo:**
   ```bash
   python create_acm_logo.py
   ```

4. **Run the game:**
   ```bash
   python main_game.py
   ```

## 📁 File Structure

```
catch-game-acm/
├── main_game.py          # Main game controller
├── catch_game.py         # First half - Catch game
├── slide_puzzle.py       # Second half - Slide puzzle
├── create_acm_logo.py    # Creates ACM logo for puzzle
├── web_main.py          # Web-compatible version
├── index.html           # Landing page for web deployment
├── requirements.txt     # Python dependencies
└── assets/
    ├── basket.png
    ├── background_image.webp
    ├── chocolates.jpg
    ├── chips.jpg
    ├── donuts.jpg
    ├── pizza.jpg
    └── persons_face.png
```

## 🎮 Game Features

### ⚡ Advanced Mechanics
- **Variable Speed Items:** 70% normal speed, 30% high speed
- **Perfect Precision Required:** No margin for error
- **Progressive Difficulty:** Later items spawn faster
- **Visual Feedback:** Progress tracking and hints

### 🎨 Enhanced UI
- **Blurred Background:** Atmospheric visual effect
- **Real-time Statistics:** Score, progress, time remaining
- **Interactive Elements:** Green borders show movable tiles
- **Responsive Design:** Works on different screen sizes

### 🧠 Puzzle Features
- **Smart Shuffling:** Ensures puzzle is always solvable
- **Move Counter:** Track your efficiency
- **Progress Bar:** Visual completion indicator
- **Hint System:** Shows which tiles can be moved

## 🌐 Web Deployment

This project is configured for automatic deployment to GitHub Pages using GitHub Actions.

### Deploy to Your Own GitHub Pages:
1. Fork this repository
2. Go to repository Settings → Pages
3. Set source to "GitHub Actions"
4. Push any changes to trigger deployment
5. Your game will be live at `https://yourusername.github.io/catch-game-acm`

### Alternative Hosting Options:
- **Replit:** Import repository and run directly
- **Netlify:** Connect GitHub repo for instant deployment
- **Vercel:** One-click deployment from GitHub

## 🛠️ Technical Details

### Dependencies
- **pygame:** Game engine for graphics and interactions
- **Pillow:** Image processing for ACM logo creation
- **pygbag:** Web conversion for browser compatibility

### Performance Optimizations
- **Efficient collision detection:** Pygame rect-based collision
- **Optimized rendering:** Only updates changed elements
- **Memory management:** Proper cleanup of game objects
- **Smooth animations:** 60 FPS target with async/await for web

## 🎯 Game Balance

### Catch Game Difficulty
- **Base falling speed:** 5 pixels/frame
- **Fast items:** 9-11 pixels/frame (30% chance)
- **Final item (person's face):** 2-3 pixels/frame (slow and catchable)
- **Time limit:** 2 minutes
- **Spawn rate:** Accelerates as game progresses

### Slide Puzzle Complexity
- **Grid size:** 3×3 (8 movable tiles + 1 empty space)
- **Shuffle algorithm:** 2000 random moves for proper scrambling
- **Solvability:** Always guaranteed to be solvable
- **Visual aids:** Green borders indicate movable tiles

## 🏅 Achievement System

- **Perfect Catch:** Complete Part 1 without missing any items
- **Puzzle Master:** Solve Part 2 in minimal moves
- **Speed Runner:** Complete both parts quickly
- **ACM Champion:** Discover the complete secret message

## 🤝 Contributing

Contributions are welcome! Here are some ways you can contribute:

1. **Bug Reports:** Found a bug? Open an issue!
2. **Feature Requests:** Have ideas for improvements?
3. **Code Contributions:** Submit pull requests for enhancements
4. **Documentation:** Help improve the README and code comments

### Development Setup
```bash
# Clone and setup
git clone https://github.com/RiyanBhargava/catch-game-acm.git
cd catch-game-acm

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the game
python main_game.py
```

## 📜 License

This project is open source and available under the [MIT License](LICENSE).

## 🎉 Credits

- **Game Design:** Original ACM Challenge concept
- **Development:** Python with pygame framework
- **Graphics:** Custom assets and procedural generation
- **Web Conversion:** pygame-web (pygbag) technology
- **Hosting:** GitHub Pages with automated deployment

## 🔗 Links

- **Play Online:** [GitHub Pages Demo](https://riyanvhargava.github.io/catch-game-acm)
- **Source Code:** [GitHub Repository](https://github.com/RiyanBhargava/catch-game-acm)
- **Issues:** [Report Bugs](https://github.com/RiyanBhargava/catch-game-acm/issues)
- **Discussions:** [Community Forum](https://github.com/RiyanBhargava/catch-game-acm/discussions)

---

**🎮 Ready to take on the ACM Challenge? Test your skills and discover the secret message!**

*Good luck, and may your reflexes be quick and your puzzle-solving skills sharp!* 🎯🧩
