@echo off
REM Build script for Flappy Bird web deployment (Windows)

echo 🚀 Building Flappy Bird for Web Deployment
echo ==========================================

REM Check if pygbag is installed
python -c "import pygbag" 2>nul
if %errorlevel% neq 0 (
    echo ❌ Pygbag not found. Installing...
    pip install pygbag==0.7.1
)

REM Clean previous builds
echo 🧹 Cleaning previous builds...
if exist dist rmdir /s /q dist
if exist build rmdir /s /q build
for /d %%i in (*.egg-info) do rmdir /s /q "%%i"

REM Create dist directory
mkdir dist

REM Build with pygbag
echo 🔨 Building with pygbag...
python -m pygbag --width 288 --height 512 --name "flappy-bird-dark" --title "Flappy Bird - Dark Web Edition" --template index.html --icon flappy.ico --optimize --cdn "https://cdn.jsdelivr.net/pyodide/" main.py

if %errorlevel% equ 0 (
    echo ✅ Build completed successfully!
    echo 📁 Output directory: dist/
    echo 🌐 Ready for deployment to Netlify or Koyeb
) else (
    echo ❌ Build failed!
    exit /b 1
)

echo.
echo 📋 Deployment Instructions:
echo 1. Upload the contents of dist/ to your web hosting service
echo 2. For Netlify: Drag and drop the dist folder to netlify.com/drop
echo 3. For Koyeb: Use the GitHub integration or Docker deployment
echo 4. Ensure your hosting service supports WebAssembly (WASM)

pause