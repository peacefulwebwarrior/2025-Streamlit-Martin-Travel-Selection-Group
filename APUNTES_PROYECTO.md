# 📝 Apuntes del Proyecto - Tri-Ledger Dashboard Financiero V2

## 🎯 **Resumen del Proyecto**
Desarrollo de un dashboard financiero completo usando Streamlit, inspirado en el sistema "Tri-Ledger" para gestión de múltiples empresas de viajes. **VERSIÓN 2.0** con temas personalizados por empresa y datos en archivos CSV separados.

---

## 🚀 **Configuración Inicial del Ambiente**

### **1. Creación del Ambiente Virtual**
```bash
# Crear ambiente virtual
python -m venv .venv

# Activar en Windows (PowerShell)
.venv\Scripts\Activate.ps1

# Activar en Windows (Command Prompt)
.venv\Scripts\activate.bat

# Activar en Linux/Mac
source .venv/bin/activate
```

### **2. Instalación de Dependencias**
```bash
# Instalar Streamlit
pip install streamlit

# Instalar Plotly para gráficos
pip install plotly

# Crear requirements.txt
streamlit==1.47.1
plotly==6.2.0
```

---

## 📊 **Estructura del Dashboard V2**

### **Empresas Gestionadas:**
- **W TRAVEL CHILE** 🌍 - Agencia de viajes tradicional
- **WOLF TRAVEL CHILE** 🐺 - Turismo aventura
- **HELPMETRAVEL SPA** 🏢 - Viajes corporativos

### **Archivos de Datos:**
- `w_travel_chile.csv` - Transacciones de W TRAVEL CHILE
- `wolf_travel_chile.csv` - Transacciones de WOLF TRAVEL CHILE
- `helpmetravel_spa.csv` - Transacciones de HELPMETRAVEL SPA

### **Funcionalidades Principales:**
1. **Dashboard Principal** - Métricas financieras y gráficos con tema dinámico
2. **Gestión de Transacciones** - CRUD de movimientos
3. **Reportes Financieros** - Análisis y tendencias
4. **Temas Personalizados** - Colores únicos por empresa

---

## 🎨 **Diseño y UX V2 - Temas Personalizados**

### **W TRAVEL CHILE (Azul-Dorado):**
```css
--primary: #1e3a8a (Azul profundo)
--secondary: #3b82f6 (Azul medio)
--accent: #fbbf24 (Dorado)
--light: #f8fafc (Gris claro)
--gradient: linear-gradient(135deg, #1e3a8a 0%, #3b82f6 100%)
```
**Estilo:** Elegante, profesional, confiable

### **WOLF TRAVEL CHILE (Verde-Naranja):**
```css
--primary: #166534 (Verde bosque)
--secondary: #22c55e (Verde claro)
--accent: #ea580c (Naranja aventura)
--light: #f0fdf4 (Verde muy claro)
--gradient: linear-gradient(135deg, #166534 0%, #22c55e 100%)
```
**Estilo:** Aventurero, natural, energético

### **HELPMETRAVEL SPA (Púrpura-Azul):**
```css
--primary: #7c3aed (Púrpura)
--secondary: #a855f7 (Violeta)
--accent: #1e40af (Azul corporativo)
--light: #faf5ff (Púrpura muy claro)
--gradient: linear-gradient(135deg, #7c3aed 0%, #a855f7 100%)
```
**Estilo:** Corporativo, sofisticado, profesional

---

## ⚙️ **Funcionalidades Técnicas V2**

### **1. Sistema de Temas Dinámicos**
```python
def get_company_theme(company):
    themes = {
        "W TRAVEL CHILE": {
            "primary": "#1e3a8a",
            "secondary": "#3b82f6",
            "accent": "#fbbf24",
            "logo": "🌍"
        },
        # ... más temas
    }
    return themes.get(company)
```

### **2. CSS Dinámico Generado**
```python
def generate_dynamic_css(company):
    theme = get_company_theme(company)
    return f"""
    <style>
        :root {{
            --primary-color: {theme['primary']};
            --gradient: {theme['gradient']};
        }}
        /* CSS personalizado por empresa */
    </style>
    """
```

### **3. Carga de Datos desde CSV**
```python
def load_company_data(company):
    csv_files = {
        "W TRAVEL CHILE": "w_travel_chile.csv",
        "WOLF TRAVEL CHILE": "wolf_travel_chile.csv",
        "HELPMETRAVEL SPA": "helpmetravel_spa.csv"
    }
    csv_file = csv_files.get(company)
    if csv_file and os.path.exists(csv_file):
        return pd.read_csv(csv_file)
```

---

## 📈 **Gráficos y Visualizaciones V2**

### **1. Gráfico de Barras - Flujo de Caja**
```python
fig = go.Figure()
fig.add_trace(go.Bar(
    name='Ingresos',
    x=df_daily['Fecha'],
    y=df_daily['Ingresos'],
    marker_color='#10b981'
))
fig.add_trace(go.Bar(
    name='Gastos',
    x=df_daily['Fecha'],
    y=df_daily['Gastos'],
    marker_color='#ef4444'
))
```

### **2. Gráfico de Torta - Distribución**
```python
fig_pie = px.pie(
    type_data, 
    values='Monto', 
    names='Tipo',
    color_discrete_map={'Ingreso': '#10b981', 'Gasto': '#ef4444'}
)
```

### **3. Gráfico de Línea - Tendencia**
```python
fig_line = px.line(
    monthly_summary, 
    x='Fecha', 
    y='Monto',
    markers=True
)
fig_line.update_traces(line_color=theme['primary'])
```

---

## 🎯 **Principios de Diseño Aplicados**

