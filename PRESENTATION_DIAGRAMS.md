# 🎨 Architecture Diagrams for Presentation

## Overview

This document contains professional architecture diagrams for the African Wildlife Detection System, ready for presentations. All diagrams are in Mermaid format and can be exported as images.

---

## 1. 🏗️ Backend Architecture - Complete

### High-Level Backend Architecture

```mermaid
graph TB
    subgraph "Client Layer"
        CLI[Client Applications]
        WEB[Web Browser]
        API_CLIENT[API Clients]
    end
    
    subgraph "API Gateway Layer"
        FLASK[Flask API Server<br/>Port 8000]
        SWAGGER[Swagger/OpenAPI<br/>Documentation]
    end
    
    subgraph "Model Layer"
        YOLO[YOLOv11 Model<br/>best.pt<br/>Bounding Box Detection]
        HERDNET[HerdNet Model<br/>baseline.pth<br/>Point Detection]
        LOADER[Model Loader<br/>Google Drive Sync]
    end
    
    subgraph "Processing Layer"
        IMG_PROC[Image Processing<br/>PIL, OpenCV]
        BATCH[Batch Processing<br/>ZIP Handler]
        ANNO[Annotation Generator<br/>Bounding Boxes/Points]
        BASE64[Base64 Encoder<br/>Image Serialization]
    end
    
    subgraph "Data Layer"
        DB[(SQLite Database<br/>wildlife_detection.db)]
        TASKS[Tasks Table]
        DETECTIONS[Detections Table]
    end
    
    subgraph "Configuration Layer"
        ENV[Environment Variables<br/>Model Paths, Extensions, etc.]
        COLORS[Color Scheme<br/>Species Mapping]
    end
    
    CLI --> FLASK
    WEB --> FLASK
    API_CLIENT --> FLASK
    FLASK --> SWAGGER
    
    FLASK --> YOLO
    FLASK --> HERDNET
    FLASK --> BATCH
    
    LOADER -.->|Downloads| YOLO
    LOADER -.->|Downloads| HERDNET
    
    YOLO --> IMG_PROC
    HERDNET --> IMG_PROC
    
    IMG_PROC --> ANNO
    ANNO --> BASE64
    
    FLASK --> DB
    DB --> TASKS
    DB --> DETECTIONS
    
    ENV -.->|Configures| FLASK
    ENV -.->|Configures| LOADER
    COLORS -.->|Configures| ANNO
    
    style FLASK fill:#4CAF50
    style YOLO fill:#2196F3
    style HERDNET fill:#FF9800
    style DB fill:#9C27B0
```

### Backend Component Details

```mermaid
graph LR
    subgraph "Flask Application (app.py)"
        INIT[Initialization<br/>Models & Database]
        ROUTES[API Endpoints<br/>8 Routes]
        HEALTH[Health Check]
        YOLO_BATCH[YOLO Batch Analysis]
        YOLO_SINGLE[YOLO Single Image]
        HERD_BATCH[HerdNet Batch Analysis]
        HERD_SINGLE[HerdNet Single Image]
        TASKS[Task Management]
        STATS[Database Statistics]
    end
    
    subgraph "Model Loader (model_loader.py)"
        GDRIVE[Google Drive API]
        CHECK[File Existence Check]
        DOWNLOAD[Download Models]
        VERIFY[Verify Models]
    end
    
    subgraph "Database (database.py)"
        INIT_DB[Initialize Schema]
        TASK_OPS[Task Operations<br/>CRUD]
        DET_OPS[Detection Operations<br/>Save/Query]
        STATS_OPS[Statistics Queries]
    end
    
    subgraph "Configuration"
        ENV_VARS[Environment Variables<br/>25+ Variables]
        SPANISH[Spanish Translation<br/>Species Names & Colors]
        FILE_EXT[Allowed Extensions<br/>Images & Archives]
    end
    
    INIT --> GDRIVE
    INIT --> INIT_DB
    ROUTES --> HEALTH
    ROUTES --> YOLO_BATCH
    ROUTES --> YOLO_SINGLE
    ROUTES --> HERD_BATCH
    ROUTES --> HERD_SINGLE
    ROUTES --> TASKS
    ROUTES --> STATS
    
    GDRIVE --> CHECK
    CHECK --> DOWNLOAD
    DOWNLOAD --> VERIFY
    
    INIT_DB --> TASK_OPS
    INIT_DB --> DET_OPS
    INIT_DB --> STATS_OPS
    
    ENV_VARS -.-> INIT
    SPANISH -.-> ROUTES
    FILE_EXT -.-> ROUTES
    
    style INIT fill:#4CAF50
    style ROUTES fill:#2196F3
    style GDRIVE fill:#FF9800
    style INIT_DB fill:#9C27B0
```

