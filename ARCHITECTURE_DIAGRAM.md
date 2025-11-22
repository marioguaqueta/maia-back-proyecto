# Sistema de Detección de Fauna - Diagramas de Arquitectura

## 1. Arquitectura de Alto Nivel

```mermaid
graph TB
    subgraph "Interfaz de Usuario"
        User[👤 Usuario Final<br/>Navegador Web]
    end
    
    subgraph "Streamlit Cloud ☁️"
        Frontend[🌐 Frontend Streamlit<br/>streamlit_app.py<br/>Puerto: 8501]
    end
    
    subgraph "Instancia AWS EC2 🖥️"
        Backend[🔧 API Backend Flask<br/>app.py<br/>Puerto: 8000]
        Database[(💾 BD SQLite<br/>wildlife_detection.db)]
        Models[🤖 Modelos ML<br/>- YOLOv11 best.pt<br/>- HerdNet herdnet_model.pth]
    end
    
    subgraph "Google Drive ☁️"
        GDrive[(📦 Almacenamiento de Modelos<br/>ID Carpeta: 11uMn45...)]
    end
    
    User -->|HTTPS| Frontend
    Frontend -->|API REST<br/>Peticiones HTTP| Backend
    Backend -->|Leer/Escribir| Database
    Backend -->|Cargar Modelos| Models
    Backend -.->|Descargar<br/>Primera Ejecución| GDrive
    Backend -->|Respuesta JSON| Frontend
    Frontend -->|Mostrar Resultados| User
    
    style Frontend fill:#e1f5ff
    style Backend fill:#fff4e1
    style Database fill:#f0f0f0
    style Models fill:#e8f5e9
    style GDrive fill:#fff3e0
    style User fill:#f3e5f5
```

---

## 2. Arquitectura de Despliegue

```mermaid
graph TB
    subgraph "Internet 🌐"
        Users[👥 Usuarios]
    end
    
    subgraph "Streamlit Cloud - Frontend"
        StreamlitApp[Aplicación Web Streamlit<br/>- Python 3.11<br/>- requirements-streamlit.txt<br/>- Dependencias mínimas]
        StreamlitConfig[Configuración de Secretos<br/>API_BASE_URL]
    end
    
    subgraph "Instancia AWS EC2 - Backend"
        LB[Balanceador de Carga /<br/>Proxy Inverso]
        
        subgraph "Contenedor Docker"
            Gunicorn[Servidor WSGI Gunicorn<br/>2 workers, 2 threads<br/>Puerto: 8000]
            FlaskApp[Aplicación Flask<br/>- app.py<br/>- database.py<br/>- model_loader.py<br/>- infer.py]
            
            subgraph "Almacenamiento"
                DB[(BD SQLite)]
                ModelsDir[Directorio de Modelos<br/>best.pt<br/>herdnet_model.pth]
                Uploads[Uploads/<br/>Archivos Temporales]
            end
        end
        
        SecurityGroup[Grupo de Seguridad<br/>- Puerto 8000: HTTP<br/>- Puerto 22: SSH]
    end
    
    subgraph "Servicios Externos"
        GDrive[Google Drive<br/>Descarga de Modelos]
    end
    
    Users -->|HTTPS| StreamlitApp
    StreamlitConfig -.->|Configurar| StreamlitApp
    StreamlitApp -->|Llamadas API HTTP| LB
    LB --> Gunicorn
    Gunicorn --> FlaskApp
    FlaskApp --> DB
    FlaskApp --> ModelsDir
    FlaskApp --> Uploads
    FlaskApp -.->|Primera Ejecución| GDrive
    SecurityGroup -.->|Protege| LB
    
    style StreamlitApp fill:#00d4ff
    style FlaskApp fill:#ff9800
    style Gunicorn fill:#4caf50
    style DB fill:#9e9e9e
    style SecurityGroup fill:#f44336
    style GDrive fill:#ffc107
```

---

## 3. Diagrama de Flujo de Datos

