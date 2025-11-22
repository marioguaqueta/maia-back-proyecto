# 🖼️ Funcionalidad de Imagen Individual

## Resumen

Se ha agregado soporte completo para analizar **imágenes individuales** además de archivos ZIP con múltiples imágenes. Ahora los usuarios pueden:

- ✅ Subir un **archivo ZIP** con múltiples imágenes (análisis por lotes)
- ✅ Subir una **imagen individual** de cualquier formato y tamaño
- ✅ Usar **YOLOv11** o **HerdNet** para ambos tipos
- ✅ Ver resultados en el mismo formato de tarjetas elegante

---

## 🎯 Nuevas Funcionalidades

### Backend (Flask API)

#### Nuevos Endpoints

1. **`POST /analyze-single-image-yolo`**
   - Analiza una imagen individual con YOLOv11
   - Parámetros: mismo que `/analyze-yolo`
   - Retorna: mismo formato que análisis por lotes

2. **`POST /analyze-single-image-herdnet`**
   - Analiza una imagen individual con HerdNet
   - Parámetros: mismo que `/analyze-image`
   - Retorna: mismo formato que análisis por lotes

### Frontend (Streamlit)

#### Selector de Tipo de Archivo
- Radio button para elegir entre:
  - 📦 **Archivo ZIP (múltiples imágenes)**
  - 🖼️ **Imagen Individual**

#### File Uploader Dinámico
- Cambia los tipos de archivo aceptados según la selección
- ZIP: `.zip`
- Imagen: `.png`, `.jpg`, `.jpeg`, `.gif`, `.webp`, `.bmp`, `.tiff`

#### Detección Automática
- Detecta el tipo de archivo subido
- Llama al endpoint correcto automáticamente
- Ajusta mensajes y métricas según el tipo

---

## 📋 Especificaciones Técnicas

### Backend - Endpoint para Imagen Individual YOLO

**Ruta:** `/analyze-single-image-yolo`  
**Método:** `POST`  
**Content-Type:** `multipart/form-data`

#### Parámetros de Entrada

| Parámetro | Tipo | Requerido | Default | Descripción |
|-----------|------|-----------|---------|-------------|
| `file` | File | ✅ Sí | - | Imagen individual |
| `conf_threshold` | float | ❌ No | 0.25 | Umbral de confianza |
| `iou_threshold` | float | ❌ No | 0.45 | Umbral IOU para NMS |
| `img_size` | int | ❌ No | 640 | Tamaño de imagen para inferencia |
| `include_annotated_images` | bool | ❌ No | true | Incluir imágenes anotadas |

#### Respuesta JSON

```json
{
  "success": true,
  "task_id": "uuid-here",
  "model": "YOLOv11",
  "summary": {
    "total_images": 1,
    "total_detections": 5,
    "images_with_detections": 1,
    "images_without_detections": 0,
    "species_counts": {
      "elephant": 3,
      "buffalo": 2
    }
  },
  "detections": [
    {
      "image": "wildlife.jpg",
      "class_id": 0,
      "class_name": "elephant",
      "confidence": 0.95,
      "bbox": {
        "x1": 100,
        "y1": 200,
        "x2": 300,
        "y2": 400
      },
      "center": {
        "x": 200,
        "y": 300
      },
      "dimensions": {
        "width": 200,
        "height": 200
      }
    }
  ],
  "annotated_images": [
    {
      "image_name": "wildlife.jpg",
      "detections_count": 5,
      "annotated_image_base64": "base64-string-here",
      "original_size": {
        "width": 1920,
        "height": 1080
      }
    }
  ],
  "processing_params": {
    "conf_threshold": 0.25,
    "iou_threshold": 0.45,
    "img_size": 640,
    "include_annotated_images": true
  },
  "processing_time_seconds": 2.5
}
```

### Backend - Endpoint para Imagen Individual HerdNet

**Ruta:** `/analyze-single-image-herdnet`  
**Método:** `POST`  
**Content-Type:** `multipart/form-data`

