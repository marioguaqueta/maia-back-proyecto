# 🔧 Guía de Configuración de Variables de Entorno

Esta guía explica cómo configurar las variables de entorno para el **Backend (Flask API)** y el **Frontend (Streamlit)**.

---

## 📋 Índice

- [Backend - API Flask](#backend---api-flask)
- [Frontend - Streamlit](#frontend---streamlit)
- [Configuración Rápida](#configuración-rápida)
- [Variables por Categoría](#variables-por-categoría)
- [Ejemplos de Uso](#ejemplos-de-uso)

---

## 🔙 Backend - API Flask

### 📁 Ubicación
```
/env.example  →  Copiar a  →  /.env
```

### ⚙️ Configuración

#### Paso 1: Copiar archivo de ejemplo
```bash
cp env.example .env
```

#### Paso 2: Editar variables

```bash
nano .env
# o usar tu editor favorito
```

### 📝 Variables Requeridas

#### 🔑 Configuración de Google Drive
```env
# ID de la carpeta de Google Drive donde están los modelos
GDRIVE_FOLDER_ID=1BMy6W7_3JhSA6uSEzze48ZR22qJv4s2R

# Nombres de los archivos de modelos
YOLO_MODEL_FILENAME=best.pt
HERDNET_MODEL_FILENAME=herdnet_baseline_model.pth
```

> **📌 Nota**: El `GDRIVE_FOLDER_ID` se encuentra en la URL de la carpeta de Google Drive:
> `https://drive.google.com/drive/folders/[ESTE_ES_EL_ID]`

#### 📂 Configuración de Archivos
```env
# Extensiones permitidas (sin comillas, sin espacios)
ALLOWED_IMAGE_EXTENSIONS=png,jpg,jpeg,gif,webp,bmp
ALLOWED_ZIP_EXTENSIONS=zip
```

⚠️ **IMPORTANTE**: 
- ✅ Correcto: `png,jpg,jpeg`
- ❌ Incorrecto: `'png,jpg,jpeg'` o `"png,jpg,jpeg"` o `['png','jpg']`

#### 🌐 Configuración de Flask
```env
# Modo debug (False en producción)
FLASK_DEBUG=True

# Host (0.0.0.0 para aceptar conexiones externas)
FLASK_HOST=0.0.0.0

# Puerto
FLASK_PORT=8000
```

### 📝 Variables Opcionales

```env
# Base de datos (opcional, por defecto: wildlife_detection.db)
DATABASE_NAME=wildlife_detection.db

# Tamaño máximo de archivo en MB (opcional)
MAX_UPLOAD_SIZE_MB=200

# Directorio temporal (opcional)
TEMP_DIR=/tmp/wildlife_detection
```

---

## 🎨 Frontend - Streamlit

### 📁 Ubicación
```
/.streamlit/env.example  →  Copiar a  →  /.streamlit/.env
```

### ⚙️ Configuración

#### Paso 1: Copiar archivo de ejemplo
```bash
cp .streamlit/env.example .streamlit/.env
```

#### Paso 2: Editar variables

```bash
nano .streamlit/.env
# o usar tu editor favorito
```

### 📝 Variables Esenciales

#### 🔗 Conexión con API
```env
# URL del backend Flask
API_BASE_URL=http://localhost:8000

# Email del administrador
ADMIN_EMAIL=info@grupo12.yolomodel.com

# URLs de ayuda y documentación
EXPLAIN_VIDEO_URL=https://example.com/tutorials
DOCS_URL=https://example.com/docs
```

#### 🤖 Disponibilidad de Modelos
```env
# Habilitar/deshabilitar modelo HerdNet en la UI
ENABLE_HERDNET=true
```

### 📝 Variables de Interfaz (Opcionales)

#### YOLOv11 - Configuración de UI
```env
# Sliders de confianza
YOLO_CONF_MIN=0.1
YOLO_CONF_MAX=0.9
YOLO_CONF_DEFAULT=0.25
YOLO_CONF_STEP=0.05

# Sliders de IOU
YOLO_IOU_MIN=0.1
YOLO_IOU_MAX=0.9
YOLO_IOU_DEFAULT=0.45
YOLO_IOU_STEP=0.05

# Opciones de tamaño de imagen
YOLO_IMG_SIZES=416,480,640,800,960,1280,2560,5120,10240
YOLO_IMG_SIZE_DEFAULT_INDEX=2
```

#### HerdNet - Configuración de UI
```env
# Opciones de tamaño de parche
HERDNET_PATCH_SIZES=384,512,768,1024,2048,4096,8192,16384
HERDNET_PATCH_SIZE_DEFAULT_INDEX=1

# Opciones de rotación
HERDNET_ROTATION_OPTIONS=0,1,2,3
HERDNET_ROTATION_DEFAULT_INDEX=0

# Sliders de superposición
HERDNET_OVERLAP_MIN=0
HERDNET_OVERLAP_MAX=300
HERDNET_OVERLAP_DEFAULT=160
HERDNET_OVERLAP_STEP=16

# Sliders de miniatura
HERDNET_THUMBNAIL_MIN=128
HERDNET_THUMBNAIL_MAX=512
HERDNET_THUMBNAIL_DEFAULT=256
HERDNET_THUMBNAIL_STEP=32
```

#### Zoom de Imágenes con Plotly
```env
# Dimensión máxima para display (default: 1500)
PLOTLY_MAX_DIMENSION=1500

# Umbral para fallback a imagen estática (default: 3000)
PLOTLY_FALLBACK_THRESHOLD=3000
```

> **📌 Nota**: Estos valores optimizan el rendimiento del zoom interactivo:
> - Imágenes < 1500px: Resolución completa con zoom Plotly
> - Imágenes 1500-3000px: Downsample a 1500px + zoom Plotly
> - Imágenes > 3000px: Visor estático (previene crashes)

---

## 🚀 Configuración Rápida

### Opción 1: Desarrollo Local

```bash
# Backend
cd /path/to/project
cp env.example .env
# Editar .env con tus valores

# Frontend
cp .streamlit/env.example .streamlit/.env
# Editar .streamlit/.env con tus valores

# Iniciar servicios
docker-compose up -d          # Backend
streamlit run streamlit_app.py # Frontend
```

### Opción 2: Producción (Docker)

```bash
# Backend: Las variables se definen en docker-compose.yml
# Frontend (Streamlit Cloud): Configurar en Secrets

# Streamlit Cloud → Settings → Secrets
# Agregar todas las variables del .streamlit/env.example
```

### Opción 3: Variables de Sistema

```bash
# Linux/Mac
export GDRIVE_FOLDER_ID="1BMy6W7_3JhSA6uSEzze48ZR22qJv4s2R"
export FLASK_PORT=8000
export API_BASE_URL="http://localhost:8000"

# Windows (PowerShell)
$env:GDRIVE_FOLDER_ID="1BMy6W7_3JhSA6uSEzze48ZR22qJv4s2R"
$env:FLASK_PORT=8000
$env:API_BASE_URL="http://localhost:8000"

# Windows (CMD)
set GDRIVE_FOLDER_ID=1BMy6W7_3JhSA6uSEzze48ZR22qJv4s2R
set FLASK_PORT=8000
set API_BASE_URL=http://localhost:8000
```

---

## 📊 Variables por Categoría

### Backend

| Categoría | Variables | Requeridas |
|-----------|-----------|-----------|
| **Google Drive** | `GDRIVE_FOLDER_ID`, `YOLO_MODEL_FILENAME`, `HERDNET_MODEL_FILENAME` | ✅ Sí |
| **Archivos** | `ALLOWED_IMAGE_EXTENSIONS`, `ALLOWED_ZIP_EXTENSIONS` | ⚠️ Recomendado |
| **Flask** | `FLASK_DEBUG`, `FLASK_HOST`, `FLASK_PORT` | ❌ Opcional |
| **Base de Datos** | `DATABASE_NAME` | ❌ Opcional |
| **Otros** | `MAX_UPLOAD_SIZE_MB`, `TEMP_DIR` | ❌ Opcional |

### Frontend

| Categoría | Variables | Requeridas |
|-----------|-----------|-----------|
| **Conexión API** | `API_BASE_URL`, `ADMIN_EMAIL` | ✅ Sí |
| **Ayuda** | `EXPLAIN_VIDEO_URL`, `DOCS_URL` | ⚠️ Recomendado |
| **Modelos** | `ENABLE_HERDNET` | ❌ Opcional |
| **YOLO UI** | `YOLO_CONF_*`, `YOLO_IOU_*`, `YOLO_IMG_*` | ❌ Opcional |
| **HerdNet UI** | `HERDNET_PATCH_*`, `HERDNET_OVERLAP_*`, etc. | ❌ Opcional |
| **Zoom** | `PLOTLY_MAX_DIMENSION`, `PLOTLY_FALLBACK_THRESHOLD` | ❌ Opcional |

---

## 💡 Ejemplos de Uso

### Ejemplo 1: Desarrollo Local Completo

**Backend (`.env`):**
```env
# Modelos
GDRIVE_FOLDER_ID=1BMy6W7_3JhSA6uSEzze48ZR22qJv4s2R
YOLO_MODEL_FILENAME=best.pt
HERDNET_MODEL_FILENAME=herdnet_baseline_model.pth

# Archivos
ALLOWED_IMAGE_EXTENSIONS=png,jpg,jpeg,gif,webp,bmp
ALLOWED_ZIP_EXTENSIONS=zip

# Flask
FLASK_DEBUG=True
FLASK_HOST=0.0.0.0
FLASK_PORT=8000
```

**Frontend (`.streamlit/.env`):**
```env
# API
API_BASE_URL=http://localhost:8000
ADMIN_EMAIL=tu-email@ejemplo.com

# Ayuda
EXPLAIN_VIDEO_URL=https://tu-sitio.com/tutorials
DOCS_URL=https://tu-sitio.com/docs

# Modelos
ENABLE_HERDNET=true
```

### Ejemplo 2: Producción AWS EC2

**Backend (`docker-compose.yml`):**
```yaml
environment:
  - GDRIVE_FOLDER_ID=1BMy6W7_3JhSA6uSEzze48ZR22qJv4s2R
  - YOLO_MODEL_FILENAME=best.pt
  - HERDNET_MODEL_FILENAME=herdnet_baseline_model.pth
  - ALLOWED_IMAGE_EXTENSIONS=png,jpg,jpeg,gif,webp,bmp
  - ALLOWED_ZIP_EXTENSIONS=zip
  - FLASK_DEBUG=False
  - FLASK_HOST=0.0.0.0
  - FLASK_PORT=8000
```

**Frontend (Streamlit Cloud Secrets):**
```toml
# .streamlit/secrets.toml
API_BASE_URL = "http://tu-ec2-ip:8000"
ADMIN_EMAIL = "admin@tu-dominio.com"
EXPLAIN_VIDEO_URL = "https://tu-sitio.com/tutorials"
DOCS_URL = "https://tu-sitio.com/docs"
ENABLE_HERDNET = "true"
```

### Ejemplo 3: Solo YOLOv11 (Sin HerdNet)

**Frontend (`.streamlit/.env`):**
```env
API_BASE_URL=http://localhost:8000
ADMIN_EMAIL=admin@ejemplo.com
ENABLE_HERDNET=false  # ← Deshabilitar HerdNet en UI
```

### Ejemplo 4: Zoom Optimizado para Imágenes Grandes

**Frontend (`.streamlit/.env`):**
```env
# Para imágenes muy grandes (mayor rendimiento)
PLOTLY_MAX_DIMENSION=1200
PLOTLY_FALLBACK_THRESHOLD=2500

# Para mejor calidad visual (menor rendimiento)
PLOTLY_MAX_DIMENSION=2000
PLOTLY_FALLBACK_THRESHOLD=4000
```

---

## 🔒 Seguridad

### ⚠️ Importante

1. **NUNCA** subir archivos `.env` a Git
   ```bash
   # Verificar que .env esté en .gitignore
   grep -q "\.env" .gitignore && echo "✅ Protegido" || echo "❌ Agregar a .gitignore"
   ```

2. **Usar secretos** en producción
   - GitHub Secrets para CI/CD
   - Streamlit Cloud Secrets para frontend
   - Variables de entorno del sistema para backend

3. **Rotar credenciales** periódicamente
   - Cambiar `GDRIVE_FOLDER_ID` si se comparte
   - Actualizar claves de API regularmente

4. **Valores por defecto** solo para desarrollo
   - Cambiar `ADMIN_EMAIL` en producción
   - Usar URLs reales para `EXPLAIN_VIDEO_URL` y `DOCS_URL`

---

## 🐛 Troubleshooting

### Problema: Backend no encuentra modelos

**Solución:**
```bash
# Verificar variables
echo $GDRIVE_FOLDER_ID
echo $YOLO_MODEL_FILENAME

# Si están vacías, cargar .env
source .env  # Linux/Mac
# o reiniciar el servicio Docker
```

### Problema: Frontend no conecta con Backend

**Solución:**
```bash
# Verificar URL del backend
echo $API_BASE_URL

# Debe coincidir con el puerto del backend
curl http://localhost:8000/health

# Si falla, verificar:
# 1. Backend está corriendo
# 2. Puerto correcto en API_BASE_URL
# 3. Firewall/security groups
```

### Problema: Error "File must be a zip file"

**Solución:**
```bash
# Las extensiones deben estar sin comillas y sin espacios
# ❌ Incorrecto:
ALLOWED_ZIP_EXTENSIONS='zip'

# ✅ Correcto:
ALLOWED_ZIP_EXTENSIONS=zip
```

### Problema: Configuración no se aplica en Streamlit

**Solución:**
```bash
# Reiniciar Streamlit
# Ctrl+C y luego:
streamlit run streamlit_app.py

# O forzar recarga
# En el navegador: Ctrl+R o Cmd+R
```

---

## 📚 Referencias

- **Backend**: Ver `env.example` en raíz del proyecto
- **Frontend**: Ver `.streamlit/env.example`
- **Docker**: Ver `docker-compose.yml` para variables en contenedor
- **Streamlit Cloud**: [Documentación de Secrets](https://docs.streamlit.io/streamlit-community-cloud/deploy-your-app/secrets-management)

---

## ✅ Checklist de Configuración

### Backend
- [ ] Archivo `.env` creado desde `env.example`
- [ ] `GDRIVE_FOLDER_ID` configurado
- [ ] Nombres de modelos correctos
- [ ] Extensiones de archivo sin comillas
- [ ] Puerto Flask configurado (default: 8000)

### Frontend
- [ ] Archivo `.streamlit/.env` creado desde `.streamlit/env.example`
- [ ] `API_BASE_URL` apunta al backend correcto
- [ ] `ADMIN_EMAIL` configurado
- [ ] URLs de ayuda actualizadas
- [ ] `ENABLE_HERDNET` según necesidad

### Verificación
- [ ] Backend inicia sin errores: `docker-compose up -d`
- [ ] Health check responde: `curl http://localhost:8000/health`
- [ ] Frontend conecta: `streamlit run streamlit_app.py`
- [ ] Modelos se descargan correctamente
- [ ] Análisis de imágenes funciona

---

## 🎯 Resumen Rápido

### Mínimo Necesario para Funcionar

**Backend:**
```env
GDRIVE_FOLDER_ID=1BMy6W7_3JhSA6uSEzze48ZR22qJv4s2R
```

**Frontend:**
```env
API_BASE_URL=http://localhost:8000
```

Todo lo demás tiene valores por defecto razonables. 🚀

---

**Última actualización**: Noviembre 2025  
**Versión**: 2.9.0  
**Mantenedores**: Proyecto MAIA - Grupo 12