```mermaid
sequenceDiagram
    participant User as Usuario
    participant Streamlit as Frontend Streamlit<br/>(Streamlit Cloud)
    participant API as Backend Flask<br/>(AWS EC2)
    participant DB as Base de Datos SQLite
    participant Models as Modelos ML<br/>(YOLO/HerdNet)
    participant GDrive as Google Drive
    
    Note over User,GDrive: Configuración Primera Vez
    API->>GDrive: Verificar si existen modelos
    GDrive-->>API: Descargar best.pt y herdnet_model.pth
    API->>DB: Inicializar esquema de base de datos
    
    Note over User,GDrive: Flujo de Análisis de Imagen
    User->>Streamlit: Subir archivo ZIP
    User->>Streamlit: Seleccionar modelo y parámetros
    Streamlit->>API: POST /analyze-yolo o /analyze-image
    
    API->>DB: Generar task_id, guardar tarea
    API->>API: Extraer imágenes del ZIP
    API->>Models: Cargar modelo y ejecutar inferencia
    Models-->>API: Resultados de detección
    
    API->>API: Generar imágenes anotadas/miniaturas
    API->>DB: Guardar resultados completos + detecciones
    API-->>Streamlit: Respuesta JSON con task_id
    
    Streamlit->>Streamlit: Analizar resultados y crear visualizaciones
    Streamlit->>User: Mostrar tabla, gráficos, imágenes
    
    Note over User,GDrive: Recuperar Resultados Anteriores
    User->>Streamlit: Ingresar task_id o navegar historial
    Streamlit->>API: GET /tasks/{task_id}
    API->>DB: Consultar tarea y resultados
    DB-->>API: Respuesta JSON completa
    API-->>Streamlit: Datos de tarea con imágenes
    Streamlit->>User: Mostrar análisis anterior
    
    Note over User,GDrive: Ver Estadísticas
    User->>Streamlit: Abrir página de estadísticas
    Streamlit->>API: GET /database/stats
    API->>DB: Estadísticas agregadas
    DB-->>API: Conteos y distribuciones
    API-->>Streamlit: JSON de estadísticas
    Streamlit->>Streamlit: Crear gráficos
    Streamlit->>User: Mostrar panel de estadísticas
```

---

## 4. Interacción de Componentes

```mermaid
graph LR
    subgraph "Componentes Frontend"
        UI1[Página Nuevo Análisis]
        UI2[Página Ver Resultados]
        UI3[Página Estadísticas]
        UI4[Página Acerca de]
    end
    
    subgraph "Endpoints API"
        EP1[POST /analyze-yolo]
        EP2[POST /analyze-image]
        EP3[GET /tasks]
        EP4[GET /tasks/task_id]
        EP5[GET /database/stats]
        EP6[GET /health]
    end
    
    subgraph "Servicios Backend"
        Service1[Inferencia YOLO]
        Service2[Inferencia HerdNet]
        Service3[Servicio de BD]
        Service4[Cargador de Modelos]
    end
    
    subgraph "Almacenamiento de Datos"
        DB1[(tabla tasks)]
        DB2[(tabla task_results)]
        DB3[(tabla detections)]
        Files[(Archivos de Modelos)]
    end
    
    UI1 --> EP1
    UI1 --> EP2
    UI2 --> EP3
    UI2 --> EP4
    UI3 --> EP5
    UI4 --> EP6
    
    EP1 --> Service1
    EP2 --> Service2
    EP3 --> Service3
    EP4 --> Service3
    EP5 --> Service3
    
    Service1 --> Files
    Service2 --> Files
    Service3 --> DB1
    Service3 --> DB2
    Service3 --> DB3
    Service4 --> Files
    
    style UI1 fill:#e3f2fd
    style UI2 fill:#e3f2fd
    style UI3 fill:#e3f2fd
    style UI4 fill:#e3f2fd
    style Service1 fill:#fff3e0
    style Service2 fill:#fff3e0
    style Service3 fill:#e8f5e9
    style Service4 fill:#f3e5f5
```

---

## 5. Flujo de Despliegue

```mermaid
graph TD
    Start([Iniciar Despliegue])
    
    subgraph "Despliegue Backend (EC2)"
        B1[Subir código a GitHub]
        B2[SSH a instancia EC2]
        B3[Obtener código más reciente]
        B4[Construir imagen Docker]
        B5[Ejecutar docker-compose up]
        B6[Modelos se descargan de GDrive]
        B7[Base de datos se inicializa]
        B8[Backend listo en puerto 8000]
    end
    
    subgraph "Despliegue Frontend (Streamlit Cloud)"
        F1[Subir código a GitHub]
        F2[Iniciar sesión en Streamlit Cloud]
        F3[Crear/Actualizar app]
        F4[Configurar ajustes<br/>- Python 3.11<br/>- requirements-streamlit.txt]
        F5[Establecer secretos<br/>API_BASE_URL]
        F6[Desplegar app]
        F7[Frontend listo en 8501]
    end
    
    Start --> B1
    Start --> F1
    
    B1 --> B2
    B2 --> B3
    B3 --> B4
    B4 --> B5
    B5 --> B6
    B6 --> B7
    B7 --> B8
    
    F1 --> F2
    F2 --> F3
    F3 --> F4
    F4 --> F5
    F5 --> F6
    F6 --> F7
    
    B8 --> Connected{Backend <-> Frontend<br/>¿Conectado?}
    F7 --> Connected
    
    Connected -->|Sí| Success([✅ Despliegue Completo])
    Connected -->|No| Debug[Depurar conexión<br/>Verificar API_BASE_URL<br/>Verificar grupos de seguridad]
    Debug --> Connected
    
    style B1 fill:#ffecb3
    style B8 fill:#c8e6c9
    style F1 fill:#e1bee7
    style F7 fill:#b2dfdb
    style Success fill:#81c784
    style Debug fill:#ffab91
```

---

## 6. Arquitectura de Seguridad

