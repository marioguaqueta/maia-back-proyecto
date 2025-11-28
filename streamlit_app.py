"""
Interfaz Web Streamlit para API de Detección de Fauna Silvestre
"""

import streamlit as st
import requests
import json
import base64
from io import BytesIO
from PIL import Image
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from datetime import datetime
import os
import toml
import numpy as np

config = toml.load(".streamlit/config.toml")
max_mb = config["server"]["maxUploadSize"]

# Configuración - puede ser sobrescrita por variable de entorno o secretos de Streamlit
API_BASE_URL = os.getenv(
    "API_BASE_URL",
    st.secrets.get("API_BASE_URL", "http://localhost:8000")
)

ADMIN_EMAIL = os.getenv(
    "ADMIN_EMAIL",
    st.secrets.get("ADMIN_EMAIL", "info@grupo12.yolomodel.com")
)

EXPLAIN_VIDEO_URL = os.getenv(
    "EXPLAIN_VIDEO_URL",
    st.secrets.get("EXPLAIN_VIDEO_URL", "https://example.com/tutorials")
)

DOCS_URL = os.getenv(
    "DOCS_URL",
    st.secrets.get("DOCS_URL", "https://example.com/docs")
)

# ========================================
# YOLOv11 UI Configuration
# ========================================
# Confidence Threshold Slider
YOLO_CONF_MIN = float(os.getenv("YOLO_CONF_MIN", "0.1"))
YOLO_CONF_MAX = float(os.getenv("YOLO_CONF_MAX", "0.9"))
YOLO_CONF_DEFAULT = float(os.getenv("YOLO_CONF_DEFAULT", "0.25"))
YOLO_CONF_STEP = float(os.getenv("YOLO_CONF_STEP", "0.05"))

# IOU Threshold Slider
YOLO_IOU_MIN = float(os.getenv("YOLO_IOU_MIN", "0.1"))
YOLO_IOU_MAX = float(os.getenv("YOLO_IOU_MAX", "0.9"))
YOLO_IOU_DEFAULT = float(os.getenv("YOLO_IOU_DEFAULT", "0.45"))
YOLO_IOU_STEP = float(os.getenv("YOLO_IOU_STEP", "0.05"))

# Image Size Options
YOLO_IMG_SIZES = [int(x) for x in os.getenv("YOLO_IMG_SIZES", "416,480,640,800,960,1280,2560,5120,10240").split(",")]
YOLO_IMG_SIZE_DEFAULT_INDEX = int(os.getenv("YOLO_IMG_SIZE_DEFAULT_INDEX", "2"))

# ========================================
# Model Availability Configuration
# ========================================
# Enable/Disable HerdNet model in UI
ENABLE_HERDNET = os.getenv("ENABLE_HERDNET", "true").lower() in ("true", "1", "yes", "on")

# ========================================
# HerdNet UI Configuration
# ========================================
# Patch Size Options
HERDNET_PATCH_SIZES = [int(x) for x in os.getenv("HERDNET_PATCH_SIZES", "384,512,768,1024,2048,4096,8192,16384").split(",")]
HERDNET_PATCH_SIZE_DEFAULT_INDEX = int(os.getenv("HERDNET_PATCH_SIZE_DEFAULT_INDEX", "1"))

# Rotation Options
HERDNET_ROTATION_OPTIONS = [int(x) for x in os.getenv("HERDNET_ROTATION_OPTIONS", "0,1,2,3").split(",")]
HERDNET_ROTATION_DEFAULT_INDEX = int(os.getenv("HERDNET_ROTATION_DEFAULT_INDEX", "0"))

# Overlap Slider
HERDNET_OVERLAP_MIN = int(os.getenv("HERDNET_OVERLAP_MIN", "0"))
HERDNET_OVERLAP_MAX = int(os.getenv("HERDNET_OVERLAP_MAX", "300"))
HERDNET_OVERLAP_DEFAULT = int(os.getenv("HERDNET_OVERLAP_DEFAULT", "160"))
HERDNET_OVERLAP_STEP = int(os.getenv("HERDNET_OVERLAP_STEP", "16"))

# Thumbnail Size Slider
HERDNET_THUMBNAIL_MIN = int(os.getenv("HERDNET_THUMBNAIL_MIN", "128"))
HERDNET_THUMBNAIL_MAX = int(os.getenv("HERDNET_THUMBNAIL_MAX", "512"))
HERDNET_THUMBNAIL_DEFAULT = int(os.getenv("HERDNET_THUMBNAIL_DEFAULT", "256"))
HERDNET_THUMBNAIL_STEP = int(os.getenv("HERDNET_THUMBNAIL_STEP", "32"))

# ========================================
# Image Zoom Configuration
# ========================================
# Zoom Control Parameters
# Image Zoom Configuration with Plotly
# -------------------------------------
# Plotly provides interactive zoom/pan controls
# To avoid WebSocket overload with large images, we downsample for display
PLOTLY_MAX_DIMENSION = int(os.getenv("PLOTLY_MAX_DIMENSION", "1500"))  # Max width or height for Plotly display
PLOTLY_FALLBACK_THRESHOLD = int(os.getenv("PLOTLY_FALLBACK_THRESHOLD", "3000"))  # Use st.image for images larger than this

# Configuración de página
st.set_page_config(
    page_title="Detección de Fauna Africana",
    page_icon="🐘",
    layout="wide"
)

