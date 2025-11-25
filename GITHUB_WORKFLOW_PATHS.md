# 🚀 GitHub Workflow - Path Filtering

Documentación sobre el filtrado de rutas en el workflow de GitHub Actions para evitar despliegues innecesarios.

## 📋 Problema

Antes, **cualquier cambio** en el repositorio activaba el despliegue completo a EC2, incluso si solo se modificaban archivos del frontend (Streamlit) o documentación.

Esto causaba:
- ❌ Despliegues innecesarios del backend
- ❌ Uso excesivo de recursos
- ❌ Tiempo perdido en despliegues que no afectan el backend
- ❌ Posibles interrupciones del servicio sin razón

## ✅ Solución

Se agregó `paths-ignore` al workflow de GitHub Actions para **ignorar archivos que no afectan el backend**.

### Archivos Ignorados

```yaml
paths-ignore:
  # Frontend files (Streamlit) - no need to redeploy backend
  - 'streamlit_app.py'
  - '.streamlit/**'
  - 'requirements-streamlit.txt'
  # Documentation files
  - '**.md'
  - 'CHANGELOG.md'
  - 'README*.md'
  - 'docs/**'
  # Test and helper files
  - 'test_*.py'
  - 'create_test_zip.py'
  # Git and IDE files
  - '.gitignore'
  - '.vscode/**'
  - '.idea/**'
  # Other non-backend files
  - 'start.sh'
  - 'start.bat'
```

## 🎯 Resultado

### El workflow SE ACTIVARÁ cuando cambies:
- ✅ `app.py` (backend principal)
- ✅ `database.py` (módulo de base de datos)
- ✅ `model_loader.py` (cargador de modelos)
- ✅ `requirements.txt` o `requirements-backend.txt`
- ✅ `Dockerfile` o `docker-compose.yml`
- ✅ Archivos de configuración del backend
- ✅ `.github/workflows/deploy.yml` (el propio workflow)

### El workflow NO SE ACTIVARÁ cuando cambies:
- ❌ `streamlit_app.py` (frontend)
- ❌ `.streamlit/config.toml` (configuración de Streamlit)
- ❌ Archivos `.md` (documentación)
- ❌ Scripts de prueba (`test_*.py`)
- ❌ Scripts de ayuda (`start.sh`, `start.bat`)
- ❌ Archivos de IDE (`.vscode`, `.idea`)

## 📝 Ejemplos

### Ejemplo 1: Solo cambios en Streamlit

```bash
# Modificas streamlit_app.py
git add streamlit_app.py
git commit -m "Update Streamlit UI labels to Spanish"
git push origin main
```

**Resultado:** ✅ No se activa el despliegue a EC2 (correcto, es solo frontend)

### Ejemplo 2: Solo cambios en documentación

```bash
# Modificas README.md
git add README.md
git commit -m "Update documentation"
git push origin main
```

**Resultado:** ✅ No se activa el despliegue a EC2 (correcto, es solo documentación)

### Ejemplo 3: Cambios en backend

```bash
# Modificas app.py
git add app.py
git commit -m "Add new endpoint for animal statistics"
git push origin main
```

**Resultado:** ✅ SE ACTIVA el despliegue a EC2 (correcto, el backend cambió)

### Ejemplo 4: Cambios mixtos (Frontend + Backend)

```bash
# Modificas streamlit_app.py Y app.py
git add streamlit_app.py app.py
git commit -m "Update both frontend and backend"
git push origin main
```

**Resultado:** ✅ SE ACTIVA el despliegue a EC2 (correcto, el backend cambió)

**Nota:** Si **cualquier archivo** que no está en `paths-ignore` cambia, el workflow se activa.

## 🔧 Despliegue Manual

Si necesitas desplegar manualmente (incluso sin cambios en el backend), usa:

```bash
# Opción 1: Desde GitHub UI
1. Ve a Actions → Deploy to AWS EC2
2. Click "Run workflow"
3. Selecciona branch (main)
4. Click "Run workflow"

# Opción 2: Desde línea de comandos con gh CLI
gh workflow run deploy.yml
```

## 🎨 Personalización

### Agregar más archivos a ignorar

Si tienes otros archivos frontend o de documentación que no deben activar el despliegue:

```yaml
paths-ignore:
  # ... archivos existentes ...
  - 'mi_archivo_frontend.py'
  - 'docs_nuevos/**'
```

### Ignorar solo archivos específicos

```yaml
paths-ignore:
  - 'archivo_especifico.py'
  - 'carpeta_especifica/**'
```

