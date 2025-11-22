# Wildlife Detection System - Architecture Diagrams

## 1. High-Level Architecture

```mermaid
graph TB
    subgraph "User Interface"
        User[👤 End User<br/>Web Browser]
    end
    
    subgraph "Streamlit Cloud ☁️"
        Frontend[🌐 Streamlit Frontend<br/>streamlit_app.py<br/>Port: 8501]
    end
    
    subgraph "AWS EC2 Instance 🖥️"
        Backend[🔧 Flask Backend API<br/>app.py<br/>Port: 8000]
        Database[(💾 SQLite DB<br/>wildlife_detection.db)]
        Models[🤖 ML Models<br/>- YOLOv11 best.pt<br/>- HerdNet herdnet_model.pth]
    end
    
    subgraph "Google Drive ☁️"
        GDrive[(📦 Model Storage<br/>Folder ID: 11uMn45...)]
    end
    
    User -->|HTTPS| Frontend
    Frontend -->|REST API<br/>HTTP Requests| Backend
    Backend -->|Read/Write| Database
    Backend -->|Load Models| Models
    Backend -.->|Download<br/>On First Run| GDrive
    Backend -->|JSON Response| Frontend
    Frontend -->|Display Results| User
    
    style Frontend fill:#e1f5ff
    style Backend fill:#fff4e1
    style Database fill:#f0f0f0
    style Models fill:#e8f5e9
    style GDrive fill:#fff3e0
    style User fill:#f3e5f5
```

---

## 2. Deployment Architecture

```mermaid
graph TB
    subgraph "Internet 🌐"
        Users[👥 Users]
    end
    
    subgraph "Streamlit Cloud - Frontend"
        StreamlitApp[Streamlit Web App<br/>- Python 3.11<br/>- requirements-streamlit.txt<br/>- Minimal dependencies]
        StreamlitConfig[Secrets Configuration<br/>API_BASE_URL]
    end
    
    subgraph "AWS EC2 Instance - Backend"
        LB[Load Balancer /<br/>Reverse Proxy]
        
        subgraph "Docker Container"
            Gunicorn[Gunicorn WSGI Server<br/>2 workers, 2 threads<br/>Port: 8000]
            FlaskApp[Flask Application<br/>- app.py<br/>- database.py<br/>- model_loader.py<br/>- infer.py]
            
            subgraph "Storage"
                DB[(SQLite DB)]
                ModelsDir[Models Directory<br/>best.pt<br/>herdnet_model.pth]
                Uploads[Uploads/<br/>Temporary Files]
            end
        end
        
        SecurityGroup[Security Group<br/>- Port 8000: HTTP<br/>- Port 22: SSH]
    end
    
    subgraph "External Services"
        GDrive[Google Drive<br/>Model Downloads]
    end
    
    Users -->|HTTPS| StreamlitApp
    StreamlitConfig -.->|Configure| StreamlitApp
    StreamlitApp -->|HTTP API Calls| LB
    LB --> Gunicorn
    Gunicorn --> FlaskApp
    FlaskApp --> DB
    FlaskApp --> ModelsDir
    FlaskApp --> Uploads
    FlaskApp -.->|First Run| GDrive
    SecurityGroup -.->|Protects| LB
    
    style StreamlitApp fill:#00d4ff
    style FlaskApp fill:#ff9800
    style Gunicorn fill:#4caf50
    style DB fill:#9e9e9e
    style SecurityGroup fill:#f44336
    style GDrive fill:#ffc107
```

---

## 3. Data Flow Diagram

