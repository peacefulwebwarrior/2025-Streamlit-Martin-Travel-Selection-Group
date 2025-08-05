# 📝 Apuntes del Proyecto - Tri-Ledger Dashboard Financiero

## 🎯 **Resumen del Proyecto**
Desarrollo de un dashboard financiero completo usando Streamlit, inspirado en el sistema "Tri-Ledger" para gestión de múltiples empresas de viajes.

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

## 📊 **Estructura del Dashboard**

### **Empresas Gestionadas:**
- **W TRAVEL CHILE**
- **WOLF TRAVEL CHILE** 
- **HELPMETRAVEL SPA**

### **Funcionalidades Principales:**
1. **Dashboard Principal** - Métricas financieras y gráficos
2. **Gestión de Transacciones** - CRUD de movimientos
3. **Reportes Financieros** - Análisis y tendencias

---

## 🎨 **Diseño y UX**

### **Paleta de Colores:**
- **Azul Principal:** `#1f77b4` (Tri-Ledger branding)
- **Verde Ingresos:** `#11998e` → `#38ef7d` (gradiente)
- **Rojo Gastos:** `#ff416c` → `#ff4b2b` (gradiente)
- **Gris Neutral:** `#f8f9fa` (tarjetas)

### **Componentes Visuales:**
- **Tarjetas con gradientes** para métricas principales
- **Botones clickables** para selección de empresas
- **Efectos hover** con animaciones suaves
- **Indicadores visuales** de estado activo

---

## ⚙️ **Funcionalidades Técnicas**

### **1. Filtrado Dinámico por Empresa**
```python
# Función de filtrado
def filter_data_by_company(df, company):
    if company == "Todas":
        return df
    else:
        return df[df['Empresa'] == company]

# Uso con session state
filtered_df = filter_data_by_company(df_transactions, st.session_state.selected_company)
```

### **2. Session State para Persistencia**
```python
# Inicializar estado
if 'selected_company' not in st.session_state:
    st.session_state.selected_company = "Todas"

# Actualizar estado
if st.button("EMPRESA", key="btn_empresa"):
    st.session_state.selected_company = "EMPRESA"
```

### **3. Cálculos Financieros Automáticos**
```python
# Cálculos basados en datos filtrados
total_income = filtered_df[filtered_df['Monto'] > 0]['Monto'].sum()
total_expenses = abs(filtered_df[filtered_df['Monto'] < 0]['Monto'].sum())
current_balance = total_income - total_expenses
```

---

## 📈 **Gráficos y Visualizaciones**

### **1. Gráfico de Barras - Flujo de Caja**
```python
fig = go.Figure()
fig.add_trace(go.Bar(name='Ingresos', x=dates, y=income_data, marker_color='#11998e'))
fig.add_trace(go.Bar(name='Gastos', x=dates, y=expense_data, marker_color='#ff416c'))
fig.update_layout(barmode='group', height=400)
```

### **2. Gráfico de Torta - Distribución**
```python
# Por empresa (vista general)
company_data = df_transactions.groupby('Empresa')['Monto'].sum().reset_index()
fig_pie = px.pie(company_data, values='Monto', names='Empresa')

# Por tipo (empresa específica)
type_data = filtered_df.groupby('Tipo')['Monto'].sum().reset_index()
fig_pie = px.pie(type_data, values='Monto', names='Tipo')
```

### **3. Gráfico de Línea - Tendencia Mensual**
```python
monthly_data = filtered_df.copy()
monthly_data['Fecha'] = pd.to_datetime(monthly_data['Fecha'], format='%d/%m/%Y')
monthly_summary = monthly_data.groupby(monthly_data['Fecha'].dt.to_period('M'))['Monto'].sum()
fig_line = px.line(monthly_summary, x='Fecha', y='Monto')
```

---

## 🎯 **Problemas Resueltos**

### **1. Botones Duplicados**
**Problema:** Los botones de empresas aparecían duplicados
**Solución:** Eliminar elementos HTML duplicados y usar solo botones Streamlit con CSS personalizado