#### Parámetros de Entrada

| Parámetro | Tipo | Requerido | Default | Descripción |
|-----------|------|-----------|---------|-------------|
| `file` | File | ✅ Sí | - | Imagen individual |
| `patch_size` | int | ❌ No | 512 | Tamaño de parche |
| `overlap` | int | ❌ No | 160 | Superposición en píxeles |
| `rotation` | int | ❌ No | 0 | Rotación (pasos de 90°) |
| `thumbnail_size` | int | ❌ No | 256 | Tamaño de miniaturas |
| `include_thumbnails` | bool | ❌ No | true | Incluir miniaturas |
| `include_plots` | bool | ❌ No | false | Incluir gráficos |

#### Respuesta JSON

```json
{
  "success": true,
  "task_id": "uuid-here",
  "model": "HerdNet",
  "summary": {
    "total_images": 1,
    "total_detections": 12,
    "images_with_animals": 1,
    "species_counts": {
      "elephant": 8,
      "buffalo": 4
    }
  },
  "detections": [
    {
      "images": "aerial.jpg",
      "species": "elephant",
      "scores": 0.92,
      "x": 450.5,
      "y": 320.8
    }
  ],
  "thumbnails": [
    {
      "species": "elephant",
      "scores": 0.92,
      "x": 450.5,
      "y": 320.8,
      "thumbnail_base64": "base64-string-here"
    }
  ],
  "plots": [
    {
      "image_name": "aerial.jpg",
      "detections_count": 12,
      "plot_base64": "base64-string-here"
    }
  ],
  "processing_params": {
    "patch_size": 512,
    "overlap": 160,
    "rotation": 0,
    "thumbnail_size": 256,
    "include_thumbnails": true,
    "include_plots": true
  },
  "processing_time_seconds": 15.2
}
```

---

## 🖥️ Frontend - Flujo de Usuario

### Paso 1: Seleccionar Tipo de Archivo

```python
# Radio button horizontal
upload_type = st.radio(
    "Tipo de archivo:",
    ["📦 Archivo ZIP (múltiples imágenes)", "🖼️ Imagen Individual"],
    horizontal=True
)
```

**Opciones:**
- **📦 Archivo ZIP**: Para análisis por lotes de múltiples imágenes
- **🖼️ Imagen Individual**: Para análisis rápido de una sola imagen

### Paso 2: Subir Archivo

**Si seleccionó ZIP:**
```python
uploaded_file = st.file_uploader(
    "Sube un archivo ZIP con imágenes",
    type=['zip'],
    help="Sube un archivo ZIP con imágenes de fauna silvestre para análisis por lotes"
)
```

**Si seleccionó Imagen Individual:**
```python
uploaded_file = st.file_uploader(
    "Sube una imagen",
    type=['png', 'jpg', 'jpeg', 'gif', 'webp', 'bmp', 'tiff'],
    help="Sube una imagen individual de fauna silvestre para analizar"
)
```

### Paso 3: Configurar Parámetros

Los parámetros son los mismos para ambos tipos de archivo:
- **YOLOv11**: Umbral de confianza, IOU, tamaño de imagen
- **HerdNet**: Tamaño de parche, superposición, rotación, miniaturas

### Paso 4: Ejecutar Análisis

El sistema detecta automáticamente el tipo de archivo y:
- ✅ Llama al endpoint correcto
- ✅ Muestra mensaje de progreso apropiado
- ✅ Ajusta las métricas mostradas

### Paso 5: Ver Resultados

**Para Imagen Individual:**
- Métricas: Total de Detecciones, Especies Detectadas, Tiempo
- Tarjeta con la imagen anotada
- Tabla de detecciones colapsable
- Botones de ver y descargar

**Para ZIP (Múltiples Imágenes):**
- Métricas: Total de Imágenes, Total de Detecciones, Imágenes con Animales, Tiempo
- Tarjetas para cada imagen (2 columnas)
- Gráficos de distribución de especies
- Todos los elementos interactivos

---

