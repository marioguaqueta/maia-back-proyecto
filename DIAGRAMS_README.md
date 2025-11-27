# 📊 Architecture Diagrams Documentation

## 🎯 Overview

This folder contains comprehensive architecture diagrams for the **African Wildlife Detection System** ready for presentations, documentation, and technical communication.

---

## 📁 Files Created

### 1. **PRESENTATION_DIAGRAMS.md** (Comprehensive Guide)
- **Purpose**: Complete technical documentation with all diagrams
- **Contains**: 8+ major architecture diagrams with detailed explanations
- **Audience**: Technical teams, developers, architects
- **Features**:
  - Backend Architecture
  - Frontend Architecture
  - Integration Architecture
  - Complete System Interaction
  - Data Flow Diagrams (YOLO & HerdNet)
  - Technology Stack
  - Deployment Architecture
  - Security Architecture
  - User Journey
  - Export instructions

### 2. **architecture_diagrams.html** (Interactive Viewer)
- **Purpose**: View all diagrams in browser with rendered graphics
- **Contains**: All diagrams from PRESENTATION_DIAGRAMS.md
- **Usage**: 
  ```bash
  # Just open in any browser
  open architecture_diagrams.html
  ```
- **Features**:
  - Beautiful UI with navigation
  - Smooth scrolling
  - Color-coded sections
  - Print-friendly
  - Export instructions
  - Responsive design

### 3. **PRESENTATION_SLIDES_DIAGRAMS.md** (Slide-Ready)
- **Purpose**: Presentation-optimized diagrams for slides
- **Contains**: 15+ slide-specific diagrams
- **Audience**: Presentations, stakeholders, executives
- **Features**:
  - Simplified diagrams for clarity
  - Slide-by-slide breakdown
  - Export guidelines
  - Recommended presentation structure
  - Color palette reference

---

## 🚀 Quick Start

### Option 1: View in Browser (Easiest)
```bash
# Navigate to project folder
cd /Users/marioguaqueta/Desktop/MAIA/2025-4/ProyectoFinal/back

# Open HTML file
open architecture_diagrams.html
```

### Option 2: View Markdown
Open any `.md` file in:
- **VS Code**: Preview with `Cmd+Shift+V`
- **GitHub**: Auto-renders Mermaid diagrams
- **Obsidian**: Install Mermaid plugin
- **Typora**: Native Mermaid support

### Option 3: Export as Images

#### A. Online Tool (No Installation)
1. Go to https://mermaid.live/
2. Copy diagram code from any `.md` file
3. Paste into editor
4. Click **Actions** → **Export PNG/SVG**
5. Download high-resolution image

#### B. Command Line Tool
```bash
# Install mermaid-cli (one-time)
npm install -g @mermaid-js/mermaid-cli

# Export single diagram
mmdc -i diagram.mmd -o output.png -w 1920 -H 1080

# Export with transparent background
mmdc -i diagram.mmd -o output.png -w 1920 -H 1080 -b transparent

# Export as SVG (vector, scalable)
mmdc -i diagram.mmd -o output.svg
```

---

## 📊 Diagram Catalog

### System Architecture Diagrams

| Diagram | File | Best For |
|---------|------|----------|
| **System Overview** | PRESENTATION_SLIDES_DIAGRAMS.md (Slide 1) | Quick introduction |
| **Backend Complete** | PRESENTATION_DIAGRAMS.md (Section 1) | Technical deep-dive |
| **Frontend Complete** | PRESENTATION_DIAGRAMS.md (Section 2) | UI/UX discussion |
| **Integration** | PRESENTATION_DIAGRAMS.md (Section 3) | API communication |
| **Sequence Diagram** | PRESENTATION_SLIDES_DIAGRAMS.md (Slide 6) | Process flow |

### Technical Diagrams

