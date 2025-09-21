# 🎮 Flappy Bird - Dark Web Edition

A modern, dark-themed web version of the classic Flappy Bird game with enhanced features and optimizations for web deployment.

![Dark Theme Preview](screenshot1.png)

## ✨ Features

### 🌑 **Dark Theme UI**
- Modern dark interface optimized for web browsers
- Sleek gradients and smooth animations
- Eye-friendly color scheme
- Enhanced visual effects and glow

### 🎵 **Enhanced Audio**
- Death background music for dramatic effect
- WAV-only audio system for better web compatibility
- Improved sound management

### 🐦 **Bigger Blue Bird**
- Enhanced blue bird sprite (32% larger)
- Streamlined single-bird experience
- Optimized sprite assets

### 📹 **Smart Video System**
- Real video playback with OpenCV (desktop)
- Web-compatible fallback placeholders
- Automatic detection of environment capabilities

### 🌐 **Web Optimized**
- Built with pygbag for WebAssembly deployment
- Responsive design for all screen sizes
- Touch controls for mobile devices
- Fast loading and smooth performance

## 🚀 Quick Deploy

### Netlify (Recommended)
1. **Drag & Drop**: Build locally and drag `dist/` to [netlify.com/drop](https://netlify.com/drop)
2. **GitHub**: Connect your repo and auto-deploy on push
3. **CLI**: `netlify deploy --prod --dir=dist`

### Local Development
```bash
# Install dependencies
pip install -r requirements.txt

# Run locally
python main.py

# Build for web
./build.bat  # Windows
./build.sh   # Linux/Mac
```

## 🎮 Controls

| Input | Action |
|-------|--------|
| `SPACE` or `UP` | Flap wings |
| `ESC` | Quit game |
| `Click/Tap` | Flap wings (mobile) |

## 📁 Project Structure

```
FlapPyBird/
├── src/
│   ├── entities/          # Game objects
│   │   ├── dark_welcome_message.py    # Dark theme welcome
│   │   ├── dark_game_over.py          # Dark theme game over
│   │   └── video_player.py            # Web-compatible video
│   └── utils/
│       └── dark_theme.py              # Dark theme system
├── assets/                # Game assets
├── index.html            # Web template
├── netlify.toml          # Netlify config
├── requirements.txt      # Python deps
├── build.bat/.sh         # Build scripts
└── DEPLOYMENT.md         # Full deployment guide
```

## 🔧 Configuration

### Environment Detection
The game automatically detects web vs desktop environment:
- **Web Mode**: Dark theme UI, web-compatible video placeholders
- **Desktop Mode**: Standard UI with full video support

### Customization
- **Colors**: Edit `src/utils/dark_theme.py`
- **UI Layout**: Modify `src/entities/dark_*.py` files
- **Web Template**: Update `index.html`

## 🐛 Troubleshooting

### Common Issues

**Build fails:**
```bash
pip install pygbag==0.7.1
```

**Audio not working:**
- Web browsers require user interaction before audio
- Click/tap the game area first

**Mobile controls:**
- Use tap/touch instead of keyboard
- Game automatically adapts to mobile

**Performance:**
- Ensure hosting service supports WebAssembly
- Enable HTTPS for all features

## 📊 Performance

### Optimizations
- **Asset Compression**: Sprites optimized to <2KB each
- **WebAssembly**: Native-speed execution in browsers
- **CDN**: Fast global asset delivery
- **Responsive**: Adapts to any screen size

### Browser Compatibility
- ✅ Chrome 88+
- ✅ Firefox 84+
- ✅ Safari 14+
- ✅ Edge 88+
- ✅ Mobile browsers

## 🎯 Deployment Targets

### Supported Platforms
- **Netlify** ⭐ (Recommended)
- **Koyeb** (Docker)
- **Vercel**
- **GitHub Pages**
- **Any static host with WASM support**

### Production URLs
- **Demo**: [Your deployed URL here]
- **Source**: [GitHub repository URL]

## 🛠️ Development

### Local Setup
```bash
git clone <repository>
cd FlapPyBird
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
.venv\Scripts\activate     # Windows
pip install -r requirements.txt
python main.py
```

### Adding Features
1. **New UI Elements**: Extend `DarkTheme` class
2. **Game Mechanics**: Modify entity classes
3. **Web Features**: Update `index.html` template
4. **Build Process**: Edit build scripts

## 📈 Analytics & Monitoring

Ready for integration with:
- Google Analytics
- Hotjar/FullStory
- Performance monitoring
- Error tracking

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Add your enhancements
4. Test web deployment
5. Submit a pull request

## 📝 License

Based on the original Flappy Bird implementation with modern enhancements.

## 🎉 Deploy Your Own

Ready to deploy? Follow the [DEPLOYMENT.md](DEPLOYMENT.md) guide for detailed instructions!

---

**Built with ❤️ using Pygame, Pygbag, and modern web technologies**