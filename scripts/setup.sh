#!/bin/bash

echo "🏠 Setting up HomeHealth Monorepo..."

# Check if .env exists
if [ ! -f .env ]; then
    echo "📝 Creating .env file from template..."
    cp env.example .env
    echo "⚠️  Please update .env with your Supabase credentials"
fi

# Install backend dependencies
echo "🐍 Setting up Python backend..."
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
cd ..

# Install frontend dependencies
echo "⚛️  Setting up React frontend..."
cd frontend
npm install
cd ..

echo "✅ Setup complete!"
echo ""
echo "Next steps:"
echo "1. Update .env with your Supabase credentials"
echo "2. Run 'docker-compose up' for development"
echo "3. Or run services individually:"
echo "   - Backend: cd backend && source venv/bin/activate && uvicorn app.main:app --reload"
echo "   - Frontend: cd frontend && npm run dev" 