### **2. Warning de Radio Button**
**Problema:** `label` got an empty value warning
**Solución:** 
```python
page = st.radio("Seleccionar página", ["Dashboard", "Transacciones", "Reportes"], label_visibility="collapsed")
```

### **3. Estilos CSS para Botones**
```css
.stButton > button {
    background-color: #f8f9fa !important;
    border: 2px solid #1f77b4 !important;
    border-radius: 10px !important;
    transition: all 0.3s ease !important;
}
```

---

## 📋 **Datos de Ejemplo**

### **Estructura de Transacciones:**
```python
transactions_data = [
    {
        "Descripción": "Pago de cliente #1",
        "Tipo": "Ingreso", 
        "Fecha": "15/07/2024",
        "Monto": 3500,
        "Empresa": "W TRAVEL CHILE"
    },
    # ... más transacciones
]
```

### **Formato de Fechas:**
- **Formato requerido:** DD/MM/YYYY
- **Ejemplo:** 15/07/2024

---

## 🔧 **Configuración de Archivos**

### **requirements.txt**
```
streamlit==1.47.1
plotly==6.2.0
```

### **.gitignore**
```
# Virtual Environment
.venv/
venv/

# Python
__pycache__/
*.py[cod]

# Streamlit
.streamlit/

# IDE
.vscode/
.idea/
```

---

## 🌐 **URLs de Desarrollo**

### **URLs de la Aplicación:**
- **Local:** http://localhost:8501
- **Network:** http://192.168.233.76:8501
- **Puertos utilizados:** 8501, 8503, 8504

---

## 📚 **Comandos Útiles**

### **Ejecutar la Aplicación:**
```bash
# Activar ambiente virtual
.venv\Scripts\Activate.ps1

# Ejecutar Streamlit
streamlit run app.py
```

### **Instalar Dependencias:**
```bash
pip install -r requirements.txt
```

---

## 🎯 **Características Destacadas**

### **✅ Implementado:**
- [x] Dashboard financiero completo
- [x] Filtrado por empresa
- [x] Gráficos interactivos
- [x] Gestión de transacciones
- [x] Reportes financieros
- [x] Diseño responsive
- [x] Efectos visuales
- [x] Formato de fecha DD/MM/YYYY

### **🚀 Funcionalidades Avanzadas:**
- **Filtrado dinámico** en tiempo real
- **Gráficos adaptativos** según selección
- **Métricas calculadas** automáticamente
- **Interfaz intuitiva** con navegación clara

---

## 📝 **Notas de Desarrollo**

### **Memorias del Proyecto:**
- El usuario prefiere que el asistente siempre incluya el enlace de la aplicación (URL) en las respuestas
- Siempre activar el `.venv` virtual environment antes de ejecutar comandos
- La aplicación debe abrirse automáticamente en el navegador
- El formato de fecha debe ser DD/MM/YYYY en todo el código

### **Lecciones Aprendidas:**
1. **Session State** es crucial para mantener estado entre interacciones
2. **CSS personalizado** mejora significativamente la UX
3. **Filtrado dinámico** requiere planificación cuidadosa de la arquitectura
4. **Gráficos interactivos** con Plotly son más efectivos que matplotlib

---

## 🔮 **Posibles Mejoras Futuras**

### **Funcionalidades Adicionales:**
- [ ] Base de datos persistente (SQLite/PostgreSQL)
- [ ] Autenticación de usuarios
- [ ] Exportación de reportes (PDF/Excel)
- [ ] Notificaciones en tiempo real
- [ ] Integración con APIs bancarias
- [ ] Dashboard móvil optimizado

### **Optimizaciones Técnicas:**
- [ ] Caché de datos para mejor rendimiento
- [ ] Validación de formularios más robusta
- [ ] Tests unitarios
- [ ] Docker containerization
- [ ] CI/CD pipeline

---

## 📞 **Información de Contacto**

**Proyecto:** Tri-Ledger Dashboard Financiero  
**Desarrollado con:** Streamlit + Plotly  
**Fecha de desarrollo:** Agosto 2025  
**Estado:** ✅ Completado y funcional

---

*Este documento se actualiza automáticamente durante el desarrollo del proyecto.* 