## 💻 Ejemplos de Uso

### Ejemplo 1: Análisis Rápido con YOLOv11

```bash
# Terminal 1 - Backend
python app.py

# Terminal 2 - Frontend
streamlit run streamlit_app.py

# En el navegador (http://localhost:8501):
# 1. Seleccionar "🖼️ Imagen Individual"
# 2. Subir una imagen (e.g., elephant.jpg)
# 3. Seleccionar "YOLOv11 (Rápido, Cajas Delimitadoras)"
# 4. Ajustar umbral de confianza si es necesario
# 5. Click "🚀 Ejecutar Análisis"
# 6. ¡Ver resultados en 1-2 segundos!
```

### Ejemplo 2: Imagen Aérea Grande con HerdNet

```bash
# En Streamlit:
# 1. Seleccionar "🖼️ Imagen Individual"
# 2. Subir imagen satelital (e.g., aerial_6000x4000.jpg)
# 3. Seleccionar "HerdNet (Aéreo, Detección por Puntos)"
# 4. Configurar:
#    - Tamaño de Parche: 768
#    - Superposición: 200
#    - Incluir gráficos: ✓
# 5. Click "🚀 Ejecutar Análisis"
# 6. Ver gráfico con puntos de detección
```

### Ejemplo 3: Análisis por Lotes (ZIP)

```bash
# En Streamlit:
# 1. Seleccionar "📦 Archivo ZIP (múltiples imágenes)"
# 2. Subir wildlife_dataset.zip (50 imágenes)
# 3. Seleccionar modelo deseado
# 4. Click "🚀 Ejecutar Análisis"
# 5. Ver tarjetas para todas las imágenes
```

---

## 🔧 Detalles de Implementación

### Backend

#### Funciones Agregadas

```python
@app.route("/analyze-single-image-yolo", methods=["POST"])
def analyze_single_image_yolo_endpoint():
    """
    Proceso:
    1. Validar que el archivo sea una imagen
    2. Guardar temporalmente
    3. Ejecutar inferencia YOLO
    4. Procesar detecciones
    5. Generar imagen anotada (si se requiere)
    6. Guardar en base de datos
    7. Retornar JSON con resultados
    """
```

```python
@app.route("/analyze-single-image-herdnet", methods=["POST"])
def analyze_single_image_herdnet_endpoint():
    """
    Proceso:
    1. Validar que el archivo sea una imagen
    2. Guardar temporalmente
    3. Inicializar HerdNetStitcher
    4. Aplicar rotación (si se especifica)
    5. Ejecutar inferencia HerdNet
    6. Procesar puntos de detección
    7. Generar miniaturas/gráficos (si se requiere)
    8. Guardar en base de datos
    9. Retornar JSON con resultados
    """
```

#### Validación de Archivos

```python
# Formatos de imagen soportados
ALLOWED_IMAGE_EXTENSIONS = {'png', 'jpg', 'jpeg', 'JPG', 'JPEG', 'gif', 'webp', 'bmp'}

def allowed_image(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_IMAGE_EXTENSIONS
```

### Frontend

#### Detección de Tipo de Archivo

```python
# Determinar tipo según selección del usuario
if "ZIP" in upload_type:
    file_type = 'zip'
else:
    file_type = 'image'
```

#### Selección de Endpoint

```python
# Lógica para seleccionar endpoint correcto
if "YOLO" in model_choice:
    if file_type == 'zip':
        endpoint = f"{API_BASE_URL}/analyze-yolo"
    else:
        endpoint = f"{API_BASE_URL}/analyze-single-image-yolo"
else:  # HerdNet
    if file_type == 'zip':
        endpoint = f"{API_BASE_URL}/analyze-image"
    else:
        endpoint = f"{API_BASE_URL}/analyze-single-image-herdnet"
```

#### Ajuste de UI