```mermaid
sequenceDiagram
    participant User
    participant Streamlit as Streamlit Frontend<br/>(Streamlit Cloud)
    participant API as Flask Backend<br/>(AWS EC2)
    participant DB as SQLite Database
    participant Models as ML Models<br/>(YOLO/HerdNet)
    participant GDrive as Google Drive
    
    Note over User,GDrive: First Time Setup
    API->>GDrive: Check if models exist
    GDrive-->>API: Download best.pt & herdnet_model.pth
    API->>DB: Initialize database schema
    
    Note over User,GDrive: Image Analysis Workflow
    User->>Streamlit: Upload ZIP file
    User->>Streamlit: Select model & parameters
    Streamlit->>API: POST /analyze-yolo or /analyze-image
    
    API->>DB: Generate task_id, save task
    API->>API: Extract images from ZIP
    API->>Models: Load model & run inference
    Models-->>API: Detection results
    
    API->>API: Generate annotated images/thumbnails
    API->>DB: Save complete results + detections
    API-->>Streamlit: JSON response with task_id
    
    Streamlit->>Streamlit: Parse results & create visualizations
    Streamlit->>User: Display table, charts, images
    
    Note over User,GDrive: Retrieve Past Results
    User->>Streamlit: Enter task_id or browse history
    Streamlit->>API: GET /tasks/{task_id}
    API->>DB: Query task & results
    DB-->>API: Complete JSON response
    API-->>Streamlit: Task data with images
    Streamlit->>User: Display past analysis
    
    Note over User,GDrive: View Statistics
    User->>Streamlit: Open statistics page
    Streamlit->>API: GET /database/stats
    API->>DB: Aggregate statistics
    DB-->>API: Counts & distributions
    API-->>Streamlit: Statistics JSON
    Streamlit->>Streamlit: Create charts
    Streamlit->>User: Display statistics dashboard
```

---

## 4. Component Interaction

```mermaid
graph LR
    subgraph "Frontend Components"
        UI1[New Analysis Page]
        UI2[View Results Page]
        UI3[Statistics Page]
        UI4[About Page]
    end
    
    subgraph "API Endpoints"
        EP1[POST /analyze-yolo]
        EP2[POST /analyze-image]
        EP3[GET /tasks]
        EP4[GET /tasks/task_id]
        EP5[GET /database/stats]
        EP6[GET /health]
    end
    
    subgraph "Backend Services"
        Service1[YOLO Inference]
        Service2[HerdNet Inference]
        Service3[Database Service]
        Service4[Model Loader]
    end
    
    subgraph "Data Storage"
        DB1[(tasks table)]
        DB2[(task_results table)]
        DB3[(detections table)]
        Files[(Model Files)]
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

## 5. Deployment Flow

```mermaid
graph TD
    Start([Start Deployment])
    
    subgraph "Backend Deployment (EC2)"
        B1[Push code to GitHub]
        B2[SSH into EC2 instance]
        B3[Pull latest code]
        B4[Build Docker image]
        B5[Run docker-compose up]
        B6[Models download from GDrive]
        B7[Database initializes]
        B8[Backend ready on port 8000]
    end
    
    subgraph "Frontend Deployment (Streamlit Cloud)"
        F1[Push code to GitHub]
        F2[Login to Streamlit Cloud]
        F3[Create/Update app]
        F4[Configure settings<br/>- Python 3.11<br/>- requirements-streamlit.txt]
        F5[Set secrets<br/>API_BASE_URL]
        F6[Deploy app]
        F7[Frontend ready on 8501]
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
    
    B8 --> Connected{Backend <-> Frontend<br/>Connected?}
    F7 --> Connected
    
    Connected -->|Yes| Success([✅ Deployment Complete])
    Connected -->|No| Debug[Debug connection<br/>Check API_BASE_URL<br/>Check security groups]
    Debug --> Connected
    
    style B1 fill:#ffecb3
    style B8 fill:#c8e6c9
    style F1 fill:#e1bee7
    style F7 fill:#b2dfdb
    style Success fill:#81c784
    style Debug fill:#ffab91