# CSS personalizado
st.markdown("""
<style>
/* Usar todo el ancho de la página */
.stApp {
    max-width: 100%;
    padding-left: 1rem;
    padding-right: 1rem;
}

/* Remover padding adicional del contenedor principal */
.main .block-container {
    max-width: 100%;
    padding-left: 2rem;
    padding-right: 2rem;
    padding-top: 2rem;
}

/* Ajustar para pantallas muy pequeñas */
@media (max-width: 768px) {
    .main .block-container {
        padding-left: 1rem;
        padding-right: 1rem;
    }
}

.upload-section {
    padding: 2rem;
    border-radius: 10px;
    background-color: #f0f2f6;
}

/* Estilos para tarjetas de resultados */
.result-card {
    border: 2px solid #e0e0e0;
    border-radius: 12px;
    padding: 20px;
    background: linear-gradient(135deg, #fafafa 0%, #f5f5f5 100%);
    margin-bottom: 25px;
    box-shadow: 0 2px 8px rgba(0,0,0,0.1);
    transition: all 0.3s ease;
}

.result-card:hover {
    box-shadow: 0 4px 16px rgba(0,0,0,0.15);
    transform: translateY(-2px);
}

.card-header {
    margin-top: 0;
    color: #2c3e50;
    font-size: 18px;
    font-weight: 600;
}

.card-subtitle {
    color: #666;
    font-size: 14px;
    margin-top: 5px;
    margin-bottom: 15px;
}

.detection-badge {
    display: inline-block;
    background-color: #4CAF50;
    color: white;
    padding: 4px 12px;
    border-radius: 12px;
    font-size: 13px;
    font-weight: 600;
    margin-right: 8px;
}

.size-badge {
    display: inline-block;
    background-color: #2196F3;
    color: white;
    padding: 4px 12px;
    border-radius: 12px;
    font-size: 13px;
    font-weight: 600;
}

/* Estilos para expandibles */
.stExpander {
    border: 1px solid #e0e0e0;
    border-radius: 8px;
    background-color: white;
    margin-top: 10px;
}

/* Contenedor de imagen */
.image-container {
    border-radius: 8px;
    overflow: hidden;
    margin: 15px 0;
    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}


/* ============================================
   BOTÓN: Reemplazar “Browse files”
   ============================================ */

/* Oculta el texto original del botón */
[data-testid="stFileUploader"] [data-testid="stBaseButton-secondary"] {
    font-size: 0 !important;
}

/* Inserta texto nuevo */
[data-testid="stFileUploader"] [data-testid="stBaseButton-secondary"]::after {
    content: "Examinar archivos" !important;
    font-size: 14px !important;
    font-weight: 500 !important;
}

/* ============================================
   TEXTO PRINCIPAL: “Drag and drop file here”
   ============================================ */

/* Oculta SOLO el texto principal (primer span dentro del div de instrucciones) */
[data-testid="stFileUploaderDropzoneInstructions"] div span:nth-of-type(1) {
    font-size: 0 !important;
}

[data-testid="stFileUploaderDropzoneInstructions"] div span:nth-of-type(1)::after {
    content: "Arrastra y suelta el archivo aquí" !important;
    font-size: 14px !important;
}

/* ============================================
   TEXTO SECUNDARIO: “Limit XMB per file • ZIP”
   ============================================ */

/* Oculta el texto secundario (segundo span dentro del div) */
[data-testid="stFileUploaderDropzoneInstructions"] div span:nth-of-type(2) {
    font-size: 0 !important;
}

[data-testid="stFileUploaderDropzoneInstructions"] div span:nth-of-type(2)::after {
    content: f"Límite {max_mb}MB por archivo • ZIP" !important;
    font-size: 12px !important;
    opacity: 0.85;
}

</style>
""", unsafe_allow_html=True)





def main():
    """Aplicación principal de Streamlit."""
    st.title("🦁 Sistema de Detección de Fauna Africana")
    st.markdown(f"Impulsado por modelos de aprendizaje profundo YOLOv11 {'y HerdNet' if ENABLE_HERDNET else ''}")
    
    # Navegación en la barra lateral
    page = st.sidebar.selectbox(
        "Navegación",
        ["🎯 Nuevo Análisis", "📊 Ver Resultados", "📈 Estadísticas", "📚 Ayuda", "ℹ️ Acerca de"]
    )
    
    if page == "🎯 Nuevo Análisis":
        new_analysis_page()
    elif page == "📊 Ver Resultados":
        view_results_page()
    elif page == "📈 Estadísticas":
        statistics_page()
    elif page == "📚 Ayuda":
        help_page()
    elif page == "ℹ️ Acerca de":
        about_page()


