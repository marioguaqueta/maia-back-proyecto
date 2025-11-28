# 🚀 Guía de Despliegue - Sistema de Detección de Fauna

Guía completa para desplegar el **Backend (Docker)** y **Frontend (Streamlit)** en diferentes entornos.

---

## 📋 Tabla de Contenidos

- [Requisitos Previos](#requisitos-previos)
- [Arquitectura de Despliegue](#arquitectura-de-despliegue)
- [Backend con Docker](#backend-con-docker)
- [Frontend con Streamlit](#frontend-con-streamlit)
- [CI/CD con GitHub Actions](#cicd-con-github-actions)
- [Verificación y Monitoreo](#verificación-y-monitoreo)
- [Troubleshooting](#troubleshooting)

---

## 📦 Requisitos Previos

### Para Backend (Docker)

#### Local
```bash
✅ Docker Engine 20.10+
✅ Docker Compose 2.0+
✅ 4GB RAM mínimo (8GB recomendado)
✅ 10GB espacio en disco
✅ Puerto 8000 disponible
```

#### Producción (AWS EC2)
```bash
✅ Instancia EC2 (t2.medium o superior)
✅ Ubuntu 20.04/22.04 LTS
✅ Docker y Docker Compose instalados
✅ Security Group con puertos 22 (SSH) y 8000 (HTTP)
✅ IP Elástica (recomendado)
```

### Para Frontend (Streamlit)

#### Local
```bash
✅ Python 3.11+
✅ pip o conda
✅ Puerto 8501 disponible
✅ Acceso a la API del backend
```

#### Streamlit Cloud
```bash
✅ Cuenta de GitHub
✅ Repositorio público/privado
✅ Cuenta de Streamlit Cloud (gratis)
```

---

## 🏗️ Arquitectura de Despliegue

```
┌─────────────────────────────────────────────────────────┐
│                    INTERNET                              │
└────────────────────┬────────────────────────────────────┘
                     │
        ┌────────────┴────────────┐
        │                         │
   ┌────▼──────┐           ┌─────▼──────┐
   │ Streamlit │           │   GitHub   │
   │   Cloud   │           │  (código)  │
   │  (8501)   │           └─────┬──────┘
   └────┬──────┘                 │
        │                   ┌────▼──────────┐
        │                   │ GitHub Actions│
        │                   │    (CI/CD)    │
        │                   └────┬──────────┘
        │                        │
        │   API HTTP         ┌───▼─────────────────┐
        └────────────────────►│   AWS EC2 / VPS    │
                              │  Ubuntu + Docker   │
                              │                    │
                              │  ┌──────────────┐ │
                              │  │   Backend    │ │
                              │  │   Flask API  │ │
                              │  │  (Port 8000) │ │
                              │  └──────────────┘ │
                              │  ┌──────────────┐ │
                              │  │   Modelos ML │ │
                              │  │   BD SQLite  │ │
                              │  └──────────────┘ │
                              └────────────────────┘
```

---

## 🐳 Backend con Docker

### Opción 1: Despliegue Local (Desarrollo)

#### Paso 1: Clonar Repositorio

```bash
# Clonar proyecto
git clone https://github.com/tu-usuario/tu-proyecto.git
cd tu-proyecto
```

#### Paso 2: Configurar Variables de Entorno

```bash
# Copiar archivo de ejemplo
cp env.example .env

# Editar variables (opcional, hay valores por defecto)
nano .env
```

**Variables mínimas requeridas:**
```env
GDRIVE_FOLDER_ID=1BMy6W7_3JhSA6uSEzze48ZR22qJv4s2R
YOLO_MODEL_FILENAME=best.pt
HERDNET_MODEL_FILENAME=herdnet_baseline_model.pth
```

> Ver [README_ENVS.md](README_ENVS.md) para configuración detallada.

#### Paso 3: Construir y Levantar Servicios

```bash
# Construir imagen Docker
docker-compose build

# Iniciar servicios en segundo plano
docker-compose up -d

# Ver logs en tiempo real
docker-compose logs -f
```

#### Paso 4: Verificar Despliegue

```bash
# Verificar que el contenedor esté corriendo
docker-compose ps

# Verificar salud del servicio
curl http://localhost:8000/health

# Respuesta esperada:
# {"message": "API is healthy", "status": "ok", ...}
```

#### Comandos Útiles

```bash
# Ver logs
docker-compose logs -f animal-detection-api

# Reiniciar servicio
docker-compose restart

# Detener servicio
docker-compose down

# Detener y eliminar volúmenes
docker-compose down -v

# Ver uso de recursos
docker stats animal-detection-api

# Acceder al contenedor
docker exec -it animal-detection-api bash
```

---

### Opción 2: Despliegue en AWS EC2 (Producción)

#### Preparación de la Instancia EC2

##### 1. Crear y Configurar Instancia

```bash
# Tipo de instancia recomendada:
# - t2.medium (4GB RAM) - Mínimo
# - t2.large (8GB RAM) - Recomendado
# - t3.medium (4GB RAM) - Alternativa económica

# Sistema operativo:
# Ubuntu Server 22.04 LTS (AMI)

# Almacenamiento:
# 20GB gp3 (mínimo)
# 30GB gp3 (recomendado)
```

##### 2. Configurar Security Group

| Tipo | Puerto | Origen | Descripción |
|------|--------|--------|-------------|
| SSH | 22 | Tu IP | Acceso SSH |
| HTTP | 8000 | 0.0.0.0/0 | API Backend |
| HTTPS | 443 | 0.0.0.0/0 | (Opcional) SSL |

##### 3. Conectarse a la Instancia

```bash
# Descargar tu clave .pem y conectarte
chmod 400 tu-clave.pem
ssh -i tu-clave.pem ubuntu@tu-ip-publica-ec2
```

##### 4. Instalar Docker y Docker Compose

```bash
# Actualizar sistema
sudo apt update && sudo apt upgrade -y

# Instalar Docker
sudo apt install -y docker.io
sudo systemctl start docker
sudo systemctl enable docker

# Agregar usuario al grupo docker
sudo usermod -aG docker ubuntu

# Instalar Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

# Verificar instalación
docker --version
docker-compose --version

# Cerrar sesión y volver a conectar para aplicar cambios
exit
ssh -i tu-clave.pem ubuntu@tu-ip-publica-ec2
```

#### Despliegue Manual en EC2

##### 1. Clonar Proyecto

```bash
# Crear directorio de proyecto
cd /home/ubuntu
mkdir -p maia-back-proyecto
cd maia-back-proyecto

# Clonar repositorio
git clone https://github.com/tu-usuario/tu-proyecto.git .
```

##### 2. Configurar Variables de Entorno

```bash
# Copiar archivo de ejemplo
cp env.example .env

# Editar con valores de producción
nano .env

# Configurar para producción:
FLASK_DEBUG=False
FLASK_HOST=0.0.0.0
FLASK_PORT=8000
```

##### 3. Desplegar con Docker Compose

```bash
# Construir y levantar servicios
docker-compose up -d --build

# Esperar a que los modelos se descarguen
# (Primera vez puede tardar 5-10 minutos)

# Monitorear logs
docker-compose logs -f

# Verificar estado
docker-compose ps
```

##### 4. Verificar Despliegue

```bash
# Desde la instancia EC2
curl http://localhost:8000/health

# Desde tu máquina local
curl http://TU-IP-PUBLICA-EC2:8000/health
```

##### 5. Configurar Auto-inicio (Opcional)

```bash
# Crear servicio systemd
sudo nano /etc/systemd/system/animal-detection.service

# Contenido del archivo:
[Unit]
Description=Animal Detection API
Requires=docker.service
After=docker.service

[Service]
Type=oneshot
RemainAfterExit=yes
WorkingDirectory=/home/ubuntu/maia-back-proyecto
ExecStart=/usr/local/bin/docker-compose up -d
ExecStop=/usr/local/bin/docker-compose down
TimeoutStartSec=0

[Install]
WantedBy=multi-user.target

# Habilitar y iniciar servicio
sudo systemctl enable animal-detection.service
sudo systemctl start animal-detection.service
```

---

### Opción 3: Despliegue Automático con GitHub Actions (CI/CD)

> Esta es la **opción recomendada** para producción.

#### Configuración Inicial

##### 1. Configurar GitHub Secrets

Ve a: `GitHub Repo → Settings → Secrets and variables → Actions`

Agregar los siguientes secrets:

| Secret | Descripción | Ejemplo |
|--------|-------------|---------|
| `EC2_SSH_KEY` | Clave privada SSH (contenido del .pem) | -----BEGIN RSA PRIVATE KEY----- ... |
| `EC2_HOST` | IP pública o hostname de EC2 | `3.123.45.67` o `api.tudominio.com` |
| `EC2_USER` | Usuario SSH | `ubuntu` |

##### 2. Verificar Workflow

El archivo `.github/workflows/deploy.yml` ya está configurado.

**Triggers:**
- ✅ Push a `main` o `master`
- ✅ Ignora cambios en frontend, docs y tests
- ✅ Permite ejecución manual

##### 3. Probar Despliegue Automático

```bash
# Hacer un cambio en el backend
echo "# Test deployment" >> app.py

# Commit y push
git add .
git commit -m "test: trigger CI/CD deployment"
git push origin main

# Monitorear en GitHub:
# https://github.com/tu-usuario/tu-repo/actions
```

##### 4. Proceso Automático

El workflow ejecutará:

1. ✅ Checkout del código
2. ✅ Setup SSH con tu clave EC2
3. ✅ Rsync de archivos a EC2
4. ✅ `docker-compose down`
5. ✅ `docker system prune -f`
6. ✅ `docker-compose up -d --build`
7. ✅ Health check (5 intentos)
8. ✅ Notificación de éxito/fallo

**Tiempo total:** ~3-5 minutos

---

## 🎨 Frontend con Streamlit

### Opción 1: Ejecución Local

#### Paso 1: Instalar Dependencias

```bash
# Navegar al proyecto
cd tu-proyecto

# Crear entorno virtual (recomendado)
python -m venv venv

# Activar entorno virtual
# Linux/Mac:
source venv/bin/activate
# Windows:
venv\Scripts\activate

# Instalar dependencias
pip install -r requirements-streamlit.txt
```

#### Paso 2: Configurar Variables

```bash
# Copiar archivo de ejemplo
cp .streamlit/env.example .streamlit/.env

# Editar configuración
nano .streamlit/.env

# Configurar URL del backend
API_BASE_URL=http://localhost:8000
# o si está en EC2:
API_BASE_URL=http://tu-ip-ec2:8000
```

#### Paso 3: Ejecutar Streamlit

```bash
# Iniciar aplicación
streamlit run streamlit_app.py

# La aplicación se abrirá en:
# http://localhost:8501
```

#### Comandos Útiles

```bash
# Ejecutar en puerto específico
streamlit run streamlit_app.py --server.port 8502

# Ejecutar en red local
streamlit run streamlit_app.py --server.address 0.0.0.0

# Modo headless (sin abrir navegador)
streamlit run streamlit_app.py --server.headless true
```

---

### Opción 2: Despliegue en Streamlit Cloud (Recomendado)

#### Paso 1: Preparar Repositorio

```bash
# Asegurarse de tener estos archivos en el repositorio:
streamlit_app.py
requirements-streamlit.txt
.streamlit/config.toml

# Opcional pero recomendado:
.streamlit/env.example  # Para documentación
```

#### Paso 2: Crear Cuenta en Streamlit Cloud

1. Ve a: [share.streamlit.io](https://share.streamlit.io)
2. Inicia sesión con GitHub
3. Autoriza Streamlit a acceder a tus repositorios

#### Paso 3: Crear Nueva App

```
1. Click en "New app"
2. Seleccionar:
   - Repository: tu-usuario/tu-proyecto
   - Branch: main
   - Main file path: streamlit_app.py
3. Click "Advanced settings..."
```

#### Paso 4: Configurar Secrets

En "Advanced settings → Secrets":

```toml
# .streamlit/secrets.toml
API_BASE_URL = "http://tu-ip-ec2:8000"
ADMIN_EMAIL = "admin@tudominio.com"
EXPLAIN_VIDEO_URL = "https://tudominio.com/tutorials"
DOCS_URL = "https://tudominio.com/docs"
ENABLE_HERDNET = "true"

# Opcional: Agregar todas las variables de .streamlit/env.example
YOLO_CONF_MIN = "0.1"
YOLO_CONF_MAX = "0.9"
# ... etc
```

#### Paso 5: Desplegar

```
1. Click "Deploy!"
2. Esperar ~2-5 minutos
3. Tu app estará disponible en:
   https://tu-usuario-tu-proyecto.streamlit.app
```

#### Actualizar Deployment

```bash
# Cualquier push a main actualizará automáticamente
git add streamlit_app.py
git commit -m "feat: update streamlit UI"
git push origin main

# Streamlit Cloud detectará el cambio y re-desplegará
# Tiempo: ~1-2 minutos
```

#### Gestionar App en Streamlit Cloud

```
Dashboard: https://share.streamlit.io/

Opciones disponibles:
- ⚙️ Settings: Cambiar configuración
- 🔐 Secrets: Actualizar variables
- 📊 Metrics: Ver uso y analytics
- 🔄 Reboot: Reiniciar app
- 🗑️ Delete: Eliminar app
- 📝 Logs: Ver logs en tiempo real
```

---

## 🔄 CI/CD con GitHub Actions

### Workflow Completo

```yaml
# Archivo: .github/workflows/deploy.yml

Trigger:
  ✅ Push a main/master
  ✅ Excluye: frontend, docs, tests
  ✅ Manual (workflow_dispatch)

Pasos:
  1. Checkout código
  2. Setup SSH
  3. Rsync a EC2
  4. Deploy con Docker
  5. Health check
  6. Notificar resultado
```

### Monitoreo del Workflow

```bash
# Ver workflows en GitHub
https://github.com/tu-usuario/tu-repo/actions

# Ver un workflow específico
https://github.com/tu-usuario/tu-repo/actions/runs/WORKFLOW_ID

# Logs en tiempo real
https://github.com/tu-usuario/tu-repo/actions/runs/WORKFLOW_ID
```

### Ejecutar Manualmente

```
1. Ve a: Actions → Deploy to AWS EC2
2. Click en "Run workflow"
3. Selecciona branch (main)
4. Click "Run workflow"
```

### Detener Deployment en Progreso

```
1. Ve al workflow en ejecución
2. Click "Cancel workflow"
```

---

## ✅ Verificación y Monitoreo

### Verificar Backend

#### Health Check
```bash
# Local
curl http://localhost:8000/health

# Producción
curl http://TU-IP-EC2:8000/health

# Respuesta esperada:
{
  "status": "ok",
  "message": "API is healthy",
  "yolo_model_loaded": true,
  "herdnet_model_loaded": true,
  "database_connected": true
}
```

#### Endpoints Disponibles
```bash
# Información de modelos
curl http://localhost:8000/models/info

# Estadísticas de base de datos
curl http://localhost:8000/database/stats

# Swagger UI (interactivo)
http://localhost:8000/apidocs
```

#### Logs del Backend

```bash
# Docker Compose
docker-compose logs -f animal-detection-api

# Ver últimas 100 líneas
docker-compose logs --tail=100 animal-detection-api

# Buscar errores
docker-compose logs animal-detection-api | grep -i error
```

#### Métricas del Contenedor

```bash
# Uso de recursos en tiempo real
docker stats animal-detection-api

# Información del contenedor
docker inspect animal-detection-api

# Procesos dentro del contenedor
docker top animal-detection-api
```

### Verificar Frontend

#### Streamlit Local
```bash
# La app debe estar accesible en:
http://localhost:8501

# Verificar que conecta con backend:
# Probar análisis de una imagen
```

#### Streamlit Cloud
```bash
# Verificar URL pública
https://tu-usuario-tu-proyecto.streamlit.app

# Ver logs en tiempo real:
Dashboard → Tu App → Manage app → Logs
```

### Monitoreo Continuo

#### Script de Monitoreo
```bash
#!/bin/bash
# monitor.sh

while true; do
  echo "=========================================="
  echo "$(date)"
  
  # Backend health
  echo "Backend Health:"
  curl -s http://localhost:8000/health | jq '.'
  
  # Docker stats
  echo ""
  echo "Container Stats:"
  docker stats animal-detection-api --no-stream
  
  # Disk usage
  echo ""
  echo "Disk Usage:"
  df -h /
  
  echo ""
  sleep 60
done
```

```bash
# Ejecutar monitor
chmod +x monitor.sh
./monitor.sh
```

---

## 🐛 Troubleshooting

### Problemas Comunes del Backend

#### 1. Contenedor no inicia

**Síntomas:**
```bash
docker-compose ps
# Estado: Restarting o Exit 1
```

**Soluciones:**
```bash
# Ver logs completos
docker-compose logs animal-detection-api

# Verificar variables de entorno
docker-compose config

# Reconstruir desde cero
docker-compose down
docker-compose build --no-cache
docker-compose up -d

# Verificar puertos disponibles
sudo netstat -tulpn | grep 8000
```

#### 2. Modelos no se descargan

**Síntomas:**
```bash
# Error en logs:
# Failed to download model from Google Drive
```

**Soluciones:**
```bash
# Verificar ID de carpeta
echo $GDRIVE_FOLDER_ID

# Verificar conectividad
docker exec -it animal-detection-api bash
curl https://drive.google.com

# Descargar manualmente
# En el contenedor:
cd /app
python model_loader.py
```

#### 3. Out of Memory

**Síntomas:**
```bash
# Error: Killed
# O contenedor se detiene inesperadamente
```

**Soluciones:**
```bash
# Verificar memoria
free -h

# Limitar memoria del contenedor
# En docker-compose.yml:
services:
  animal-detection-api:
    deploy:
      resources:
        limits:
          memory: 4G

# Limpiar caché de Docker
docker system prune -a
```

#### 4. Health Check Falla

**Síntomas:**
```bash
# Health check: unhealthy
```

**Soluciones:**
```bash
# Verificar desde dentro del contenedor
docker exec -it animal-detection-api bash
curl http://localhost:8000/health

# Verificar que Flask esté corriendo
ps aux | grep gunicorn

# Verificar logs de Gunicorn
docker-compose logs | grep gunicorn
```

### Problemas Comunes del Frontend

#### 1. No Conecta con Backend

**Síntomas:**
```
Error: Connection refused
o
Request failed with status 500
```

**Soluciones:**
```bash
# Verificar API_BASE_URL
# En .streamlit/.env o Secrets:
API_BASE_URL=http://CORRECT-IP:8000

# Verificar que backend responda
curl http://BACKEND-URL:8000/health

# Verificar firewall/security groups
# Puerto 8000 debe estar abierto
```

#### 2. Streamlit Cloud Build Falla

**Síntomas:**
```
Error during build
Requirements file error
```

**Soluciones:**
```bash
# Verificar requirements-streamlit.txt
# Debe tener solo dependencias del frontend

# Verificar Python version
# En .streamlit/config.toml:
[server]
pythonVersion = "3.11"

# Re-desplegar
# Dashboard → Reboot app
```

#### 3. Secrets No Se Aplican

**Síntomas:**
```
Using default values instead of secrets
```

**Soluciones:**
```toml
# Verificar formato en Secrets
# Debe ser TOML, no ENV:

# ❌ Incorrecto:
API_BASE_URL=http://example.com

# ✅ Correcto:
API_BASE_URL = "http://example.com"

# Después de cambiar secrets:
# Dashboard → Reboot app
```

### Problemas de CI/CD

#### 1. Workflow Falla en SSH

**Síntomas:**
```
Permission denied (publickey)
```

**Soluciones:**
```bash
# Verificar que EC2_SSH_KEY esté correcto
# Debe incluir:
-----BEGIN RSA PRIVATE KEY-----
[contenido completo de la clave]
-----END RSA PRIVATE KEY-----

# Verificar EC2_HOST
# Debe ser IP pública o hostname

# Verificar Security Group
# Puerto 22 debe estar abierto para GitHub Actions
# IP range de GitHub: https://api.github.com/meta
```

#### 2. Health Check Timeout

**Síntomas:**
```
Health check failed after 5 attempts
```

**Soluciones:**
```bash
# SSH a EC2 y verificar manualmente
ssh -i tu-clave.pem ubuntu@TU-EC2-IP

# Verificar contenedor
docker-compose ps
docker-compose logs

# El servicio puede tardar más de 15 segundos
# Aumentar timeout en deploy.yml si es necesario
sleep 30  # en lugar de sleep 15
```

#### 3. Rsync Falla

**Síntomas:**
```
rsync: command not found
o
failed to sync files
```

**Soluciones:**
```bash
# Instalar rsync en EC2
sudo apt update
sudo apt install -y rsync

# Verificar conectividad SSH
ssh -i tu-clave.pem ubuntu@TU-EC2-IP

# Verificar permisos de carpeta destino
ls -la /home/ubuntu/maia-back-proyecto
```

---

## 📊 Checklist de Despliegue

### Pre-Despliegue

**Backend:**
- [ ] Docker y Docker Compose instalados
- [ ] Puerto 8000 disponible
- [ ] Variables de entorno configuradas
- [ ] Google Drive folder accesible
- [ ] Al menos 10GB espacio en disco

**Frontend:**
- [ ] Python 3.11+ instalado (local)
- [ ] Cuenta de Streamlit Cloud (cloud)
- [ ] Backend URL configurada
- [ ] Secrets configurados

**CI/CD:**
- [ ] GitHub Secrets configurados
- [ ] Security Groups abiertos (22, 8000)
- [ ] Clave SSH válida
- [ ] Workflow verificado

### Post-Despliegue

**Backend:**
- [ ] Health check responde OK
- [ ] Modelos descargados correctamente
- [ ] Base de datos inicializada
- [ ] Swagger UI accesible
- [ ] Logs sin errores críticos

**Frontend:**
- [ ] Aplicación accesible
- [ ] Conecta con backend
- [ ] Puede analizar imágenes
- [ ] Interfaz responde correctamente

**CI/CD:**
- [ ] Primer deployment exitoso
- [ ] Health check automático pasa
- [ ] Notificaciones funcionan
- [ ] Rollback testeado

---

## 📚 Recursos Adicionales

### Documentación

- [README.md](README.md) - Guía principal del proyecto
- [README_ENVS.md](README_ENVS.md) - Configuración de variables
- [ARCHITECTURE_DIAGRAM.md](ARCHITECTURE_DIAGRAM.md) - Arquitectura del sistema

### Enlaces Útiles

- **Docker**: https://docs.docker.com/
- **Docker Compose**: https://docs.docker.com/compose/
- **Streamlit**: https://docs.streamlit.io/
- **Streamlit Cloud**: https://docs.streamlit.io/streamlit-community-cloud
- **GitHub Actions**: https://docs.github.com/actions
- **AWS EC2**: https://docs.aws.amazon.com/ec2/

### Soporte

- **Issues**: https://github.com/tu-usuario/tu-repo/issues
- **Email**: admin@tudominio.com
- **Documentación**: https://tu-docs.com

---

## 🎯 Resumen de Comandos

### Backend (Docker)

```bash
# Desarrollo local
docker-compose up -d                    # Iniciar
docker-compose logs -f                  # Ver logs
docker-compose down                     # Detener
docker-compose restart                  # Reiniciar

# Producción (EC2)
git pull origin main                    # Actualizar código
docker-compose down                     # Detener
docker-compose up -d --build            # Rebuild y reiniciar
curl http://localhost:8000/health       # Verificar
```

### Frontend (Streamlit)

```bash
# Local
streamlit run streamlit_app.py          # Iniciar
Ctrl+C                                  # Detener

# Cloud
git push origin main                    # Desplegar
# Ver en: https://share.streamlit.io/
```

### CI/CD

```bash
# Trigger deployment
git push origin main

# Ver progreso
# https://github.com/tu-usuario/tu-repo/actions
```

---

**Última actualización**: Noviembre 2025  
**Versión**: 3.0.0  
**Mantenedores**: Proyecto MAIA - Grupo 12

---

## 🚀 ¡Listo para Desplegar!

Sigue esta guía paso a paso y tendrás tu sistema de detección de fauna desplegado y funcionando en minutos. Para cualquier problema, consulta la sección de [Troubleshooting](#troubleshooting) o crea un [issue en GitHub](https://github.com/tu-usuario/tu-repo/issues).

¡Buena suerte con tu despliegue! 🎉