```

---

## 6. Security Architecture

```mermaid
graph TB
    subgraph "Public Internet"
        Internet[🌐 Internet Users]
    end
    
    subgraph "Streamlit Cloud"
        StreamlitSSL[HTTPS SSL/TLS]
        StreamlitApp[Streamlit App<br/>No sensitive data<br/>Only UI logic]
    end
    
    subgraph "AWS EC2"
        SecurityGroup[AWS Security Group]
        
        subgraph "Docker Container"
            FlaskSSL[HTTP/HTTPS<br/>Consider adding SSL]
            FlaskApp[Flask Backend]
            
            subgraph "Protected Resources"
                DB[SQLite Database<br/>- task_id as primary key<br/>- No user authentication yet]
                Models[ML Models<br/>Read-only access]
                Uploads[Temporary Uploads<br/>Auto-cleanup]
            end
        end
    end
    
    subgraph "External Services"
        GDriveAPI[Google Drive API<br/>Read-only access<br/>Public folder]
    end
    
    Internet -->|HTTPS| StreamlitSSL
    StreamlitSSL --> StreamlitApp
    StreamlitApp -->|HTTP API| SecurityGroup
    
    SecurityGroup -->|Port 8000| FlaskSSL
    SecurityGroup -->|Port 22 SSH<br/>IP Restricted| FlaskApp
    
    FlaskSSL --> FlaskApp
    FlaskApp --> DB
    FlaskApp --> Models
    FlaskApp --> Uploads
    FlaskApp -.->|HTTPS| GDriveAPI
    
    Note1[🔒 Security Measures:<br/>- Security Groups limit access<br/>- API has no authentication yet<br/>- Database stored locally<br/>- Model files read-only<br/>- Temporary files auto-deleted]
    
    style SecurityGroup fill:#f44336
    style StreamlitSSL fill:#4caf50
    style FlaskSSL fill:#ff9800
    style DB fill:#9e9e9e
    style Note1 fill:#fff9c4
```

---

## Technology Stack

### Frontend (Streamlit Cloud)
- **Framework**: Streamlit 1.28.0
- **Language**: Python 3.11
- **Visualization**: Plotly
- **HTTP Client**: requests
- **Deployment**: Streamlit Cloud (Free Tier)

### Backend (AWS EC2)
- **Framework**: Flask 3.0.0
- **WSGI Server**: Gunicorn
- **Language**: Python 3.11
- **Container**: Docker
- **Database**: SQLite
- **ML Models**: 
  - YOLOv11 (ultralytics)
  - HerdNet (custom)
- **Deep Learning**: PyTorch
- **Computer Vision**: OpenCV, albumentations
- **Deployment**: AWS EC2 (Docker Compose)

### External Services
- **Model Storage**: Google Drive
- **Version Control**: GitHub
- **CI/CD**: Manual deployment (can be automated)

---

## Scaling Considerations

```mermaid
graph TB
    subgraph "Current Architecture"
        C1[Single EC2 Instance]
        C2[SQLite Database]
        C3[Local Model Storage]
    end
    
    subgraph "Future Scaling Options"
        S1[Load Balancer + Multiple EC2]
        S2[PostgreSQL / RDS]
        S3[S3 for Model Storage]
        S4[Redis Cache]
        S5[Async Queue Celery]
    end
    
    C1 -.->|Scale to| S1
    C2 -.->|Migrate to| S2
    C3 -.->|Move to| S3
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

## How to Convert These to PNG

### Option 1: Using Mermaid CLI
```bash
# Install mermaid-cli
npm install -g @mermaid-js/mermaid-cli

# Convert to PNG
mmdc -i ARCHITECTURE_DIAGRAM.md -o architecture.png -b transparent
```

### Option 2: Using Online Tools
1. Copy the mermaid code
2. Go to https://mermaid.live/
3. Paste the code
4. Click "Download PNG"

### Option 3: Using VS Code Extension
1. Install "Markdown Preview Mermaid Support" extension
2. Open this file in VS Code
3. Right-click on diagram → "Export as PNG"

### Option 4: Using Python
```python
# Install: pip install mermaid
from mermaid import Mermaid

diagram = """
graph TB
    A[User] --> B[Streamlit]
    B --> C[Flask API]
"""

Mermaid(diagram).to_png("diagram.png")
```