def new_analysis_page():
    """Página para crear nuevo análisis."""
    st.header("🎯 Nuevo Análisis de Detección de Fauna")
    
    # Verificar estado de la API
    try:
        response = requests.get(f"{API_BASE_URL}/health")
        health = response.json()
        
        col1, col2 = st.columns(2)
        with col1:
            st.success(f"✓ Estado del servicio: {health['status']}. La herramienta está lista para ser usada.")
        with col2:
            models_info = health.get('models', {})
            yolo_status = "✓ Cargado" if models_info.get('yolov11', {}).get('loaded') else "✗ No cargado"
            
            if ENABLE_HERDNET:
                herdnet_status = "✓ Cargado" if models_info.get('herdnet', {}).get('loaded') else "✗ No cargado"
                st.info(f"YOLOv11: {yolo_status} | HerdNet: {herdnet_status}")
            else:
                st.info(f"YOLOv11: {yolo_status}")
    except:
        st.error(f"❌ No se puede conectar con el servicio. Por favor, contacta al administrador de la plataforma para resolver el problema al correo {ADMIN_EMAIL}.")
        return
    
    st.markdown("---")
    
    # Carga de archivos
    st.subheader("📁 Cargar Imágenes")
    
    # Opción de tipo de archivo
    upload_type = st.radio(
        "Tipo de archivo:",
        ["📦 Archivo ZIP (múltiples imágenes)", "🖼️ Imagen Individual"],
        horizontal=True
    )
    
    # File uploader según el tipo
    if "ZIP" in upload_type:
        uploaded_file = st.file_uploader(
            f"📦 Selecciona tu archivo ZIP, da click en el botón 'Examinar archivos' para seleccionar el archivo o arrastra y suelta el archivo aquí. Máximo tamaño {max_mb}MB",
            type=['zip'],
            help="El archivo ZIP debe contener imágenes de fauna silvestre en formato JPG, PNG o JPEG. Puedes incluir múltiples imágenes para procesamiento por lotes.",
            label_visibility="visible",
            key="zip_uploader"
        )
        file_type = 'zip'
    else:
        uploaded_file = st.file_uploader(
            f"🖼️ Selecciona tu imagen, da click en el botón 'Examinar archivos' para seleccionar el archivo o arrastra y suelta el archivo aquí. Máximo tamaño {max_mb}MB",
            type=['png', 'jpg', 'jpeg'],
            help="Formatos soportados: PNG, JPG, JPEG. La imagen será analizada para detectar fauna silvestre.",
            label_visibility="visible",
            key="image_uploader"
        )
        file_type = 'image'
    
    if not uploaded_file:
        if file_type == 'zip':
            st.info("👆 Por favor sube un archivo ZIP para continuar")
        else:
            st.info("👆 Por favor sube una imagen para continuar")
        return
    
    # Mostrar información del archivo
    file_size_kb = uploaded_file.size / 1024
    file_size_mb = file_size_kb / 1024
    
    if file_size_mb > 1:
        size_display = f"{file_size_mb:.1f} MB"
    else:
        size_display = f"{file_size_kb:.1f} KB"
    
    st.success(f"✓ Archivo cargado: {uploaded_file.name} ({size_display})")
    
    # Selección de modelo
    st.subheader("🤖 Selección de Modelo")
    
    # Build model options based on availability
    model_options = ["YOLOv11 (Cajas Delimitadoras)"]
    if ENABLE_HERDNET:
        model_options.append("HerdNet (Detección por Puntos)")
    
    # Show appropriate help text
    if ENABLE_HERDNET:
        help_text = "YOLOv11: Detección rápida con cajas delimitadoras | HerdNet: Optimizado para imágenes aéreas con detección por puntos"
    else:
        help_text = "YOLOv11: Detección rápida con cajas delimitadoras. Modelo optimizado para identificación de fauna silvestre."
    
    model_choice = st.radio(
        "Elige el modelo de detección:",
        model_options,
        help=help_text
    )
    
    # Parámetros según el modelo
    st.subheader("⚙️ Parámetros")
    
    if "YOLO" in model_choice:
        col1, col2, col3 = st.columns(3)
        with col1:
            conf_threshold = st.slider(
                "Umbral de Confianza", 
                YOLO_CONF_MIN, 
                YOLO_CONF_MAX, 
                YOLO_CONF_DEFAULT, 
                YOLO_CONF_STEP
            )
        with col2:
            iou_threshold = st.slider(
                "Umbral de Coincidencia (IOU)", 
                YOLO_IOU_MIN, 
                YOLO_IOU_MAX, 
                YOLO_IOU_DEFAULT, 
                YOLO_IOU_STEP
            )
        with col3:
            img_size = st.selectbox(
                "Tamaño de Imagen", 
                YOLO_IMG_SIZES, 
                index=YOLO_IMG_SIZE_DEFAULT_INDEX
            )
        
        include_annotated = True
        
    else:  # HerdNet
        col1, col2 = st.columns(2)
        with col1:
            patch_size = st.selectbox(
                "Tamaño de Parche", 
                HERDNET_PATCH_SIZES, 
                index=HERDNET_PATCH_SIZE_DEFAULT_INDEX
            )
            rotation = st.selectbox(
                "Rotación (pasos de 90°)", 
                HERDNET_ROTATION_OPTIONS, 
                index=HERDNET_ROTATION_DEFAULT_INDEX
            )
        with col2:
            overlap = st.slider(
                "Superposición (píxeles)", 
                HERDNET_OVERLAP_MIN, 
                HERDNET_OVERLAP_MAX, 
                HERDNET_OVERLAP_DEFAULT, 
                HERDNET_OVERLAP_STEP
            )
            thumbnail_size = st.slider(
                "Tamaño de Miniatura", 
                HERDNET_THUMBNAIL_MIN, 
                HERDNET_THUMBNAIL_MAX, 
                HERDNET_THUMBNAIL_DEFAULT, 
                HERDNET_THUMBNAIL_STEP
            )
        
        col3, col4 = st.columns(2)
        with col3:
            include_thumbnails = False
        with col4:
            include_plots = True
    
    # Botón para ejecutar análisis
    st.markdown("---")
    if st.button("Ejecutar Análisis", type="primary", use_container_width=True):
        spinner_text = "Procesando imagen..." if file_type == 'image' else "Procesando imágenes... Esto puede tomar algunos minutos."
        
        with st.spinner(spinner_text):
            try:
                # Determinar endpoint según tipo de archivo y modelo
                if "YOLO" in model_choice:
                    if file_type == 'zip':
                        endpoint = f"{API_BASE_URL}/analyze-yolo"
                    else:
                        endpoint = f"{API_BASE_URL}/analyze-single-image-yolo"
                    
                    data = {
                        'conf_threshold': conf_threshold,
                        'iou_threshold': iou_threshold,
                        'img_size': img_size,
                        'include_annotated_images': str(include_annotated).lower()
                    }
                else:  # HerdNet
                    if file_type == 'zip':
                        endpoint = f"{API_BASE_URL}/analyze-image"
                    else:
                        endpoint = f"{API_BASE_URL}/analyze-single-image-herdnet"
                    
                    data = {
                        'patch_size': patch_size,
                        'overlap': overlap,
                        'rotation': rotation,
                        'thumbnail_size': thumbnail_size,
                        'include_thumbnails': str(include_thumbnails).lower(),
                        'include_plots': str(include_plots).lower()
                    }
                
                # Hacer solicitud
                response = requests.post(endpoint, files={'file': uploaded_file}, data=data)
                
                if response.status_code == 200:
                    result = response.json()
                    display_results(result, model_choice, file_type)
                else:
                    error_msg = response.json().get('message', response.json().get('error', 'Error desconocido'))
                    st.error(f"❌ Análisis fallido: Por favor comparte este mensaje al administrador para resolver el problema al {ADMIN_EMAIL}: {error_msg}")
                    
            except Exception as e:
                st.error(f"❌ Error: Por favor comparte este mensaje al administrador para resolver el problema al {ADMIN_EMAIL}: {str(e)}")


def create_detections_table(result, model_choice):
    """Crear una tabla mostrando detecciones por imagen y especie."""
    detections = result.get('detections', [])
    
    if not detections:
        return None
    
    # Obtener todas las especies del resultado
    species_counts = result.get('summary', {}).get('species_counts', {})
    all_species = sorted(species_counts.keys())
    
    # Crear un diccionario para almacenar conteos por imagen
    image_data = {}
    
    # Procesar detecciones según el tipo de modelo
    if "YOLO" in model_choice:
        for det in detections:
            img_name = det.get('image', 'Desconocido')
            species = det.get('class_name', 'Desconocido')
            
            if img_name not in image_data:
                image_data[img_name] = {sp: 0 for sp in all_species}
                image_data[img_name]['Total'] = 0
            
            image_data[img_name][species] = image_data[img_name].get(species, 0) + 1
            image_data[img_name]['Total'] += 1
    else:  # HerdNet
        for det in detections:
            img_name = det.get('images', 'Desconocido')
            species = det.get('species', 'Desconocido')
            
            if img_name not in image_data:
                image_data[img_name] = {sp: 0 for sp in all_species}
                image_data[img_name]['Total'] = 0
            
            image_data[img_name][species] = image_data[img_name].get(species, 0) + 1
            image_data[img_name]['Total'] += 1
    
    # Convertir a DataFrame
    rows = []
    for img_name, counts in image_data.items():
        row = {'Imagen': img_name, 'Total': counts['Total']}
        for species in all_species:
            row[species.capitalize()] = counts.get(species, 0)
        rows.append(row)
    
    df = pd.DataFrame(rows)
    
    # Reordenar columnas: Imagen, Total, luego especies
    cols = ['Imagen', 'Total'] + [sp.capitalize() for sp in all_species]
    df = df[cols]
    
    return df


