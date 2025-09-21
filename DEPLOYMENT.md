# 🚀 Deployment Guide - Flappy Bird Dark Edition

This guide will help you deploy your enhanced Flappy Bird game to web hosting platforms like Netlify or Koyeb.

## 📋 Prerequisites

- Python 3.11+ installed
- Git (for version control)
- A Netlify or Koyeb account

## 🔧 Local Build Setup

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Build for Web
Run the build script for your platform:

**Windows:**
```bash
./build.bat
```

**Linux/Mac:**
```bash
chmod +x build.sh
./build.sh
```

**Manual Build:**
```bash
python -m pygbag --width 288 --height 512 --name "flappy-bird-dark" --title "Flappy Bird - Dark Web Edition" --template index.html --icon flappy.ico --optimize main.py
```

## 🌐 Deployment Options

### Option 1: Netlify (Recommended)

#### Quick Deploy (Drag & Drop)
1. Build the project locally (see above)
2. Go to [netlify.com/drop](https://netlify.com/drop)
3. Drag and drop the `dist/` folder
4. Your game is live! 🎉

#### GitHub Integration (Automatic)
1. Push your code to GitHub
2. Connect your GitHub repo to Netlify
3. Set build command: `python -m pygbag --width 288 --height 512 --name "flappy-bird-dark" --title "Flappy Bird - Dark Web Edition" --template index.html --icon flappy.ico --optimize main.py`
4. Set publish directory: `dist`
5. Deploy automatically on each push

#### Using Netlify CLI
```bash
npm install -g netlify-cli
netlify login
netlify deploy --prod --dir=dist
```

### Option 2: Koyeb

#### Docker Deployment
1. Create a `Dockerfile`:
```dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY . .

RUN pip install -r requirements.txt
RUN python -m pygbag --width 288 --height 512 --name "flappy-bird-dark" --title "Flappy Bird - Dark Web Edition" --template index.html --icon flappy.ico --optimize main.py

EXPOSE 8000
CMD ["python", "-m", "http.server", "8000", "--directory", "dist"]
```

2. Deploy to Koyeb:
   - Connect your GitHub repository
   - Set build type to Docker
   - Configure port 8000
   - Deploy

### Option 3: Vercel
```bash
npm install -g vercel
vercel --prod
```

### Option 4: GitHub Pages
1. Enable GitHub Pages in repository settings
2. Use GitHub Actions workflow (included in `.github/workflows/deploy.yml`)
3. Set secrets: `NETLIFY_AUTH_TOKEN` and `NETLIFY_SITE_ID` (if using Netlify integration)

## 🎮 Game Features

Your deployed game includes:

- **🌑 Dark Theme UI**: Modern dark interface optimized for web
- **🎵 Death BGM**: Background music on game over
- **🐦 Enhanced Bird**: 32% larger blue bird sprite
- **📹 Video Support**: Real video playback with OpenCV
- **📱 Mobile Friendly**: Touch controls and responsive design
- **⚡ Web Optimized**: Fast loading with WebAssembly

## 🔧 Configuration

### Environment Variables
- `PYTHON_VERSION`: Python version for build (default: 3.11)
- `PYGBAG_OPTIONS`: Additional pygbag build options

### Customization
- Modify `index.html` for UI changes
- Update `src/utils/dark_theme.py` for color schemes
- Edit `assets/` for game sprites and sounds

## 🐛 Troubleshooting

### Common Issues

**Build fails with "pygbag not found":**
```bash
pip install pygbag==0.7.1
```

**WebAssembly not loading:**
- Ensure your hosting service supports WASM
- Check CORS headers (included in `netlify.toml`)
- Verify HTTPS is enabled

**Game assets not loading:**
- Ensure all files in `assets/` are included
- Check file paths are relative
- Verify no spaces in filenames

**Audio not playing:**
- Web browsers require user interaction before audio
- Click/tap the game area first
- Check browser audio permissions

### Performance Tips

1. **Optimize Assets**: Use the included `resize_sprites.py` to optimize image sizes
2. **Enable Compression**: Most hosting services automatically compress files
3. **CDN**: Use a CDN for faster global loading (already configured)

## 📊 Analytics & Monitoring

### Add Analytics (Optional)
Add to `index.html` before `</head>`:
```html
<!-- Google Analytics -->
<script async src="https://www.googletagmanager.com/gtag/js?id=GA_MEASUREMENT_ID"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());
  gtag('config', 'GA_MEASUREMENT_ID');
</script>
```

### Performance Monitoring
- Use Lighthouse for performance audits
- Monitor Core Web Vitals
- Check loading times across different devices

## 🚀 Going Live

### Final Checklist
- [ ] Game builds successfully
- [ ] All assets load correctly
- [ ] Touch controls work on mobile
- [ ] Audio plays after user interaction
- [ ] Game is responsive on different screen sizes
- [ ] HTTPS is enabled
- [ ] Custom domain configured (optional)

### Custom Domain Setup
1. Purchase a domain (e.g., `flappybird-dark.com`)
2. Configure DNS to point to your hosting service
3. Enable HTTPS/SSL certificate
4. Update any hardcoded URLs

## 🎉 Success!

Your Flappy Bird Dark Edition is now live and ready for players worldwide!

Share your game:
- Social media links
- QR codes for mobile access
- Embed in other websites
- Submit to game directories

---

Need help? Check the troubleshooting section or create an issue in the repository.