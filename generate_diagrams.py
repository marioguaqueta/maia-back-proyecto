"""
Generate PNG diagrams from Mermaid markdown
Requires: pip install requests
"""

import os
import re
import requests
import base64
from pathlib import Path

# Mermaid diagrams as code
DIAGRAMS = {
    "1_architecture": """
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
""",
    
    "2_deployment": """
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
""",

    "3_dataflow": """
sequenceDiagram
    participant User
    participant Streamlit as Streamlit Frontend<br/>(Streamlit Cloud)
    participant API as Flask Backend<br/>(AWS EC2)
    participant DB as SQLite Database
    participant Models as ML Models<br/>(YOLO/HerdNet)
    
    Note over User,Models: Image Analysis Workflow
    User->>Streamlit: Upload ZIP file
    User->>Streamlit: Select model & parameters
    Streamlit->>API: POST /analyze-yolo or /analyze-image
    
    API->>DB: Generate task_id, save task
    API->>API: Extract images from ZIP
    API->>Models: Load model & run inference
    Models-->>API: Detection results
    
    API->>API: Generate annotated images
    API->>DB: Save complete results
    API-->>Streamlit: JSON response with task_id
    
    Streamlit->>Streamlit: Create visualizations
    Streamlit->>User: Display results
""",

    "4_components": """
graph LR
    subgraph "Frontend"
        UI1[New Analysis]
        UI2[View Results]
        UI3[Statistics]
    end
    
    subgraph "API Endpoints"
        EP1[POST /analyze-yolo]
        EP2[POST /analyze-image]
        EP3[GET /tasks]
        EP4[GET /database/stats]
    end
    
    subgraph "Backend Services"
        Service1[YOLO Inference]
        Service2[HerdNet Inference]
        Service3[Database Service]
    end
    
    subgraph "Storage"
        DB1[(tasks)]
        DB2[(results)]
        Files[(Models)]
    end
    
    UI1 --> EP1
    UI1 --> EP2
    UI2 --> EP3
    UI3 --> EP4
    
    EP1 --> Service1
    EP2 --> Service2
    EP3 --> Service3
    EP4 --> Service3
    
    Service1 --> Files
    Service2 --> Files
    Service3 --> DB1
    Service3 --> DB2
    
    style UI1 fill:#e3f2fd
    style UI2 fill:#e3f2fd
    style UI3 fill:#e3f2fd
    style Service1 fill:#fff3e0
    style Service2 fill:#fff3e0
    style Service3 fill:#e8f5e9
""",

    "5_deployment_flow": """
graph TD
    Start([Start])
    
    subgraph "Backend EC2"
        B1[Push to GitHub]
        B2[SSH to EC2]
        B3[Pull code]
        B4[Build Docker]
        B5[Run compose]
        B6[Backend Ready]
    end
    
    subgraph "Frontend Streamlit"
        F1[Push to GitHub]
        F2[Streamlit Cloud]
        F3[Configure]
        F4[Set secrets]
        F5[Deploy]
        F6[Frontend Ready]
    end
    
    Start --> B1
    Start --> F1
    
    B1 --> B2
    B2 --> B3
    B3 --> B4
    B4 --> B5
    B5 --> B6
    
    F1 --> F2
    F2 --> F3
    F3 --> F4
    F4 --> F5
    F5 --> F6
    
    B6 --> Success
    F6 --> Success
    Success([✅ Complete])
    
    style B6 fill:#c8e6c9
    style F6 fill:#b2dfdb
    style Success fill:#81c784
"""
}


def generate_diagrams_kroki():
    """Generate PNG diagrams using Kroki API (free, no install needed)"""
    print("Generating diagrams using Kroki API...\n")
    
    output_dir = Path("diagrams")
    output_dir.mkdir(exist_ok=True)
    
    for name, diagram in DIAGRAMS.items():
        print(f"Generating {name}.png...")
        
        try:
            # Kroki API endpoint
            url = "https://kroki.io/mermaid/png"
            
            # Send diagram to Kroki
            response = requests.post(
                url,
                json={"diagram_source": diagram},
                headers={"Content-Type": "application/json"}
            )
            
            if response.status_code == 200:
                # Save PNG
                output_file = output_dir / f"{name}.png"
                with open(output_file, 'wb') as f:
                    f.write(response.content)
                print(f"  ✅ Saved to {output_file}")
            else:
                print(f"  ❌ Error: {response.status_code}")
                
        except Exception as e:
            print(f"  ❌ Error: {str(e)}")
    
    print(f"\n✨ Done! Diagrams saved to {output_dir}/")
    print(f"\nGenerated files:")
    for file in sorted(output_dir.glob("*.png")):
        size_kb = file.stat().st_size / 1024
        print(f"  - {file.name} ({size_kb:.1f} KB)")


def generate_diagrams_mermaid_ink():
    """Alternative: Generate using mermaid.ink (simpler API)"""
    print("Generating diagrams using mermaid.ink API...\n")
    
    output_dir = Path("diagrams")
    output_dir.mkdir(exist_ok=True)
    
    for name, diagram in DIAGRAMS.items():
        print(f"Generating {name}.png...")
        
        try:
            # Encode diagram to base64
            diagram_bytes = diagram.encode('utf-8')
            diagram_base64 = base64.urlsafe_b64encode(diagram_bytes).decode('ascii')
            
            # mermaid.ink API
            url = f"https://mermaid.ink/img/{diagram_base64}"
            
            response = requests.get(url)
            
            if response.status_code == 200:
                output_file = output_dir / f"{name}.png"
                with open(output_file, 'wb') as f:
                    f.write(response.content)
                print(f"  ✅ Saved to {output_file}")
            else:
                print(f"  ❌ Error: {response.status_code}")
                
        except Exception as e:
            print(f"  ❌ Error: {str(e)}")
    
    print(f"\n✨ Done! Diagrams saved to {output_dir}/")


if __name__ == "__main__":
    print("="*60)
    print("🎨 Wildlife Detection System - Diagram Generator")
    print("="*60)
    print()
    
    # Try mermaid.ink first (simpler, more reliable)
    try:
        generate_diagrams_mermaid_ink()
    except Exception as e:
        print(f"mermaid.ink failed: {e}")
        print("\nTrying Kroki API...")
        generate_diagrams_kroki()
    
    print("\n" + "="*60)
    print("✅ Complete!")
    print("="*60)
    print("\nYou can also:")
    print("1. View diagrams: Open PNG files in diagrams/ folder")
    print("2. Edit diagrams: Modify DIAGRAMS dict in this script")
    print("3. Online editor: https://mermaid.live/")
    print("="*60)