| Diagram | File | Best For |
|---------|------|----------|
| **API Endpoints** | PRESENTATION_SLIDES_DIAGRAMS.md (Slide 5) | API documentation |
| **Data Flow (YOLO)** | PRESENTATION_DIAGRAMS.md (Section 5) | Processing pipeline |
| **Data Flow (HerdNet)** | PRESENTATION_DIAGRAMS.md (Section 5) | Processing pipeline |
| **Technology Stack** | PRESENTATION_SLIDES_DIAGRAMS.md (Slide 12) | Tech overview |

### Deployment & Operations

| Diagram | File | Best For |
|---------|------|----------|
| **Deployment Architecture** | PRESENTATION_DIAGRAMS.md (Section 4) | DevOps, Infrastructure |
| **CI/CD Pipeline** | PRESENTATION_SLIDES_DIAGRAMS.md (Slide 9) | Deployment process |
| **Security Architecture** | PRESENTATION_DIAGRAMS.md (Section 8) | Security discussion |

### Business & Use Cases

| Diagram | File | Best For |
|---------|------|----------|
| **User Journey** | PRESENTATION_DIAGRAMS.md (Section 7) | UX demonstration |
| **Use Cases** | PRESENTATION_SLIDES_DIAGRAMS.md (Slide 15) | Business value |
| **Model Comparison** | PRESENTATION_SLIDES_DIAGRAMS.md (Slide 4) | Feature comparison |

---

## 🎨 Creating a Presentation

### Suggested Slide Order

#### **Technical Presentation (20 minutes)**

1. **Title Slide**: Project name, team, institution
2. **Problem Statement**: Wildlife monitoring challenges
3. **System Overview**: PRESENTATION_SLIDES_DIAGRAMS.md - Slide 1
4. **Backend Architecture**: PRESENTATION_SLIDES_DIAGRAMS.md - Slide 2
5. **Frontend Architecture**: PRESENTATION_SLIDES_DIAGRAMS.md - Slide 3
6. **Model Comparison**: PRESENTATION_SLIDES_DIAGRAMS.md - Slide 4
7. **API Endpoints**: PRESENTATION_SLIDES_DIAGRAMS.md - Slide 5
8. **Request/Response Flow**: PRESENTATION_SLIDES_DIAGRAMS.md - Slide 6
9. **Data Pipeline**: PRESENTATION_SLIDES_DIAGRAMS.md - Slide 7
10. **Technology Stack**: PRESENTATION_SLIDES_DIAGRAMS.md - Slide 12
11. **Deployment**: PRESENTATION_SLIDES_DIAGRAMS.md - Slide 9
12. **Configuration**: PRESENTATION_SLIDES_DIAGRAMS.md - Slide 8
13. **Live Demo**: (Streamlit interface screenshots)
14. **Results**: PRESENTATION_SLIDES_DIAGRAMS.md - Slide 14
15. **Use Cases**: PRESENTATION_SLIDES_DIAGRAMS.md - Slide 15
16. **Metrics**: PRESENTATION_SLIDES_DIAGRAMS.md - Bonus
17. **Conclusions**: Key achievements
18. **Q&A**: Questions

#### **Executive Presentation (10 minutes)**

1. **Title Slide**: Project overview
2. **Problem**: Wildlife monitoring needs
3. **Solution**: PRESENTATION_SLIDES_DIAGRAMS.md - Slide 1
4. **Features**: PRESENTATION_SLIDES_DIAGRAMS.md - Slide 10
5. **Technology**: PRESENTATION_SLIDES_DIAGRAMS.md - Slide 12 (simplified)
6. **Demo Screenshots**: Key UI elements
7. **Results**: Sample detections
8. **Use Cases**: PRESENTATION_SLIDES_DIAGRAMS.md - Slide 15
9. **Impact**: Benefits and metrics
10. **Next Steps**: Future enhancements

---

## 💡 Export Tips

### For PowerPoint/Google Slides

1. **High-Resolution PNG** (recommended):
   ```bash
   mmdc -i diagram.mmd -o slide.png -w 1920 -H 1080 -b white
   ```

2. **With Transparent Background**:
   ```bash
   mmdc -i diagram.mmd -o slide.png -w 1920 -H 1080 -b transparent
   ```

