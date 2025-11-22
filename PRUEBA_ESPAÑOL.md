# 🇪🇸 Guía Rápida - Prueba de Traducción al Español

## 🚀 Inicio Rápido

### Paso 1: Iniciar la Aplicación

```bash
# Terminal 1 - Backend (API)
cd /Users/marioguaqueta/Desktop/MAIA/2025-4/ProyectoFinal/back
python app.py

# Terminal 2 - Frontend (Streamlit)
streamlit run streamlit_app.py
```

### Paso 2: Abrir en Navegador

Abre: `http://localhost:8501`

---

## ✅ Lista de Verificación de Traducción

### 📱 Navegación Principal

Al abrir la aplicación, verifica:

- [ ] **Título**: "🦁 Sistema de Detección de Fauna Africana"
- [ ] **Subtítulo**: "Impulsado por modelos de aprendizaje profundo YOLOv11 y HerdNet"
- [ ] **Menú lateral** con opciones:
  - [ ] 🎯 Nuevo Análisis
  - [ ] 📊 Ver Resultados
  - [ ] 📈 Estadísticas
  - [ ] ℹ️ Acerca de

---

### 🎯 Página: Nuevo Análisis

Haz clic en "🎯 Nuevo Análisis" y verifica:

#### Estado de la API
- [ ] "✓ Estado de la API: healthy"
- [ ] "YOLOv11: ✓ Cargado | HerdNet: ✓ Cargado"

#### Sección de Carga
- [ ] **Encabezado**: "📁 Cargar Imágenes"
- [ ] **Label**: "Sube un archivo ZIP con imágenes"
- [ ] **Mensaje**: "👆 Por favor sube un archivo ZIP para continuar"

#### Selección de Modelo
- [ ] **Encabezado**: "🤖 Selección de Modelo"
- [ ] **Label**: "Elige el modelo de detección:"
- [ ] **Opción 1**: "YOLOv11 (Rápido, Cajas Delimitadoras)"
- [ ] **Opción 2**: "HerdNet (Aéreo, Detección por Puntos)"

#### Parámetros (YOLOv11)
Selecciona YOLOv11 y verifica:
- [ ] "⚙️ Parámetros"
- [ ] "Umbral de Confianza"
- [ ] "Umbral IOU"
- [ ] "Tamaño de Imagen"
- [ ] "Incluir imágenes anotadas"

#### Parámetros (HerdNet)
Selecciona HerdNet y verifica:
- [ ] "Tamaño de Parche"
- [ ] "Rotación (pasos de 90°)"
- [ ] "Superposición (píxeles)"
- [ ] "Tamaño de Miniatura"
- [ ] "Incluir miniaturas"
- [ ] "Incluir gráficos de detección"

#### Botón de Acción
- [ ] **Botón**: "🚀 Ejecutar Análisis"
- [ ] **Spinner**: "Procesando imágenes... Esto puede tomar algunos minutos."

---

### 📊 Resultados del Análisis

Después de ejecutar un análisis, verifica:

#### Encabezados
- [ ] "✅ ¡Análisis Completo!"
- [ ] "📋 ID de Tarea: `{id}` - ¡Guarda esto para recuperar resultados después!"
- [ ] "📊 Resumen"

#### Métricas
- [ ] "Total de Imágenes"
- [ ] "Total de Detecciones"
- [ ] "Imágenes con Animales"
- [ ] "Tiempo de Procesamiento"

#### Gráficos
- [ ] "🦁 Distribución de Especies"
- [ ] Gráfico de barras con etiqueta "Especie" y "Cantidad"
- [ ] Gráfico circular con especies

#### Tarjetas de Imágenes (YOLO)
- [ ] "🖼️ Imágenes Anotadas - Resultados"
- [ ] **Badge verde**: "🎯 {n} detecciones"
- [ ] **Badge azul**: "📐 {ancho} × {alto} px"
- [ ] **Expandible**: "📊 Ver Detalles de Detección ({n} elementos)"
- [ ] **Tabla** con columnas:
  - [ ] "Especie"
  - [ ] "Confianza"
  - [ ] "X"
  - [ ] "Y"
  - [ ] "Ancho"
  - [ ] "Alto"
- [ ] **Botones**:
  - [ ] "🔍 Ver Tamaño Completo"
  - [ ] "⬇️ Descargar Imagen"

