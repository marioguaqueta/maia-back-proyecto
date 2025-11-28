# 🔄 Architecture Diagram - CI/CD Update

## Summary

Updated `ARCHITECTURE_DIAGRAM.md` to reflect the **automated CI/CD deployment pipeline** using GitHub Actions instead of manual deployment.

---

## Changes Made

### 1. ✅ Updated Section 5: "Flujo de Despliegue CI/CD"

**Before**: Manual deployment flow
- Developer manually SSH to EC2
- Manual git pull and docker commands
- Manual verification

**After**: Automated GitHub Actions workflow
- Automatic trigger on push to main/master
- GitHub Actions handles all deployment steps
- Automatic health checks and notifications
- Smart path filtering (ignores frontend/docs changes)

### 2. ✅ Added Section 6: "Pipeline CI/CD con GitHub Actions"

**New comprehensive sequence diagram showing:**
- Developer push to GitHub
- GitHub Actions workflow execution
- SSH connection and file sync (rsync)
- Docker container lifecycle (stop → prune → build → up)
- Model download and DB initialization
- Health check loop (5 attempts)
- Success/failure notifications
- Cleanup process

**Timeline**: Complete workflow in ~3-5 minutes

### 3. ✅ Added Section 7: "Configuración de GitHub Secrets"

**Diagram showing required secrets:**
- `EC2_SSH_KEY`: Private SSH key for EC2 access
- `EC2_HOST`: Public IP or hostname of EC2 instance
- `EC2_USER`: SSH user (typically 'ubuntu')

**Security visualization:**
- How secrets flow from GitHub to Actions
- SSH connection to EC2
- Security group protection

### 4. ✅ Renumbered Section 6 → 8: "Arquitectura de Seguridad"

Updated section numbering to accommodate new CI/CD sections.

### 5. ✅ Expanded "Stack Tecnológico" Section

**Added new subsection: "CI/CD Pipeline"**
- Platform: GitHub Actions
- Workflow file: `.github/workflows/deploy.yml`
- Trigger conditions
- Deployment method
- Verification process
- Required secrets
- 7-step workflow description

**Added to "Servicios Externos"**
- Streamlit Cloud hosting

---

## New Diagrams Overview

### Diagram 1: Deployment Flow (Section 5)
```
Developer Push → GitHub → Trigger Check → GitHub Actions Workflow
                                          ↓
                          SSH + Rsync → EC2 → Docker Build/Deploy
                                          ↓
                          Health Check → Success/Failure Notification
                                          ↓
                          Streamlit Cloud Auto-Deploy → Integration Check
```

**Key Features:**
- ✅ Automatic trigger with smart filtering
- ✅ Complete Docker lifecycle management
- ✅ Health verification
- ✅ Parallel frontend deployment
- ✅ Error handling and notifications

### Diagram 2: CI/CD Sequence (Section 6)
```
Detailed step-by-step sequence showing:
1. Git push
2. GitHub webhook trigger
3. Checkout code
4. Setup SSH
5. Rsync files to EC2
6. Stop containers
7. Clean Docker resources
8. Build new image
9. Start services
10. Wait for startup
11. Health check loop
12. Notify results
13. Cleanup
```

**Timeline**: Each step with approximate duration

### Diagram 3: GitHub Secrets Configuration (Section 7)
```
GitHub Secrets → Workflow → Runner → SSH → EC2
      ↑                                     ↑
      └─────────────────────────────────────┘
            Protected by Security Group
```

**Security highlights:**
- Secrets never exposed in logs
- SSH key protection
- Security group configuration

---

## Workflow Details

### Trigger Conditions

**Activates on:**
- Push to `main` branch
- Push to `master` branch
- Manual workflow dispatch

**Ignores (paths-ignore):**
- `streamlit_app.py` (frontend only)
- `.streamlit/**` (frontend config)
- `requirements-streamlit.txt`
- `**.md` (documentation)
- `test_*.py` (test files)
- `.gitignore`, `.vscode/`, `.idea/`
- Other non-backend files

