#!/bin/bash
# Build script for Flappy Bird web deployment

echo "🚀 Building Flappy Bird for Web Deployment"
echo "=========================================="

# Check if pygbag is installed
if ! python -c "import pygbag" 2>/dev/null; then
    echo "❌ Pygbag not found. Installing..."
    pip install pygbag==0.7.1
fi

# Clean previous builds
echo "🧹 Cleaning previous builds..."
rm -rf dist/
rm -rf build/
rm -rf *.egg-info/

# Create dist directory
mkdir -p dist

# Build with pygbag
echo "🔨 Building with pygbag..."
python -m pygbag \
    --width 288 \
    --height 512 \
    --name "flappy-bird-dark" \
    --title "Flappy Bird - Dark Web Edition" \
    --template index.html \
    --icon flappy.ico \
    --optimize \
    --cdn "https://cdn.jsdelivr.net/pyodide/" \
    main.py

if [ $? -eq 0 ]; then
    echo "✅ Build completed successfully!"
    echo "📁 Output directory: dist/"
    echo "🌐 Ready for deployment to Netlify or Koyeb"
else
    echo "❌ Build failed!"
    exit 1
fi

echo ""
echo "📋 Deployment Instructions:"
echo "1. Upload the contents of dist/ to your web hosting service"
echo "2. For Netlify: Drag and drop the dist folder to netlify.com/drop"
echo "3. For Koyeb: Use the GitHub integration or Docker deployment"
echo "4. Ensure your hosting service supports WebAssembly (WASM)"