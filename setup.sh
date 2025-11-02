#!/usr/bin/env bash

# Fintech AI News Platform - Setup Script
# This script helps you get started quickly

set -e

echo "🚀 Fintech AI News Platform - Setup"
echo "===================================="
echo ""

# Check Node.js
if ! command -v node &> /dev/null; then
    echo "❌ Node.js is not installed. Please install Node.js 18+ first."
    echo "   Visit: https://nodejs.org/"
    exit 1
fi

NODE_VERSION=$(node -v | cut -d'v' -f2 | cut -d'.' -f1)
if [ "$NODE_VERSION" -lt 18 ]; then
    echo "❌ Node.js version must be 18 or higher. Current version: $(node -v)"
    exit 1
fi

echo "✅ Node.js $(node -v) detected"
echo ""

# Install frontend dependencies
echo "📦 Installing frontend dependencies..."
npm install

# Install mock backend dependencies
echo "📦 Installing mock backend dependencies..."
cd mock-backend
npm install
cd ..

echo ""
echo "✅ Setup complete!"
echo ""
echo "📋 Next steps:"
echo "   1. Open Terminal 1: cd mock-backend && node server.js"
echo "   2. Open Terminal 2: npm run dev"
echo "   3. Open browser: http://localhost:5173"
echo ""
echo "📖 For more details, read QUICKSTART.md"
echo ""

