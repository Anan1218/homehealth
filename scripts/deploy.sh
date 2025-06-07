#!/bin/bash

# HomeHealth Production Deployment Script

set -e

echo "🚀 Starting HomeHealth deployment..."

# Check if git is clean
if [ -n "$(git status --porcelain)" ]; then
    echo "❌ Git working directory is not clean. Please commit your changes first."
    exit 1
fi

# Build and test locally first
echo "🔧 Building frontend..."
cd frontend
npm install
npm run build
cd ..

echo "🔧 Testing backend..."
cd backend
pip install -r requirements.txt
python -m pytest
cd ..

echo "✅ Local build and tests passed!"

# Deploy based on platform choice
echo "Choose deployment platform:"
echo "1) Render (both frontend & backend)"
echo "2) Vercel (frontend) + Render (backend)"
echo "3) Manual Docker deployment"

read -p "Enter choice (1-3): " choice

case $choice in
    1)
        echo "🚀 Deploying to Render..."
        echo "Push your code to GitHub and connect your repo to Render"
        echo "Use the render.yaml file for configuration"
        git push origin main
        ;;
    2)
        echo "🚀 Deploying Frontend to Vercel..."
        npx vercel --prod
        echo "🚀 Deploy Backend to Render manually using Dockerfile.prod"
        ;;
    3)
        echo "🐳 Building production Docker images..."
        docker build -f backend/Dockerfile.prod -t homehealth-api ./backend
        echo "Backend image built as 'homehealth-api'"
        echo "Frontend static files are in frontend/dist/"
        ;;
    *)
        echo "❌ Invalid choice"
        exit 1
        ;;
esac

echo "✅ Deployment process completed!" 