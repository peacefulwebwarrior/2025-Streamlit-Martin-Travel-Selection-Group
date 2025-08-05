# Proyecto Streamlit - Martin Travel Selection Group

Este proyecto utiliza Streamlit para crear aplicaciones web interactivas.

## Configuración del Ambiente Virtual

### Activación del ambiente virtual

En Windows (PowerShell):
```powershell
.venv\Scripts\Activate.ps1
```

En Windows (Command Prompt):
```cmd
.venv\Scripts\activate.bat
```

En Linux/Mac:
```bash
source .venv/bin/activate
```

### Instalación de dependencias

```bash
pip install -r requirements.txt
```

## Ejecutar la aplicación

```bash
streamlit run app.py
```

La aplicación estará disponible en: http://localhost:8501

## Estructura del proyecto

- `app.py` - Aplicación principal de Streamlit
- `requirements.txt` - Dependencias del proyecto
- `.venv/` - Ambiente virtual (no incluido en el control de versiones)

## Notas importantes

- Siempre activa el ambiente virtual antes de trabajar en el proyecto
- El formato de fecha debe ser DD/MM/YYYY en todo el código
- La aplicación se abrirá automáticamente en el navegador al ejecutarla 