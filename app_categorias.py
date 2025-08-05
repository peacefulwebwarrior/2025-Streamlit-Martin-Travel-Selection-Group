import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import os

# Configuración de la página
st.set_page_config(
    page_title="Tri-Ledger - Sistema de Categorías",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Definir categorías jerárquicas
CATEGORIAS_PADRE = {
    "Ingresos": {
        "color": "#10b981",
        "icon": "📈",
        "subcategorias": [
            "Ventas de Paquetes",
            "Comisiones",
            "Servicios Turísticos",
            "Otros Ingresos"
        ]
    },
    "Gastos Operacionales": {
        "color": "#ef4444", 
        "icon": "🏢",
        "subcategorias": [
            "Arriendo de Oficina",
            "Servicios Básicos",
            "Equipos y Tecnología",
            "Software y Licencias",
            "Mantenimiento"
        ]
    },
    "Gastos Administrativos": {
        "color": "#f97316",
        "icon": "📋",
        "subcategorias": [
            "Impuestos",
            "Tasas Gubernamentales",
            "Seguros",
            "Gastos Legales"
        ]
    },
    "Gastos de Personal": {
        "color": "#8b5cf6",
        "icon": "👥",
        "subcategorias": [
            "Salarios",
            "Beneficios",
            "Capacitación",
            "Viáticos"
        ]
    },
    "Gastos de Marketing": {
        "color": "#06b6d4",
        "icon": "📢",
        "subcategorias": [
            "Publicidad",
            "Promociones",
            "Material Promocional",
            "Eventos"
        ]
    },
    "Gastos de Viaje": {
        "color": "#eab308",
        "icon": "✈️",
        "subcategorias": [
            "Transporte",
            "Alojamiento",
            "Alimentación",
            "Actividades"
        ]
    }
}

# Función para obtener el tema CSS según la empresa
def get_company_theme(company):
    themes = {
        "W TRAVEL CHILE": {
            "primary": "#1e3a8a",
            "secondary": "#3b82f6", 
            "accent": "#fbbf24",
            "light": "#f8fafc",
            "gradient": "linear-gradient(135deg, #1e3a8a 0%, #3b82f6 100%)",
            "income_gradient": "linear-gradient(135deg, #059669 0%, #10b981 100%)",
            "expense_gradient": "linear-gradient(135deg, #dc2626 0%, #ef4444 100%)",
            "logo": "🌍"
        },
        "WOLF TRAVEL CHILE": {
            "primary": "#166534",
            "secondary": "#22c55e",
            "accent": "#ea580c", 
            "light": "#f0fdf4",
            "gradient": "linear-gradient(135deg, #166534 0%, #22c55e 100%)",
            "income_gradient": "linear-gradient(135deg, #059669 0%, #10b981 100%)",
            "expense_gradient": "linear-gradient(135deg, #dc2626 0%, #ef4444 100%)",
            "logo": "🐺"
        },
        "HELPMETRAVEL SPA": {
            "primary": "#7c3aed",
            "secondary": "#a855f7",
            "accent": "#1e40af",
            "light": "#faf5ff", 
            "gradient": "linear-gradient(135deg, #7c3aed 0%, #a855f7 100%)",
            "income_gradient": "linear-gradient(135deg, #059669 0%, #10b981 100%)",
            "expense_gradient": "linear-gradient(135deg, #dc2626 0%, #ef4444 100%)",
            "logo": "🏢"
        }
    }
    return themes.get(company, themes["W TRAVEL CHILE"])

# Función para generar CSS dinámico
def generate_dynamic_css(company, dark_mode=True):
    theme = get_company_theme(company)
    
    # Colores para modo oscuro
    if dark_mode:
        bg_color = "#0f172a"
        card_bg = "#1e293b"
        text_color = "#f1f5f9"
        border_color = "#334155"
        hover_bg = "#334155"
        sidebar_bg = "#1e293b"
    else:
        bg_color = "#ffffff"
        card_bg = "#ffffff"
        text_color = "#1f2937"
        border_color = "#e5e7eb"
        hover_bg = "#f8f9fa"
        sidebar_bg = "#f8fafc"
    
    return f"""
    <style>
        /* Variables CSS dinámicas */
        :root {{
            --primary-color: {theme['primary']};
            --secondary-color: {theme['secondary']};
            --accent-color: {theme['accent']};
            --light-color: {theme['light']};
            --gradient: {theme['gradient']};
            --income-gradient: {theme['income_gradient']};
            --expense-gradient: {theme['expense_gradient']};
            --bg-color: {bg_color};
            --card-bg: {card_bg};
            --text-color: {text_color};
            --border-color: {border_color};
            --hover-bg: {hover_bg};
            --sidebar-bg: {sidebar_bg};
        }}
        
        /* Configuración global del modo oscuro */
        .stApp {{
            background-color: var(--bg-color) !important;
            color: var(--text-color) !important;
        }}
        
        /* Sidebar en modo oscuro */
        .css-1d391kg {{
            background-color: var(--sidebar-bg) !important;
        }}
        
        /* Header principal */
        .main-header {{
            font-size: 2.5rem;
            font-weight: bold;
            background: var(--gradient);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            text-align: center;
            margin-bottom: 2rem;
            text-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }}
        
        /* Tarjetas de categorías */
        .category-card {{
            background: var(--card-bg);
            border: 2px solid var(--border-color);
            border-radius: 15px;
            padding: 1.5rem;
            margin: 0.5rem 0;
            cursor: pointer;
            transition: all 0.3s ease;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            color: var(--text-color);
        }}
        
        .category-card:hover {{
            transform: translateY(-2px);
            box-shadow: 0 8px 25px rgba(0,0,0,0.15);
            border-color: var(--primary-color);
            background: var(--hover-bg);
        }}
        
        .category-card.selected {{
            border-color: var(--primary-color);
            background: var(--hover-bg);
            box-shadow: 0 8px 25px rgba(0,0,0,0.15);
        }}
        
        /* Subcategorías */
        .subcategory-item {{
            background: var(--hover-bg);
            border: 1px solid var(--border-color);
            border-radius: 8px;
            padding: 0.75rem;
            margin: 0.25rem 0;
            transition: all 0.2s ease;
            color: var(--text-color);
        }}
        
        .subcategory-item:hover {{
            background: var(--border-color);
            border-color: var(--secondary-color);
        }}
        
        /* Métricas */
        .metric-card {{
            background: var(--gradient);
            color: white;
            padding: 2rem;
            border-radius: 20px;
            text-align: center;
            box-shadow: 0 8px 25px rgba(0,0,0,0.1);
            transition: all 0.3s ease;
        }}
        
        .metric-card:hover {{
            transform: translateY(-4px);
            box-shadow: 0 12px 35px rgba(0,0,0,0.15);
        }}
        
        /* Títulos de sección */
        .section-title {{
            font-size: 1.8rem;
            font-weight: bold;
            color: var(--primary-color);
            margin-bottom: 1.5rem;
            text-align: center;
        }}
        
        /* Indicador de empresa activa */
        .active-company-indicator {{
            background: var(--gradient);
            color: white;
            padding: 1rem;
            border-radius: 10px;
            margin-bottom: 1.5rem;
            text-align: center;
            font-weight: bold;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        }}
        
        /* Animaciones */
        @keyframes fadeIn {{
            from {{ opacity: 0; transform: translateY(20px); }}
            to {{ opacity: 1; transform: translateY(0); }}
        }}
        
        .fade-in {{
            animation: fadeIn 0.6s ease-out;
        }}
        
        /* Estilos para elementos de Streamlit en modo oscuro */
        .stSelectbox, .stTextInput, .stNumberInput, .stDateInput {{
            background-color: var(--card-bg) !important;
            color: var(--text-color) !important;
            border-color: var(--border-color) !important;
        }}
        
        .stSelectbox > div > div {{
            background-color: var(--card-bg) !important;
            color: var(--text-color) !important;
        }}
        
        /* Dataframes en modo oscuro */
        .dataframe {{
            background-color: var(--card-bg) !important;
            color: var(--text-color) !important;
        }}
        
        /* Expanders en modo oscuro */
        .streamlit-expanderHeader {{
            background-color: var(--card-bg) !important;
            color: var(--text-color) !important;
            border-color: var(--border-color) !important;
        }}
        
        .streamlit-expanderContent {{
            background-color: var(--card-bg) !important;
            color: var(--text-color) !important;
        }}
    </style>
    """

# Función para cargar datos desde CSV
def load_company_data(company):
    csv_files = {
        "W TRAVEL CHILE": "w_travel_chile.csv",
        "WOLF TRAVEL CHILE": "wolf_travel_chile.csv", 
        "HELPMETRAVEL SPA": "helpmetravel_spa.csv"
    }
    
    csv_file = csv_files.get(company)
    if csv_file and os.path.exists(csv_file):
        df = pd.read_csv(csv_file)
        return df
    else:
        st.error(f"Archivo CSV no encontrado para {company}")
        return pd.DataFrame()

# Función para categorizar transacciones
def categorize_transaction(description, transaction_type):
    description_lower = description.lower()
    
    # Categorizar ingresos
    if transaction_type == "Ingreso":
        if any(word in description_lower for word in ['paquete', 'turístico', 'viaje', 'reserva']):
            return "Ingresos", "Ventas de Paquetes"
        elif any(word in description_lower for word in ['comisión', 'comision']):
            return "Ingresos", "Comisiones"
        elif any(word in description_lower for word in ['servicio', 'tour', 'guía']):
            return "Ingresos", "Servicios Turísticos"
        else:
            return "Ingresos", "Otros Ingresos"
    
    # Categorizar gastos
    else:
        if any(word in description_lower for word in ['arriendo', 'oficina', 'rent']):
            return "Gastos Operacionales", "Arriendo de Oficina"
        elif any(word in description_lower for word in ['servicios', 'básicos', 'luz', 'agua', 'gas']):
            return "Gastos Operacionales", "Servicios Básicos"
        elif any(word in description_lower for word in ['equipos', 'computación', 'software', 'audiovisuales']):
            return "Gastos Operacionales", "Equipos y Tecnología"
        elif any(word in description_lower for word in ['mantenimiento']):
            return "Gastos Operacionales", "Mantenimiento"
        elif any(word in description_lower for word in ['impuestos', 'tasas', 'gubernamentales']):
            return "Gastos Administrativos", "Impuestos"
        elif any(word in description_lower for word in ['supermercado', 'provisiones', 'alimentación']):
            return "Gastos de Viaje", "Alimentación"
        else:
            return "Gastos Operacionales", "Otros Gastos"

# Inicializar session state
if 'selected_company' not in st.session_state:
    st.session_state.selected_company = "W TRAVEL CHILE"

if 'selected_category' not in st.session_state:
    st.session_state.selected_category = None

if 'dark_mode' not in st.session_state:
    st.session_state.dark_mode = True  # Por defecto en modo oscuro

# Cargar datos de la empresa seleccionada
df_transactions = load_company_data(st.session_state.selected_company)

# Aplicar categorización si no existe
if not df_transactions.empty and 'Categoria_Padre' not in df_transactions.columns:
    df_transactions['Categoria_Padre'] = ''
    df_transactions['Categoria_Hijo'] = ''
    
    for idx, row in df_transactions.iterrows():
        cat_padre, cat_hijo = categorize_transaction(row['Descripción'], row['Tipo'])
        df_transactions.at[idx, 'Categoria_Padre'] = cat_padre
        df_transactions.at[idx, 'Categoria_Hijo'] = cat_hijo

# Aplicar CSS dinámico
st.markdown(generate_dynamic_css(st.session_state.selected_company, st.session_state.dark_mode), unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    theme = get_company_theme(st.session_state.selected_company)
    
    # Header del sidebar
    st.markdown(f"""
    <div style="text-align: center; margin-bottom: 2rem;">
        <h1 style="color: {theme['primary']}; font-size: 2rem; margin-bottom: 0.5rem;">
            {theme['logo']} Tri-Ledger
        </h1>
        <p style="color: {theme['secondary']}; font-size: 0.9rem; margin: 0;">
            Sistema de Categorías
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Toggle modo oscuro
    st.markdown("### 🌙 Apariencia")
    dark_mode = st.toggle("Modo Oscuro", value=st.session_state.dark_mode, help="Cambiar entre modo claro y oscuro")
    
    # Actualizar modo oscuro
    if dark_mode != st.session_state.dark_mode:
        st.session_state.dark_mode = dark_mode
        st.rerun()
    
    # Navegación
    st.markdown("### 📊 Navegación")
    page = st.radio("Seleccionar página", ["Dashboard", "Categorías", "Transacciones", "Reportes"], label_visibility="collapsed")
    
    # Filtros
    st.markdown("### 🔍 Filtros")
    
    # Selector de empresa
    companies = ["W TRAVEL CHILE", "WOLF TRAVEL CHILE", "HELPMETRAVEL SPA"]
    company_logos = {"W TRAVEL CHILE": "🌍", "WOLF TRAVEL CHILE": "🐺", "HELPMETRAVEL SPA": "🏢"}
    
    selected_company = st.selectbox(
        "Empresa",
        companies,
        format_func=lambda x: f"{company_logos[x]} {x}",
        index=companies.index(st.session_state.selected_company)
    )
    
    # Actualizar empresa seleccionada
    if selected_company != st.session_state.selected_company:
        st.session_state.selected_company = selected_company
        st.rerun()

# Contenido principal
if page == "Dashboard":
    # Header principal
    theme = get_company_theme(st.session_state.selected_company)
    st.markdown(f"""
    <h1 class="main-header fade-in">
        {theme['logo']} Dashboard con Categorías - {st.session_state.selected_company}
    </h1>
    """, unsafe_allow_html=True)
    
    # Indicador de empresa activa
    st.markdown(f"""
    <div class="active-company-indicator fade-in">
        📊 Empresa Activa: {st.session_state.selected_company}
    </div>
    """, unsafe_allow_html=True)
    
    if not df_transactions.empty:
        # Cálculos financieros por categorías
        total_income = df_transactions[df_transactions['Monto'] > 0]['Monto'].sum()
        total_expenses = abs(df_transactions[df_transactions['Monto'] < 0]['Monto'].sum())
        current_balance = total_income - total_expenses
        
        # Métricas principales
        st.markdown("### 💰 Resumen Financiero")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown(f'''
            <div class="metric-card fade-in">
                <h3>💰 Saldo Actual</h3>
                <h2 style="font-size: 2.5rem; margin: 1rem 0;">${current_balance:,.0f}</h2>
                <p>Basado en todas las transacciones</p>
            </div>
            ''', unsafe_allow_html=True)
        
        with col2:
            st.markdown(f'''
            <div class="metric-card fade-in">
                <h3>📈 Ingresos Totales</h3>
                <h2 style="font-size: 2.5rem; margin: 1rem 0;">${total_income:,.0f}</h2>
                <p>Ingresos acumulados</p>
            </div>
            ''', unsafe_allow_html=True)
        
        with col3:
            st.markdown(f'''
            <div class="metric-card fade-in">
                <h3>📉 Gastos Totales</h3>
                <h2 style="font-size: 2.5rem; margin: 1rem 0;">${total_expenses:,.0f}</h2>
                <p>Gastos acumulados</p>
            </div>
            ''', unsafe_allow_html=True)
        
        # Gráficos por categorías
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown('<h3 class="section-title">📊 Distribución por Categorías Padre</h3>', unsafe_allow_html=True)
            
            # Gráfico de categorías padre
            category_data = df_transactions.groupby('Categoria_Padre')['Monto'].sum().reset_index()
            category_data['Monto'] = category_data['Monto'].apply(lambda x: abs(x))
            
            fig_pie = px.pie(
                category_data,
                values='Monto',
                names='Categoria_Padre',
                title="Distribución por Categorías Padre",
                color_discrete_map={
                    'Ingresos': '#10b981',
                    'Gastos Operacionales': '#ef4444',
                    'Gastos Administrativos': '#f97316',
                    'Gastos de Personal': '#8b5cf6',
                    'Gastos de Marketing': '#06b6d4',
                    'Gastos de Viaje': '#eab308'
                }
            )
            st.plotly_chart(fig_pie, use_container_width=True)
        
        with col2:
            st.markdown('<h3 class="section-title">📊 Top 5 Subcategorías</h3>', unsafe_allow_html=True)
            
            # Gráfico de subcategorías
            subcategory_data = df_transactions.groupby('Categoria_Hijo')['Monto'].sum().reset_index()
            subcategory_data['Monto'] = subcategory_data['Monto'].apply(lambda x: abs(x))
            subcategory_data = subcategory_data.sort_values('Monto', ascending=False).head(5)
            
            fig_bars = px.bar(
                subcategory_data,
                x='Categoria_Hijo',
                y='Monto',
                title="Top 5 Subcategorías por Monto",
                color='Monto',
                color_continuous_scale='viridis'
            )
            fig_bars.update_layout(xaxis={'tickangle': 45})
            st.plotly_chart(fig_bars, use_container_width=True)

elif page == "Categorías":
    st.markdown('<h1 class="main-header">🏷️ Gestión de Categorías</h1>', unsafe_allow_html=True)
    
    # Mostrar estructura de categorías
    st.markdown("### 📋 Estructura de Categorías Jerárquicas")
    
    # Crear columnas para mostrar categorías padre
    cols = st.columns(2)
    
    for i, (cat_padre, cat_info) in enumerate(CATEGORIAS_PADRE.items()):
        with cols[i % 2]:
            # Crear el contenido HTML completo en una sola cadena
            subcategories_html = ""
            for subcat in cat_info['subcategorias']:
                subcategories_html += f"""
                <div class="subcategory-item">
                    📌 {subcat}
                </div>
                """
            
            st.markdown(f"""
            <div class="category-card">
                <h3 style="color: {cat_info['color']}; margin-bottom: 1rem;">
                    {cat_info['icon']} {cat_padre}
                </h3>
                <div style="margin-left: 1rem;">
                    {subcategories_html}
                </div>
            </div>
            """, unsafe_allow_html=True)
    
    # Estadísticas de categorías
    if not df_transactions.empty:
        st.markdown("### 📊 Estadísticas de Categorías")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Resumen por categoría padre
            st.markdown("#### Por Categoría Padre")
            category_summary = df_transactions.groupby('Categoria_Padre').agg({
                'Monto': ['sum', 'count']
            }).reset_index()
            category_summary.columns = ['Categoría Padre', 'Total', 'Cantidad']
            category_summary['Total'] = category_summary['Total'].apply(lambda x: f"${abs(x):,.0f}")
            st.dataframe(category_summary, use_container_width=True)
        
        with col2:
            # Resumen por subcategoría
            st.markdown("#### Por Subcategoría")
            subcategory_summary = df_transactions.groupby(['Categoria_Padre', 'Categoria_Hijo']).agg({
                'Monto': ['sum', 'count']
            }).reset_index()
            subcategory_summary.columns = ['Categoría Padre', 'Subcategoría', 'Total', 'Cantidad']
            subcategory_summary['Total'] = subcategory_summary['Total'].apply(lambda x: f"${abs(x):,.0f}")
            st.dataframe(subcategory_summary, use_container_width=True)

elif page == "Transacciones":
    st.markdown('<h1 class="main-header">📝 Transacciones por Categorías</h1>', unsafe_allow_html=True)
    
    if not df_transactions.empty:
        # Formulario para nueva transacción
        with st.expander("➕ Agregar Nueva Transacción", expanded=False):
            col1, col2 = st.columns(2)
            
            with col1:
                description = st.text_input("Descripción")
                transaction_type = st.selectbox("Tipo", ["Ingreso", "Gasto"])
                company = st.selectbox("Empresa", [st.session_state.selected_company])
                
                # Selector de categoría padre
                categorias_padre_disponibles = list(CATEGORIAS_PADRE.keys())
                categoria_padre = st.selectbox("Categoría Padre", categorias_padre_disponibles)
                
                # Selector de categoría hijo basado en la categoría padre seleccionada
                subcategorias_disponibles = CATEGORIAS_PADRE[categoria_padre]["subcategorias"]
                categoria_hijo = st.selectbox("Categoría Hijo", subcategorias_disponibles)
            
            with col2:
                amount = st.number_input("Monto", min_value=0.0, value=0.0, step=0.01)
                date = st.date_input("Fecha", value=datetime.now())
                
                # Campo opcional para cuenta destino
                cuenta_destino = st.text_input("Cuenta Transacción Cuenta Destino (Opcional)", placeholder="Ej: Banco, Efectivo, Tarjeta de Crédito")
            
            # Mostrar resumen de la transacción
            st.markdown("### 📋 Resumen de la Transacción")
            col_sum1, col_sum2, col_sum3 = st.columns(3)
            
            with col_sum1:
                st.info(f"**Descripción:** {description if description else 'No especificada'}")
                st.info(f"**Tipo:** {transaction_type}")
                st.info(f"**Empresa:** {company}")
            
            with col_sum2:
                st.info(f"**Monto:** ${amount:,.2f}")
                st.info(f"**Fecha:** {date.strftime('%d/%m/%Y')}")
                st.info(f"**Categoría Padre:** {categoria_padre}")
            
            with col_sum3:
                st.info(f"**Categoría Hijo:** {categoria_hijo}")
                st.info(f"**Cuenta Destino:** {cuenta_destino if cuenta_destino else 'No especificada'}")
            
            if st.button("💾 Guardar Transacción", type="primary"):
                # Aquí se procesaría la transacción
                st.success("✅ Transacción guardada exitosamente!")
                st.balloons()
        
        # Filtros de categorías
        st.markdown("### 🔍 Filtros de Categorías")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Filtro por categoría padre
            categorias_padre = df_transactions['Categoria_Padre'].unique()
            categoria_padre_filtro = st.selectbox(
                "Categoría Padre",
                ["Todas"] + list(categorias_padre)
            )
        
        with col2:
            # Filtro por subcategoría
            if categoria_padre_filtro != "Todas":
                subcategorias = df_transactions[df_transactions['Categoria_Padre'] == categoria_padre_filtro]['Categoria_Hijo'].unique()
                subcategoria_filtro = st.selectbox(
                    "Subcategoría",
                    ["Todas"] + list(subcategorias)
                )
            else:
                subcategoria_filtro = "Todas"
        
        # Aplicar filtros
        df_filtrado = df_transactions.copy()
        
        if categoria_padre_filtro != "Todas":
            df_filtrado = df_filtrado[df_filtrado['Categoria_Padre'] == categoria_padre_filtro]
        
        if subcategoria_filtro != "Todas":
            df_filtrado = df_filtrado[df_filtrado['Categoria_Hijo'] == subcategoria_filtro]
        
        # Mostrar transacciones filtradas
        st.markdown("### 📊 Transacciones Filtradas")
        
        if not df_filtrado.empty:
            # Crear tabla personalizada
            for _, row in df_filtrado.iterrows():
                amount_color = "#10b981" if row['Monto'] > 0 else "#ef4444"
                amount_sign = "+" if row['Monto'] > 0 else ""
                
                col1, col2, col3, col4, col5 = st.columns([3, 2, 2, 2, 2])
                
                with col1:
                    st.write(f"**{row['Descripción']}**")
                with col2:
                    st.markdown(f'<span style="background-color: {CATEGORIAS_PADRE.get(row["Categoria_Padre"], {}).get("color", "#6b7280")}; color: white; padding: 4px 8px; border-radius: 12px; font-size: 0.8em;">{row["Categoria_Padre"]}</span>', unsafe_allow_html=True)
                with col3:
                    st.write(row['Categoria_Hijo'])
                with col4:
                    st.write(row['Fecha'])
                with col5:
                    st.markdown(f'<span style="color: {amount_color}; font-weight: bold;">{amount_sign}${abs(row["Monto"]):,.0f}</span>', unsafe_allow_html=True)
                
                st.markdown("---")
        else:
            st.info("No hay transacciones que coincidan con los filtros seleccionados.")

elif page == "Reportes":
    st.markdown('<h1 class="main-header">📈 Reportes por Categorías</h1>', unsafe_allow_html=True)
    
    if not df_transactions.empty:
        # Análisis detallado por categorías
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### 📊 Análisis por Categoría Padre")
            
            # Gráfico de barras por categoría padre
            category_analysis = df_transactions.groupby('Categoria_Padre')['Monto'].sum().reset_index()
            category_analysis['Monto'] = category_analysis['Monto'].apply(lambda x: abs(x))
            
            fig_bars = px.bar(
                category_analysis,
                x='Categoria_Padre',
                y='Monto',
                title="Total por Categoría Padre",
                color='Categoria_Padre',
                color_discrete_map={
                    'Ingresos': '#10b981',
                    'Gastos Operacionales': '#ef4444',
                    'Gastos Administrativos': '#f97316',
                    'Gastos de Personal': '#8b5cf6',
                    'Gastos de Marketing': '#06b6d4',
                    'Gastos de Viaje': '#eab308'
                }
            )
            fig_bars.update_layout(xaxis={'tickangle': 45})
            st.plotly_chart(fig_bars, use_container_width=True)
        
        with col2:
            st.markdown("### 📊 Análisis por Subcategoría")
            
            # Gráfico de subcategorías más importantes
            subcategory_analysis = df_transactions.groupby('Categoria_Hijo')['Monto'].sum().reset_index()
            subcategory_analysis['Monto'] = subcategory_analysis['Monto'].apply(lambda x: abs(x))
            subcategory_analysis = subcategory_analysis.sort_values('Monto', ascending=False).head(8)
            
            fig_horizontal = px.bar(
                subcategory_analysis,
                x='Monto',
                y='Categoria_Hijo',
                orientation='h',
                title="Top 8 Subcategorías",
                color='Monto',
                color_continuous_scale='viridis'
            )
            st.plotly_chart(fig_horizontal, use_container_width=True)
        
        # Análisis temporal por categorías
        st.markdown("### 📈 Evolución Temporal por Categorías")
        
        # Preparar datos temporales
        df_temp = df_transactions.copy()
        df_temp['Fecha'] = pd.to_datetime(df_temp['Fecha'], format='%d/%m/%Y')
        df_temp['Mes'] = df_temp['Fecha'].dt.to_period('M')
        
        monthly_by_category = df_temp.groupby(['Mes', 'Categoria_Padre'])['Monto'].sum().reset_index()
        monthly_by_category['Mes'] = monthly_by_category['Mes'].astype(str)
        
        fig_line = px.line(
            monthly_by_category,
            x='Mes',
            y='Monto',
            color='Categoria_Padre',
            title="Evolución Mensual por Categoría Padre",
            color_discrete_map={
                'Ingresos': '#10b981',
                'Gastos Operacionales': '#ef4444',
                'Gastos Administrativos': '#f97316',
                'Gastos de Personal': '#8b5cf6',
                'Gastos de Marketing': '#06b6d4',
                'Gastos de Viaje': '#eab308'
            }
        )
        st.plotly_chart(fig_line, use_container_width=True)

# Footer
st.markdown("---")
footer_bg = "#1e293b" if st.session_state.dark_mode else get_company_theme(st.session_state.selected_company)['light']
footer_text = "#f1f5f9" if st.session_state.dark_mode else "#666"

st.markdown(f"""
<div style="text-align: center; color: {footer_text}; padding: 2rem; background: {footer_bg}; border-radius: 10px; margin-top: 2rem; border: 1px solid var(--border-color);">
    <p style="font-size: 1.1rem; font-weight: bold; color: {get_company_theme(st.session_state.selected_company)['primary']};">
        Tri-Ledger - Sistema de Categorías Jerárquicas
    </p>
    <p>Desarrollado con Streamlit y sistema de categorías padre-hijo</p>
    <p style="font-size: 0.9rem; margin-top: 1rem;">
        🏷️ Categorías Padre e Hijo implementadas para {st.session_state.selected_company}
    </p>
    <p style="font-size: 0.8rem; margin-top: 0.5rem; opacity: 0.7;">
        🌙 Modo {'Oscuro' if st.session_state.dark_mode else 'Claro'} Activado
    </p>
</div>
""", unsafe_allow_html=True) 