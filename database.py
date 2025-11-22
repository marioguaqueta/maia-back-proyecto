"""
Database module for storing analysis tasks and results
"""

import sqlite3
import json
import uuid
from datetime import datetime
from pathlib import Path

DB_PATH = Path(__file__).parent / "wildlife_detection.db"


def get_connection():
    """Get database connection."""
    conn = sqlite3.connect(str(DB_PATH))
    conn.row_factory = sqlite3.Row
    return conn


def init_database():
    """Initialize database tables."""
    conn = get_connection()
    cursor = conn.cursor()
    
    # Tasks table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            task_id TEXT PRIMARY KEY,
            model_type TEXT NOT NULL,
            created_at TIMESTAMP NOT NULL,
            status TEXT NOT NULL,
            filename TEXT,
            num_images INTEGER,
            processing_time_seconds REAL,
            total_detections INTEGER,
            images_with_detections INTEGER,
            species_counts TEXT,
            processing_params TEXT,
            error_message TEXT
        )
    """)
    
    # Results table  
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS task_results (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            task_id TEXT NOT NULL,
            result_data TEXT NOT NULL,
            created_at TIMESTAMP NOT NULL,
            FOREIGN KEY (task_id) REFERENCES tasks (task_id)
        )
    """)
    
    # Detections table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS detections (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            task_id TEXT NOT NULL,
            image_name TEXT NOT NULL,
            species TEXT NOT NULL,
            confidence REAL NOT NULL,
            x REAL,
            y REAL,
            bbox_x1 REAL,
            bbox_y1 REAL,
            bbox_x2 REAL,
            bbox_y2 REAL,
            detection_data TEXT,
            FOREIGN KEY (task_id) REFERENCES tasks (task_id)
        )
    """)
    
    conn.commit()
    conn.close()
    print(f"✓ Database initialized: {DB_PATH}")


def generate_task_id():
    """Generate unique task ID."""
    return str(uuid.uuid4())


def save_task(task_id, model_type, filename, num_images, processing_params):
    """Save new task."""
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
        INSERT INTO tasks (task_id, model_type, created_at, status, filename, num_images, processing_params)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (task_id, model_type, datetime.now().isoformat(), 'processing', filename, num_images, json.dumps(processing_params)))
    
    conn.commit()
    conn.close()
    return task_id


def update_task_success(task_id, processing_time, total_detections, images_with_detections, species_counts, result_data):
    """Update task with success."""
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
        UPDATE tasks SET status = 'completed', processing_time_seconds = ?,
               total_detections = ?, images_with_detections = ?, species_counts = ?
        WHERE task_id = ?
    """, (processing_time, total_detections, images_with_detections, json.dumps(species_counts), task_id))
    
    cursor.execute("""
        INSERT INTO task_results (task_id, result_data, created_at)
        VALUES (?, ?, ?)
    """, (task_id, json.dumps(result_data), datetime.now().isoformat()))
    
    conn.commit()
    conn.close()


def save_detections(task_id, detections, model_type):
    """Save detections."""
    conn = get_connection()
    cursor = conn.cursor()
    
    for d in detections:
        if model_type == 'yolo':
            cursor.execute("""
                INSERT INTO detections (task_id, image_name, species, confidence, x, y, bbox_x1, bbox_y1, bbox_x2, bbox_y2, detection_data)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (task_id, d.get('image', ''), d.get('class_name', ''), d.get('confidence', 0.0),
                  d.get('center', {}).get('x'), d.get('center', {}).get('y'),
                  d.get('bbox', {}).get('x1'), d.get('bbox', {}).get('y1'),
                  d.get('bbox', {}).get('x2'), d.get('bbox', {}).get('y2'),
                  json.dumps(d)))
        else:
            cursor.execute("""
                INSERT INTO detections (task_id, image_name, species, confidence, x, y, detection_data)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (task_id, d.get('images', ''), d.get('species', ''), d.get('scores', 0.0),
                  d.get('x'), d.get('y'), json.dumps(d)))
    
    conn.commit()
    conn.close()


def update_task_error(task_id, error_message):
    """Update task with error."""
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute("""
        UPDATE tasks SET status = 'failed', error_message = ?
        WHERE task_id = ?
    """, (error_message, task_id))
    
    conn.commit()
    conn.close()


def get_task_by_id(task_id):
    """Get task by ID."""
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM tasks WHERE task_id = ?", (task_id,))
    task_row = cursor.fetchone()
    
    if not task_row:
        conn.close()
        return None
    
    task = dict(task_row)
    if task['processing_params']:
        task['processing_params'] = json.loads(task['processing_params'])
    if task['species_counts']:
        task['species_counts'] = json.loads(task['species_counts'])
    
    cursor.execute("""
        SELECT result_data FROM task_results WHERE task_id = ?
        ORDER BY created_at DESC LIMIT 1
    """, (task_id,))
    
    result_row = cursor.fetchone()
    if result_row:
        task['result_data'] = json.loads(result_row['result_data'])
    
    conn.close()
    return task


def get_all_tasks(model_type=None, status=None, limit=100, offset=0):
    """Get all tasks with filtering."""
    conn = get_connection()
    cursor = conn.cursor()
    
    query = "SELECT * FROM tasks WHERE 1=1"
    params = []
    
    if model_type:
        query += " AND model_type = ?"
        params.append(model_type)
    if status:
        query += " AND status = ?"
        params.append(status)
    
    query += " ORDER BY created_at DESC LIMIT ? OFFSET ?"
    params.extend([limit, offset])
    
    cursor.execute(query, params)
    rows = cursor.fetchall()
    
    tasks = []
    for row in rows:
        task = dict(row)
        if task['processing_params']:
            task['processing_params'] = json.loads(task['processing_params'])
        if task['species_counts']:
            task['species_counts'] = json.loads(task['species_counts'])
        tasks.append(task)
    
    conn.close()
    return tasks


def get_database_stats():
    """Get database statistics."""
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute("SELECT COUNT(*) as count FROM tasks")
    total_tasks = cursor.fetchone()['count']
    
    cursor.execute("SELECT model_type, COUNT(*) as count FROM tasks GROUP BY model_type")
    tasks_by_model = {row['model_type']: row['count'] for row in cursor.fetchall()}
    
    cursor.execute("SELECT status, COUNT(*) as count FROM tasks GROUP BY status")
    tasks_by_status = {row['status']: row['count'] for row in cursor.fetchall()}
    
    cursor.execute("SELECT COUNT(*) as count FROM detections")
    total_detections = cursor.fetchone()['count']
    
    cursor.execute("SELECT species, COUNT(*) as count FROM detections GROUP BY species ORDER BY count DESC")
    species_distribution = {row['species']: row['count'] for row in cursor.fetchall()}
    
    conn.close()
    
    return {
        'total_tasks': total_tasks,
        'tasks_by_model': tasks_by_model,
        'tasks_by_status': tasks_by_status,
        'total_detections': total_detections,
        'species_distribution': species_distribution
    }


if __name__ == "__main__":
    init_database()
    print("Database ready!")

