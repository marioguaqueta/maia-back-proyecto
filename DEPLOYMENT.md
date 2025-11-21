# AWS EC2 Deployment Guide

This guide will walk you through deploying the Animal Detection API to an AWS EC2 instance using Docker containers.

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [AWS EC2 Setup](#aws-ec2-setup)
3. [Manual Deployment](#manual-deployment)
4. [Automated Deployment (Script)](#automated-deployment-script)
5. [GitHub Actions CI/CD](#github-actions-cicd)
6. [Running Multiple Apps on Same EC2](#running-multiple-apps-on-same-ec2)
7. [SSL/HTTPS Setup](#sslhttps-setup)
8. [Monitoring and Maintenance](#monitoring-and-maintenance)
9. [Troubleshooting](#troubleshooting)

---

## Prerequisites

### Local Machine
- Git
- SSH client
- AWS CLI (optional, but recommended)

### AWS Account
- Active AWS account
- EC2 instance (recommended: t3.large or better for ML models)
- SSH key pair for EC2 access
- Security groups configured

---

## AWS EC2 Setup

### 1. Launch EC2 Instance

1. Go to AWS Console → EC2 → Launch Instance
2. **Choose AMI**: Ubuntu 22.04 LTS or Amazon Linux 2023
3. **Instance Type**: 
   - Minimum: `t3.large` (2 vCPU, 8 GB RAM)
   - Recommended: `t3.xlarge` (4 vCPU, 16 GB RAM) or better
   - For GPU support: `g4dn.xlarge` or similar
4. **Storage**: At least 30 GB (50 GB+ recommended)
5. **Key Pair**: Create or select an existing key pair (download and save the `.pem` file)

### 2. Configure Security Group

Create/edit security group with the following inbound rules:

| Type  | Protocol | Port Range | Source    | Description         |
|-------|----------|------------|-----------|---------------------|
| SSH   | TCP      | 22         | My IP     | SSH access          |
| HTTP  | TCP      | 80         | 0.0.0.0/0 | HTTP access         |
| HTTPS | TCP      | 443        | 0.0.0.0/0 | HTTPS access (SSL)  |
| Custom| TCP      | 8000       | My IP     | Direct API access   |

### 3. Connect to Your EC2 Instance

```bash
# Change key permissions
chmod 400 /path/to/your-key.pem

# Connect via SSH
ssh -i /path/to/your-key.pem ubuntu@<EC2-PUBLIC-IP>
# or for Amazon Linux
ssh -i /path/to/your-key.pem ec2-user@<EC2-PUBLIC-IP>
```

---

## Manual Deployment

### Step 1: Install Docker on EC2

```bash
# For Ubuntu
sudo apt-get update
sudo apt-get install -y ca-certificates curl gnupg lsb-release

# Add Docker's official GPG key
sudo mkdir -p /etc/apt/keyrings
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg

# Set up repository
echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu \
  $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

# Install Docker
sudo apt-get update
sudo apt-get install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin

# Add user to docker group
sudo usermod -aG docker $USER

# For Amazon Linux
sudo yum update -y
sudo yum install -y docker
sudo service docker start
sudo systemctl enable docker
sudo usermod -aG docker $USER
```

### Step 2: Install Docker Compose

```bash
# Download Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose

# Make it executable
sudo chmod +x /usr/local/bin/docker-compose

# Verify installation
docker-compose --version
```

### Step 3: Install Nginx

```bash
# For Ubuntu
sudo apt-get install -y nginx
sudo systemctl enable nginx
sudo systemctl start nginx

# For Amazon Linux
sudo yum install -y nginx
sudo systemctl enable nginx
sudo systemctl start nginx
```

### Step 4: Clone Repository and Deploy

```bash
# Create app directory
mkdir -p ~/apps
cd ~/apps

# Clone your repository
git clone https://github.com/your-username/your-repo.git animal-detection-api
cd animal-detection-api

# Build and start the container
docker-compose up -d --build

# Check container status
docker-compose ps

# View logs
docker-compose logs -f
```

### Step 5: Configure Nginx

```bash
# Copy nginx configuration
sudo cp nginx.conf /etc/nginx/sites-available/animal-detection-api

# Create symlink
sudo ln -s /etc/nginx/sites-available/animal-detection-api /etc/nginx/sites-enabled/

# Remove default site
sudo rm -f /etc/nginx/sites-enabled/default

# Update server_name in config with your EC2 public DNS
EC2_DNS=$(curl -s http://169.254.169.254/latest/meta-data/public-hostname)
sudo sed -i "s|your-ec2-public-dns.compute.amazonaws.com|$EC2_DNS|g" /etc/nginx/sites-available/animal-detection-api

# Test nginx configuration
sudo nginx -t

# Reload nginx
sudo systemctl reload nginx
```

### Step 6: Test the Deployment

```bash
# Test health endpoint
curl http://localhost:8000/health

# Test via nginx
curl http://<EC2-PUBLIC-IP>/api/animal-detection/health
```

---

## Automated Deployment (Script)

Use the provided `deploy-ec2.sh` script for automated deployment:

```bash
# Make script executable
chmod +x deploy-ec2.sh

# Run deployment
./deploy-ec2.sh ec2-user@<EC2-PUBLIC-IP> /path/to/your-key.pem
```

The script will:
1. Check SSH connection
2. Install Docker, Docker Compose, and Nginx (if not present)
3. Copy application files
4. Build and start Docker containers
5. Configure Nginx
6. Verify deployment

---

## GitHub Actions CI/CD

### Setup

1. **Add GitHub Secrets**:
   - Go to your repository → Settings → Secrets and variables → Actions
   - Add the following secrets:
     - `EC2_SSH_KEY`: Content of your `.pem` file
     - `EC2_HOST`: Your EC2 public IP or DNS
     - `EC2_USER`: SSH user (ubuntu or ec2-user)

2. **Push to Main Branch**:
   ```bash
   git add .
   git commit -m "Add deployment configuration"
   git push origin main
   ```

3. **Monitor Deployment**:
   - Go to Actions tab in your GitHub repository
   - Watch the deployment progress

### Manual Trigger

You can also manually trigger the deployment:
- Go to Actions → Deploy to AWS EC2 → Run workflow

---

## Running Multiple Apps on Same EC2

To run multiple applications on the same EC2 instance:

### 1. Deploy Second App with Different Port

Create a new docker-compose file for your second app with a different port:

```yaml
# docker-compose-app2.yml
version: '3.8'

services:
  app2:
    build:
      context: .
      dockerfile: Dockerfile
    container_name: app2
    restart: unless-stopped
    ports:
      - "8001:8001"  # Different port
    environment:
      - FLASK_APP=app.py
    networks:
      - app-network

networks:
  app-network:
    driver: bridge
```

### 2. Update Nginx Configuration

Edit `/etc/nginx/sites-available/animal-detection-api`:

```nginx
# Add upstream for second app
upstream app2_backend {
    server localhost:8001;
}

# Add location block
location /api/app2/ {
    proxy_pass http://app2_backend/;
    proxy_http_version 1.1;
    proxy_set_header Upgrade $http_upgrade;
    proxy_set_header Connection 'upgrade';
    proxy_set_header Host $host;
    proxy_cache_bypass $http_upgrade;
}
```

### 3. Start Second App

```bash
docker-compose -f docker-compose-app2.yml up -d --build
```

Now both apps will be accessible:
- App 1: `http://<EC2-IP>/api/animal-detection/`
- App 2: `http://<EC2-IP>/api/app2/`

---

## SSL/HTTPS Setup

### Using Let's Encrypt (Certbot)

```bash
# Install Certbot
sudo apt-get install -y certbot python3-certbot-nginx

# Get SSL certificate (replace with your domain)
sudo certbot --nginx -d your-domain.com -d www.your-domain.com

# Certbot will automatically configure nginx
# Test renewal
sudo certbot renew --dry-run
```

### Manual SSL Configuration

1. Obtain SSL certificates
2. Update nginx configuration:

```nginx
server {
    listen 443 ssl http2;
    server_name your-domain.com;
    
    ssl_certificate /path/to/fullchain.pem;
    ssl_certificate_key /path/to/privkey.pem;
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers HIGH:!aNULL:!MD5;
    
    # ... rest of configuration
}

# Redirect HTTP to HTTPS
server {
    listen 80;
    server_name your-domain.com;
    return 301 https://$server_name$request_uri;
}
```

---

## Monitoring and Maintenance

### View Logs

```bash
# View container logs
docker-compose logs -f

# View specific container
docker-compose logs -f animal-detection-api

# View nginx logs
sudo tail -f /var/log/nginx/access.log
sudo tail -f /var/log/nginx/error.log
```

### Container Management

```bash
# Check status
docker-compose ps

# Restart containers
docker-compose restart

# Stop containers
docker-compose down

# Update and restart
git pull origin main
docker-compose up -d --build

# Remove unused images
docker image prune -a
```

### System Monitoring

```bash
# Check disk usage
df -h

# Check memory usage
free -h

# Check CPU usage
top

# Check Docker stats
docker stats
```

### Backups

```bash
# Backup important data
tar -czf backup-$(date +%Y%m%d).tar.gz \
    ~/apps/animal-detection-api/results \
    ~/apps/animal-detection-api/uploads

# Copy to S3 (if configured)
aws s3 cp backup-$(date +%Y%m%d).tar.gz s3://your-bucket/backups/
```

---

## Troubleshooting

### Container Won't Start

```bash
# Check logs
docker-compose logs

# Check Docker daemon
sudo systemctl status docker

# Restart Docker
sudo systemctl restart docker
```

### Out of Memory

```bash
# Check memory
free -h

# Clear cache
sudo sync; echo 3 | sudo tee /proc/sys/vm/drop_caches

# Consider upgrading EC2 instance type
```

### Nginx Issues

```bash
# Test configuration
sudo nginx -t

# Check nginx status
sudo systemctl status nginx

# Restart nginx
sudo systemctl restart nginx

# Check nginx logs
sudo tail -f /var/log/nginx/error.log
```

### Port Already in Use

```bash
# Find process using port
sudo lsof -i :8000

# Kill process
sudo kill -9 <PID>
```

### Can't Connect from Outside

1. Check EC2 Security Group rules
2. Check that nginx is running: `sudo systemctl status nginx`
3. Check that container is running: `docker-compose ps`
4. Test locally first: `curl http://localhost:8000/health`

### Model Loading Issues

```bash
# Check if model files exist
ls -lh best.pt herdnet_model.pth

# Check container logs for errors
docker-compose logs | grep -i error

# Verify Python dependencies
docker-compose exec animal-detection-api pip list
```

---

## API Endpoints

After deployment, your API will be available at:

- **Health Check**: `http://<EC2-IP>/api/animal-detection/health`
- **Models Info**: `http://<EC2-IP>/api/animal-detection/models/info`
- **HerdNet Analysis**: `http://<EC2-IP>/api/animal-detection/analyze-image`
- **YOLO Analysis**: `http://<EC2-IP>/api/animal-detection/analyze-yolo`

---

## Cost Optimization

### 1. Use Spot Instances

For development/testing, use EC2 Spot Instances to reduce costs by up to 90%.

### 2. Stop Instance When Not in Use

```bash
# From AWS CLI
aws ec2 stop-instances --instance-ids i-1234567890abcdef0
```

### 3. Use Auto Scaling (Production)

Set up auto-scaling groups to scale based on demand.

### 4. Monitor Costs

- Enable AWS Cost Explorer
- Set up billing alerts
- Use AWS Budgets

---

## Security Best Practices

1. **Keep Software Updated**
   ```bash
   sudo apt-get update && sudo apt-get upgrade -y
   ```

2. **Use SSH Keys Only** (disable password authentication)
   ```bash
   sudo nano /etc/ssh/sshd_config
   # Set: PasswordAuthentication no
   sudo systemctl restart sshd
   ```

3. **Configure Firewall**
   ```bash
   sudo ufw enable
   sudo ufw allow 22
   sudo ufw allow 80
   sudo ufw allow 443
   ```

4. **Regular Backups**

5. **Use SSL/HTTPS in Production**

6. **Implement Rate Limiting** (in Nginx)

7. **Monitor Logs** for suspicious activity

---

## Next Steps

- [ ] Set up CloudWatch for monitoring
- [ ] Configure automatic backups to S3
- [ ] Set up CloudFront CDN for better performance
- [ ] Implement API authentication (JWT, API keys)
- [ ] Set up database for storing results
- [ ] Configure auto-scaling

---

## Support

For issues or questions:
1. Check the troubleshooting section
2. Review container logs
3. Check AWS EC2 console for instance health
4. Review GitHub Actions logs for CI/CD issues

---

## Additional Resources

- [Docker Documentation](https://docs.docker.com/)
- [AWS EC2 Documentation](https://docs.aws.amazon.com/ec2/)
- [Nginx Documentation](https://nginx.org/en/docs/)
- [Flask Documentation](https://flask.palletsprojects.com/)
- [GitHub Actions Documentation](https://docs.github.com/en/actions)

