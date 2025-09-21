#!/usr/bin/env python3

"""
Web build script for deploying Flappy Bird to Netlify
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path

def build_for_web():
    """Build the game for web deployment"""
    
    print("🚀 Building Flappy Bird for Web Deployment...")
    
    # Ensure we're in the right directory
    project_root = Path(__file__).parent
    os.chdir(project_root)
    
    # Clean previous builds
    dist_dir = project_root / "dist"
    if dist_dir.exists():
        print("🧹 Cleaning previous build...")
        shutil.rmtree(dist_dir)
    
    # Create deployment configuration
    print("⚙️ Configuring for web deployment...")
    
    # Build with pygbag
    build_command = [
        sys.executable, "-m", "pygbag",
        "--title", "Flappy Bird - Web Edition",
        "--template", "index.html",
        "--icon", "flappy.ico",
        "--cdn", "https://pygbag.github.io/",
        "main.py"
    ]
    
    print("🔨 Building with pygbag...")
    print(f"Command: {' '.join(build_command)}")
    
    try:
        result = subprocess.run(build_command, check=True, capture_output=True, text=True)
        print("✅ Build successful!")
        print(result.stdout)
        
        # Create netlify-ready structure
        netlify_dir = project_root / "netlify-deploy"
        if netlify_dir.exists():
            shutil.rmtree(netlify_dir)
        netlify_dir.mkdir()
        
        # Copy dist contents to netlify deploy folder
        if dist_dir.exists():
            shutil.copytree(dist_dir, netlify_dir / "dist")
        
        # Copy additional files for netlify
        files_to_copy = ["netlify.toml", "README.md", "LICENSE"]
        for file_name in files_to_copy:
            file_path = project_root / file_name
            if file_path.exists():
                shutil.copy2(file_path, netlify_dir)
        
        print(f"📦 Netlify deployment files ready in: {netlify_dir}")
        print("🌐 Ready to deploy to Netlify!")
        
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Build failed: {e}")
        print(f"Error output: {e.stderr}")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        return False

def show_deployment_instructions():
    """Show deployment instructions"""
    print("\n" + "="*60)
    print("📋 DEPLOYMENT INSTRUCTIONS")
    print("="*60)
    
    print("\n🔗 GITHUB DEPLOYMENT:")
    print("1. Initialize git repo: git init")
    print("2. Add files: git add .")
    print("3. Commit: git commit -m 'Initial Flappy Bird commit'")
    print("4. Create GitHub repo and add remote")
    print("5. Push: git push -u origin main")
    
    print("\n🌐 NETLIFY DEPLOYMENT:")
    print("1. Go to https://netlify.com")
    print("2. Connect your GitHub repository")
    print("3. Set build command: python build_web.py")
    print("4. Set publish directory: netlify-deploy/dist")
    print("5. Deploy!")
    
    print("\n🚀 MANUAL NETLIFY DEPLOYMENT:")
    print("1. Zip the 'netlify-deploy' folder")
    print("2. Go to https://app.netlify.com/drop")
    print("3. Drag and drop the zip file")
    print("4. Your game will be live!")

if __name__ == "__main__":
    success = build_for_web()
    show_deployment_instructions()
    
    if success:
        print("\n✅ Build completed successfully!")
        print("🎮 Your Flappy Bird is ready for deployment!")
    else:
        print("\n❌ Build failed. Please check the errors above.")
        sys.exit(1)