#### Tarjetas de Imágenes (HerdNet)
- [ ] "🗺️ Gráficos de Detección - Resultados"
- [ ] "Gráfico de Detección HerdNet"
- [ ] **Tabla** con columnas:
  - [ ] "Especie"
  - [ ] "Confianza"
  - [ ] "X"
  - [ ] "Y"
- [ ] **Botones**:
  - [ ] "🔍 Ver Tamaño Completo"
  - [ ] "⬇️ Descargar Gráfico"

#### Miniaturas
- [ ] "🔍 Miniaturas de Animales"

---

### 🔍 Visor de Imagen con Zoom

Haz clic en "🔍 Ver Tamaño Completo" y verifica:

- [ ] **Título del modal**: "Visor de Imagen con Zoom"
- [ ] **Info**: "🎯 {n} detecciones" o "📍 Gráfico de Detección HerdNet"
- [ ] **Caption**: "Tamaño original: {ancho} × {alto} píxeles"
- [ ] **Control**: "🔍 Nivel de Zoom"
- [ ] **Botón**: "⬇️ Descargar Imagen"

---

### 📊 Página: Ver Resultados

Haz clic en "📊 Ver Resultados" y verifica:

#### Encabezado
- [ ] "📊 Ver Resultados Anteriores"

#### Filtros
- [ ] **Dropdown 1**: "Modelo"
  - [ ] "Todos"
  - [ ] "yolo"
  - [ ] "herdnet"
- [ ] **Dropdown 2**: "Estado"
  - [ ] "Todos"
  - [ ] "completed"
  - [ ] "processing"
  - [ ] "failed"
- [ ] **Input numérico**: "Límite"

#### Mensajes
- [ ] "Se encontraron {n} tareas" o "No se encontraron tareas"

#### Tarjetas de Tareas
- [ ] Emoji de estado: ✅ / ⏳ / ❌
- [ ] "Tarea {id}..."
- [ ] **Campos**:
  - [ ] "**Modelo:**"
  - [ ] "**Estado:**"
  - [ ] "**Creado:**"
  - [ ] "**Imágenes:**"
  - [ ] "**Detecciones:**"
  - [ ] "**Tiempo:**"
- [ ] **Botón**: "Ver Resultados Completos"

---

### 📈 Página: Estadísticas

Haz clic en "📈 Estadísticas" y verifica:

#### Encabezado
- [ ] "📈 Estadísticas de la Base de Datos"

#### Métricas Principales
- [ ] "Total de Tareas"
- [ ] "Total de Detecciones"
- [ ] "Completadas"

#### Gráficos
- [ ] "Tareas por Modelo"
  - [ ] Columnas: "Modelo", "Cantidad"
- [ ] "Distribución de Especies (Histórico)"
  - [ ] Columnas: "Especie", "Cantidad"

---

### ℹ️ Página: Acerca de

Haz clic en "ℹ️ Acerca de" y verifica:

#### Encabezado
- [ ] "ℹ️ Acerca de"

#### Contenido Principal
- [ ] "Sistema de Detección de Fauna Africana"
- [ ] Descripción en español del sistema

#### Sección de Modelos
- [ ] "### Modelos"
- [ ] **YOLOv11**:
  - [ ] "**Tipo:**"
  - [ ] "**Velocidad:**"
  - [ ] "**Mejor para:**"
  - [ ] "**Salida:**"
- [ ] **HerdNet** (mismos campos)

#### Especies
- [ ] "### Especies Soportadas"
- [ ] Lista numerada:
  1. [ ] "Búfalo (*Syncerus caffer*)"
  2. [ ] "Elefante (*Loxodonta africana*)"
  3. [ ] "Kob (*Kobus kob*)"
  4. [ ] "Topi (*Damaliscus lunatus*)"
  5. [ ] "Jabalí Verrugoso (*Phacochoerus africanus*)"
  6. [ ] "Antílope Acuático (*Kobus ellipsiprymnus*)"

#### Otras Secciones
- [ ] "### Citas"
- [ ] "### Contacto y Soporte"
- [ ] "### Versión"

---

## 🧪 Pruebas de Funcionalidad

### Flujo Completo de Análisis

