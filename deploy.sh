#!/bin/bash

# Ubuntu deployment script
echo "🚀 Deploying Airtable Server..."

# Update system
sudo apt update

# Install Docker if not present
if ! command -v docker &> /dev/null; then
    echo "Installing Docker..."
    sudo apt install -y docker.io docker-compose
    sudo systemctl start docker
    sudo systemctl enable docker
fi

# Clone repository
git clone https://github.com/haythemtimoumi/airtable-server.git
cd airtable-server

# Setup environment
cp .env.example .env
echo "⚠️  Edit .env with your Airtable credentials:"
echo "nano .env"
read -p "Press Enter after editing .env..."

# Build and run
docker-compose up -d

echo "✅ Server running on http://localhost:8000"
echo "🔍 Check logs: docker-compose logs -f"