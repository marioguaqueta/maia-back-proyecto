# Docker Quick Start Guide

This guide shows you how to quickly get started with Docker locally or deploy to production.

## Local Development with Docker

### Prerequisites
- Docker installed ([Install Docker](https://docs.docker.com/get-docker/))
- Docker Compose installed ([Install Docker Compose](https://docs.docker.com/compose/install/))

### Quick Start (3 steps)

1. **Build the Docker image**:
   ```bash
   docker-compose build
   ```

2. **Start the container**:
   ```bash
   docker-compose up -d
   ```

3. **Test the API**:
   ```bash
   curl http://localhost:8000/health
   ```

That's it! Your API is now running at `http://localhost:8000`

### View Logs

```bash
docker-compose logs -f
```

### Stop the Container

```bash
docker-compose down
```

## Testing the API

### Health Check

```bash
curl http://localhost:8000/health
```

### Get Models Info

```bash
curl http://localhost:8000/models/info
```

### Analyze Images (HerdNet)

```bash
curl -X POST -F "file=@/path/to/your/images.zip" \
  -F "patch_size=512" \
  -F "overlap=160" \
  http://localhost:8000/analyze-image
```

### Analyze Images (YOLO)

```bash
curl -X POST -F "file=@/path/to/your/images.zip" \
  -F "conf_threshold=0.25" \
  -F "iou_threshold=0.45" \
  http://localhost:8000/analyze-yolo
```

## Docker Commands Cheat Sheet

### Container Management

```bash
# Start containers
docker-compose up -d

# Stop containers
docker-compose down

# Restart containers
docker-compose restart

# View running containers
docker-compose ps

# View logs
docker-compose logs -f

# View logs for specific service
docker-compose logs -f animal-detection-api

# Execute command in container
docker-compose exec animal-detection-api bash
```

### Image Management

```bash
# Build image
docker-compose build

# Build without cache
docker-compose build --no-cache

# Pull latest images
docker-compose pull

# List images
docker images

# Remove unused images
docker image prune -a
```

### Troubleshooting

```bash
# Check container status
docker-compose ps

# Check container health
docker inspect --format='{{.State.Health.Status}}' animal-detection-api

# View detailed logs
docker-compose logs --tail=100

# Access container shell
docker-compose exec animal-detection-api /bin/bash

# Check resource usage
docker stats
```

## Environment Variables

You can customize the container behavior using environment variables in `docker-compose.yml`:

```yaml
environment:
  - FLASK_APP=app.py
  - PYTHONUNBUFFERED=1
  - LOG_LEVEL=INFO
```

## Volume Mounts

The default `docker-compose.yml` includes volume mounts for persistent data:

```yaml
volumes:
  - ./uploads:/app/uploads
  - ./results:/app/results
```

This ensures your uploaded files and results persist even if the container is recreated.

## Production Deployment

For production deployment to AWS EC2, see:
- [DEPLOYMENT.md](DEPLOYMENT.md) - Comprehensive deployment guide
- [deploy-ec2.sh](deploy-ec2.sh) - Automated deployment script

## Common Issues

### Port Already in Use

```bash
# Find what's using port 8000
lsof -i :8000

# Use a different port
# Edit docker-compose.yml: "8001:8000"
```

### Container Keeps Restarting

```bash
# Check logs
docker-compose logs --tail=50

# Common causes:
# - Model files missing (best.pt, herdnet_model.pth)
# - Insufficient memory
# - Python dependency issues
```

### Out of Disk Space

```bash
# Clean up Docker
docker system prune -a --volumes

# Remove old images
docker image prune -a

# Remove old containers
docker container prune
```

## Performance Tips

1. **Allocate More Memory**: Edit Docker Desktop settings to allocate more RAM
2. **Use GPU**: For GPU support, use `nvidia-docker` and update `docker-compose.yml`
3. **Optimize Workers**: Adjust gunicorn workers in `Dockerfile` CMD

## Building for Production

For a production-optimized build:

```bash
# Build with specific tag
docker build -t animal-detection-api:v1.0 .

# Run with production settings
docker run -d \
  --name animal-detection-api \
  -p 8000:8000 \
  --restart unless-stopped \
  animal-detection-api:v1.0
```

## Multi-Stage Build (Optional)

For smaller images, consider using multi-stage builds. Create a new `Dockerfile.multistage`:

```dockerfile
# Builder stage
FROM python:3.11-slim as builder
WORKDIR /app
COPY requirements.txt .
RUN pip install --user --no-cache-dir -r requirements.txt

# Runtime stage
FROM python:3.11-slim
WORKDIR /app
COPY --from=builder /root/.local /root/.local
COPY . .
ENV PATH=/root/.local/bin:$PATH
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "app:app"]
```

## Docker Compose for Multiple Apps

To run multiple apps on the same machine:

```yaml
version: '3.8'

services:
  animal-detection-api:
    build: ./animal-detection-api
    ports:
      - "8000:8000"
    networks:
      - app-network

  other-app:
    build: ./other-app
    ports:
      - "8001:8001"
    networks:
      - app-network

  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf
    depends_on:
      - animal-detection-api
      - other-app
    networks:
      - app-network

networks:
  app-network:
    driver: bridge
```

## Next Steps

- Add database for storing results
- Implement caching (Redis)
- Add message queue (RabbitMQ/Celery) for async processing
- Set up monitoring (Prometheus + Grafana)
- Implement CI/CD with GitHub Actions

## Resources

- [Official Docker Documentation](https://docs.docker.com/)
- [Docker Compose Documentation](https://docs.docker.com/compose/)
- [Best Practices for Writing Dockerfiles](https://docs.docker.com/develop/develop-images/dockerfile_best-practices/)