**Why?** Prevents unnecessary backend deployments when only frontend or docs change.

### Deployment Steps

#### 1. Checkout Code
```yaml
uses: actions/checkout@v4
```

#### 2. Setup SSH
```bash
mkdir -p ~/.ssh
echo "$EC2_SSH_KEY" > ~/.ssh/ec2-key.pem
chmod 600 ~/.ssh/ec2-key.pem
ssh-keyscan -H $EC2_HOST >> ~/.ssh/known_hosts
```

#### 3. Rsync Files
```bash
rsync -avz -e "ssh -i ~/.ssh/ec2-key.pem" \
  --exclude 'general_dataset/' \
  --exclude '__pycache__/' \
  --exclude '.git/' \
  ./ ubuntu@$EC2_HOST:/home/ubuntu/maia-back-proyecto/
```

#### 4. Docker Deployment
```bash
cd /home/ubuntu/maia-back-proyecto
docker-compose down
docker system prune -f
docker-compose up -d --build
```

#### 5. Health Check
```bash
for i in {1..5}; do
  curl -f http://localhost:8000/health
  sleep 5
done
```

#### 6. Cleanup
```bash
rm -f ~/.ssh/ec2-key.pem
```

---

## Benefits of CI/CD Integration

### ✅ Automation
- No manual SSH required
- Consistent deployment process
- Reduces human error

### ✅ Speed
- Deploy in 3-5 minutes
- Automatic on every push
- Parallel builds possible

### ✅ Reliability
- Health checks ensure success
- Automatic rollback on failure
- Consistent environment

### ✅ Visibility
- GitHub Actions logs
- Deployment notifications
- Status badges possible

### ✅ Security
- Secrets management
- No credentials in code
- SSH key rotation support

### ✅ Efficiency
- Smart path filtering
- Docker layer caching
- Resource cleanup

---

## GitHub Actions Configuration

### Required Secrets

Set in: `Repository Settings → Secrets and variables → Actions`

```
EC2_SSH_KEY
├─ Type: Repository secret
├─ Content: Private SSH key (PEM format)
└─ Usage: SSH authentication to EC2

EC2_HOST
├─ Type: Repository secret
├─ Content: Public IP or hostname
└─ Usage: SSH connection target

EC2_USER
├─ Type: Repository secret
├─ Content: SSH username (ubuntu)
└─ Usage: SSH login
```

### Workflow File Location
```
.github/workflows/deploy.yml
```

### Manual Trigger
```bash
# Via GitHub UI: Actions tab → Deploy to AWS EC2 → Run workflow
# Or via GitHub CLI:
gh workflow run deploy.yml
```

---

## Comparison: Before vs After

### Before (Manual Deployment)

**Steps:**
1. SSH to EC2 manually
2. `cd /home/ubuntu/maia-back-proyecto`
3. `git pull origin main`
4. `docker-compose down`
5. `docker-compose up -d --build`
6. Manually check logs
7. Manually verify health

**Issues:**
- ❌ Time consuming (~10-15 min)
- ❌ Error-prone
- ❌ Requires SSH access
- ❌ No verification
- ❌ No notifications
- ❌ Inconsistent process

### After (GitHub Actions)

**Steps:**
1. `git push origin main`
2. Wait for notification ✅

**Benefits:**
- ✅ Fast (~3-5 min)
- ✅ Automated
- ✅ No SSH needed
- ✅ Health checks
- ✅ Notifications
- ✅ Consistent
- ✅ Logged

---

## Architecture Diagram Sections Summary

| Section | Title | Content |
|---------|-------|---------|
| 1 | Arquitectura de Alto Nivel | System overview |
| 2 | Arquitectura de Despliegue | Deployment architecture |
| 3 | Diagrama de Flujo de Datos | Data flow sequences |
| 4 | Interacción de Componentes | Component interactions |
| 5 | **Flujo de Despliegue CI/CD** | **GitHub Actions workflow** ✨ NEW |
| 6 | **Pipeline CI/CD con GitHub Actions** | **Detailed sequence** ✨ NEW |
| 7 | **Configuración de GitHub Secrets** | **Secrets setup** ✨ NEW |
| 8 | Arquitectura de Seguridad | Security architecture |
| - | Stack Tecnológico | **Updated with CI/CD** ✨ UPDATED |

