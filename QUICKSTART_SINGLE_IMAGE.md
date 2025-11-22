# 🚀 Inicio Rápido - Análisis de Imagen Individual

## ✨ Nueva Funcionalidad

Ahora puedes analizar **imágenes individuales** sin necesidad de crear archivos ZIP!

---

## 🎯 Cómo Usar (Streamlit)

### 1. Inicia la Aplicación

```bash
# Terminal 1 - Backend
python app.py

# Terminal 2 - Frontend
streamlit run streamlit_app.py
```

### 2. Selecciona el Tipo de Archivo

En la página "Nuevo Análisis", verás un selector:

```
Tipo de archivo:
○ 📦 Archivo ZIP (múltiples imágenes)
● 🖼️ Imagen Individual
```

**Selecciona "Imagen Individual"**

### 3. Sube tu Imagen

- Formatos soportados: PNG, JPG, JPEG, GIF, WebP, BMP, TIFF
- Cualquier tamaño (hasta límites del servidor)
- Arrástrala o haz clic para seleccionar

### 4. Elige el Modelo

- **YOLOv11**: Rápido, cajas delimitadoras
- **HerdNet**: Imágenes aéreas, detección por puntos

### 5. Ajusta Parámetros (Opcional)

**YOLO:**
- Umbral de Confianza: 0.25 (default)
- Umbral IOU: 0.45 (default)
- Tamaño de Imagen: 640 (default)

**HerdNet:**
- Tamaño de Parche: 512 (default)
- Superposición: 160 (default)
- Incluir gráficos: ✓

### 6. Ejecuta el Análisis

Click en **"🚀 Ejecutar Análisis"**

### 7. ¡Ve los Resultados!

Verás:
- 📊 Métricas del resumen
- 🖼️ Tarjeta con imagen anotada
- 📋 Tabla de detecciones (colapsable)
- 🔍 Visor con zoom
- ⬇️ Botón de descarga

---

## 💻 Cómo Usar (API Directa)

### YOLO - Imagen Individual

```bash
curl -X POST http://localhost:8000/analyze-single-image-yolo \
  -F "file=@elephant.jpg" \
  -F "conf_threshold=0.3" \
  -F "iou_threshold=0.5" \
  -F "img_size=640"
```

### HerdNet - Imagen Individual

```bash
curl -X POST http://localhost:8000/analyze-single-image-herdnet \
  -F "file=@aerial_image.jpg" \
  -F "patch_size=768" \
  -F "overlap=200" \
  -F "include_plots=true"
```

### Python

```python
import requests

# YOLO
url = "http://localhost:8000/analyze-single-image-yolo"
files = {'file': open('wildlife.jpg', 'rb')}
data = {
    'conf_threshold': 0.25,
    'img_size': 640
}

response = requests.post(url, files=files, data=data)
result = response.json()

print(f"Task ID: {result['task_id']}")
print(f"Detections: {result['summary']['total_detections']}")
print(f"Species: {result['summary']['species_counts']}")
```

---

## 🆚 ZIP vs Imagen Individual

| Característica | ZIP | Imagen Individual |
|----------------|-----|-------------------|
| **Velocidad** | ⚫⚫⚫⚪⚪ | ⚫⚫⚫⚫⚫ |
| **Uso ideal** | Análisis masivo | Pruebas rápidas |
| **Tiempo típico** | Minutos | Segundos |
| **Formatos** | Solo ZIP | PNG, JPG, GIF, WebP, BMP, TIFF |
| **Setup requerido** | Crear ZIP | Ninguno |

---

## 📊 Ejemplo de Respuesta

```json
{
  "success": true,
  "task_id": "abc-123-def-456",
  "model": "YOLOv11",
  "summary": {
    "total_images": 1,
    "total_detections": 5,
    "images_with_detections": 1,
    "species_counts": {
      "elephant": 3,
      "buffalo": 2
    }
  },
  "detections": [
    {
      "image": "wildlife.jpg",
      "class_name": "elephant",
      "confidence": 0.95,
      "bbox": {"x1": 100, "y1": 200, "x2": 300, "y2": 400},
      "center": {"x": 200, "y": 300}
    }
  ],
  "annotated_images": [{
    "image_name": "wildlife.jpg",
    "detections_count": 5,
    "annotated_image_base64": "...",
    "original_size": {"width": 1920, "height": 1080}
  }],
  "processing_time_seconds": 1.8
}
```

---

## 💡 Casos de Uso

### 1. Prueba Rápida
Prueba diferentes parámetros en una imagen antes de procesar un lote completo.

```
1. Sube una imagen de prueba
2. Ajusta conf_threshold: 0.2
3. Ve resultados
4. Ajusta conf_threshold: 0.3
5. Compara resultados
```

### 2. Análisis en Tiempo Real
Analiza imágenes conforme llegan sin crear ZIPs.

```
Nueva imagen capturada → Sube directamente → Resultados inmediatos
```

### 3. Imágenes Aéreas Grandes
Procesa imágenes satelitales grandes con HerdNet.

```
Imagen: 6000x4000px
Modelo: HerdNet
Patch: 768
Resultado: Detecciones precisas con gráfico
```

---

## ⚡ Ventajas

✅ **Más Rápido**: No necesitas crear archivos ZIP  
✅ **Más Simple**: Sube directamente desde tu explorador  
✅ **Más Flexible**: Soporta múltiples formatos de imagen  
✅ **Ideal para Testing**: Prueba parámetros rápidamente  
✅ **Mismo UI**: Tarjetas elegantes, zoom, descarga  
✅ **Base de Datos**: Se guarda igual que análisis por lotes  

---

## 🐛 Solución de Problemas

### ❌ "File must be an image"

**Solución:** Usa PNG, JPG, JPEG, GIF, WebP, BMP o TIFF

### ❌ Imagen muy grande - Timeout

**Solución:** 
- Reduce el tamaño de la imagen
- Usa HerdNet con patches grandes
- Aumenta timeout del servidor

### ❌ "Model not available"

**Solución:** 
- Verifica que el backend esté corriendo
- Espera a que los modelos se descarguen (primera ejecución)
- Revisa logs del backend

---

## 📚 Más Información

- **Documentación Completa:** `SINGLE_IMAGE_FEATURE.md`
- **API Endpoints:** Ver `README.md` sección "API Endpoints"
- **Changelog:** Ver `CHANGELOG.md` versión 2.3.0

---

## 🎉 ¡Listo!

Ahora tienes dos formas de analizar imágenes:

1. **📦 ZIP (Lotes)** → Para procesar muchas imágenes
2. **🖼️ Individual** → Para análisis rápido y pruebas

**¡Elige el que mejor se adapte a tu necesidad!** 🚀

