# Sistema de Detección, conteo y clasificación de especies específicas Fauna Africana con imágenes aéreas
Este proyecto ofrece un API REST basada en Flask (Python) para detectar, contar y clasificar especies específicas de fauna africana utilizando imágenes aéreas, utilizando las predicciones de los modelos de aprendizaje profundo **YOLOv11** con entrenamiento específico y como referencia base **HerdNet**, facilitando el uso de usuarios finales a través de una interfaz web Streamlit.

## ✨ Características

### Detección Principal
- 🦁 **Soporte Dual de Modelos**: Elige entre YOLOv11 (cajas delimitadoras) o HerdNet (detección por puntos)
- 🎯 **Detección YOLOv11**: Detección rápida y precisa de cajas delimitadoras con imágenes anotadas
- 📍 **Detección HerdNet**: Detección precisa basada en puntos optimizada para imágenes aéreas
- 🗺️ **Soporte para Imágenes Grandes**: Procesa imágenes satelitales grandes (6000x4000+) usando unión inteligente
- 📦 **Procesamiento por Lotes**: Sube archivos ZIP con múltiples imágenes para análisis por lotes hasta 100 MB
- 🖼️ **Análisis de Imagen Individual**: Sube imágenes individuales (PNG, JPG y JPEG) para pruebas rápidas
- ⚡ **Entrada Flexible**: Elige entre ZIP (lotes) o imagen individual según tus necesidades

### Gestión de Datos
- 💾 **Almacenamiento en Base de Datos**: Base de datos SQLite almacena todas las tareas de análisis y resultados completos
- 🔍 **Seguimiento de Tareas**: Cada análisis obtiene un task_id único para fácil recuperación
- 📈 **Estadísticas**: Ver estadísticas completas sobre todos los análisis

### Interfaces de Usuario
- 🌐 **Interfaz Web Streamlit**: Interfaz web intuitiva y fácil de usar
- 🔌 **API REST**: API REST completa para acceso programático desde diferentes aplicaciones web
- 📱 **Diseño Responsivo**: Funciona en escritorio, tablet y móvil

### Despliegue
- ☁️ **Listo para la Nube**: Los modelos se descargan automáticamente desde Google Drive
- 🚀 **Configuración Fácil**: Sin archivos grandes en el repositorio

## 🚀 Inicio Rápido

### 1. Instalación

```bash
# Clonar el repositorio
git clone https://github.com/marioguaqueta/maia-back-proyecto.git
cd maia-back-proyecto

# Crear entorno virtual
python3 -m venv .venv

# Linux/MacOS
source .venv/bin/activate  

#Windows
.venv/bin/activate

# Instalar dependencias
pip install -r requirements.txt

# Instalar HerdNet
pip install git+https://github.com/Alexandre-Delplanque/HerdNet.git
```

**Nota:** Los archivos de modelos (`best.pt` y `herdnet_model.pth`) se **descargarán automáticamente desde Google Drive** en la primera ejecución!

Es importante que los archivos estén dentro de un folder publico de google drive, y que se configure la variable GDRIVE_FOLDER_ID en dicho folder

**Opción A: Inicio manual (dos terminales) para uso local**

Crear archivos de configuración
`.env` y `.streamlit/.env` según las instrucciones en la sección de Variables de Entorno, seguir la plantilla en ./env.example y ./.streamlit/env.example


Terminal 1 - Backend:
```bash
python app.py
```

Terminal 2 - Frontend:
```bash
streamlit run streamlit_app.py
```

### 3. Acceder a la Aplicación

- **🌐 Interfaz Web:** http://localhost:8501 (Interfaz Streamlit)
- **🔌 API Endpoint:** http://localhost:8000 (API Flask)

## 🎯 ¿Qué Modelo Debo Usar?

### Usa YOLOv11 si quieres:
- ✅ Procesamiento rápido (1-2 segundos por imagen)
- ✅ Cajas delimitadoras alrededor de los animales
- ✅ Tamaños de imagen estándar
- ✅ Capacidades de detección en tiempo real
- ✅ Salida simple y directa

### Usa HerdNet si quieres:
- ✅ Imágenes satelitales muy grandes (6000x4000+)
- ✅ Ubicaciones precisas del punto central
- ✅ Miniaturas individuales de animales
- ✅ Precisión de grado científico
- ✅ Procesamiento optimizado de imágenes aéreas

**💡 Consejo:** ¡Prueba ambos modelos y compara resultados!

## 🌐 Usando la Interfaz Streamlit

La interfaz web Streamlit proporciona una hermosa interfaz basada en tarjetas para un fácil acceso al sistema:

### 📁 Página de Nuevo Análisis
1. Sube un archivo ZIP con imágenes de fauna
2. Selecciona modelo YOLOv11 o HerdNet
3. Configura parámetros (confianza, tamaño de parche, etc.)
4. Haz clic en "Ejecutar Análisis"
5. **Ver resultados en diseño moderno de tarjetas:**
   - 🖼️ **Tarjetas de Imagen**: Cada imagen en su propia tarjeta estilizada
   - 🎯 **Insignias de Detección**: Conteos codificados por color y dimensiones
   - 📊 **Tablas Plegables**: Detalles de detección expandibles por imagen
   - 🔍 **Visor Interactivo**: Vista de tamaño completo con zoom y paneo
   - ⬇️ **Descarga Rápida**: Descarga directa desde cada tarjeta
6. Guarda el task_id para recuperar resultados más tarde

### 📊 Página de Ver Resultados
- Explorar todos los análisis pasados
- Filtrar por tipo de modelo y estado
- Ver resultados JSON completos en formato de tarjeta
- Ver estadísticas de procesamiento

### 📈 Página de Estadísticas
- Ver estadísticas agregadas
- Gráficos de distribución de especies
- Tendencias de análisis en el tiempo
- Comparación de uso de modelos

### 📚 Página Ayuda
- Preguntas frecuentes
- Materia de apoyo
- Documentación disponible en línea

### ℹ️ Página Acerca de
- Información y comparaciones de modelos
- Especies soportadas
- Información de citación

### 🎨 Características de la Interfaz de Tarjetas
- **Diseño de Cuadrícula de 2 Columnas**: Navegación de imágenes estilo galería
- **Efectos Hover**: Animaciones suaves y sombras
- **Diseño Responsivo**: Se adapta al tamaño de pantalla
- **Detalles Plegables**: Mantén la interfaz limpia, expande cuando sea necesario
- **Acciones Integradas**: Ver y descargar directamente desde las tarjetas



## 🔌 Endpoints de la API

### Verificación de Salud

**GET** `/health`

Verifica si la API está funcionando y los modelos están cargados.

```json
{
  "status": "healthy",
  "models": {
    "herdnet": {"loaded": true, "num_classes": 7},
    "yolov11": {"loaded": true, "num_classes": 6}
  }
}
```

### Analizar con YOLO

**POST** `/analyze-yolo`

Sube un archivo ZIP para análisis con YOLOv11.

**Parámetros:**
- `file`: Archivo ZIP con imágenes (requerido)
- `conf_threshold`: Umbral de confianza (predeterminado: 0.25)
- `iou_threshold`: Umbral IOU para NMS (predeterminado: 0.45)
- `img_size`: Tamaño de imagen para inferencia (predeterminado: 640)
- `include_annotated_images`: Incluir imágenes anotadas (predeterminado: true)

**Respuesta:**
```json
{
  "success": true,
  "task_id": "123e4567-e89b-12d3-a456-426614174000",
  "model": "YOLOv11",
  "summary": {
    "total_images": 5,
    "total_detections": 47,
    "species_counts": {"buffalo": 15, "elephant": 12}
  },
  "detections": [...],
  "annotated_images": [...],
  "processing_time_seconds": 12.5
}
```

### Analizar con HerdNet

**POST** `/analyze-image`

Sube un archivo ZIP para análisis con HerdNet.

**Parámetros:**
- `file`: Archivo ZIP con imágenes (requerido)
- `patch_size`: Tamaño de parche para unión (predeterminado: 512)
- `overlap`: Superposición para unión (predeterminado: 160)
- `rotation`: Número de rotaciones de 90 grados (predeterminado: 0)
- `thumbnail_size`: Tamaño para miniaturas (predeterminado: 256)
- `include_thumbnails`: Incluir miniaturas (predeterminado: true)
- `include_plots`: Incluir gráficos de detección (predeterminado: false)

**Respuesta:**
```json
{
  "success": true,
  "task_id": "456e7890-e89b-12d3-a456-426614174111",
  "model": "HerdNet",
  "summary": {
    "total_images": 5,
    "total_detections": 82,
    "species_counts": {"buffalo": 25, "elephant": 18}
  },
  "detections": [...],
  "thumbnails": [...],
  "processing_time_seconds": 45.8
}
```

### Analizar Imagen Individual con YOLO

**POST** `/analyze-single-image-yolo`

Sube una imagen individual para análisis con YOLOv11.

**Parámetros:**
- `file`: Archivo de imagen individual (PNG, JPG, JPEG, GIF, WebP, BMP, TIFF) (requerido)
- `conf_threshold`: Umbral de confianza (predeterminado: 0.25)
- `iou_threshold`: Umbral IOU para NMS (predeterminado: 0.45)
- `img_size`: Tamaño de imagen para inferencia (predeterminado: 640)
- `include_annotated_images`: Incluir imágenes anotadas (predeterminado: true)

**Respuesta:** Mismo formato que análisis por lotes, pero con `total_images: 1`

### Analizar Imagen Individual con HerdNet