---

## 2. 💻 Frontend Architecture - Complete

### Streamlit Frontend Architecture

```mermaid
graph TB
    subgraph "User Interface Layer"
        BROWSER[Web Browser<br/>User Access]
        PAGES[Navigation Pages<br/>4 Main Pages]
    end
    
    subgraph "Page Components"
        NEW[🎯 New Analysis<br/>Upload & Configure]
        RESULTS[📊 View Results<br/>Past Analyses]
        STATS[📈 Statistics<br/>Database Insights]
        ABOUT[ℹ️ About<br/>Documentation]
    end
    
    subgraph "UI Components"
        UPLOAD[File Upload<br/>ZIP & Images]
        MODEL_SELECT[Model Selection<br/>YOLO/HerdNet Toggle]
        PARAMS[Parameter Controls<br/>Sliders & Inputs]
        ZOOM[Zoom Controls<br/>Slider + Quick Buttons]
        IMAGES[Image Display<br/>Side-by-Side View]
        TABLES[Detection Tables<br/>Data Grids]
        CHARTS[Plotly Charts<br/>Bar & Pie Charts]
    end
    
    subgraph "State Management"
        SESSION[Session State<br/>Zoom Levels, etc.]
        CACHE[Cache<br/>API Responses]
    end
    
    subgraph "Configuration"
        ENV_ST[Streamlit Env Vars<br/>20+ UI Parameters]
        TOML[config.toml<br/>Server Settings]
        CSS[Custom CSS<br/>Spanish Translation]
    end
    
    subgraph "API Integration"
        API_CALLS[HTTP Requests<br/>requests library]
        BASE64_DEC[Base64 Decoder<br/>Image Processing]
    end
    
    BROWSER --> PAGES
    PAGES --> NEW
    PAGES --> RESULTS
    PAGES --> STATS
    PAGES --> ABOUT
    
    NEW --> UPLOAD
    NEW --> MODEL_SELECT
    NEW --> PARAMS
    
    RESULTS --> IMAGES
    RESULTS --> ZOOM
    RESULTS --> TABLES
    RESULTS --> CHARTS
    
    STATS --> CHARTS
    
    ZOOM --> SESSION
    UPLOAD --> API_CALLS
    PARAMS --> API_CALLS
    
    API_CALLS --> BASE64_DEC
    BASE64_DEC --> IMAGES
    
    ENV_ST -.->|Configures| PARAMS
    ENV_ST -.->|Configures| ZOOM
    TOML -.->|Configures| UPLOAD
    CSS -.->|Styles| UPLOAD
    
    style BROWSER fill:#4CAF50
    style NEW fill:#2196F3
    style IMAGES fill:#FF9800
    style API_CALLS fill:#9C27B0
```

### Frontend Component Hierarchy