```mermaid
graph TB
    subgraph "Internet Público"
        Internet[🌐 Usuarios de Internet]
    end
    
    subgraph "Streamlit Cloud"
        StreamlitSSL[HTTPS SSL/TLS]
        StreamlitApp[App Streamlit<br/>Sin datos sensibles<br/>Solo lógica UI]
    end
    
    subgraph "AWS EC2"
        SecurityGroup[Grupo de Seguridad AWS]
        
        subgraph "Contenedor Docker"
            FlaskSSL[HTTP/HTTPS<br/>Considerar agregar SSL]
            FlaskApp[Backend Flask]
            
            subgraph "Recursos Protegidos"
                DB[Base de Datos SQLite<br/>- task_id como clave primaria<br/>- Sin autenticación aún]
                Models[Modelos ML<br/>Acceso solo lectura]
                Uploads[Subidas Temporales<br/>Auto-limpieza]
            end
        end
    end
    
    subgraph "Servicios Externos"
        GDriveAPI[API Google Drive<br/>Acceso solo lectura<br/>Carpeta pública]
    end
    
    Internet -->|HTTPS| StreamlitSSL
    StreamlitSSL --> StreamlitApp
    StreamlitApp -->|API HTTP| SecurityGroup
    
    SecurityGroup -->|Puerto 8000| FlaskSSL
    SecurityGroup -->|Puerto 22 SSH<br/>IP Restringida| FlaskApp
    
    FlaskSSL --> FlaskApp
    FlaskApp --> DB
    FlaskApp --> Models
    FlaskApp --> Uploads
    FlaskApp -.->|HTTPS| GDriveAPI
    
    Note1[🔒 Medidas de Seguridad:<br/>- Grupos de seguridad limitan acceso<br/>- API sin autenticación aún<br/>- Base de datos almacenada localmente<br/>- Archivos de modelo solo lectura<br/>- Archivos temporales auto-eliminados]
    
    style SecurityGroup fill:#f44336
    style StreamlitSSL fill:#4caf50
    style FlaskSSL fill:#ff9800
    style DB fill:#9e9e9e
    style Note1 fill:#fff9c4
```

---

## Stack Tecnológico

### Frontend (Streamlit Cloud)
- **Framework**: Streamlit 1.28.0
- **Lenguaje**: Python 3.11
- **Visualización**: Plotly
- **Cliente HTTP**: requests
- **Despliegue**: Streamlit Cloud (Nivel Gratuito)

### Backend (AWS EC2)
- **Framework**: Flask 3.0.0
- **Servidor WSGI**: Gunicorn
- **Lenguaje**: Python 3.11
- **Contenedor**: Docker
- **Base de Datos**: SQLite
- **Modelos ML**: 
  - YOLOv11 (ultralytics)
  - HerdNet (personalizado)
- **Aprendizaje Profundo**: PyTorch
- **Visión por Computadora**: OpenCV, albumentations
- **Despliegue**: AWS EC2 (Docker Compose)

### Servicios Externos
- **Almacenamiento de Modelos**: Google Drive
- **Control de Versiones**: GitHub
- **CI/CD**: Despliegue manual (puede automatizarse)

---

## Consideraciones de Escalabilidad

```mermaid
graph TB
    subgraph "Arquitectura Actual"
        C1[Instancia EC2 Única]
        C2[Base de Datos SQLite]
        C3[Almacenamiento Local de Modelos]
    end
    
    subgraph "Opciones Futuras de Escalado"
        S1[Balanceador de Carga + Múltiples EC2]
        S2[PostgreSQL / RDS]
        S3[S3 para Almacenamiento de Modelos]
        S4[Caché Redis]
        S5[Cola Asíncrona Celery]
    end
    
    C1 -.->|Escalar a| S1
    C2 -.->|Migrar a| S2
    C3 -.->|Mover a| S3
    S1 --> S4
    S1 --> S5
    
    style C1 fill:#ffecb3
    style C2 fill:#ffecb3
    style C3 fill:#ffecb3
    style S1 fill:#c8e6c9
    style S2 fill:#c8e6c9
    style S3 fill:#c8e6c9
    style S4 fill:#b2dfdb
    style S5 fill:#b2dfdb
```

---

## Cómo Convertir Estos a PNG

### Opción 1: Usando Mermaid CLI
```bash
# Instalar mermaid-cli
npm install -g @mermaid-js/mermaid-cli

# Convertir a PNG
mmdc -i ARCHITECTURE_DIAGRAM.md -o architecture.png -b transparent
```

### Opción 2: Usando Herramientas en Línea
1. Copiar el código mermaid
2. Ir a https://mermaid.live/
3. Pegar el código
4. Click en "Descargar PNG"

### Opción 3: Usando Extensión de VS Code
1. Instalar extensión "Markdown Preview Mermaid Support"
2. Abrir este archivo en VS Code
3. Click derecho en diagrama → "Exportar como PNG"

### Opción 4: Usando Python
```python
# Instalar: pip install mermaid
from mermaid import Mermaid

diagram = """
graph TB
    A[Usuario] --> B[Streamlit]
    B --> C[API Flask]
"""

Mermaid(diagram).to_png("diagrama.png")
```