1. **Preparar un ZIP de prueba** con imágenes de fauna
2. **Cargar el archivo** en "Nuevo Análisis"
3. **Seleccionar modelo** (probar ambos)
4. **Ajustar parámetros** (probar diferentes valores)
5. **Ejecutar análisis** y verificar que:
   - [ ] Spinner aparece en español
   - [ ] Mensaje de éxito en español
   - [ ] Tarjetas se muestran correctamente
   - [ ] Tablas están en español
   - [ ] Botones funcionan

### Pruebas de Interacción

1. **Tarjetas de Resultados**
   - [ ] Hover sobre tarjeta (efecto de elevación)
   - [ ] Expandir/colapsar tabla
   - [ ] Ver tamaño completo (abre modal)
   - [ ] Descargar imagen

2. **Visor con Zoom**
   - [ ] Abrir modal
   - [ ] Ajustar zoom (50% - 200%)
   - [ ] Descargar desde modal
   - [ ] Cerrar modal

3. **Navegación**
   - [ ] Cambiar entre páginas
   - [ ] Aplicar filtros en "Ver Resultados"
   - [ ] Verificar gráficos en "Estadísticas"

---

## ❌ Pruebas de Mensajes de Error

### Simular Errores

1. **API Desconectada**
   - Detén el backend (`Ctrl+C` en Terminal 1)
   - Recarga Streamlit
   - Verifica mensaje: "❌ No se puede conectar a la API..."

2. **Archivo Inválido**
   - Intenta subir un archivo que no sea ZIP
   - Verifica que el uploader solo acepta ZIP

3. **Sin Tareas**
   - En "Ver Resultados", si no hay tareas previas
   - Verifica mensaje: "No se encontraron tareas"

---

## 📸 Capturas de Pantalla Sugeridas

Para documentación, toma capturas de:

1. [ ] Página principal con menú lateral
2. [ ] Formulario de "Nuevo Análisis"
3. [ ] Tarjetas de resultados con badges
4. [ ] Tabla de detección expandida
5. [ ] Visor de imagen con zoom
6. [ ] Página de estadísticas
7. [ ] Página "Acerca de"
8. [ ] Lista de tareas en "Ver Resultados"

---

## 🐛 Problemas Comunes

### Si no ves texto en español:

1. **Verifica que guardaste el archivo**
   ```bash
   # Confirma que streamlit_app.py tiene la traducción
   head -n 5 streamlit_app.py
   # Debería mostrar: "Interfaz Web Streamlit..."
   ```

2. **Reinicia Streamlit**
   ```bash
   # Detén: Ctrl+C
   # Inicia de nuevo:
   streamlit run streamlit_app.py
   ```

3. **Limpia caché de Streamlit**
   - En la interfaz, presiona `C` para limpiar caché
   - O borra: `.streamlit/cache/`

### Si hay errores de conexión:

1. **Verifica el backend**
   ```bash
   curl http://localhost:8000/health
   # Debería responder con JSON
   ```

2. **Verifica puertos**
   - Backend: `http://localhost:8000`
   - Frontend: `http://localhost:8501`

---

## ✅ Checklist Final

Antes de dar por completa la prueba:

- [ ] Todas las páginas visibles en español
- [ ] Todos los botones en español
- [ ] Todos los mensajes en español
- [ ] Tablas con encabezados en español
- [ ] Gráficos con etiquetas en español
- [ ] Modal de zoom en español
- [ ] Mensajes de error en español
- [ ] Página "Acerca de" completamente en español
- [ ] Especies con nombres en español
- [ ] Sin errores en consola del navegador
- [ ] Sin errores en terminal de Streamlit
- [ ] Funcionalidad completa preservada

---

## 📝 Reporte de Prueba

Después de completar las pruebas, documenta:

### ✅ Elementos Verificados
- Número total de elementos revisados: _____
- Elementos correctamente traducidos: _____
- Elementos con problemas: _____

### 🐛 Problemas Encontrados
(Describe cualquier problema)

### 💡 Sugerencias de Mejora
(Traducciones alternativas, ajustes de texto)

---

**Fecha de Prueba:** __________  
**Probado por:** __________  
**Versión:** 2.2.0  
**Estado:** ✅ Aprobado / ⚠️ Con Observaciones / ❌ Rechazado