3. **4K Quality** (for large screens):
   ```bash
   mmdc -i diagram.mmd -o slide.png -w 3840 -H 2160
   ```

### For Posters/Publications

1. **Vector Format** (scalable, print-quality):
   ```bash
   mmdc -i diagram.mmd -o diagram.svg
   ```

2. **High-Resolution PNG**:
   ```bash
   mmdc -i diagram.mmd -o poster.png -w 4000 -H 3000
   ```

### For Documentation

1. **Keep as Mermaid** in Markdown files (GitHub renders automatically)
2. **Use HTML file** for interactive web documentation
3. **Export SVG** for embedding in technical docs

---

## 🎨 Customization

### Changing Colors

Edit the Mermaid diagram code and modify `style` directives:

```mermaid
style NODE_NAME fill:#4CAF50  # Green
style NODE_NAME fill:#2196F3  # Blue
style NODE_NAME fill:#FF9800  # Orange
style NODE_NAME fill:#9C27B0  # Purple
```

### Standard Color Palette

| Color | Hex | Purpose |
|-------|-----|---------|
| 🟢 Green | `#4CAF50` | User-facing, Success |
| 🔵 Blue | `#2196F3` | Processing, APIs |
| 🟠 Orange | `#FF9800` | ML Models |
| 🟣 Purple | `#9C27B0` | Data, Storage |
| 🔴 Red | `#F44336` | Errors, Security |

### Adding New Diagrams

1. Copy existing diagram structure
2. Modify nodes and connections
3. Update colors with `style` directives
4. Test in https://mermaid.live/
5. Add to appropriate `.md` file

---

## 📱 Viewing on Different Platforms

### GitHub
- ✅ Native Mermaid support
- Automatically renders diagrams
- No additional setup needed

### VS Code
- Install: **Markdown Preview Mermaid Support** extension
- View: `Cmd+Shift+V` (Mac) or `Ctrl+Shift+V` (Windows)

### Obsidian
- Native support (no plugin needed)
- Real-time preview

### Notion
- Export diagrams as images first
- Upload to Notion

### Confluence
- Use **Mermaid Diagrams for Confluence** plugin
- Or export as images

---

## 🔧 Troubleshooting

### Diagrams Not Rendering

**Problem**: Diagrams show as code blocks

**Solutions**:
1. Use the HTML file (`architecture_diagrams.html`)
2. View on GitHub (native support)
3. Use Mermaid Live Editor: https://mermaid.live/
4. Export as images using `mmdc` CLI

### Export Command Not Working

**Problem**: `mmdc` command not found

**Solution**:
```bash
# Install Node.js first (if not installed)
brew install node  # Mac
# or download from: https://nodejs.org/

# Then install mermaid-cli
npm install -g @mermaid-js/mermaid-cli

# Verify installation
mmdc --version
```

### Low-Quality Images

**Problem**: Exported images look pixelated

**Solution**:
```bash
# Use higher resolution
mmdc -i diagram.mmd -o output.png -w 3840 -H 2160

# Or use vector format (SVG)
mmdc -i diagram.mmd -o output.svg
```

---

## 📚 Additional Resources

### Mermaid Documentation
- **Official Docs**: https://mermaid.js.org/
- **Live Editor**: https://mermaid.live/
- **Syntax Guide**: https://mermaid.js.org/intro/syntax-reference.html

### Diagram Types
- **Flowcharts**: Process flows
- **Sequence Diagrams**: Interactions over time
- **Class Diagrams**: OOP structure
- **State Diagrams**: State machines
- **Entity-Relationship**: Database design
- **Gantt Charts**: Project timelines
- **Pie Charts**: Data distribution
- **Journey Maps**: User experiences

### Tools
- **Mermaid Live Editor**: https://mermaid.live/
- **Draw.io**: https://app.diagrams.net/ (alternative)
- **PlantUML**: https://plantuml.com/ (alternative)
- **Lucidchart**: https://www.lucidchart.com/ (commercial)