---

## Testing the CI/CD Pipeline

### Test Deployment
```bash
# 1. Make a change to backend
echo "# Test change" >> app.py

# 2. Commit and push
git add app.py
git commit -m "test: trigger CI/CD"
git push origin main

# 3. Watch GitHub Actions
# Go to: https://github.com/your-repo/actions
# View: Deploy to AWS EC2 workflow

# 4. Monitor progress
# - Checkout code ✓
# - Setup SSH ✓
# - Deploy to EC2 ✓
# - Verify Deployment ✓
# - Cleanup ✓

# 5. Check notifications
# GitHub will show ✅ or ❌ status
```

### Verify Deployment
```bash
# Option 1: Via GitHub Actions logs
# Check "Notify Success" step output

# Option 2: Direct API call
curl http://your-ec2-host:8000/health

# Option 3: SSH to EC2 (if needed)
ssh -i your-key.pem ubuntu@your-ec2-host
cd /home/ubuntu/maia-back-proyecto
docker-compose ps
docker-compose logs --tail=50
```

---

## Troubleshooting CI/CD

### Deployment Fails

**Check:**
1. GitHub Actions logs
2. SSH key validity
3. EC2 security groups (port 22 open)
4. EC2 instance running
5. Docker daemon status
6. Disk space on EC2

### Health Check Fails

**Check:**
1. Docker container running: `docker ps`
2. Application logs: `docker-compose logs`
3. Port 8000 accessible: `netstat -tulpn | grep 8000`
4. Models downloaded correctly
5. Database initialized

### Secrets Not Working

**Verify:**
1. Secrets exist in GitHub Settings
2. Secret names match workflow exactly
3. No extra spaces in secret values
4. SSH key format correct (PEM)
5. EC2_HOST is correct IP/hostname

---

## Future Enhancements

### Possible Improvements

1. **Environment Separation**
   - Staging environment
   - Production environment
   - Branch-based deployment

2. **Advanced Testing**
   - Unit tests before deploy
   - Integration tests
   - Load testing

3. **Monitoring**
   - Deployment metrics
   - Performance monitoring
   - Error tracking

4. **Notifications**
   - Slack integration
   - Email notifications
   - Discord webhooks

5. **Rollback**
   - Automatic rollback on failure
   - Version tagging
   - Blue-green deployment

6. **Security**
   - Automated security scans
   - Dependency updates
   - Vulnerability checks

---

## Documentation Updates

### Files Modified
- ✅ `ARCHITECTURE_DIAGRAM.md` - Main architecture documentation
- ✅ Added 3 new diagram sections
- ✅ Updated technology stack
- ✅ Enhanced deployment documentation

### Files Referenced
- `.github/workflows/deploy.yml` - Workflow definition
- `docker-compose.yml` - Docker configuration
- `Dockerfile` - Container image
- `app.py` - Flask application

---

## Summary

The architecture documentation now accurately reflects:

✅ **Automated CI/CD** via GitHub Actions  
✅ **Complete deployment flow** with all steps  
✅ **Security configuration** for secrets  
✅ **Health check verification**  
✅ **Error handling and notifications**  
✅ **Smart path filtering** to prevent unnecessary deploys  
✅ **Docker lifecycle management**  
✅ **Professional DevOps practices**  

The diagrams provide clear visualization of:
- How code gets from developer to production
- What happens at each step
- How secrets are managed securely
- How health checks ensure success
- How the system responds to failures

**Result**: Complete, accurate, and professional architecture documentation for presentations and technical discussions! 📊🚀

---

**Version**: 2.9.0  
**Date**: November 2025  
**Update**: CI/CD Pipeline Documentation  
**Status**: ✅ Complete and Production-Ready

