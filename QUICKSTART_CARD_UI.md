# 🚀 Quick Start - Card-Based UI

## See the New UI in 3 Steps

### Step 1: Start the Applications

```bash
# Terminal 1 - Backend
cd /Users/marioguaqueta/Desktop/MAIA/2025-4/ProyectoFinal/back
python app.py

# Terminal 2 - Frontend
cd /Users/marioguaqueta/Desktop/MAIA/2025-4/ProyectoFinal/back
streamlit run streamlit_app.py
```

### Step 2: Upload & Analyze

1. Open browser to `http://localhost:8501`
2. Go to "**New Analysis**" page
3. Upload a ZIP with wildlife images
4. Select **YOLOv11** or **HerdNet**
5. Click "**Run Analysis**"

### Step 3: See the Magic ✨

You'll see:
- 🖼️ **Beautiful cards** in a 2-column grid
- 🎯 **Color-coded badges** (green for detections, blue for dimensions)
- 📊 **Collapsible tables** - click to expand/collapse
- 🔍 **Interactive viewer** - click "View Full Size"
- ⬇️ **Quick download** - click "Download"

---

## 📱 Try the Demo (No Backend Needed)

Open the static demo in your browser:

```bash
cd /Users/marioguaqueta/Desktop/MAIA/2025-4/ProyectoFinal/back
open card_ui_demo.html
```

### Demo Features:
- ✅ Hover over cards (see lift effect)
- ✅ Click expander headers (toggle tables)
- ✅ See all styling in action

---

## 🎨 What's New

### Card Features
Each image gets its own card with:

| Feature | Description |
|---------|-------------|
| **Header** | Image name with icon (📷 or 📍) |
| **Badges** | Detections (green) + Dimensions (blue) |
| **Image** | Full-width annotated image/plot |
| **Expander** | Collapsible detection details table |
| **Buttons** | View full-size + Download |

### Layout
- **2-column grid** (less scrolling!)
- **Hover effects** (cards lift up)
- **Smooth animations** (all transitions)
- **Responsive** (works on mobile)

---

## 🔍 Compare Results

### YOLO Cards
- Show annotated images with **bounding boxes**
- Detection table has: Species, Confidence, Center X/Y, Width, Height
- Green detection count badge

### HerdNet Cards
- Show detection **plots with points**
- Detection table has: Species, Confidence, X, Y
- Labeled as "HerdNet Detection Plot"

---

## 📖 Full Documentation

- **`CARD_UI_DESIGN.md`** - Complete design documentation
- **`CARD_UI_IMPLEMENTATION_SUMMARY.md`** - Technical details
- **`README.md`** - Updated usage guide

---

## 💡 Tips

1. **Quick Browse**: Just look at card headers and badges
2. **Details**: Expand the collapsible table in any card
3. **Full View**: Click "View Full Size" for zoom & pan
4. **Download**: Get individual images right from the card

---

## ❓ Troubleshooting

**Cards look plain?**
- Refresh the page (CSS might not have loaded)

**Images not showing?**
- Check backend is running (`http://localhost:8000/health`)

**Slow performance?**
- Process fewer images per batch
- Close other browser tabs

---

**Enjoy the new UI! 🎉**