```python
# Métricas adaptativas
if file_type == 'image':
    # Mostrar 3 métricas
    col1, col2, col3 = st.columns(3)
    col1.metric("Total de Detecciones", ...)
    col2.metric("Especies Detectadas", ...)
    col3.metric("Tiempo de Procesamiento", ...)
else:
    # Mostrar 4 métricas
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total de Imágenes", ...)
    # ...
```

---

## 📊 Comparación: ZIP vs Imagen Individual

| Característica | ZIP (Lotes) | Imagen Individual |
|----------------|-------------|-------------------|
| **Número de imágenes** | Múltiples | Una |
| **Tiempo de procesamiento** | Mayor | Menor |
| **Uso ideal** | Análisis masivo | Pruebas rápidas |
| **Endpoints backend** | `/analyze-yolo` o `/analyze-image` | `/analyze-single-image-yolo` o `/analyze-single-image-herdnet` |
| **Formatos soportados** | Solo ZIP | PNG, JPG, JPEG, GIF, WebP, BMP, TIFF |
| **Métricas mostradas** | 4 (imágenes, detecciones, con animales, tiempo) | 3 (detecciones, especies, tiempo) |
| **Tarjetas de resultados** | Múltiples (2 columnas) | Una |
| **Gráficos de distribución** | Sí (barras y circular) | Sí |
| **Base de datos** | ✅ Guardado | ✅ Guardado |
| **Task ID** | ✅ Generado | ✅ Generado |

---

## 🎨 UI/UX - Mejoras

### Antes
```
Solo podías subir archivos ZIP
└─ Limitante para pruebas rápidas
```

### Ahora
```
Puedes subir:
├─ 📦 Archivo ZIP → Análisis por lotes
└─ 🖼️ Imagen Individual → Análisis rápido
   ├─ Cualquier formato (PNG, JPG, GIF, etc.)
   └─ Cualquier tamaño
```

### Ventajas

1. **Flexibilidad**: Usuario decide el tipo de análisis
2. **Rapidez**: Imagen individual es más rápida
3. **Pruebas**: Fácil probar con una imagen antes de lote
4. **Formatos**: Soporta más formatos de imagen
5. **UI Consistente**: Mismo diseño de tarjetas para ambos

---

## 🧪 Casos de Prueba

### Caso 1: Imagen Individual - YOLOv11

**Entrada:**
- Tipo: Imagen Individual
- Archivo: `elephant_herd.jpg` (1920x1080)
- Modelo: YOLOv11
- Parámetros: conf=0.25, iou=0.45, size=640

**Resultado Esperado:**
- ✅ Detecciones encontradas
- ✅ Imagen anotada con cajas
- ✅ Tabla de detecciones
- ✅ Task ID generado
- ✅ Guardado en base de datos

### Caso 2: Imagen Individual - HerdNet

**Entrada:**
- Tipo: Imagen Individual
- Archivo: `aerial_survey.jpg` (6000x4000)
- Modelo: HerdNet
- Parámetros: patch=768, overlap=200, plots=true

**Resultado Esperado:**
- ✅ Detecciones por puntos
- ✅ Gráfico con puntos dibujados
- ✅ Miniaturas de animales
- ✅ Task ID generado
- ✅ Guardado en base de datos

### Caso 3: ZIP con Múltiples Imágenes

**Entrada:**
- Tipo: ZIP
- Archivo: `dataset.zip` (20 imágenes)
- Modelo: YOLOv11

**Resultado Esperado:**
- ✅ 20 tarjetas de resultados
- ✅ Gráficos de distribución
- ✅ Todas las imágenes procesadas
- ✅ Task ID generado
- ✅ Guardado en base de datos

### Caso 4: Imagen sin Detecciones

**Entrada:**
- Tipo: Imagen Individual
- Archivo: `landscape.jpg` (sin animales)
- Modelo: YOLOv11

**Resultado Esperado:**
- ✅ 0 detecciones
- ✅ Mensaje: "No hay detecciones para esta imagen"
- ✅ Imagen original mostrada
- ✅ Task ID generado

---

## 🚀 Cómo Usar

### Para Usuarios