def prepare_image_for_plotly(img, max_dimension=None):
    """
    Prepara una imagen PIL para visualización en Plotly.
    Reduce el tamaño si es necesario para evitar sobrecargar WebSocket.
    
    Args:
        img: PIL Image
        max_dimension: Dimensión máxima permitida (ancho o alto)
    
    Returns:
        tuple: (img_resized, was_resized, original_size, display_size)
    """
    if max_dimension is None:
        max_dimension = PLOTLY_MAX_DIMENSION
    
    original_width, original_height = img.size
    
    # Verificar si necesita redimensionamiento
    max_current = max(original_width, original_height)
    
    if max_current <= max_dimension:
        # No necesita redimensionamiento
        return img, False, (original_width, original_height), (original_width, original_height)
    
    # Calcular nuevas dimensiones manteniendo proporción
    scale = max_dimension / max_current
    new_width = int(original_width * scale)
    new_height = int(original_height * scale)
    
    # Redimensionar imagen para display
    img_resized = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
    
    return img_resized, True, (original_width, original_height), (new_width, new_height)


def should_use_plotly(img):
    """
    Determina si se debe usar Plotly o fallback a st.image.
    Imágenes muy grandes pueden sobrecargar WebSocket.
    
    Args:
        img: PIL Image
    
    Returns:
        bool: True si debe usar Plotly, False para usar st.image
    """
    width, height = img.size
    max_dim = max(width, height)
    return max_dim < PLOTLY_FALLBACK_THRESHOLD


@st.dialog("Visor de Imagen con Zoom", width="large")
def show_image_modal(img_data, img_name, model_type):
    """Mostrar imagen en un modal con capacidades de zoom interactivo usando Plotly."""
    st.subheader(f"📷 {img_name}")
    
    # Decodificar imagen
    if model_type == "yolo":
        img_bytes = base64.b64decode(img_data['annotated_image_base64'])
        detections_count = img_data.get('detections_count', 0)
        st.info(f"🎯 {detections_count} detecciones")
    else:  # herdnet plot
        img_bytes = base64.b64decode(img_data['plot_base64'])
        st.info(f"📍 Gráfico de Detección HerdNet")
    
    img = Image.open(BytesIO(img_bytes))
    
    # Obtener dimensiones de la imagen
    width, height = img.size
    st.caption(f"Tamaño original: {width} × {height} píxeles")
    
    # Instrucciones de zoom interactivo
    st.info("🔍 **Controles interactivos:** Usa la rueda del ratón para zoom, arrastra para desplazar, doble clic para resetear")
    
    # Verificar si usar Plotly o fallback
    if should_use_plotly(img):
        # Preparar imagen para Plotly (downsample si es necesario)
        img_display, was_resized, orig_size, display_size = prepare_image_for_plotly(img, max_dimension=2000)
        
        # Convertir a array numpy para Plotly
        img_array = np.array(img_display)
        
        # Crear figura Plotly con zoom interactivo
        fig = go.Figure()
        fig.add_trace(go.Image(z=img_array))
        
        # Configurar layout para zoom interactivo
        fig.update_layout(
            margin=dict(l=0, r=0, t=0, b=0),
            xaxis=dict(showticklabels=False, showgrid=False, zeroline=False),
            yaxis=dict(showticklabels=False, showgrid=False, zeroline=False),
            dragmode='pan',
            hovermode=False,
            height=600
        )
        
        # Configurar para permitir zoom y pan
        config = {
            'scrollZoom': True,
            'displayModeBar': True,
            'displaylogo': False,
            'modeBarButtonsToRemove': ['lasso2d', 'select2d'],
            'toImageButtonOptions': {
                'format': 'png',
                'filename': img_name,
                'height': display_size[1],
                'width': display_size[0],
                'scale': 1
            }
        }
        
        st.plotly_chart(fig, use_container_width=True, config=config)
        
        # Mostrar información de dimensiones
        if was_resized:
            st.caption(f"📐 Visualizando a {display_size[0]}×{display_size[1]}px para mejor rendimiento")
    else:
        # Imagen muy grande: usar st.image con advertencia
        st.warning(f"⚠️ Imagen muy grande ({width}×{height}px). Usando visor estático para mejor rendimiento.")
        st.image(img, use_column_width=True)
    
    # Botón de descarga
    st.markdown("---")
    buf = BytesIO()
    img.save(buf, format="PNG")
    btn = st.download_button(
        label="⬇️ Descargar Imagen",
        data=buf.getvalue(),
        file_name=f"{img_name}",
        mime="image/png",
        use_container_width=True
    )