```mermaid
graph TD
    subgraph "Main Application (streamlit_app.py)"
        MAIN[main<br/>Entry Point]
        CONFIG[Load Configuration<br/>Env Vars & TOML]
    end
    
    subgraph "Page Functions"
        NEW_PAGE[new_analysis_page<br/>Analysis Interface]
        VIEW_PAGE[view_results_page<br/>Results Browser]
        STATS_PAGE[statistics_page<br/>DB Analytics]
        ABOUT_PAGE[about_page<br/>Documentation]
    end
    
    subgraph "Display Functions"
        DISPLAY[display_results<br/>Main Results]
        YOLO_CARD[render_yolo_image_card<br/>YOLO Results]
        HERD_CARD[render_herdnet_image_card<br/>HerdNet Results]
        MODAL[show_image_modal<br/>Zoom Dialog]
        TABLE[create_detections_table<br/>Data Table]
    end
    
    subgraph "Helper Functions"
        RECURSIVE[render_images_recursively<br/>Batch Display]
        BASE64_FUNC[base64_to_image<br/>Decoder]
    end
    
    MAIN --> CONFIG
    MAIN --> NEW_PAGE
    MAIN --> VIEW_PAGE
    MAIN --> STATS_PAGE
    MAIN --> ABOUT_PAGE
    
    NEW_PAGE --> DISPLAY
    VIEW_PAGE --> DISPLAY
    
    DISPLAY --> YOLO_CARD
    DISPLAY --> HERD_CARD
    DISPLAY --> TABLE
    
    YOLO_CARD --> MODAL
    HERD_CARD --> MODAL
    
    DISPLAY --> RECURSIVE
    RECURSIVE --> YOLO_CARD
    RECURSIVE --> HERD_CARD
    
    YOLO_CARD --> BASE64_FUNC
    HERD_CARD --> BASE64_FUNC
    MODAL --> BASE64_FUNC
    
    style MAIN fill:#4CAF50
    style NEW_PAGE fill:#2196F3
    style YOLO_CARD fill:#FF9800
    style HERD_CARD fill:#E91E63
```

---

## 3. 🔗 Backend-Frontend Integration

### Integration Architecture

```mermaid
graph TB
    subgraph "Frontend - Streamlit"
        UI[User Interface<br/>streamlit_app.py]
        UPLOAD_UI[File Upload Widget]
        PARAMS_UI[Parameter Controls]
        DISPLAY_UI[Results Display]
    end
    
    subgraph "Network Layer"
        HTTP[HTTP/HTTPS Protocol]
        JSON[JSON Payloads]
        MULTIPART[Multipart Form Data]
    end
    
    subgraph "Backend - Flask API"
        API[Flask Server<br/>app.py]
        ENDPOINTS[8 REST Endpoints]
        VALIDATION[Input Validation]
    end
    
    subgraph "API Endpoints"
        E1[GET /health]
        E2[GET /models/info]
        E3[POST /analyze-yolo]
        E4[POST /analyze-single-image-yolo]
        E5[POST /analyze-image]
        E6[POST /analyze-single-image-herdnet]
        E7[GET /tasks]
        E8[GET /database/stats]
    end
    
    subgraph "Response Flow"
        PROCESS[Model Processing]
        DB_SAVE[Save to Database]
        RESPONSE[JSON Response<br/>+ Base64 Images]
    end
    
    UI --> UPLOAD_UI
    UI --> PARAMS_UI
    
    UPLOAD_UI -->|File + Params| MULTIPART
    PARAMS_UI -->|Configuration| JSON
    
    MULTIPART --> HTTP
    JSON --> HTTP
    
    HTTP --> API
    API --> ENDPOINTS
    ENDPOINTS --> VALIDATION
    
    VALIDATION --> E1
    VALIDATION --> E2
    VALIDATION --> E3
    VALIDATION --> E4
    VALIDATION --> E5
    VALIDATION --> E6
    VALIDATION --> E7
    VALIDATION --> E8
    
    E3 --> PROCESS
    E4 --> PROCESS
    E5 --> PROCESS
    E6 --> PROCESS
    
    PROCESS --> DB_SAVE
    DB_SAVE --> RESPONSE
    
    RESPONSE --> HTTP
    HTTP --> DISPLAY_UI
    
    style UI fill:#4CAF50
    style API fill:#2196F3
    style PROCESS fill:#FF9800
    style RESPONSE fill:#9C27B0
```

### API Communication Flow