### Activar solo en archivos específicos (opción alternativa)

En lugar de `paths-ignore`, puedes usar `paths` para activar **solo** en archivos específicos:

```yaml
on:
  push:
    branches:
      - main
    paths:
      - 'app.py'
      - 'database.py'
      - 'model_loader.py'
      - 'requirements-backend.txt'
      - 'Dockerfile'
      - 'docker-compose.yml'
```

**Ventaja:** Más explícito sobre qué activa el workflow  
**Desventaja:** Debes actualizar la lista cada vez que agregas un nuevo archivo backend

## 📊 Comparación de Estrategias

| Estrategia | Ventajas | Desventajas |
|------------|----------|-------------|
| **paths-ignore** (actual) | Más flexible, nuevos archivos backend activan automáticamente | Debes recordar agregar archivos frontend a la lista |
| **paths** (específico) | Muy explícito, control total | Menos flexible, más mantenimiento |
| **Sin filtro** | Simple | Muchos despliegues innecesarios |

## 🔍 Verificar Configuración

### Ver si un cambio activará el workflow

Usa la GitHub Actions CLI:

```bash
# Instalar gh CLI si no lo tienes
brew install gh  # macOS
# o
sudo apt install gh  # Ubuntu

# Ver workflows
gh workflow list

# Ver runs recientes
gh workflow view deploy.yml
```

### Probar localmente

```bash
# Ver qué archivos has cambiado
git status

# Comparar con la lista de paths-ignore
# Si todos tus cambios están en paths-ignore, NO se desplegará
```

## 🚨 Consideraciones Importantes

### 1. Cambios Mixtos

Si cambias **tanto** archivos ignorados **como** archivos backend:
- El workflow **SÍ se activará** porque hay cambios en backend
- Esto es correcto: el backend necesita desplegarse

### 2. Dependencias entre Frontend y Backend

Si `streamlit_app.py` depende de cambios en `app.py`:
1. Primero hacer commit y push de `app.py` (se despliega el backend)
2. Luego hacer commit y push de `streamlit_app.py` (no se despliega, correcto)

O hacer commit de ambos juntos (se despliega una vez).

### 3. Emergencias

Si necesitas despliegue urgente y solo cambiaste frontend:
- Usa despliegue manual desde GitHub Actions UI
- O haz un pequeño cambio en un archivo backend (ej: comentario en app.py)

## 📚 Documentación Relacionada

- **GitHub Actions - Workflow Syntax**: https://docs.github.com/en/actions/using-workflows/workflow-syntax-for-github-actions#onpushpull_requestpaths
- **Path Filtering**: https://docs.github.com/en/actions/using-workflows/workflow-syntax-for-github-actions#example-including-paths
- **Glob Patterns**: https://docs.github.com/en/actions/using-workflows/workflow-syntax-for-github-actions#filter-pattern-cheat-sheet

## 🎓 Patterns de Glob Usados

| Pattern | Descripción | Ejemplos |
|---------|-------------|----------|
| `*.md` | Archivos .md en raíz | `README.md`, `CHANGELOG.md` |
| `**.md` | Todos los .md en cualquier carpeta | `docs/api.md`, `guides/setup.md` |
| `test_*.py` | Archivos que empiezan con test_ | `test_api.py`, `test_model.py` |
| `.streamlit/**` | Todo dentro de .streamlit | `.streamlit/config.toml` |
| `docs/**` | Todo dentro de docs | `docs/api/endpoints.md` |

## ✅ Checklist de Verificación

Antes de hacer push, verifica:

- [ ] ¿Mis cambios afectan el backend?
  - **Sí** → El workflow se activará ✅
  - **No** → El workflow no se activará ✅

- [ ] ¿Solo cambié archivos frontend/documentación?
  - **Sí** → No se desplegará (correcto) ✅
  - **No** → Se desplegará (correcto) ✅

- [ ] ¿Necesito que el backend se actualice?
  - **Sí, pero solo cambié frontend** → Usa despliegue manual
  - **Sí, y cambié backend** → Push normal

## 💡 Consejos

1. **Commits separados**: Separa cambios de frontend y backend en commits diferentes
2. **Branches separados**: Considera tener branches `frontend` y `backend` para desarrollo
3. **Review antes de push**: Revisa qué archivos cambiaron con `git status`
4. **Testing local**: Prueba cambios localmente antes de hacer push

---

**Última Actualización**: Noviembre 2025  
**Versión del Workflow**: 1.1.0  
**Estrategia**: paths-ignore (lista de exclusión)

