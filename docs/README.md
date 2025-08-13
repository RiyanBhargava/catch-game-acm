# ACM Challenge Game

A two-part interactive Python game that challenges your reflexes and puzzle-solving skills to reveal a secret ACM message.

## 🎮 Game Overview

### Part 1: Catch Game
- Control a basket with your mouse to catch falling items
- Must catch ALL items without missing any to proceed
- Items include: chocolates, chips, donuts, pizza, and a person's face
- Different items fall at different speeds to increase difficulty

### Part 2: Slide Puzzle  
- Solve a 3x3 sliding puzzle featuring the ACM logo
- Click tiles adjacent to the empty space to move them
- Arrange tiles to form the complete ACM logo
- Reveals the final secret message when solved

## 🚀 How to Play

### Option 1: Play Online (Replit)
Visit: [https://replit.com/@RiyanBhargava/catch-game-acm](https://replit.com/@RiyanBhargava/catch-game-acm)

### Option 2: Local Installation (Recommended)

1. **Clone the repository:**
   ```bash
   git clone https://github.com/RiyanBhargava/catch-game-acm.git
   cd catch-game-acm
   ```

2. **Install Python dependencies:**
   ```bash
   pip install pygame Pillow
   ```

3. **Run the game:**
   ```bash
   python main_game.py
   ```

## 📁 Project Structure

```
catch-game-acm/
├── main_game.py          # Main game controller
├── catch_game.py         # Part 1: Catch game implementation  
├── slide_puzzle.py       # Part 2: Slide puzzle implementation
├── create_acm_logo.py    # Generates ACM logo for puzzle
├── web_main.py           # Web-compatible version
├── docs/
│   └── index.html        # GitHub Pages landing page
├── assets/
│   ├── basket.png        # Player basket sprite
│   ├── background_image.webp  # Blurred background
│   ├── persons_face.png  # Special falling item
│   ├── chocolates.jpg    # Falling food items
│   ├── chips.jpg
│   ├── donuts.jpg
│   └── pizza.jpg
└── .github/workflows/    # GitHub Actions for deployment
```

## 🎯 Game Rules

### Catch Game Rules:
- Move your mouse to control the basket
- Catch all falling items (38 total items)
- Missing ANY item results in game over
- Person's face appears last and moves slowly
- Complete all catches to unlock the slide puzzle

### Slide Puzzle Rules:
- 3x3 grid with one empty space
- Click tiles next to the empty space to move them
- Arrange tiles to form the complete ACM logo
- Puzzle is scrambled with 2000 random moves at start

## 🏆 The Secret Message

Complete both parts to discover the hidden ACM message: **"AcM_is_tHe_gOaT"**

## 🛠️ Technical Details

- **Language:** Python 3.11+
- **Framework:** Pygame 2.6+
- **Graphics:** PIL/Pillow for image processing
- **Web Version:** Pygbag for browser compatibility
- **Deployment:** GitHub Pages with GitHub Actions

## 🎨 Features

- **High-speed gameplay** with variable falling speeds
- **Perfect precision required** - no mistakes allowed
- **Blurred background effects** for visual appeal
- **Progressive difficulty** from catching to puzzle solving
- **Mouse-controlled interface** for intuitive gameplay
- **Visual feedback** with progress tracking
- **Cross-platform compatibility** (Windows, Mac, Linux)

## 📱 Platform Support

| Platform | Status | Instructions |
|----------|--------|--------------|
| **Local Python** | ✅ Fully Supported | Install pygame and run main_game.py |
| **Replit** | ✅ Web Ready | Click play button, no installation needed |
| **GitHub Pages** | 🚧 In Development | Web version being optimized |
| **Windows** | ✅ Tested | Python 3.11+ recommended |
| **macOS** | ✅ Compatible | May need pygame installation |
| **Linux** | ✅ Compatible | Install pygame via package manager |

## 🐛 Troubleshooting

### Common Issues:

1. **"pygame not found"**
   ```bash
   pip install pygame Pillow
   ```

2. **Images not loading**
   - Ensure all image files are in the same directory as the Python scripts
   - Check that file paths use the correct case sensitivity

3. **Game runs too fast/slow**
   - The game targets 60 FPS but adapts to your system
   - Close other applications for better performance

4. **Web version not working**
   - Try the Replit version for guaranteed compatibility
   - Local installation provides the best experience

## 🤝 Contributing

This is an educational project created for the ACM community. Feel free to:
- Report bugs by creating GitHub issues
- Suggest improvements or new features
- Fork the repository for your own modifications
- Share with other ACM members and programming enthusiasts

## 📄 License

This project is open source and available under the MIT License. Created for educational purposes and ACM community engagement.

## 🎓 Educational Value

This game demonstrates:
- **Game development** with Python and Pygame
- **Event handling** and real-time user input
- **Collision detection** algorithms
- **State management** between game phases
- **Image processing** and manipulation
- **Algorithm implementation** (puzzle solving logic)
- **Web deployment** strategies for Python games

## 🔗 Links

- **GitHub Repository:** [https://github.com/RiyanBhargava/catch-game-acm](https://github.com/RiyanBhargava/catch-game-acm)
- **Play Online:** [https://replit.com/@RiyanBhargava/catch-game-acm](https://replit.com/@RiyanBhargava/catch-game-acm)
- **GitHub Pages:** [https://riyanbhargava.github.io/catch-game-acm](https://riyanbhargava.github.io/catch-game-acm)

---

🎮 **Good luck solving the ACM Challenge!** Can you discover the secret message?