def render_yolo_image_card(img_data, all_detections, img_idx):
    """
    Renderiza una tarjeta de imagen con detecciones YOLO usando Plotly para zoom interactivo.
    Función recursiva que maneja cada imagen individualmente.
    """
    # Crear contenedor de tarjeta
    with st.container():
        # Encabezado de tarjeta
        st.markdown(f"""
        <div class="result-card">
            <div class="card-header">📷 {img_data['image_name']}</div>
            <div class="card-subtitle">
                <span class="detection-badge">🎯 {img_data['detections_count']} detecciones</span>
                <span class="size-badge">📐 {img_data.get('original_size', {}).get('width', '?')} × {img_data.get('original_size', {}).get('height', '?')} px</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Instrucciones de zoom interactivo
        st.info("🔍 **Controles interactivos:** Usa la rueda del ratón para zoom, arrastra para desplazar, doble clic para resetear")
        
        # Mostrar imágenes lado a lado
        col1, col2 = st.columns(2)
        
        # Columna izquierda: Imagen Original
        with col1:
            st.markdown("**🖼️ Imagen Cargada**")
            if 'original_image_base64' in img_data:
                original_bytes = base64.b64decode(img_data['original_image_base64'])
                original_img = Image.open(BytesIO(original_bytes))
                
                # Verificar si usar Plotly o fallback
                if should_use_plotly(original_img):
                    # Preparar imagen para Plotly (downsample si es necesario)
                    img_display, was_resized, orig_size, display_size = prepare_image_for_plotly(original_img)
                    
                    # Convertir a array numpy para Plotly
                    img_array = np.array(img_display)
                    
                    # Crear figura Plotly con zoom interactivo
                    fig = go.Figure()
                    fig.add_trace(go.Image(z=img_array))
                    
                    # Configurar layout para zoom interactivo
                    fig.update_layout(
                        margin=dict(l=0, r=0, t=0, b=0),
                        xaxis=dict(showticklabels=False, showgrid=False, zeroline=False),
                        yaxis=dict(showticklabels=False, showgrid=False, zeroline=False),
                        dragmode='pan',
                        hovermode=False,
                        height=400
                    )
                    
                    # Configurar para permitir zoom y pan
                    config = {
                        'scrollZoom': True,
                        'displayModeBar': True,
                        'displaylogo': False,
                        'modeBarButtonsToRemove': ['lasso2d', 'select2d'],
                        'toImageButtonOptions': {
                            'format': 'png',
                            'filename': f'original_{img_data["image_name"]}',
                            'height': display_size[1],
                            'width': display_size[0],
                            'scale': 1
                        }
                    }
                    
                    st.plotly_chart(fig, use_container_width=True, config=config)
                    
                    # Mostrar información de dimensiones
                    if was_resized:
                        st.caption(f"📐 Original: {orig_size[0]}×{orig_size[1]}px | Visualización: {display_size[0]}×{display_size[1]}px")
                    else:
                        st.caption(f"📐 Dimensiones: {orig_size[0]} × {orig_size[1]} px")
                else:
                    # Imagen muy grande: usar st.image con advertencia
                    st.warning(f"⚠️ Imagen grande ({original_img.width}×{original_img.height}px). Usando visor estático.")
                    st.image(original_img, use_column_width=True)
                    st.caption(f"📐 Dimensiones: {original_img.width} × {original_img.height} px")
            else:
                st.info("Imagen original no disponible")
        
        # Columna derecha: Imagen Anotada
        with col2:
            st.markdown("**🎯 Imagen Con Detecciones**")
            img_bytes = base64.b64decode(img_data['annotated_image_base64'])
            img = Image.open(BytesIO(img_bytes))
            
            # Verificar si usar Plotly o fallback
            if should_use_plotly(img):
                # Preparar imagen para Plotly (downsample si es necesario)
                img_display, was_resized, orig_size, display_size = prepare_image_for_plotly(img)
                
                # Convertir a array numpy para Plotly
                img_array = np.array(img_display)
                
                # Crear figura Plotly con zoom interactivo
                fig = go.Figure()
                fig.add_trace(go.Image(z=img_array))
                
                # Configurar layout para zoom interactivo
                fig.update_layout(
                    margin=dict(l=0, r=0, t=0, b=0),
                    xaxis=dict(showticklabels=False, showgrid=False, zeroline=False),
                    yaxis=dict(showticklabels=False, showgrid=False, zeroline=False),
                    dragmode='pan',
                    hovermode=False,
                    height=400
                )
                
                # Configurar para permitir zoom y pan
                config = {
                    'scrollZoom': True,
                    'displayModeBar': True,
                    'displaylogo': False,
                    'modeBarButtonsToRemove': ['lasso2d', 'select2d'],
                    'toImageButtonOptions': {
                        'format': 'png',
                        'filename': f'annotated_{img_data["image_name"]}',
                        'height': display_size[1],
                        'width': display_size[0],
                        'scale': 1
                    }
                }
                
                st.plotly_chart(fig, use_container_width=True, config=config)
                
                # Mostrar información de dimensiones
                if was_resized:
                    st.caption(f"📐 Original: {orig_size[0]}×{orig_size[1]}px | Visualización: {display_size[0]}×{display_size[1]}px")
                else:
                    st.caption(f"📐 Dimensiones: {orig_size[0]} × {orig_size[1]} px")
            else:
                # Imagen muy grande: usar st.image con advertencia
                st.warning(f"⚠️ Imagen grande ({img.width}×{img.height}px). Usando visor estático.")
                st.image(img, use_column_width=True)
                st.caption(f"📐 Dimensiones: {img.width} × {img.height} px")
        
        # Obtener detecciones para esta imagen
        image_detections = [d for d in all_detections if d.get('image') == img_data['image_name']]
        
        # Tabla de detección colapsable
        with st.expander(f"📊 Ver Detalles de Detección ({len(image_detections)} elementos)", expanded=False):
            if image_detections:
                # Crear DataFrame para detecciones
                det_data = []
                for det in image_detections:
                    det_data.append({
                        'Especie': det.get('class_name', 'Desconocido'),
                        'Confianza': f"{det.get('confidence', 0):.2%}",
                        'X': f"{det.get('center', {}).get('x', 0):.1f}",
                        'Y': f"{det.get('center', {}).get('y', 0):.1f}",
                        'Ancho': f"{det.get('bbox', {}).get('x2', 0) - det.get('bbox', {}).get('x1', 0):.1f}",
                        'Alto': f"{det.get('bbox', {}).get('y2', 0) - det.get('bbox', {}).get('y1', 0):.1f}"
                    })
                
                det_df = pd.DataFrame(det_data)
                st.dataframe(det_df, use_container_width=True, hide_index=True)
            else:
                st.info("No hay detecciones para esta imagen")
        
        st.markdown("<br>", unsafe_allow_html=True)


def render_herdnet_image_card(plot_data, all_detections, plot_idx):
    """
    Renderiza una tarjeta de gráfico con detecciones HerdNet usando Plotly para zoom interactivo.
    Función recursiva que maneja cada gráfico individualmente.
    """
    # Crear contenedor de tarjeta
    with st.container():
        # Encabezado de tarjeta
        st.markdown(f"""
        <div class="result-card">
            <div class="card-header">📍 {plot_data['image_name']}</div>
            <div class="card-subtitle">
                <span class="detection-badge">🎯 {plot_data.get('detections_count', 0)} detecciones</span>
                <span class="size-badge">🗺️ Gráfico de Detección HerdNet</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Instrucciones de zoom interactivo
        st.info("🔍 **Controles interactivos:** Usa la rueda del ratón para zoom, arrastra para desplazar, doble clic para resetear")
        
        # Mostrar imágenes lado a lado
        col1, col2 = st.columns(2)
        
        # Columna izquierda: Imagen Original
        with col1:
            st.markdown("**🖼️ Imagen Cargada**")
            if 'original_image_base64' in plot_data:
                original_bytes = base64.b64decode(plot_data['original_image_base64'])
                original_img = Image.open(BytesIO(original_bytes))
                
                # Verificar si usar Plotly o fallback
                if should_use_plotly(original_img):
                    # Preparar imagen para Plotly (downsample si es necesario)
                    img_display, was_resized, orig_size, display_size = prepare_image_for_plotly(original_img)
                    
                    # Convertir a array numpy para Plotly
                    img_array = np.array(img_display)
                    
                    # Crear figura Plotly con zoom interactivo
                    fig = go.Figure()
                    fig.add_trace(go.Image(z=img_array))
                    
                    # Configurar layout para zoom interactivo
                    fig.update_layout(
                        margin=dict(l=0, r=0, t=0, b=0),
                        xaxis=dict(showticklabels=False, showgrid=False, zeroline=False),
                        yaxis=dict(showticklabels=False, showgrid=False, zeroline=False),
                        dragmode='pan',
                        hovermode=False,
                        height=400
                    )
                    
                    # Configurar para permitir zoom y pan
                    config = {
                        'scrollZoom': True,
                        'displayModeBar': True,
                        'displaylogo': False,
                        'modeBarButtonsToRemove': ['lasso2d', 'select2d'],
                        'toImageButtonOptions': {
                            'format': 'png',
                            'filename': f'original_{plot_data["image_name"]}',
                            'height': display_size[1],
                            'width': display_size[0],
                            'scale': 1
                        }
                    }
                    
                    st.plotly_chart(fig, use_container_width=True, config=config)
                    
                    # Mostrar información de dimensiones
                    if was_resized:
                        st.caption(f"📐 Original: {orig_size[0]}×{orig_size[1]}px | Visualización: {display_size[0]}×{display_size[1]}px")
                    else:
                        st.caption(f"📐 Dimensiones: {orig_size[0]} × {orig_size[1]} px")
                else:
                    # Imagen muy grande: usar st.image con advertencia
                    st.warning(f"⚠️ Imagen grande ({original_img.width}×{original_img.height}px). Usando visor estático.")
                    st.image(original_img, use_column_width=True)
                    st.caption(f"📐 Dimensiones: {original_img.width} × {original_img.height} px")
            else:
                st.info("Imagen original no disponible")
        
        # Columna derecha: Gráfico con Detecciones
        with col2:
            st.markdown("**🎯 Imagen Con Detecciones**")
            img_bytes = base64.b64decode(plot_data['plot_base64'])
            img = Image.open(BytesIO(img_bytes))
            
            # Verificar si usar Plotly o fallback
            if should_use_plotly(img):
                # Preparar imagen para Plotly (downsample si es necesario)
                img_display, was_resized, orig_size, display_size = prepare_image_for_plotly(img)
                
                # Convertir a array numpy para Plotly
                img_array = np.array(img_display)
                
                # Crear figura Plotly con zoom interactivo
                fig = go.Figure()
                fig.add_trace(go.Image(z=img_array))
                
                # Configurar layout para zoom interactivo
                fig.update_layout(
                    margin=dict(l=0, r=0, t=0, b=0),
                    xaxis=dict(showticklabels=False, showgrid=False, zeroline=False),
                    yaxis=dict(showticklabels=False, showgrid=False, zeroline=False),
                    dragmode='pan',
                    hovermode=False,
                    height=400
                )
                
                # Configurar para permitir zoom y pan
                config = {
                    'scrollZoom': True,
                    'displayModeBar': True,
                    'displaylogo': False,
                    'modeBarButtonsToRemove': ['lasso2d', 'select2d'],
                    'toImageButtonOptions': {
                        'format': 'png',
                        'filename': f'annotated_{plot_data["image_name"]}',
                        'height': display_size[1],
                        'width': display_size[0],
                        'scale': 1
                    }
                }
                
                st.plotly_chart(fig, use_container_width=True, config=config)
                
                # Mostrar información de dimensiones
                if was_resized:
                    st.caption(f"📐 Original: {orig_size[0]}×{orig_size[1]}px | Visualización: {display_size[0]}×{display_size[1]}px")
                else:
                    st.caption(f"📐 Dimensiones: {orig_size[0]} × {orig_size[1]} px")
            else:
                # Imagen muy grande: usar st.image con advertencia
                st.warning(f"⚠️ Imagen grande ({img.width}×{img.height}px). Usando visor estático.")
                st.image(img, use_column_width=True)
                st.caption(f"📐 Dimensiones: {img.width} × {img.height} px")
        
        # Obtener detecciones para esta imagen
        image_detections = [d for d in all_detections if d.get('images') == plot_data['image_name']]
        
        # Tabla de detección colapsable
        with st.expander(f"📊 Ver Detalles de Detección ({len(image_detections)} elementos)", expanded=False):
            if image_detections:
                # Crear DataFrame para detecciones
                det_data = []
                for det in image_detections:
                    det_data.append({
                        'Especie': det.get('species', 'Desconocido'),
                        'Confianza': f"{det.get('scores', 0):.2%}",
                        'X': f"{det.get('x', 0):.1f}",
                        'Y': f"{det.get('y', 0):.1f}"
                    })
                
                det_df = pd.DataFrame(det_data)
                st.dataframe(det_df, use_container_width=True, hide_index=True)
            else:
                st.info("No hay detecciones para esta imagen")
        
        st.markdown("<br>", unsafe_allow_html=True)


def render_images_recursively(images, all_detections, render_func, images_per_row=2):
    """
    Renderiza imágenes de forma recursiva en una cuadrícula.
    
    Args:
        images: Lista de imágenes a renderizar
        all_detections: Todas las detecciones del análisis
        render_func: Función para renderizar cada imagen (render_yolo_image_card o render_herdnet_image_card)
        images_per_row: Número de imágenes por fila (default: 2)
    """
    if not images:
        return
    
    # Procesar imágenes en grupos de images_per_row
    for idx in range(0, len(images), images_per_row):
        # Crear columnas
        cols = st.columns(images_per_row)
        
        # Renderizar cada imagen en su columna
        for col_idx in range(images_per_row):
            img_idx = idx + col_idx
            
            # Verificar si hay más imágenes
            if img_idx >= len(images):
                break
            
            with cols[col_idx]:
                # Llamada recursiva a la función de renderizado
                render_func(images[img_idx], all_detections, img_idx)


def display_results(result, model_choice, file_type='zip'):
    """Mostrar resultados del análisis."""
    st.success("✅ ¡Análisis Completo!")
    
    # ID de tarea
    st.info(f"📋 ID de Tarea: `{result.get('task_id', 'N/A')}` - ¡Guarda esto para recuperar resultados después!")

    # Si no hay detecciones, mostrar mensaje y salir
    if result.get('summary', {}).get('total_detections', 0) == 0:
        st.warning(" No hay detecciones en las imágenes procesadas. Puedes intentar con diferentes parámetros o un archivo diferente.")
        
    
    # Estadísticas resumen
    st.subheader("📊 Resumen")
    summary = result.get('summary', {})
    
    # Ajustar métricas según el tipo de archivo
    if file_type == 'image':
        col1, col2, col3 = st.columns(3)
        col1.metric("Total de Detecciones", summary.get('total_detections', 0))
        col2.metric("Especies Detectadas", len(summary.get('species_counts', {})))
        col3.metric("Tiempo de Procesamiento", f"{result.get('processing_time_seconds', 0):.1f}s")
    else:
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Total de Imágenes", summary.get('total_images', 0))
        col2.metric("Total de Detecciones", summary.get('total_detections', 0))
        col3.metric("Imágenes con Animales", summary.get('images_with_animals', summary.get('images_with_detections', 0)))
        col4.metric("Tiempo de Procesamiento", f"{result.get('processing_time_seconds', 0):.1f}s")
    
    # Distribución de especies
    if summary.get('species_counts'):
        st.subheader("🦁 Distribución de Especies")
        species_df = pd.DataFrame(list(summary['species_counts'].items()), columns=['Especie', 'Cantidad'])
        
        col1, col2 = st.columns([1, 1])
        with col1:
            fig = px.bar(species_df, x='Especie', y='Cantidad', color='Especie')
            fig.update_layout(showlegend=False)
            st.plotly_chart(fig, use_container_width=True)
        with col2:
            fig = px.pie(species_df, names='Especie', values='Cantidad')
            st.plotly_chart(fig, use_container_width=True)
    
    # ========================================
    # Tarjetas de Imágenes con Resultados (Renderizado Recursivo)
    # ========================================
    
    # Imágenes anotadas (YOLO)
    if 'annotated_images' in result:
        st.subheader("🖼️ Imágenes Anotadas - Resultados")
        
        # Obtener detecciones para tabla
        all_detections = result.get('detections', [])
        
        # Renderizar imágenes recursivamente (sin botones)
        render_images_recursively(
            images=result['annotated_images'],
            all_detections=all_detections,
            render_func=render_yolo_image_card,
            images_per_row=1
        )
    elif 'plots' in result:

        st.subheader("🗺️ Gráficos de Detección - Resultados")
        
        # Obtener detecciones para tabla
        all_detections = result.get('detections', [])
        
        # Renderizar gráficos recursivamente (sin botones)
        render_images_recursively(
            images=result['plots'],
            all_detections=all_detections,
            render_func=render_herdnet_image_card,
            images_per_row=1
        )
    else:
        st.subheader("❌ No se encontraron resultados")
        st.info("No se encontraron resultados para esta tarea, por favor intente nuevamente con nuevos parámetros o suba un nuevo archivo") 
        if result.get('model', "") == "YOLOv11":
            st.info("Por favor intente nuevamente con nuevos parámetros de Umbral de Confianza, Umbral de Coincidencia (IOU) y Tamaño de Imagen")
        elif result.get('model', "") == "HerdNet":
            st.info("Por favor intente nuevamente con nuevos parámetros de Tamaño de Parche, Tamaño de Miniatura, Rotación y Superposición")
        
def view_results_page():
    """Página para ver resultados pasados."""
    st.header("📊 Ver Resultados Anteriores")
    
    # Filtros
    col1, col2, col3 = st.columns(3)
    with col1:
        model_filter = st.selectbox("Modelo", ["Todos", "yolo", "herdnet"])
    with col2:
        status_filter = st.selectbox("Estado", ["Todos", "completed", "processing", "failed"])
    with col3:
        limit = st.number_input("Límite", 1, 100, 20)
    
    # Obtener tareas
    try:
        params = {'limit': limit}
        if model_filter != "Todos":
            params['model_type'] = model_filter
        if status_filter != "Todos":
            params['status'] = status_filter
        
        response = requests.get(f"{API_BASE_URL}/tasks", params=params)
        if response.status_code == 200:
            data = response.json()
            tasks = data.get('tasks', [])
            
            if not tasks:
                st.info("No se encontraron tareas")
                return
            
            st.success(f"Se encontraron {len(tasks)} tareas")
            
            # Mostrar tareas
            for task in tasks:
                status_emoji = {"completed": "✅", "processing": "⏳", "failed": "❌"}.get(task['status'], "❓")
                with st.expander(f"{status_emoji} Tarea {task['task_id'][:8]}... - {task.get('filename', 'N/A')} ({task['status']})"):
                    col1, col2 = st.columns(2)
                    with col1:
                        st.write(f"**Modelo:** {task['model_type']}")
                        st.write(f"**Estado:** {task['status']}")
                        st.write(f"**Creado:** {task['created_at']}")
                    with col2:
                        st.write(f"**Imágenes:** {task.get('num_images', 0)}")
                        st.write(f"**Detecciones:** {task.get('total_detections', 0)}")
                        st.write(f"**Tiempo:** {task.get('processing_time_seconds', 0):.1f}s")
                    
                    # Botón para ver resultados completos
                    if st.button(f"Ver Resultados Completos", key=task['task_id']):
                        # Obtener tarea completa
                        task_response = requests.get(f"{API_BASE_URL}/tasks/{task['task_id']}")
                        if task_response.status_code == 200:
                            full_task = task_response.json()['task']
                            st.json(full_task.get('result_data', {}))
        else:
            st.error(f"Error al obtener tareas: {response.status_code}")
    except Exception as e:
        st.error(f"Error: {str(e)}")


def statistics_page():
    """Página de estadísticas de la base de datos."""
    st.header("📈 Estadísticas de la Base de Datos")
    
    try:
        response = requests.get(f"{API_BASE_URL}/database/stats")
        if response.status_code == 200:
            stats = response.json()['statistics']
            
            # Resumen general
            col1, col2, col3 = st.columns(3)
            col1.metric("Total de Tareas", stats.get('total_tasks', 0))
            col2.metric("Total de Detecciones", stats.get('total_detections', 0))
            col3.metric("Completadas", stats.get('tasks_by_status', {}).get('completed', 0))
            
            # Tareas por modelo
            if stats.get('tasks_by_model'):
                st.subheader("Tareas por Modelo")
                model_df = pd.DataFrame(list(stats['tasks_by_model'].items()), columns=['Modelo', 'Cantidad'])
                fig = px.bar(model_df, x='Modelo', y='Cantidad', color='Modelo')
                fig.update_layout(showlegend=False)
                st.plotly_chart(fig, use_container_width=True)
            
            # Distribución de especies
            if stats.get('species_distribution'):
                st.subheader("Distribución de Especies (Histórico)")
                species_df = pd.DataFrame(list(stats['species_distribution'].items()), columns=['Especie', 'Cantidad'])
                species_df = species_df.sort_values('Cantidad', ascending=False)
                
                col1, col2 = st.columns(2)
                with col1:
                    fig = px.bar(species_df, x='Especie', y='Cantidad', color='Especie')
                    fig.update_layout(showlegend=False)
                    st.plotly_chart(fig, use_container_width=True)
                with col2:
                    fig = px.pie(species_df, names='Especie', values='Cantidad')
                    st.plotly_chart(fig, use_container_width=True)
        else:
            st.error("Error al obtener estadísticas")
    except Exception as e:
        st.error(f"Error: {str(e)}")


def help_page():    
    """Página de ayuda con preguntas frecuentes."""
    st.header("❓ Ayuda y Preguntas Frecuentes")
    
    faq_content = f"""
    ## Preguntas Frecuentes
    
    **1. ¿Qué tipos de archivos puedo subir?**  
    Puedes subir imágenes individuales en formatos JPEG, PNG o archivos ZIP que contengan múltiples imágenes.

    **2. ¿Cuánto tiempo tarda el análisis?**  
    El tiempo de análisis depende del tamaño y número de imágenes, así como del modelo seleccionado. Generalmente, toma entre unos segundos a varios minutos.

    **3. ¿Cómo interpreto los resultados?**  
    Los resultados incluyen un resumen de detecciones, gráficos de distribución de especies y tarjetas de imágenes anotadas con detecciones resaltadas.

    **4. ¿Puedo descargar las imágenes anotadas?**  
    Sí, puedes descargar las imágenes anotadas directamente desde la interfaz después del análisis.

    **5. ¿Qué hago si encuentro un error?**  
    Si encuentras un error, por favor contacta al administrador de la plataforma al {ADMIN_EMAIL} con detalles del problema.
    
    ## Materiales de apoyo
    **- Documentación en línea:** [Enlace a la documentación]({DOCS_URL})  
    **- Tutoriales en video:** [Enlace a los tutoriales]({EXPLAIN_VIDEO_URL})  

    ## Soporte Adicional
    
    Para soporte adicional, consulta la documentación en línea o contacta al equipo de soporte.
    """
    
    st.markdown(faq_content)

def about_page():
    """Página acerca de con información de modelos."""
    st.header("ℹ️ Acerca de")
    
    # Build models section dynamically based on availability
    models_section = """
    ## Sistema de Detección de Fauna Africana
    
    Este sistema utiliza modelos de aprendizaje profundo de última generación para detectar y contar fauna africana en imágenes aéreas y satelitales.
    
    ### Modelos
    
    #### 🎯 YOLOv11s con ajuste específico para detección de imágenes aéreas con fauna africana 
    - **Tipo:** Detección de objetos con cajas delimitadoras
    - **Velocidad:** Rápido (1-2 segundos por imagen)
    - **Mejor para:** Imágenes aéreas, detección en tiempo real
    - **Salida:** Cajas delimitadoras alrededor de los animales
    """
    
    if ENABLE_HERDNET:
        models_section += """
    #### 📍 HerdNet
    - **Tipo:** Detección basada en puntos
    - **Velocidad:** Moderada (depende del tamaño de la imagen)
    - **Mejor para:** Imágenes aéreas/satelitales grandes
    - **Salida:** Puntos centrales, miniaturas y gráficos
    """
    
    models_section += """
    ### Especies Soportadas
    1. Búfalo (*Syncerus caffer*)
    2. Elefante (*Loxodonta africana*)
    3. Antilope Africano (*Kobus kob*)
    4. Antílope (*Damaliscus lunatus*)
    5. Jabalí Verrugoso (*Phacochoerus africanus*)
    6. Antílope Acuático (*Kobus ellipsiprymnus*)
    
    ### Citas
    """
    
    # Add HerdNet citation if enabled
    if ENABLE_HERDNET:
        models_section += """
    **HerdNet:**
    ```
    Delplanque, A., Foucher, S., Lejeune, P., Linchant, J., & Théau, J. (2022).
    Multispecies detection and identification of African mammals in aerial imagery 
    using convolutional neural networks. Remote Sensing in Ecology and Conservation, 8(2), 166-179.
    ```
    ```
    Alexandre Delplanque, Samuel Foucher, Jérôme Théau, Elsa Bussière, Cédric Vermeulen, Philippe Lejeune. (2023)
    From crowd to herd counting: How to precisely detect and count African mammals using aerial imagery and deep learning?, 197, 167-180
    ```
    ```
    Qian Y, Humphries GRW, Trathan PN, Lowther A, Donovan CR.  (2023)
    Counting animals in aerial images with a density map estimation model, 7;13(4)
    ```
    """
    
    models_section += f"""
    **YOLOv11:**
    ```
    Ultralytics YOLOv11 (2024)
    https://github.com/ultralytics/ultralytics
    ```
    
    ---
    
    ### Contacto y Soporte
    
    Para preguntas, sugerencias o reportar problemas, por favor contacta al administrador de la plataforma al {ADMIN_EMAIL}
    
    ### Versión
    
    **Versión:** 1.0.0  
    **Última Actualización:** Noviembre 2025  
    **Estado:** Producción
    """
    
    st.markdown(models_section)


if __name__ == "__main__":
    main()