### **1. Jerarquía Visual**
- **Header principal** con gradiente de texto
- **Métricas KPI** en tarjetas destacadas
- **Gráficos** con títulos descriptivos
- **Navegación** clara y consistente

### **2. Armonía de Colores**
- **Paletas coherentes** por empresa
- **Contraste adecuado** para legibilidad
- **Gradientes sutiles** para profundidad
- **Colores semánticos** (verde=ingresos, rojo=gastos)

### **3. UX/UI Moderno**
- **Animaciones suaves** (fadeIn, hover effects)
- **Responsive design** para móviles
- **Feedback visual** inmediato
- **Estados activos** claros

---

## 📋 **Estructura de Archivos CSV**

### **Formato de Datos:**
```csv
Descripción,Tipo,Fecha,Monto,Empresa
Venta paquete turístico Europa,Ingreso,15/01/2023,8500,W TRAVEL CHILE
Pago arriendo oficina,Gasto,05/01/2023,-1200,W TRAVEL CHILE
```

### **Campos Requeridos:**
- **Descripción:** Texto descriptivo de la transacción
- **Tipo:** "Ingreso" o "Gasto"
- **Fecha:** Formato DD/MM/YYYY
- **Monto:** Número (positivo para ingresos, negativo para gastos)
- **Empresa:** Nombre exacto de la empresa

---

## 🔧 **Configuración de Archivos V2**

### **requirements.txt**
```
streamlit==1.47.1
plotly==6.2.0
```

### **Archivos CSV:**
- `w_travel_chile.csv` - 35 transacciones
- `wolf_travel_chile.csv` - 32 transacciones  
- `helpmetravel_spa.csv` - 32 transacciones

### **Archivos de Aplicación:**
- `app_v2.py` - Dashboard principal V2
- `app.py` - Versión anterior (mantenida)

---

## 🌐 **URLs de Desarrollo**

### **URLs de la Aplicación:**
- **V2 Local:** http://localhost:8501 (ejecutar `app_v2.py`)
- **V1 Local:** http://localhost:8501 (ejecutar `app.py`)
- **Network:** http://192.168.233.76:8501
- **Puertos utilizados:** 8501, 8503, 8504

---

## 📚 **Comandos Útiles V2**

### **Ejecutar la Aplicación V2:**
```bash
# Activar ambiente virtual
.venv\Scripts\Activate.ps1

# Ejecutar Streamlit V2
streamlit run app_v2.py
```

### **Ejecutar la Aplicación V1:**
```bash
# Activar ambiente virtual
.venv\Scripts\Activate.ps1

# Ejecutar Streamlit V1
streamlit run app.py
```

### **Instalar Dependencias:**
```bash
pip install -r requirements.txt
```

---

## 🎯 **Características Destacadas V2**

### **✅ Implementado en V2:**
- [x] Temas personalizados por empresa
- [x] Datos en archivos CSV separados
- [x] CSS dinámico generado
- [x] Animaciones y efectos visuales
- [x] Logos específicos por empresa
- [x] Gradientes personalizados
- [x] Diseño responsive mejorado
- [x] Estadísticas detalladas
- [x] Gráficos interactivos avanzados
- [x] Formato de fecha DD/MM/YYYY

### **🚀 Funcionalidades Avanzadas V2:**
- **Temas dinámicos** que cambian según la empresa
- **Carga de datos** desde archivos CSV externos
- **Animaciones CSS** para mejor UX
- **Gradientes personalizados** por marca
- **Iconografía específica** por tipo de empresa
- **Estadísticas avanzadas** con métricas de rendimiento

---

## 📝 **Notas de Desarrollo V2**

### **Memorias del Proyecto:**
- El usuario prefiere que el asistente siempre incluya el enlace de la aplicación (URL) en las respuestas
- Siempre activar el `.venv` virtual environment antes de ejecutar comandos
- La aplicación debe abrirse automáticamente en el navegador
- El formato de fecha debe ser DD/MM/YYYY en todo el código
- **NUEVO:** Datos separados en archivos CSV por empresa
- **NUEVO:** Temas personalizados aplicando principios de diseño

### **Lecciones Aprendidas V2:**
1. **CSS dinámico** mejora significativamente la personalización
2. **Archivos CSV separados** facilitan el mantenimiento
3. **Temas por empresa** crean identidad visual única
4. **Animaciones CSS** mejoran la experiencia de usuario
5. **Principios de diseño** aplicados correctamente crean dashboards hermosos

---

## 🔮 **Posibles Mejoras Futuras V3**

### **Funcionalidades Adicionales:**
- [ ] Base de datos persistente (SQLite/PostgreSQL)
- [ ] Autenticación de usuarios
- [ ] Exportación de reportes (PDF/Excel)
- [ ] Notificaciones en tiempo real
- [ ] Integración con APIs bancarias
- [ ] Dashboard móvil optimizado
- [ ] **NUEVO:** Modo oscuro/claro
- [ ] **NUEVO:** Más temas personalizados
- [ ] **NUEVO:** Gráficos 3D interactivos

### **Optimizaciones Técnicas:**
- [ ] Caché de datos para mejor rendimiento
- [ ] Validación de formularios más robusta
- [ ] Tests unitarios
- [ ] Docker containerization
- [ ] CI/CD pipeline
- [ ] **NUEVO:** Lazy loading de datos
- [ ] **NUEVO:** Compresión de archivos CSV

---

## 📞 **Información de Contacto**

**Proyecto:** Tri-Ledger Dashboard Financiero V2  
**Desarrollado con:** Streamlit + Plotly + CSS Dinámico  
**Fecha de desarrollo:** Agosto 2025  
**Estado:** ✅ V2 Completada y funcional  
**Versiones:** V1 (básica) + V2 (temas personalizados)

---

*Este documento se actualiza automáticamente durante el desarrollo del proyecto.* 