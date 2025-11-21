#!/bin/bash

###############################################################################
# AWS EC2 Deployment Script for Animal Detection API
# 
# This script automates the deployment of the Flask app on an EC2 instance
# Usage: ./deploy-ec2.sh [EC2_HOST] [SSH_KEY_PATH]
#
# Prerequisites:
# - EC2 instance running Ubuntu 22.04 or Amazon Linux 2
# - SSH access to the EC2 instance
# - Docker and Docker Compose installed on EC2 (or this script will install them)
###############################################################################

set -e  # Exit on error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check arguments
if [ "$#" -lt 2 ]; then
    echo -e "${RED}Usage: $0 <EC2_HOST> <SSH_KEY_PATH>${NC}"
    echo "Example: $0 ec2-user@ec2-xx-xxx-xxx-xxx.compute-1.amazonaws.com ~/.ssh/my-key.pem"
    exit 1
fi

EC2_HOST=$1
SSH_KEY=$2
APP_NAME="animal-detection-api"

echo -e "${GREEN}═══════════════════════════════════════════════════════${NC}"
echo -e "${GREEN}  AWS EC2 Deployment Script${NC}"
echo -e "${GREEN}═══════════════════════════════════════════════════════${NC}"
echo ""
echo "EC2 Host: $EC2_HOST"
echo "SSH Key: $SSH_KEY"
echo "App Name: $APP_NAME"
echo ""

# Test SSH connection
echo -e "${YELLOW}Testing SSH connection...${NC}"
ssh -i "$SSH_KEY" -o StrictHostKeyChecking=no "$EC2_HOST" "echo 'SSH connection successful'" || {
    echo -e "${RED}Failed to connect to EC2 instance${NC}"
    exit 1
}

# Install Docker and Docker Compose on EC2 if not already installed
echo -e "${YELLOW}Checking and installing Docker on EC2...${NC}"
ssh -i "$SSH_KEY" "$EC2_HOST" << 'ENDSSH'
set -e

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo "Installing Docker..."
    
    # Detect OS
    if [ -f /etc/os-release ]; then
        . /etc/os-release
        OS=$ID
    fi
    
    if [ "$OS" = "ubuntu" ] || [ "$OS" = "debian" ]; then
        # Ubuntu/Debian
        sudo apt-get update
        sudo apt-get install -y ca-certificates curl gnupg lsb-release
        sudo mkdir -p /etc/apt/keyrings
        curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg
        echo "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
        sudo apt-get update
        sudo apt-get install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin
    elif [ "$OS" = "amzn" ]; then
        # Amazon Linux
        sudo yum update -y
        sudo yum install -y docker
        sudo service docker start
        sudo systemctl enable docker
    else
        echo "Unsupported OS. Please install Docker manually."
        exit 1
    fi
    
    # Add current user to docker group
    sudo usermod -aG docker $USER
    echo "Docker installed successfully!"
else
    echo "Docker is already installed."
fi

# Install Docker Compose if not installed
if ! command -v docker-compose &> /dev/null && ! docker compose version &> /dev/null 2>&1; then
    echo "Installing Docker Compose..."
    sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
    sudo chmod +x /usr/local/bin/docker-compose
    echo "Docker Compose installed successfully!"
else
    echo "Docker Compose is already installed."
fi

# Install Nginx if not installed
if ! command -v nginx &> /dev/null; then
    echo "Installing Nginx..."
    if [ "$OS" = "ubuntu" ] || [ "$OS" = "debian" ]; then
        sudo apt-get install -y nginx
    elif [ "$OS" = "amzn" ]; then
        sudo yum install -y nginx
    fi
    sudo systemctl enable nginx
    echo "Nginx installed successfully!"
else
    echo "Nginx is already installed."
fi

# Create application directory
mkdir -p ~/apps/animal-detection-api
ENDSSH

echo -e "${GREEN}✓ Docker, Docker Compose, and Nginx are ready${NC}"

# Copy application files to EC2
echo -e "${YELLOW}Copying application files to EC2...${NC}"
rsync -avz -e "ssh -i $SSH_KEY" \
    --exclude 'general_dataset/' \
    --exclude '__pycache__/' \
    --exclude '*.pyc' \
    --exclude '.git/' \
    --exclude 'venv/' \
    --exclude '*.zip' \
    --exclude '*.log' \
    ./ "$EC2_HOST:~/apps/$APP_NAME/"