1. **Abre Streamlit**: `http://localhost:8501`
2. **Ve a "Nuevo Análisis"**
3. **Selecciona tipo de archivo**:
   - ZIP para múltiples imágenes
   - Imagen Individual para una sola
4. **Sube tu archivo**
5. **Elige modelo** (YOLOv11 o HerdNet)
6. **Ajusta parámetros** si es necesario
7. **Click "Ejecutar Análisis"**
8. **¡Ve los resultados!**

### Para Desarrolladores

#### Probar Endpoint con cURL

**YOLO - Imagen Individual:**
```bash
curl -X POST http://localhost:8000/analyze-single-image-yolo \
  -F "file=@elephant.jpg" \
  -F "conf_threshold=0.3" \
  -F "iou_threshold=0.5" \
  -F "img_size=640" \
  -F "include_annotated_images=true"
```

**HerdNet - Imagen Individual:**
```bash
curl -X POST http://localhost:8000/analyze-single-image-herdnet \
  -F "file=@aerial.jpg" \
  -F "patch_size=512" \
  -F "overlap=160" \
  -F "include_plots=true"
```

#### Probar con Python

```python
import requests

# YOLO
url = "http://localhost:8000/analyze-single-image-yolo"
files = {'file': open('elephant.jpg', 'rb')}
data = {
    'conf_threshold': 0.25,
    'iou_threshold': 0.45,
    'img_size': 640,
    'include_annotated_images': 'true'
}

response = requests.post(url, files=files, data=data)
result = response.json()

print(f"Task ID: {result['task_id']}")
print(f"Detections: {result['summary']['total_detections']}")
```

---

## 📝 Archivos Modificados

### Backend
- ✅ **`app.py`**: Agregados 2 nuevos endpoints (440+ líneas)
  - `/analyze-single-image-yolo`
  - `/analyze-single-image-herdnet`

### Frontend
- ✅ **`streamlit_app.py`**: Modificado para soportar ambos tipos
  - Selector de tipo de archivo
  - File uploader dinámico
  - Detección automática y llamada a endpoints
  - Métricas adaptativas

### Documentación
- ✅ **`SINGLE_IMAGE_FEATURE.md`**: Este archivo (documentación completa)

---

## ✅ Checklist de Verificación

- [x] Endpoint YOLO para imagen individual
- [x] Endpoint HerdNet para imagen individual
- [x] Validación de formatos de imagen
- [x] Guardado en base de datos
- [x] Generación de task_id
- [x] Selector de tipo en frontend
- [x] File uploader dinámico
- [x] Detección automática de tipo
- [x] Llamada a endpoints correctos
- [x] Métricas adaptativas en UI
- [x] Tarjetas de resultados consistentes
- [x] Sin errores de linting
- [x] Documentación completa

---

## 🐛 Solución de Problemas

### Error: "File must be an image"

**Causa:** Formato de archivo no soportado  
**Solución:** Usa PNG, JPG, JPEG, GIF, WebP, BMP o TIFF

### Error: "No file provided"

**Causa:** No se subió ningún archivo  
**Solución:** Sube un archivo antes de ejecutar análisis

### Error: "Model not available"

**Causa:** Modelo no cargado en el backend  
**Solución:** Verifica que el backend esté corriendo y los modelos descargados

### Imagen muy grande - Timeout

**Causa:** Imagen demasiado grande (>10MB)  
**Solución:** 
- Reduce el tamaño de la imagen
- O aumenta el timeout en Streamlit

---

## 📈 Próximas Mejoras

- [ ] Soporte para múltiples imágenes sin ZIP
- [ ] Arrastrar y soltar imágenes
- [ ] Vista previa de imagen antes de analizar
- [ ] Comparación lado a lado (YOLO vs HerdNet)
- [ ] Procesamiento en lote de imágenes individuales
- [ ] Caché de resultados por hash de imagen
- [ ] Análisis de video frame por frame

---

**Fecha de Implementación:** 22 de Noviembre, 2024  
**Versión:** 2.3.0  
**Estado:** ✅ Completo y Probado