```mermaid
sequenceDiagram
    participant U as User
    participant FE as Frontend<br/>(Streamlit)
    participant API as Backend API<br/>(Flask)
    participant ML as ML Models<br/>(YOLO/HerdNet)
    participant DB as Database<br/>(SQLite)
    
    U->>FE: Upload images
    U->>FE: Select model & parameters
    U->>FE: Click "Ejecutar Análisis"
    
    FE->>FE: Validate inputs
    FE->>API: POST /analyze-yolo<br/>(multipart/form-data)
    
    API->>API: Validate file type
    API->>API: Generate Task ID
    API->>DB: Save task (processing)
    
    API->>API: Extract images from ZIP
    API->>ML: Run model inference
    ML->>ML: Detect animals
    ML->>ML: Generate annotations
    
    ML->>API: Return detections
    API->>API: Create annotated images
    API->>API: Encode to Base64
    
    API->>DB: Update task (completed)
    API->>DB: Save detections
    
    API->>FE: JSON Response<br/>(detections + images)
    
    FE->>FE: Decode Base64 images
    FE->>FE: Render results
    FE->>U: Display detections
    
    U->>FE: Adjust zoom
    FE->>FE: Resize images
    FE->>U: Update display
```

---

## 4. 🔄 Complete System Interaction

### Full System Flow

```mermaid
graph TB
    subgraph "User Layer"
        USER[User/Researcher]
        BROWSER[Web Browser]
    end
    
    subgraph "Frontend Application"
        ST_UI[Streamlit UI<br/>Port 8501]
        FILE_UP[File Upload]
        MODEL_SEL[Model Selection]
        PARAM_SET[Parameter Settings]
        RESULT_VIZ[Result Visualization]
    end
    
    subgraph "API Layer"
        FLASK_API[Flask REST API<br/>Port 8000]
        SWAGGER_UI[Swagger Documentation<br/>/docs]
        AUTH[Request Validation]
    end
    
    subgraph "Processing Pipeline"
        PRE[Preprocessing<br/>Image Loading]
        INF_Y[YOLOv11 Inference]
        INF_H[HerdNet Inference]
        POST[Postprocessing<br/>Annotations]
        ENCODE[Base64 Encoding]
    end
    
    subgraph "ML Models"
        YOLO_M[YOLOv11<br/>best.pt<br/>150MB]
        HERD_M[HerdNet<br/>baseline.pth<br/>90MB]
    end
    
    subgraph "Storage Layer"
        DB_MAIN[(SQLite DB<br/>wildlife_detection.db)]
        TASKS_T[Tasks Table<br/>Metadata]
        DETECT_T[Detections Table<br/>Results]
    end
    
    subgraph "External Services"
        GDRIVE[Google Drive<br/>Model Storage]
    end
    
    USER --> BROWSER
    BROWSER --> ST_UI
    
    ST_UI --> FILE_UP
    ST_UI --> MODEL_SEL
    ST_UI --> PARAM_SET
    
    FILE_UP -->|HTTP POST| FLASK_API
    MODEL_SEL -->|HTTP POST| FLASK_API
    PARAM_SET -->|HTTP POST| FLASK_API
    
    FLASK_API --> AUTH
    FLASK_API -.->|Docs| SWAGGER_UI
    
    AUTH --> PRE
    PRE --> INF_Y
    PRE --> INF_H
    
    INF_Y --> YOLO_M
    INF_H --> HERD_M
    
    YOLO_M --> POST
    HERD_M --> POST
    
    POST --> ENCODE
    
    FLASK_API --> DB_MAIN
    DB_MAIN --> TASKS_T
    DB_MAIN --> DETECT_T
    
    ENCODE -->|JSON + Base64| ST_UI
    ST_UI --> RESULT_VIZ
    RESULT_VIZ --> BROWSER
    
    GDRIVE -.->|Download on startup| YOLO_M
    GDRIVE -.->|Download on startup| HERD_M
    
    style USER fill:#4CAF50
    style ST_UI fill:#2196F3
    style FLASK_API fill:#FF9800
    style YOLO_M fill:#E91E63
    style HERD_M fill:#9C27B0
    style DB_MAIN fill:#00BCD4
```

### Deployment Architecture