echo -e "${GREEN}✓ Files copied successfully${NC}"

# Build and run Docker container on EC2
echo -e "${YELLOW}Building and starting Docker container...${NC}"
ssh -i "$SSH_KEY" "$EC2_HOST" << ENDSSH
cd ~/apps/$APP_NAME

# Stop and remove existing containers
docker-compose down 2>/dev/null || true

# Build and start the container
docker-compose up -d --build

# Wait for the container to be healthy
echo "Waiting for container to be healthy..."
for i in {1..30}; do
    if docker-compose ps | grep -q "healthy"; then
        echo "Container is healthy!"
        break
    fi
    echo "Waiting... (\$i/30)"
    sleep 2
done

# Show container status
docker-compose ps

# Show logs
echo ""
echo "Recent logs:"
docker-compose logs --tail=20
ENDSSH

echo -e "${GREEN}✓ Container started successfully${NC}"

# Configure Nginx
echo -e "${YELLOW}Configuring Nginx...${NC}"
ssh -i "$SSH_KEY" "$EC2_HOST" << 'ENDSSH'
cd ~/apps/animal-detection-api

# Get EC2 public DNS
EC2_DNS=$(curl -s http://169.254.169.254/latest/meta-data/public-hostname || echo "your-ec2-domain.com")

# Replace placeholder in nginx.conf
sed "s|your-ec2-public-dns.compute.amazonaws.com|$EC2_DNS|g" nginx.conf | sudo tee /etc/nginx/sites-available/animal-detection-api > /dev/null

# Enable the site
sudo ln -sf /etc/nginx/sites-available/animal-detection-api /etc/nginx/sites-enabled/ 2>/dev/null || true

# Remove default site if exists
sudo rm -f /etc/nginx/sites-enabled/default

# Test Nginx configuration
sudo nginx -t

# Reload Nginx
sudo systemctl reload nginx

echo "Nginx configured successfully!"
ENDSSH

echo -e "${GREEN}✓ Nginx configured${NC}"

# Get EC2 public IP/DNS
echo -e "${YELLOW}Getting EC2 public URL...${NC}"
EC2_PUBLIC_DNS=$(ssh -i "$SSH_KEY" "$EC2_HOST" "curl -s http://169.254.169.254/latest/meta-data/public-hostname")

echo ""
echo -e "${GREEN}═══════════════════════════════════════════════════════${NC}"
echo -e "${GREEN}  Deployment Complete! 🎉${NC}"
echo -e "${GREEN}═══════════════════════════════════════════════════════${NC}"
echo ""
echo "Your API is now running at:"
echo "  http://$EC2_PUBLIC_DNS/api/animal-detection/health"
echo ""
echo "Available endpoints:"
echo "  - Health Check: http://$EC2_PUBLIC_DNS/api/animal-detection/health"
echo "  - Models Info:  http://$EC2_PUBLIC_DNS/api/animal-detection/models/info"
echo "  - Analyze (HerdNet): http://$EC2_PUBLIC_DNS/api/animal-detection/analyze-image"
echo "  - Analyze (YOLO): http://$EC2_PUBLIC_DNS/api/animal-detection/analyze-yolo"
echo ""
echo "To check logs:"
echo "  ssh -i $SSH_KEY $EC2_HOST 'cd ~/apps/$APP_NAME && docker-compose logs -f'"
echo ""
echo "To restart the service:"
echo "  ssh -i $SSH_KEY $EC2_HOST 'cd ~/apps/$APP_NAME && docker-compose restart'"
echo ""
echo "To stop the service:"
echo "  ssh -i $SSH_KEY $EC2_HOST 'cd ~/apps/$APP_NAME && docker-compose down'"
echo ""
echo -e "${YELLOW}Note: Make sure your EC2 Security Group allows inbound traffic on:${NC}"
echo "  - Port 80 (HTTP)"
echo "  - Port 443 (HTTPS, if using SSL)"
echo "  - Port 22 (SSH)"
echo ""
ENDSSH

chmod +x "/Users/marioguaqueta/Desktop/MAIA/2025-4/ProyectoFinal/back/deploy-ec2.sh"