**POST** `/analyze-single-image-herdnet`

Sube una imagen individual para análisis con HerdNet (optimizado para imágenes aéreas/satelitales grandes).

**Parámetros:**
- `file`: Archivo de imagen individual (PNG, JPG, JPEG, GIF, WebP, BMP, TIFF) (requerido)
- `patch_size`: Tamaño de parche para unión (predeterminado: 512)
- `overlap`: Superposición para unión (predeterminado: 160)
- `rotation`: Número de rotaciones de 90 grados (predeterminado: 0)
- `thumbnail_size`: Tamaño para miniaturas (predeterminado: 256)
- `include_thumbnails`: Incluir miniaturas (predeterminado: true)
- `include_plots`: Incluir gráficos de detección (predeterminado: false)

**Respuesta:** Mismo formato que análisis por lotes, pero con `total_images: 1`

**💡 Consejo:** ¡Usa los endpoints de imagen individual para pruebas rápidas o cuando necesites análisis en tiempo real sin crear archivos ZIP!

### Obtener Tareas

**GET** `/tasks`

Lista todas las tareas de análisis con filtrado opcional.

**Parámetros de Consulta:**
- `model_type`: Filtrar por 'yolo' o 'herdnet'
- `status`: Filtrar por 'completed', 'processing', o 'failed'
- `limit`: Máximo de tareas a devolver (predeterminado: 100)
- `offset`: Desplazamiento de paginación (predeterminado: 0)

### Obtener Tarea por ID

**GET** `/tasks/<task_id>`

Recupera una tarea específica y sus resultados completos.

**La respuesta incluye:**
- Metadatos de la tarea (estado, marcas de tiempo, parámetros)
- Respuesta JSON completa con todas las detecciones
- Todas las imágenes codificadas en base64 (si se incluyeron en la solicitud original)

### Estadísticas de Base de Datos

**GET** `/database/stats`

Obtener estadísticas completas de la base de datos.

```json
{
  "success": true,
  "statistics": {
    "total_tasks": 150,
    "tasks_by_model": {"yolo": 85, "herdnet": 65},
    "total_detections": 8547,
    "species_distribution": {"buffalo": 2341, "elephant": 1876}
  }
}
```

## 💾 Características de la Base de Datos

### Qué se Almacena

Cada análisis almacena automáticamente:

**Para YOLO:**
- ✅ Todos los datos de detección (coordenadas, confianza, especies)
- ✅ Información completa de cajas delimitadoras
- ✅ **Todas las imágenes anotadas como base64** (si se solicita)
- ✅ Estadísticas resumidas y parámetros de procesamiento

**Para HerdNet:**
- ✅ Todos los datos de detección (puntos centrales, confianza, especies)
- ✅ **Todas las miniaturas de animales como base64** (si se solicita)
- ✅ **Todos los gráficos de detección como base64** (si se solicita)
- ✅ Estadísticas resumidas y parámetros de procesamiento

### Ejemplo de Flujo de Trabajo

```python
import requests

# 1. Ejecutar análisis
response = requests.post('http://localhost:8000/analyze-yolo', 
    files={'file': open('images.zip', 'rb')})
task_id = response.json()['task_id']

# 2. Recuperar resultados completos más tarde (incluso después de reiniciar el servidor)
task_response = requests.get(f'http://localhost:8000/tasks/{task_id}')
task = task_response.json()['task']

# Acceder a la respuesta JSON original completa
original_response = task['result_data']
base64_images = original_response.get('annotated_images', [])

# 3. Obtener solo detecciones
detections = requests.get(f'http://localhost:8000/tasks/{task_id}/detections')

# 4. Ver estadísticas
stats = requests.get('http://localhost:8000/database/stats')
```

## ☁️ Carga de Modelos desde Google Drive

Los modelos se descargan automáticamente desde Google Drive en la primera ejecución. Esto facilita el despliegue en plataformas en la nube como Streamlit Cloud sin comprometer archivos de modelos grandes en el repositorio.

**Características:**
- ✅ Descarga automática en la primera ejecución
- ✅ Almacenamiento en caché local para ejecuciones posteriores
- ✅ No se requiere descarga manual
- ✅ Perfecto para despliegue en Streamlit Cloud

**Archivos de Modelos:**
- `best.pt` (YOLOv11) 
- `herdnet_model.pth` (HerdNet) 

## 📊 Información de Modelos

### YOLOv11
- **Tipo:** Detección de objetos con caja delimitadora
- **Velocidad:** Rápido (~1-2s por imagen)
- **Mejor para:** Imágenes estándar, detección en tiempo real
- **Salida:** Cajas delimitadoras con puntuaciones de confianza

### HerdNet
- **Tipo:** Detección basada en puntos
- **Velocidad:** Moderada (depende del tamaño de la imagen)
- **Mejor para:** Imágenes aéreas/satelitales grandes
- **Salida:** Puntos centrales, miniaturas, gráficos