```mermaid
graph TB
    subgraph "Production Environment"
        subgraph "EC2 Instance - Ubuntu"
            subgraph "Docker Containers"
                BACKEND[Backend Container<br/>Flask API<br/>Port 8000]
                FRONTEND[Frontend Container<br/>Streamlit<br/>Port 8501]
            end
            
            subgraph "Volumes"
                VOL_MODELS[Models Volume<br/>best.pt & baseline.pth]
                VOL_DB[Database Volume<br/>wildlife_detection.db]
                VOL_UPLOADS[Uploads Volume<br/>Temporary Files]
            end
            
            NGINX[Nginx Reverse Proxy<br/>Port 80/443]
        end
        
        subgraph "External Storage"
            GDRIVE_EXT[Google Drive<br/>Model Backup]
        end
    end
    
    subgraph "Users"
        RESEARCHER[Researchers]
        ANALYST[Data Analysts]
        ADMIN[Administrators]
    end
    
    subgraph "CI/CD"
        GITHUB[GitHub Repository]
        ACTIONS[GitHub Actions<br/>Deploy Workflow]
    end
    
    RESEARCHER -->|HTTPS| NGINX
    ANALYST -->|HTTPS| NGINX
    ADMIN -->|HTTPS| NGINX
    
    NGINX --> FRONTEND
    NGINX --> BACKEND
    
    FRONTEND --> BACKEND
    
    BACKEND --> VOL_MODELS
    BACKEND --> VOL_DB
    BACKEND --> VOL_UPLOADS
    
    GDRIVE_EXT -.->|Initial Download| VOL_MODELS
    
    GITHUB --> ACTIONS
    ACTIONS -->|SSH Deploy| BACKEND
    ACTIONS -->|SSH Deploy| FRONTEND
    
    style BACKEND fill:#4CAF50
    style FRONTEND fill:#2196F3
    style NGINX fill:#FF9800
    style GDRIVE_EXT fill:#FFC107
```

---

## 5. 📊 Data Flow Diagrams

### YOLO Analysis Data Flow

```mermaid
graph LR
    subgraph "Input"
        ZIP[ZIP File<br/>Multiple Images]
        PARAMS[Parameters<br/>Conf, IOU, Size]
    end
    
    subgraph "Upload & Extract"
        UPLOAD[Upload to Flask]
        EXTRACT[Extract Images]
        VALIDATE[Validate Files]
    end
    
    subgraph "Processing"
        LOAD[Load Images<br/>PIL]
        PREPROC[Preprocessing<br/>Resize, Normalize]
        YOLO_INF[YOLOv11 Inference]
        DETECT[Extract Detections<br/>Bboxes, Classes, Conf]
    end
    
    subgraph "Annotation"
        DRAW[Draw Bounding Boxes]
        LABEL[Add Labels<br/>Species + Confidence]
        COLOR[Apply Colors<br/>Per Species]
    end
    
    subgraph "Output Preparation"
        ORIG_B64[Encode Original<br/>Base64]
        ANNO_B64[Encode Annotated<br/>Base64]
        JSON_PREP[Prepare JSON<br/>Detections + Images]
    end
    
    subgraph "Storage"
        SAVE_TASK[Save Task Info]
        SAVE_DET[Save Detections]
    end
    
    subgraph "Response"
        JSON_RESP[JSON Response<br/>Summary + Images]
        DISPLAY[Frontend Display]
    end
    
    ZIP --> UPLOAD
    PARAMS --> UPLOAD
    
    UPLOAD --> EXTRACT
    EXTRACT --> VALIDATE
    VALIDATE --> LOAD
    
    LOAD --> PREPROC
    PREPROC --> YOLO_INF
    YOLO_INF --> DETECT
    
    DETECT --> DRAW
    DRAW --> LABEL
    LABEL --> COLOR
    
    LOAD --> ORIG_B64
    COLOR --> ANNO_B64
    DETECT --> JSON_PREP
    ORIG_B64 --> JSON_PREP
    ANNO_B64 --> JSON_PREP
    
    JSON_PREP --> SAVE_TASK
    JSON_PREP --> SAVE_DET
    
    SAVE_TASK --> JSON_RESP
    SAVE_DET --> JSON_RESP
    
    JSON_RESP --> DISPLAY
    
    style ZIP fill:#4CAF50
    style YOLO_INF fill:#2196F3
    style JSON_RESP fill:#FF9800
```

### HerdNet Analysis Data Flow