---

## 📊 Diagram Statistics

### Coverage

| Category | Diagrams | Files |
|----------|----------|-------|
| **Architecture** | 8 | All files |
| **Data Flow** | 4 | PRESENTATION_DIAGRAMS.md |
| **Deployment** | 3 | Both files |
| **API/Integration** | 5 | PRESENTATION_SLIDES_DIAGRAMS.md |
| **Business/Use Cases** | 3 | PRESENTATION_SLIDES_DIAGRAMS.md |
| **Total** | **20+** | 3 files |

### Formats

- **Mermaid Code**: All diagrams (editable)
- **HTML Rendered**: `architecture_diagrams.html` (viewable)
- **Exportable**: PNG, SVG, PDF (via tools)

---

## 🎯 Best Practices

### For Presentations

1. **Keep it Simple**: Use PRESENTATION_SLIDES_DIAGRAMS.md versions
2. **One Concept per Slide**: Don't overcrowd
3. **Use Consistent Colors**: Follow the color palette
4. **High Resolution**: Export at 1920x1080 minimum
5. **Test Visibility**: Check on projector before presentation

### For Documentation

1. **Use Original Mermaid**: Keep diagrams editable in `.md` files
2. **Version Control**: Commit diagram source code
3. **Add Descriptions**: Include explanatory text
4. **Link Related Diagrams**: Create navigation
5. **Update Regularly**: Keep diagrams in sync with code

### For Sharing

1. **HTML for Web**: Use `architecture_diagrams.html`
2. **PDF for Print**: Export high-res PNG then convert
3. **PNG for Slides**: Export at presentation resolution
4. **SVG for Scaling**: Vector format for publications
5. **Markdown for GitHub**: Native rendering

---

## 📞 Support

### Need Help?

1. **Mermaid Syntax**: https://mermaid.js.org/intro/
2. **CLI Issues**: https://github.com/mermaid-js/mermaid-cli
3. **Export Problems**: Check Node.js version (`node --version`)

### Feedback

If you find issues or need additional diagrams:
1. Check existing diagrams in all three files
2. Modify existing diagrams as templates
3. Test at https://mermaid.live/ before adding
4. Keep consistent with existing style

---

## ✅ Checklist for Presentation

- [ ] Open `architecture_diagrams.html` in browser
- [ ] Review all diagrams
- [ ] Select diagrams for your presentation
- [ ] Export selected diagrams as PNG (1920x1080)
- [ ] Create slide deck (PowerPoint/Google Slides)
- [ ] Import exported images
- [ ] Add titles and bullet points
- [ ] Test presentation on projector
- [ ] Prepare speaker notes
- [ ] Practice timing (1-2 minutes per slide)

---

## 📄 Files Summary

```
back/
├── PRESENTATION_DIAGRAMS.md          # Complete technical diagrams
├── PRESENTATION_SLIDES_DIAGRAMS.md   # Presentation-optimized diagrams  
├── architecture_diagrams.html        # Interactive browser viewer
└── DIAGRAMS_README.md               # This file (usage guide)
```

---

**Version**: 1.0  
**Created**: November 2025  
**Updated**: November 2025  
**Format**: Mermaid Diagrams  
**License**: Internal use (MAIA 2025-4 Project)

---

## 🎉 Quick Commands

```bash
# View diagrams in browser
open architecture_diagrams.html

# Export all diagrams (requires mmdc)
for file in *.mmd; do
  mmdc -i "$file" -o "${file%.mmd}.png" -w 1920 -H 1080
done

# Create presentation folder
mkdir presentation_images
cd presentation_images

# Export specific diagrams for slides
mmdc -i ../backend.mmd -o slide_backend.png -w 1920 -H 1080
mmdc -i ../frontend.mmd -o slide_frontend.png -w 1920 -H 1080
mmdc -i ../integration.mmd -o slide_integration.png -w 1920 -H 1080
```

---

**Ready to create an amazing presentation! 🎉**