### Especies Soportadas
1. Búfalo (*Syncerus caffer*)
2. Elefante (*Loxodonta africana*)
3. Kob (*Kobus kob*)
4. Topi (*Damaliscus lunatus*)
5. Jabalí (*Phacochoerus africanus*)
6. Antílope Acuático (*Kobus ellipsiprymnus*)

## 🛠️ Estructura del Proyecto

```
back/
├── app.py                    # API Flask principal
├── streamlit_app.py          # Interfaz web Streamlit
├── database.py               # Módulo de base de datos SQLite
├── model_loader.py           # Script para descargar modelos desde Google Drive
├── requirements.txt         # Dependencias Python
├── README.md               # Archivo de contexto del proyecto
├── best.pt                 # Modelo YOLOv11 (auto-descargado)
├── herdnet_model.pth      # Modelo HerdNet (auto-descargado)
└── wildlife_detection.db  # Base de datos SQLite (auto-creada)
```

### Variables de entorno



### 📝 Variables Requeridas - Backend

#### 🔑 Configuración de Google Drive
```env
# ID de la carpeta de Google Drive donde están los modelos
GDRIVE_FOLDER_ID=TU_CARPETA_PUBLICA_DE_GOOGLE_DRIVE


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


### 📝 Variables Opcionales - Backend

```env
# Base de datos (opcional, por defecto: wildlife_detection.db)
DATABASE_NAME=wildlife_detection.db

# Tamaño máximo de archivo en MB (opcional)
MAX_UPLOAD_SIZE_MB=100

# Directorio temporal (opcional)
TEMP_DIR=/tmp/wildlife_detection
```



### 📝 Variables Esenciales - Frontend

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



## Despliegue en la Nube


### 📦 Requisitos Previos

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


## 🐳 Backend con Docker

### Opción 1: Despliegue Local (Desarrollo)

#### Paso 1: Clonar Repositorio

```bash
# Clonar proyecto
git clone https://github.com/marioguaqueta/maia-back-proyecto.git
cd maia-back-proyecto
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
# ID de la carpeta de Google Drive donde están los modelos
GDRIVE_FOLDER_ID=TU_CARPETA_PUBLICA_DE_GOOGLE_DRIVE

# Nombres de los archivos de modelos
YOLO_MODEL_FILENAME=best.pt
HERDNET_MODEL_FILENAME=herdnet_baseline_model.pth
```


#### Paso 3: Construir y Levantar Servicios

```bash
# Construir imagen Docker
docker-compose build --no-cache

# Iniciar servicios en segundo plano
docker-compose up -d

# Ver logs en tiempo real
docker-compose logs -f
```

#### Paso 4: Verificar Despliegue

```bash
# Verificar que el contenedor esté corriendo
docker-compose ps

```
---

## 🎨 Frontend con Streamlit

### Opción 1: Ejecución Local

#### Paso 1: Instalar Dependencias

```bash
# Navegar al proyecto
cd maia-back-proyecto

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

API_BASE_URL=http://public_ip:8000
```

#### Paso 3: Ejecutar Streamlit

```bash
# Iniciar aplicación
streamlit run streamlit_app.py

# La aplicación se abrirá en:
# http://localhost:8501
```

---
## 📚 Manual de usuario aplicación cliente

[Manual de usuario](https://github.com/MackieUni/Grupo12-ProyectoFinal/blob/main/docs/documentacion_app/MANUAL%20DE%20USUARIO%20DE%20SISTEMA%20DE%20DETECCI%C3%93N%20DE%20FAUNA%20AFRICANA.pdf)


## 📚 Citas

**HerdNet:**
```
Delplanque, A., Foucher, S., Lejeune, P., Linchant, J., & Théau, J. (2022).
Multispecies detection and identification of African mammals in aerial imagery 
using convolutional neural networks. Remote Sensing in Ecology and Conservation, 8(2), 166-179.
```

**YOLOv11:**
```
Ultralytics YOLOv11 (2024)
https://github.com/ultralytics/ultralytics
```

## 📄 Licencia

Este proyecto usa:
- **Modelo HerdNet**: Licencia MIT
- **YOLOv11**: Licencia AGPL-3.0 (Ultralytics)

## 🤝 Soporte

Para problemas relacionados con:
- **API/Streamlit**: Abre un issue en este repositorio
- **YOLOv11**: Visita https://github.com/ultralytics/ultralytics
- **HerdNet**: Visita https://github.com/Alexandre-Delplanque/HerdNet

## 🙏 Agradecimientos

- **YOLOv11** por Ultralytics
- **HerdNet** por Alexandre Delplanque (Universidad de Lieja)
- Investigación publicada en Remote Sensing in Ecology and Conservation