```mermaid
graph LR
    subgraph "Input"
        ZIP_H[ZIP File<br/>Aerial Images]
        PARAMS_H[Parameters<br/>Patch, Overlap, Rotation]
    end
    
    subgraph "Upload & Extract"
        UPLOAD_H[Upload to Flask]
        EXTRACT_H[Extract Images]
        VALIDATE_H[Validate Files]
    end
    
    subgraph "Dataset Preparation"
        DF[Create DataFrame]
        CSV_DS[CSVDataset]
        DL[DataLoader]
        TRANS[Apply Transforms<br/>Rotate, Normalize]
    end
    
    subgraph "Processing"
        STITCH[HerdNet Stitcher<br/>Patch-based]
        EVAL[HerdNet Evaluator]
        LMDS[Local Maxima Detection]
        POINTS[Extract Points<br/>x, y, class, score]
    end
    
    subgraph "Visualization"
        DRAW_P[Draw Points<br/>Red Circles]
        THUMB[Generate Thumbnails<br/>Per Detection]
        PLOT[Create Plot Image]
    end
    
    subgraph "Output Preparation"
        ORIG_B64_H[Encode Original<br/>Base64]
        PLOT_B64[Encode Plot<br/>Base64]
        THUMB_B64[Encode Thumbnails<br/>Base64]
        JSON_PREP_H[Prepare JSON<br/>Points + Images]
    end
    
    subgraph "Storage"
        SAVE_TASK_H[Save Task Info]
        SAVE_DET_H[Save Detections]
    end
    
    subgraph "Response"
        JSON_RESP_H[JSON Response<br/>Points + Plots]
        DISPLAY_H[Frontend Display]
    end
    
    ZIP_H --> UPLOAD_H
    PARAMS_H --> UPLOAD_H
    
    UPLOAD_H --> EXTRACT_H
    EXTRACT_H --> VALIDATE_H
    VALIDATE_H --> DF
    
    DF --> CSV_DS
    CSV_DS --> TRANS
    TRANS --> DL
    
    DL --> STITCH
    STITCH --> EVAL
    EVAL --> LMDS
    LMDS --> POINTS
    
    POINTS --> DRAW_P
    DRAW_P --> PLOT
    POINTS --> THUMB
    
    VALIDATE_H --> ORIG_B64_H
    PLOT --> PLOT_B64
    THUMB --> THUMB_B64
    
    POINTS --> JSON_PREP_H
    ORIG_B64_H --> JSON_PREP_H
    PLOT_B64 --> JSON_PREP_H
    THUMB_B64 --> JSON_PREP_H
    
    JSON_PREP_H --> SAVE_TASK_H
    JSON_PREP_H --> SAVE_DET_H
    
    SAVE_TASK_H --> JSON_RESP_H
    SAVE_DET_H --> JSON_RESP_H
    
    JSON_RESP_H --> DISPLAY_H
    
    style ZIP_H fill:#4CAF50
    style EVAL fill:#9C27B0
    style JSON_RESP_H fill:#FF9800
```

---

## 6. 🎯 Technology Stack

### Complete Technology Stack

