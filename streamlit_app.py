"""
Streamlit Web Interface for Wildlife Detection API
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

# Configuration - can be overridden via environment variable or Streamlit secrets
API_BASE_URL = os.getenv(
    "API_BASE_URL",
    st.secrets.get("API_BASE_URL", "http://localhost:8000")
)

# Page config
st.set_page_config(
    page_title="African Wildlife Detection",
    page_icon="🦁",
    layout="wide"
)

# Custom CSS
st.markdown("""
<style>
.stApp {
    max-width: 1400px;
    margin: 0 auto;
}
.upload-section {
    padding: 2rem;
    border-radius: 10px;
    background-color: #f0f2f6;
}
</style>
""", unsafe_allow_html=True)


def main():
    """Main Streamlit app."""
    st.title("🦁 African Wildlife Detection System")
    st.markdown("Powered by YOLOv11 and HerdNet deep learning models")
    
    # Sidebar navigation
    page = st.sidebar.selectbox(
        "Navigation",
        ["🎯 New Analysis", "📊 View Results", "📈 Statistics", "ℹ️ About"]
    )
    
    if page == "🎯 New Analysis":
        new_analysis_page()
    elif page == "📊 View Results":
        view_results_page()
    elif page == "📈 Statistics":
        statistics_page()
    elif page == "ℹ️ About":
        about_page()


def new_analysis_page():
    """Page for creating new analysis."""
    st.header("🎯 New Wildlife Detection Analysis")
    
    # Check API health
    try:
        response = requests.get(f"{API_BASE_URL}/health")
        health = response.json()
        
        col1, col2 = st.columns(2)
        with col1:
            st.success(f"✓ API Status: {health['status']}")
        with col2:
            models_info = health.get('models', {})
            yolo_status = "✓ Loaded" if models_info.get('yolov11', {}).get('loaded') else "✗ Not loaded"
            herdnet_status = "✓ Loaded" if models_info.get('herdnet', {}).get('loaded') else "✗ Not loaded"
            st.info(f"YOLOv11: {yolo_status} | HerdNet: {herdnet_status}")
    except:
        st.error("❌ Cannot connect to API. Please ensure the backend is running.")
        return
    
    st.markdown("---")
    
    # File upload
    st.subheader("📁 Upload Images")
    uploaded_file = st.file_uploader(
        "Upload a ZIP file containing images",
        type=['zip'],
        help="Upload a ZIP archive with wildlife images for analysis"
    )
    
    if not uploaded_file:
        st.info("👆 Please upload a ZIP file to continue")
        return
    
    st.success(f"✓ File uploaded: {uploaded_file.name} ({uploaded_file.size / 1024:.1f} KB)")
    
    # Model selection
    st.subheader("🤖 Model Selection")
    model_choice = st.radio(
        "Choose detection model:",
        ["YOLOv11 (Fast, Bounding Boxes)", "HerdNet (Aerial, Point Detection)"],
        help="YOLOv11: Fast detection with bounding boxes | HerdNet: Optimized for aerial imagery with point detection"
    )
    
    # Parameters based on model
    st.subheader("⚙️ Parameters")
    
    if "YOLO" in model_choice:
        col1, col2, col3 = st.columns(3)
        with col1:
            conf_threshold = st.slider("Confidence Threshold", 0.1, 0.9, 0.25, 0.05)
        with col2:
            iou_threshold = st.slider("IOU Threshold", 0.1, 0.9, 0.45, 0.05)
        with col3:
            img_size = st.selectbox("Image Size", [416, 480, 640, 800, 960, 1280], index=2)
        
        include_annotated = st.checkbox("Include annotated images", value=True)
        
    else:  # HerdNet
        col1, col2 = st.columns(2)
        with col1:
            patch_size = st.selectbox("Patch Size", [384, 512, 768, 1024], index=1)
            rotation = st.selectbox("Rotation (90° steps)", [0, 1, 2, 3], index=0)
        with col2:
            overlap = st.slider("Overlap (pixels)", 0, 300, 160, 16)
            thumbnail_size = st.slider("Thumbnail Size", 128, 512, 256, 32)
        
        col3, col4 = st.columns(2)
        with col3:
            include_thumbnails = st.checkbox("Include thumbnails", value=True)
        with col4:
            include_plots = st.checkbox("Include detection plots", value=False)
    
    # Run analysis button
    st.markdown("---")
    if st.button("🚀 Run Analysis", type="primary", use_container_width=True):
        with st.spinner("Processing images... This may take a few minutes."):
            try:
                # Prepare request
                files = {'file': uploaded_file.getvalue()}
                
                if "YOLO" in model_choice:
                    endpoint = f"{API_BASE_URL}/analyze-yolo"
                    data = {
                        'conf_threshold': conf_threshold,
                        'iou_threshold': iou_threshold,
                        'img_size': img_size,
                        'include_annotated_images': str(include_annotated).lower()
                    }
                else:
                    endpoint = f"{API_BASE_URL}/analyze-image"
                    data = {
                        'patch_size': patch_size,
                        'overlap': overlap,
                        'rotation': rotation,
                        'thumbnail_size': thumbnail_size,
                        'include_thumbnails': str(include_thumbnails).lower(),
                        'include_plots': str(include_plots).lower()
                    }
                
                # Make request
                response = requests.post(endpoint, files={'file': uploaded_file}, data=data)
                
                if response.status_code == 200:
                    result = response.json()
                    display_results(result, model_choice)
                else:
                    st.error(f"❌ Analysis failed: {response.json().get('message', 'Unknown error')}")
                    
            except Exception as e:
                st.error(f"❌ Error: {str(e)}")


def create_detections_table(result, model_choice):
    """Create a table showing detections per image and species."""
    detections = result.get('detections', [])
    
    if not detections:
        return None
    
    # Get all species from the result
    species_counts = result.get('summary', {}).get('species_counts', {})
    all_species = sorted(species_counts.keys())
    
    # Create a dictionary to store counts per image
    image_data = {}
    
    # Process detections based on model type
    if "YOLO" in model_choice:
        for det in detections:
            img_name = det.get('image', 'Unknown')
            species = det.get('class_name', 'Unknown')
            
            if img_name not in image_data:
                image_data[img_name] = {sp: 0 for sp in all_species}
                image_data[img_name]['Total'] = 0
            
            image_data[img_name][species] = image_data[img_name].get(species, 0) + 1
            image_data[img_name]['Total'] += 1
    else:  # HerdNet
        for det in detections:
            img_name = det.get('images', 'Unknown')
            species = det.get('species', 'Unknown')
            
            if img_name not in image_data:
                image_data[img_name] = {sp: 0 for sp in all_species}
                image_data[img_name]['Total'] = 0
            
            image_data[img_name][species] = image_data[img_name].get(species, 0) + 1
            image_data[img_name]['Total'] += 1
    
    # Convert to DataFrame
    rows = []
    for img_name, counts in image_data.items():
        row = {'Image': img_name, 'Total': counts['Total']}
        for species in all_species:
            row[species.capitalize()] = counts.get(species, 0)
        rows.append(row)
    
    df = pd.DataFrame(rows)
    
    # Reorder columns: Image, Total, then species
    cols = ['Image', 'Total'] + [sp.capitalize() for sp in all_species]
    df = df[cols]
    
    return df


@st.dialog("Image Viewer with Zoom", width="large")
def show_image_modal(img_data, img_name, model_type):
    """Display image in a modal with zoom and pan capabilities."""
    st.subheader(f"📷 {img_name}")
    
    # Decode image
    if model_type == "yolo":
        img_bytes = base64.b64decode(img_data['annotated_image_base64'])
        detections_count = img_data.get('detections_count', 0)
        st.info(f"🎯 {detections_count} detections")
    else:  # herdnet plot
        img_bytes = base64.b64decode(img_data['plot_base64'])
        st.info(f"📍 HerdNet Detection Plot")
    
    img = Image.open(BytesIO(img_bytes))
    
    # Get image dimensions
    width, height = img.size
    st.caption(f"Original size: {width} × {height} pixels")
    
    # Zoom controls
    st.markdown("---")
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        zoom_level = st.slider(
            "🔍 Zoom Level",
            min_value=50,
            max_value=200,
            value=100,
            step=10,
            format="%d%%",
            key=f"zoom_{img_name}"
        )
    
    # Calculate new dimensions based on zoom
    new_width = int(width * zoom_level / 100)
    new_height = int(height * zoom_level / 100)
    
    if zoom_level != 100:
        img_resized = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
        st.image(img_resized, use_column_width=False)
    else:
        st.image(img, use_column_width=True)
    
    # Download button
    st.markdown("---")
    buf = BytesIO()
    img.save(buf, format="PNG")
    btn = st.download_button(
        label="⬇️ Download Image",
        data=buf.getvalue(),
        file_name=f"{img_name}",
        mime="image/png",
        use_container_width=True
    )


def display_results(result, model_choice):
    """Display analysis results."""
    st.success("✅ Analysis Complete!")
    
    # Task ID
    st.info(f"📋 Task ID: `{result.get('task_id', 'N/A')}` - Save this to retrieve results later!")
    
    # Summary statistics
    st.subheader("📊 Summary")
    summary = result.get('summary', {})
    
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Images", summary.get('total_images', 0))
    col2.metric("Total Detections", summary.get('total_detections', 0))
    col3.metric("Images with Animals", summary.get('images_with_animals', summary.get('images_with_detections', 0)))
    col4.metric("Processing Time", f"{result.get('processing_time_seconds', 0):.1f}s")
    
    # Species distribution
    if summary.get('species_counts'):
        st.subheader("🦁 Species Distribution")
        species_df = pd.DataFrame(list(summary['species_counts'].items()), columns=['Species', 'Count'])
        
        col1, col2 = st.columns([1, 1])
        with col1:
            fig = px.bar(species_df, x='Species', y='Count', color='Species')
            st.plotly_chart(fig, use_container_width=True)
        with col2:
            fig = px.pie(species_df, names='Species', values='Count')
            st.plotly_chart(fig, use_container_width=True)
    
    # ========================================
    # NEW: Detections Table by Image
    # ========================================
    st.subheader("📋 Detections by Image")
    detections_df = create_detections_table(result, model_choice)
    
    if detections_df is not None:
        st.dataframe(
            detections_df,
            use_container_width=True,
            hide_index=True,
            column_config={
                "Image": st.column_config.TextColumn("Image", width="medium"),
                "Total": st.column_config.NumberColumn("Total", width="small"),
            }
        )
        
        # Download CSV button
        csv = detections_df.to_csv(index=False)
        st.download_button(
            label="⬇️ Download Table as CSV",
            data=csv,
            file_name=f"detections_table_{result.get('task_id', 'results')}.csv",
            mime="text/csv"
        )
    
    # ========================================
    # NEW: Image Gallery with View Buttons
    # ========================================
    
    # Annotated images (YOLO)
    if 'annotated_images' in result:
        st.subheader("🖼️ Annotated Images Gallery")
        
        # Create a mapping of image names to data
        image_map = {img['image_name']: img for img in result['annotated_images']}
        
        # Display in a grid
        for idx, img_data in enumerate(result['annotated_images']):
            col1, col2, col3 = st.columns([3, 1, 1])
            
            with col1:
                st.write(f"**{img_data['image_name']}**")
                st.caption(f"🎯 {img_data['detections_count']} detections | Size: {img_data.get('original_size', {}).get('width', '?')} × {img_data.get('original_size', {}).get('height', '?')} px")
            
            with col2:
                if st.button(f"👁️ View", key=f"view_yolo_{idx}"):
                    show_image_modal(img_data, img_data['image_name'], "yolo")
            
            with col3:
                # Download button for this specific image
                img_bytes = base64.b64decode(img_data['annotated_image_base64'])
                st.download_button(
                    label="⬇️ Download",
                    data=img_bytes,
                    file_name=img_data['image_name'],
                    mime="image/png",
                    key=f"dl_yolo_{idx}"
                )
            
            st.markdown("---")
    
    # Detection plots (HerdNet)
    if 'plots' in result:
        st.subheader("🗺️ Detection Plots Gallery")
        
        for idx, plot_data in enumerate(result['plots']):
            col1, col2, col3 = st.columns([3, 1, 1])
            
            with col1:
                st.write(f"**{plot_data['image_name']}**")
                st.caption(f"📍 Detection plot with points")
            
            with col2:
                if st.button(f"👁️ View", key=f"view_plot_{idx}"):
                    show_image_modal(plot_data, plot_data['image_name'], "herdnet")
            
            with col3:
                # Download button
                img_bytes = base64.b64decode(plot_data['plot_base64'])
                st.download_button(
                    label="⬇️ Download",
                    data=img_bytes,
                    file_name=f"plot_{plot_data['image_name']}",
                    mime="image/png",
                    key=f"dl_plot_{idx}"
                )
            
            st.markdown("---")
    
    # Thumbnails (HerdNet) - keep existing thumbnail view
    if 'thumbnails' in result:
        st.subheader("🔍 Animal Thumbnails")
        cols = st.columns(5)
        for idx, thumb in enumerate(result['thumbnails'][:20]):  # Show first 20
            with cols[idx % 5]:
                img_bytes = base64.b64decode(thumb['thumbnail_base64'])
                img = Image.open(BytesIO(img_bytes))
                st.image(img, caption=f"{thumb['species']} ({thumb['scores']:.2f})", use_container_width=True)


def view_results_page():
    """Page for viewing past results."""
    st.header("📊 View Past Results")
    
    # Filters
    col1, col2, col3 = st.columns(3)
    with col1:
        model_filter = st.selectbox("Model", ["All", "yolo", "herdnet"])
    with col2:
        status_filter = st.selectbox("Status", ["All", "completed", "processing", "failed"])
    with col3:
        limit = st.number_input("Limit", 1, 100, 20)
    
    # Fetch tasks
    try:
        params = {'limit': limit}
        if model_filter != "All":
            params['model_type'] = model_filter
        if status_filter != "All":
            params['status'] = status_filter
        
        response = requests.get(f"{API_BASE_URL}/tasks", params=params)
        if response.status_code == 200:
            data = response.json()
            tasks = data.get('tasks', [])
            
            if not tasks:
                st.info("No tasks found")
                return
            
            st.success(f"Found {len(tasks)} tasks")
            
            # Display tasks
            for task in tasks:
                with st.expander(f"Task {task['task_id'][:8]}... - {task.get('filename', 'N/A')} ({task['status']})"):
                    col1, col2 = st.columns(2)
                    with col1:
                        st.write(f"**Model:** {task['model_type']}")
                        st.write(f"**Status:** {task['status']}")
                        st.write(f"**Created:** {task['created_at']}")
                    with col2:
                        st.write(f"**Images:** {task.get('num_images', 0)}")
                        st.write(f"**Detections:** {task.get('total_detections', 0)}")
                        st.write(f"**Time:** {task.get('processing_time_seconds', 0):.1f}s")
                    
                    # View full results button
                    if st.button(f"View Full Results", key=task['task_id']):
                        # Fetch full task
                        task_response = requests.get(f"{API_BASE_URL}/tasks/{task['task_id']}")
                        if task_response.status_code == 200:
                            full_task = task_response.json()['task']
                            st.json(full_task.get('result_data', {}))
        else:
            st.error(f"Failed to fetch tasks: {response.status_code}")
    except Exception as e:
        st.error(f"Error: {str(e)}")


def statistics_page():
    """Page for database statistics."""
    st.header("📈 Database Statistics")
    
    try:
        response = requests.get(f"{API_BASE_URL}/database/stats")
        if response.status_code == 200:
            stats = response.json()['statistics']
            
            # Overview
            col1, col2, col3 = st.columns(3)
            col1.metric("Total Tasks", stats.get('total_tasks', 0))
            col2.metric("Total Detections", stats.get('total_detections', 0))
            col3.metric("Completed", stats.get('tasks_by_status', {}).get('completed', 0))
            
            # Tasks by model
            if stats.get('tasks_by_model'):
                st.subheader("Tasks by Model")
                model_df = pd.DataFrame(list(stats['tasks_by_model'].items()), columns=['Model', 'Count'])
                fig = px.bar(model_df, x='Model', y='Count', color='Model')
                st.plotly_chart(fig, use_container_width=True)
            
            # Species distribution
            if stats.get('species_distribution'):
                st.subheader("Species Distribution (All Time)")
                species_df = pd.DataFrame(list(stats['species_distribution'].items()), columns=['Species', 'Count'])
                species_df = species_df.sort_values('Count', ascending=False)
                
                col1, col2 = st.columns(2)
                with col1:
                    fig = px.bar(species_df, x='Species', y='Count', color='Species')
                    st.plotly_chart(fig, use_container_width=True)
                with col2:
                    fig = px.pie(species_df, names='Species', values='Count')
                    st.plotly_chart(fig, use_container_width=True)
        else:
            st.error("Failed to fetch statistics")
    except Exception as e:
        st.error(f"Error: {str(e)}")


def about_page():
    """About page with model information."""
    st.header("ℹ️ About")
    
    st.markdown("""
    ## African Wildlife Detection System
    
    This system uses state-of-the-art deep learning models to detect and count African wildlife in aerial and satellite imagery.
    
    ### Models
    
    #### 🎯 YOLOv11
    - **Type:** Object detection with bounding boxes
    - **Speed:** Fast (1-2 seconds per image)
    - **Best for:** Standard images, real-time detection
    - **Output:** Bounding boxes around animals
    
    #### 📍 HerdNet
    - **Type:** Point-based detection
    - **Speed:** Moderate (depends on image size)
    - **Best for:** Large aerial/satellite images
    - **Output:** Center points, thumbnails, and plots
    
    ### Supported Species
    1. Buffalo (*Syncerus caffer*)
    2. Elephant (*Loxodonta africana*)
    3. Kob (*Kobus kob*)
    4. Topi (*Damaliscus lunatus*)
    5. Warthog (*Phacochoerus africanus*)
    6. Waterbuck (*Kobus ellipsiprymnus*)
    
    ### Citations
    
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
    """)


if __name__ == "__main__":
    main()