```mermaid
graph TB
    subgraph "Frontend Technologies"
        ST[Streamlit 1.28+<br/>Web Framework]
        PY_FE[Python 3.11<br/>Language]
        PIL_FE[Pillow<br/>Image Processing]
        PLOTLY[Plotly<br/>Data Visualization]
        REQ[Requests<br/>HTTP Client]
        TOML_LIB[TOML<br/>Configuration]
    end
    
    subgraph "Backend Technologies"
        FLASK[Flask 3.0+<br/>Web Framework]
        PY_BE[Python 3.11<br/>Language]
        TORCH[PyTorch 2.0+<br/>Deep Learning]
        CV[OpenCV<br/>Computer Vision]
        PIL_BE[Pillow<br/>Image Processing]
        NUMPY[NumPy<br/>Numerical Computing]
        PANDAS[Pandas<br/>Data Analysis]
    end
    
    subgraph "ML Models"
        ULTRA[Ultralytics<br/>YOLOv11]
        ANIMALOC[AnimalOC<br/>HerdNet]
        ALBUM[Albumentations<br/>Augmentations]
    end
    
    subgraph "API & Documentation"
        FLASGGER[Flasgger<br/>Swagger/OpenAPI]
        WERKZEUG[Werkzeug<br/>WSGI Utilities]
    end
    
    subgraph "Data Storage"
        SQLITE[SQLite<br/>Database]
        JSON_LIB[JSON<br/>Serialization]
        B64[Base64<br/>Encoding]
    end
    
    subgraph "DevOps"
        DOCKER[Docker<br/>Containerization]
        COMPOSE[Docker Compose<br/>Orchestration]
        GITHUB_A[GitHub Actions<br/>CI/CD]
        NGINX_T[Nginx<br/>Reverse Proxy]
    end
    
    subgraph "Cloud Services"
        EC2[AWS EC2<br/>Compute]
        GDRIVE_T[Google Drive<br/>Storage]
    end
    
    ST --> PY_FE
    ST --> PIL_FE
    ST --> PLOTLY
    ST --> REQ
    ST --> TOML_LIB
    
    FLASK --> PY_BE
    FLASK --> TORCH
    FLASK --> CV
    FLASK --> PIL_BE
    FLASK --> NUMPY
    FLASK --> PANDAS
    
    TORCH --> ULTRA
    TORCH --> ANIMALOC
    TORCH --> ALBUM
    
    FLASK --> FLASGGER
    FLASK --> WERKZEUG
    
    FLASK --> SQLITE
    FLASK --> JSON_LIB
    FLASK --> B64
    
    DOCKER --> COMPOSE
    COMPOSE --> FLASK
    COMPOSE --> ST
    
    GITHUB_A --> EC2
    EC2 --> NGINX_T
    NGINX_T --> DOCKER
    
    GDRIVE_T -.-> ULTRA
    GDRIVE_T -.-> ANIMALOC
    
    style ST fill:#FF4B4B
    style FLASK fill:#4CAF50
    style TORCH fill:#EE4C2C
    style DOCKER fill:#2496ED
```

---

## 7. 📱 User Journey

### End-to-End User Journey

```mermaid
journey
    title Wildlife Detection Analysis - User Journey
    section Upload
      Navigate to website: 5: User
      Select model (YOLO/HerdNet): 4: User
      Upload ZIP file: 4: User
      Configure parameters: 3: User
    section Processing
      Submit analysis: 5: User
      Wait for processing: 2: User, System
      Receive notification: 4: User, System
    section Results
      View summary statistics: 5: User
      See detection images: 5: User
      Use zoom controls: 4: User
      Click quick zoom buttons: 5: User
      Inspect details: 4: User
    section Analysis
      Check species counts: 5: User
      View detection tables: 4: User
      Compare images: 4: User
      Export findings: 3: User
    section Follow-up
      Save task ID: 4: User
      View historical results: 3: User
      Check statistics: 3: User
```

---

## 8. 🔐 Security Architecture

### Security Layers

```mermaid
graph TB
    subgraph "External Layer"
        USERS[Users/Clients]
        FIREWALL[Firewall<br/>AWS Security Groups]
    end
    
    subgraph "Network Layer"
        SSL[SSL/TLS<br/>HTTPS]
        NGINX_S[Nginx<br/>Reverse Proxy]
        RATE[Rate Limiting]
    end
    
    subgraph "Application Layer"
        INPUT_VAL[Input Validation<br/>File Types, Sizes]
        SANIT[File Sanitization<br/>Secure Filenames]
        CSRF[CSRF Protection]
    end
    
    subgraph "Processing Layer"
        SANDBOX[Sandboxed Processing<br/>Temp Directories]
        CLEANUP[Automatic Cleanup<br/>After Processing]
        ERROR_HAND[Error Handling<br/>No Data Leakage]
    end
    
    subgraph "Data Layer"
        DB_PERM[Database Permissions]
        ENV_SEC[Environment Variables<br/>Secrets]
        NO_GITIGNORE[.gitignore<br/>Sensitive Files]
    end
    
    USERS --> FIREWALL
    FIREWALL --> SSL
    SSL --> NGINX_S
    NGINX_S --> RATE
    
    RATE --> INPUT_VAL
    INPUT_VAL --> SANIT
    SANIT --> CSRF
    
    CSRF --> SANDBOX
    SANDBOX --> CLEANUP
    CLEANUP --> ERROR_HAND
    
    ERROR_HAND --> DB_PERM
    DB_PERM --> ENV_SEC
    ENV_SEC --> NO_GITIGNORE
    
    style FIREWALL fill:#F44336
    style SSL fill:#FF9800
    style INPUT_VAL fill:#4CAF50
    style SANDBOX fill:#2196F3
```

---

## 📥 Export Instructions

### How to Use These Diagrams

#### 1. **Markdown/Documentation**
- Copy the Mermaid code directly into your presentation tool
- Most modern tools (GitLab, GitHub, Obsidian) support Mermaid natively

#### 2. **Export as Images**

**Online Tools:**
- [Mermaid Live Editor](https://mermaid.live/): Paste code → Export as PNG/SVG
- [Kroki](https://kroki.io/): Generate images via URL

**CLI Tool:**
```bash
# Install mermaid-cli
npm install -g @mermaid-js/mermaid-cli

# Convert to PNG
mmdc -i diagram.mmd -o diagram.png -w 1920 -H 1080

# Convert to SVG (vector, scalable)
mmdc -i diagram.mmd -o diagram.svg
```

#### 3. **PowerPoint/Google Slides**
1. Export diagrams as PNG (high resolution: 1920x1080)
2. Insert as images into slides
3. Add annotations and labels as needed

#### 4. **LaTeX/Beamer**
```latex
\begin{figure}
  \centering
  \includegraphics[width=\textwidth]{backend_architecture.png}
  \caption{Backend Architecture}
\end{figure}
```

---

## 🎨 Presentation Slide Suggestions

### Slide 1: System Overview
- Use **Diagram 4: Complete System Interaction**
- Title: "African Wildlife Detection System Architecture"
- Bullet points: Key components, technologies, features

### Slide 2: Backend Architecture
- Use **Diagram 1: Backend Architecture - Complete**
- Title: "Backend Infrastructure"
- Bullet points: Flask API, ML models, database

### Slide 3: Frontend Architecture
- Use **Diagram 2: Frontend Architecture - Complete**
- Title: "User Interface & Experience"
- Bullet points: Streamlit UI, responsive design, real-time updates

### Slide 4: Integration
- Use **Diagram 3: Backend-Frontend Integration**
- Title: "System Integration"
- Bullet points: REST API, JSON responses, Base64 encoding

### Slide 5: Data Flow - YOLO
- Use **Diagram 5: YOLO Analysis Data Flow**
- Title: "YOLOv11 Processing Pipeline"
- Bullet points: Fast detection, bounding boxes, real-time

### Slide 6: Data Flow - HerdNet
- Use **Diagram 5: HerdNet Analysis Data Flow**
- Title: "HerdNet Processing Pipeline"
- Bullet points: Large images, point detection, thumbnails

### Slide 7: Technology Stack
- Use **Diagram 6: Technology Stack**
- Title: "Technologies & Tools"
- Bullet points: Python, PyTorch, Docker, Cloud

### Slide 8: Deployment
- Use **Deployment Architecture** from Diagram 4
- Title: "Production Deployment"
- Bullet points: AWS EC2, Docker, CI/CD, scalability

### Slide 9: Security
- Use **Diagram 8: Security Architecture**
- Title: "Security & Data Protection"
- Bullet points: SSL, validation, sandboxing, secrets

### Slide 10: User Experience
- Use **Diagram 7: User Journey**
- Title: "User Workflow"
- Bullet points: Simple upload, fast processing, rich results

---

## 📊 Diagram Color Legend

- 🟢 **Green (#4CAF50)**: User-facing components, entry points
- 🔵 **Blue (#2196F3)**: Core processing, API services
- 🟠 **Orange (#FF9800)**: Machine learning, AI models
- 🟣 **Purple (#9C27B0)**: Data storage, persistence
- 🔴 **Red (#F44336)**: Security, validation
- 🟡 **Yellow (#FFC107)**: External services, integrations

---

**Version**: 1.0.0  
**Created**: November 2025  
**Format**: Mermaid Diagrams  
**Purpose**: Presentation & Documentation

