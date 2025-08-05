import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import os

# Configuración de la página
st.set_page_config(
    page_title="Tri-Ledger V2 - Dashboard Financiero",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="expanded"
)

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
def generate_dynamic_css(company):
    theme = get_company_theme(company)
    
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
        
        /* Tarjetas de empresa */
        .company-card {{
            background: var(--gradient);
            color: white;
            padding: 1.5rem;
            border-radius: 15px;
            margin: 0.5rem 0;
            cursor: pointer;
            transition: all 0.3s ease;
            text-align: center;
            font-weight: bold;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
            border: 3px solid transparent;
        }}
        
        .company-card:hover {{
            transform: translateY(-4px);
            box-shadow: 0 8px 25px rgba(0,0,0,0.15);
            border-color: var(--accent-color);
        }}
        
        .company-card.selected {{
            background: var(--accent-color);
            border-color: var(--primary-color);
            box-shadow: 0 8px 25px rgba(0,0,0,0.2);
        }}
        
        /* Botones de empresa */
        .stButton > button {{
            background: var(--gradient) !important;
            color: white !important;
            border: none !important;
            border-radius: 15px !important;
            padding: 1.5rem !important;
            font-weight: bold !important;
            text-align: center !important;
            transition: all 0.3s ease !important;
            width: 100% !important;
            height: auto !important;
            min-height: 80px !important;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1) !important;
        }}
        
        .stButton > button:hover {{
            transform: translateY(-2px) !important;
            box-shadow: 0 8px 25px rgba(0,0,0,0.15) !important;
            background: var(--accent-color) !important;
        }}
        
        .stButton > button:focus {{
            background: var(--accent-color) !important;
            box-shadow: 0 8px 25px rgba(0,0,0,0.2) !important;
        }}
        
        /* Tarjetas de métricas */
        .metric-card {{
            background: var(--gradient);
            color: white;
            padding: 2rem;
            border-radius: 20px;
            text-align: center;
            box-shadow: 0 8px 25px rgba(0,0,0,0.1);
            transition: all 0.3s ease;
            border: 2px solid transparent;
        }}
        
        .metric-card:hover {{
            transform: translateY(-4px);
            box-shadow: 0 12px 35px rgba(0,0,0,0.15);
        }}
        
        .income-card {{
            background: var(--income-gradient);
            color: white;
            padding: 2rem;
            border-radius: 20px;
            text-align: center;
            box-shadow: 0 8px 25px rgba(0,0,0,0.1);
            transition: all 0.3s ease;
        }}
        
        .income-card:hover {{
            transform: translateY(-4px);
            box-shadow: 0 12px 35px rgba(0,0,0,0.15);
        }}
        
        .expense-card {{
            background: var(--expense-gradient);
            color: white;
            padding: 2rem;
            border-radius: 20px;
            text-align: center;
            box-shadow: 0 8px 25px rgba(0,0,0,0.1);
            transition: all 0.3s ease;
        }}
        
        .expense-card:hover {{
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
            position: relative;
        }}
        
        .section-title::after {{
            content: '';
            position: absolute;
            bottom: -8px;
            left: 50%;
            transform: translateX(-50%);
            width: 60px;
            height: 4px;
            background: var(--gradient);
            border-radius: 2px;
        }}
        
        /* Tabla de transacciones */
        .transaction-table {{
            background: white;
            border-radius: 15px;
            padding: 1.5rem;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
            border: 1px solid #e5e7eb;
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
        
        /* Sidebar styling */
        .css-1d391kg {{
            background: var(--light-color);
        }}
        
        /* Animaciones */
        @keyframes fadeIn {{
            from {{ opacity: 0; transform: translateY(20px); }}
            to {{ opacity: 1; transform: translateY(0); }}
        }}
        
        .fade-in {{
            animation: fadeIn 0.6s ease-out;
        }}
        
                 /* Responsive design */
         @media (max-width: 768px) {{
             .main-header {{
                 font-size: 2rem;
             }}
             
             .metric-card, .income-card, .expense-card {{
                 padding: 1.5rem;
             }}
         }}
         
         /* Estilos para botones de tipo en transacciones */
         .transaction-type-badge {{
             background-color: var(--primary-color);
             color: white;
             padding: 6px 16px;
             border-radius: 15px;
             font-size: 0.85em;
             font-weight: bold;
             display: inline-block;
             min-width: 80px;
             text-align: center;
             white-space: nowrap;
             overflow: hidden;
             text-overflow: ellipsis;
         }}
         
         /* Mejorar responsive para columnas */
         @media (max-width: 1200px) {{
             .transaction-columns {{
                 grid-template-columns: 2fr 1fr 1fr 1fr;
             }}
         }}
         
         @media (max-width: 768px) {{
             .transaction-columns {{
                 grid-template-columns: 1fr;
                 gap: 0.5rem;
             }}
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

# Inicializar session state
if 'selected_company' not in st.session_state:
    st.session_state.selected_company = "W TRAVEL CHILE"

# Cargar datos de la empresa seleccionada
df_transactions = load_company_data(st.session_state.selected_company)

# Aplicar CSS dinámico
st.markdown(generate_dynamic_css(st.session_state.selected_company), unsafe_allow_html=True)

# Sidebar mejorado
with st.sidebar:
    theme = get_company_theme(st.session_state.selected_company)
    
    # Header del sidebar
    st.markdown(f"""
    <div style="text-align: center; margin-bottom: 2rem;">
        <h1 style="color: {theme['primary']}; font-size: 2rem; margin-bottom: 0.5rem;">
            {theme['logo']} Tri-Ledger V2
        </h1>
        <p style="color: {theme['secondary']}; font-size: 0.9rem; margin: 0;">
            Dashboard Financiero Avanzado
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Navegación
    st.markdown("### 📊 Navegación")
    page = st.radio("Seleccionar página", ["Dashboard", "Transacciones", "Reportes"], label_visibility="collapsed")
    
    # Filtros
    st.markdown("### 🔍 Filtros")
    
    # Selector de empresa con logos
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
    
    # Filtro de fechas
    if not df_transactions.empty:
        df_transactions['Fecha'] = pd.to_datetime(df_transactions['Fecha'], format='%d/%m/%Y')
        min_date = df_transactions['Fecha'].min()
        max_date = df_transactions['Fecha'].max()
        
        date_range = st.date_input(
            "📅 Rango de fechas",
            value=(min_date.date(), max_date.date()),
            min_value=min_date.date(),
            max_value=max_date.date()
        )

# Contenido principal
if page == "Dashboard":
    # Header principal
    theme = get_company_theme(st.session_state.selected_company)
    st.markdown(f"""
    <h1 class="main-header fade-in">
        {theme['logo']} Dashboard Financiero - {st.session_state.selected_company}
    </h1>
    """, unsafe_allow_html=True)
    
    # Indicador de empresa activa
    st.markdown(f"""
    <div class="active-company-indicator fade-in">
        📊 Empresa Activa: {st.session_state.selected_company}
    </div>
    """, unsafe_allow_html=True)
    
    # Selector de empresas mejorado
    st.markdown("### 🏢 Seleccionar Empresa")
    st.markdown("Haz clic en una empresa para cambiar la vista:")
    
    cols = st.columns(len(companies))
    
    for i, company in enumerate(companies):
        with cols[i]:
            company_theme = get_company_theme(company)
            is_selected = company == st.session_state.selected_company
            
            if st.button(
                f"{company_theme['logo']} {company}",
                key=f"btn_{i}",
                use_container_width=True
            ):
                st.session_state.selected_company = company
                st.rerun()
    
    if not df_transactions.empty:
        # Cálculos financieros
        total_income = df_transactions[df_transactions['Monto'] > 0]['Monto'].sum()
        total_expenses = abs(df_transactions[df_transactions['Monto'] < 0]['Monto'].sum())
        current_balance = total_income - total_expenses
        
        # Métricas principales con animaciones
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
            <div class="income-card fade-in">
                <h3>📈 Ingresos Totales</h3>
                <h2 style="font-size: 2.5rem; margin: 1rem 0;">${total_income:,.0f}</h2>
                <p>Ingresos acumulados</p>
            </div>
            ''', unsafe_allow_html=True)
        
        with col3:
            st.markdown(f'''
            <div class="expense-card fade-in">
                <h3>📉 Gastos Totales</h3>
                <h2 style="font-size: 2.5rem; margin: 1rem 0;">${total_expenses:,.0f}</h2>
                <p>Gastos acumulados</p>
            </div>
            ''', unsafe_allow_html=True)
        
        # Gráficos y análisis
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown('<h3 class="section-title">📊 Flujo de Caja - Últimos 7 Días</h3>', unsafe_allow_html=True)
            
            # Gráfico de flujo de caja
            recent_data = df_transactions.copy()
            end_date = datetime.now()
            start_date = end_date - timedelta(days=6)
            
            # Crear rango de fechas
            date_range = pd.date_range(start=start_date, end=end_date, freq='D')
            
            # Agrupar datos por fecha
            daily_data = []
            for date in date_range:
                date_str = date.strftime('%d/%m')
                day_data = recent_data[recent_data['Fecha'].dt.date == date.date()]
                day_income = day_data[day_data['Monto'] > 0]['Monto'].sum()
                day_expenses = abs(day_data[day_data['Monto'] < 0]['Monto'].sum())
                
                daily_data.append({
                    'Fecha': date_str,
                    'Ingresos': day_income,
                    'Gastos': day_expenses
                })
            
            df_daily = pd.DataFrame(daily_data)
            
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
            
            fig.update_layout(
                title="Flujo de Caja - Últimos 7 días",
                xaxis_title="Fecha",
                yaxis_title="Monto ($)",
                barmode='group',
                height=400,
                showlegend=True,
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)'
            )
            
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.markdown('<h3 class="section-title">📋 Transacciones Recientes</h3>', unsafe_allow_html=True)
            
            # Tabla de transacciones recientes
            st.markdown('<div class="transaction-table fade-in">', unsafe_allow_html=True)
            
            recent_transactions = df_transactions.head(5)
            
            for _, row in recent_transactions.iterrows():
                amount_color = "#10b981" if row['Monto'] > 0 else "#ef4444"
                amount_sign = "+" if row['Monto'] > 0 else ""
                type_color = "#10b981" if row['Tipo'] == "Ingreso" else "#6b7280"
                
                # Ajustar proporciones de columnas para evitar cortes
                col1, col2, col3, col4 = st.columns([4, 2, 2, 2])
                
                with col1:
                    st.write(f"**{row['Descripción']}**")
                with col2:
                    # Botón con más padding y mejor responsive
                    st.markdown(f'<div style="text-align: center;"><span style="background-color: {type_color}; color: white; padding: 6px 16px; border-radius: 15px; font-size: 0.85em; font-weight: bold; display: inline-block; min-width: 80px; text-align: center;">{row["Tipo"]}</span></div>', unsafe_allow_html=True)
                with col3:
                    st.write(row['Fecha'].strftime('%d/%m/%Y'))
                with col4:
                    st.markdown(f'<div style="text-align: right;"><span style="color: {amount_color}; font-weight: bold; font-size: 1.1em;">{amount_sign}${abs(row["Monto"]):,.0f}</span></div>', unsafe_allow_html=True)
                
                st.markdown("---")
            
            st.markdown('</div>', unsafe_allow_html=True)

elif page == "Transacciones":
    st.markdown('<h1 class="main-header">📝 Gestión de Transacciones</h1>', unsafe_allow_html=True)
    
    if not df_transactions.empty:
        # Formulario para nueva transacción
        with st.expander("➕ Agregar Nueva Transacción", expanded=False):
            col1, col2 = st.columns(2)
            
            with col1:
                description = st.text_input("Descripción")
                transaction_type = st.selectbox("Tipo", ["Ingreso", "Gasto"])
                company = st.selectbox("Empresa", [st.session_state.selected_company])
            
            with col2:
                amount = st.number_input("Monto", min_value=0.0, value=0.0, step=0.01)
                date = st.date_input("Fecha", value=datetime.now())
            
            if st.button("💾 Guardar Transacción", type="primary"):
                st.success("✅ Transacción guardada exitosamente!")
        
        # Tabla completa de transacciones
        st.markdown('<h3 class="section-title">📊 Todas las Transacciones</h3>', unsafe_allow_html=True)
        st.markdown(f'<p style="color: #666; text-align: center;">Mostrando transacciones de: <strong>{st.session_state.selected_company}</strong></p>', unsafe_allow_html=True)
        
        # Crear tabla personalizada con mejor formato
        st.markdown('<div class="transaction-table">', unsafe_allow_html=True)
        
        # Header de la tabla
        col1, col2, col3, col4 = st.columns([4, 2, 2, 2])
        with col1:
            st.markdown("**Descripción**")
        with col2:
            st.markdown("**Tipo**")
        with col3:
            st.markdown("**Fecha**")
        with col4:
            st.markdown("**Monto**")
        
        st.markdown("---")
        
        # Filas de transacciones
        for _, row in df_transactions.iterrows():
            amount_color = "#10b981" if row['Monto'] > 0 else "#ef4444"
            amount_sign = "+" if row['Monto'] > 0 else ""
            type_color = "#10b981" if row['Tipo'] == "Ingreso" else "#6b7280"
            
            col1, col2, col3, col4 = st.columns([4, 2, 2, 2])
            
            with col1:
                st.write(row['Descripción'])
            with col2:
                st.markdown(f'<div style="text-align: center;"><span style="background-color: {type_color}; color: white; padding: 6px 16px; border-radius: 15px; font-size: 0.85em; font-weight: bold; display: inline-block; min-width: 80px; text-align: center;">{row["Tipo"]}</span></div>', unsafe_allow_html=True)
            with col3:
                st.write(row['Fecha'].strftime('%d/%m/%Y'))
            with col4:
                st.markdown(f'<div style="text-align: right;"><span style="color: {amount_color}; font-weight: bold; font-size: 1.1em;">{amount_sign}${abs(row["Monto"]):,.0f}</span></div>', unsafe_allow_html=True)
            
            st.markdown("---")
        
        st.markdown('</div>', unsafe_allow_html=True)

elif page == "Reportes":
    st.markdown('<h1 class="main-header">📈 Reportes Financieros</h1>', unsafe_allow_html=True)
    
    if not df_transactions.empty:
        # Cálculos financieros para reportes
        total_income = df_transactions[df_transactions['Monto'] > 0]['Monto'].sum()
        total_expenses = abs(df_transactions[df_transactions['Monto'] < 0]['Monto'].sum())
        current_balance = total_income - total_expenses
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown('<h3 class="section-title">📊 Análisis por Tipo</h3>', unsafe_allow_html=True)
            
            # Gráfico de barras en lugar de torta para mejor visualización
            type_data = df_transactions.groupby('Tipo')['Monto'].sum().reset_index()
            type_data['Monto'] = type_data['Monto'].apply(lambda x: abs(x))  # Valor absoluto para visualización
            
            fig_bars = px.bar(
                type_data,
                x='Tipo',
                y='Monto',
                title=f"Total por Tipo - {st.session_state.selected_company}",
                color='Tipo',
                color_discrete_map={'Ingreso': '#10b981', 'Gasto': '#ef4444'},
                text=type_data['Monto'].apply(lambda x: f"${x:,.0f}")
            )
            fig_bars.update_traces(textposition='outside')
            fig_bars.update_layout(
                xaxis_title="Tipo de Transacción",
                yaxis_title="Monto Total ($)",
                showlegend=False,
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)'
            )
            st.plotly_chart(fig_bars, use_container_width=True)
            
            # Métricas adicionales debajo del gráfico
            col1_1, col1_2 = st.columns(2)
            with col1_1:
                income_total = type_data[type_data['Tipo'] == 'Ingreso']['Monto'].iloc[0] if len(type_data[type_data['Tipo'] == 'Ingreso']) > 0 else 0
                st.metric("💰 Total Ingresos", f"${income_total:,.0f}")
            with col1_2:
                expense_total = type_data[type_data['Tipo'] == 'Gasto']['Monto'].iloc[0] if len(type_data[type_data['Tipo'] == 'Gasto']) > 0 else 0
                st.metric("💸 Total Gastos", f"${expense_total:,.0f}")
        
        with col2:
            st.markdown('<h3 class="section-title">📈 Tendencia Mensual</h3>', unsafe_allow_html=True)
            
            # Gráfico de línea de tendencia
            monthly_data = df_transactions.copy()
            monthly_summary = monthly_data.groupby(monthly_data['Fecha'].dt.to_period('M'))['Monto'].sum().reset_index()
            monthly_summary['Fecha'] = monthly_summary['Fecha'].astype(str)
            
            fig_line = px.line(
                monthly_summary, 
                x='Fecha', 
                y='Monto', 
                title=f"Tendencia de Flujo de Caja - {st.session_state.selected_company}",
                markers=True
            )
            fig_line.update_traces(line_color=theme['primary'], marker_color=theme['secondary'])
            fig_line.update_layout(
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)'
            )
            st.plotly_chart(fig_line, use_container_width=True)
        
        # Gráfico de proporción ingresos vs gastos
        st.markdown('<h3 class="section-title">📊 Proporción Ingresos vs Gastos</h3>', unsafe_allow_html=True)
        
        # Crear gráfico de proporción más claro
        proportion_data = pd.DataFrame({
            'Tipo': ['Ingresos', 'Gastos'],
            'Monto': [total_income, total_expenses],
            'Porcentaje': [100, (total_expenses/total_income*100) if total_income > 0 else 0]
        })
        
        col_prop1, col_prop2 = st.columns(2)
        
        with col_prop1:
            # Gráfico de donut para proporción
            fig_donut = go.Figure(data=[go.Pie(
                labels=proportion_data['Tipo'],
                values=proportion_data['Monto'],
                hole=0.6,
                marker_colors=['#10b981', '#ef4444'],
                textinfo='label+percent',
                textposition='inside'
            )])
            
            fig_donut.update_layout(
                title=f"Proporción Ingresos vs Gastos - {st.session_state.selected_company}",
                showlegend=True,
                legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
            )
            st.plotly_chart(fig_donut, use_container_width=True)
        
        with col_prop2:
            # Métricas de proporción
            st.markdown("### 📈 Métricas de Proporción")
            
            # Calcular métricas
            profit_margin_pct = ((total_income - total_expenses) / total_income * 100) if total_income > 0 else 0
            expense_ratio = (total_expenses / total_income * 100) if total_income > 0 else 0
            
            col_met1, col_met2 = st.columns(2)
            with col_met1:
                st.metric("💰 Margen de Ganancia", f"{profit_margin_pct:.1f}%")
                st.metric("📊 Ratio de Gastos", f"{expense_ratio:.1f}%")
            
            with col_met2:
                st.metric("💵 Ingresos Netos", f"${current_balance:,.0f}")
                st.metric("📉 Eficiencia", f"{(1 - expense_ratio/100)*100:.1f}%")
        
        # Gráficos de categorías de gastos
        st.markdown('<h3 class="section-title">📊 Análisis de Categorías de Gastos</h3>', unsafe_allow_html=True)
        
        # Función para categorizar gastos
        def categorize_expense(description):
            description_lower = description.lower()
            if any(word in description_lower for word in ['arriendo', 'oficina', 'rent']):
                return 'Arriendo'
            elif any(word in description_lower for word in ['servicios', 'básicos', 'luz', 'agua', 'gas']):
                return 'Servicios Básicos'
            elif any(word in description_lower for word in ['impuestos', 'tasas', 'gubernamentales']):
                return 'Impuestos'
            elif any(word in description_lower for word in ['equipos', 'computación', 'software', 'audiovisuales']):
                return 'Equipos y Tecnología'
            elif any(word in description_lower for word in ['mantenimiento', 'vehículos', 'seguro']):
                return 'Mantenimiento y Seguros'
            elif any(word in description_lower for word in ['supermercado', 'provisiones', 'alimentación']):
                return 'Alimentación y Provisiones'
            else:
                return 'Otros Gastos'
        
        # Crear DataFrame con categorías
        expenses_df = df_transactions[df_transactions['Monto'] < 0].copy()
        expenses_df['Categoría'] = expenses_df['Descripción'].apply(categorize_expense)
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Gráfico de barras por categorías de gastos (más claro que torta)
            if not expenses_df.empty:
                category_data = expenses_df.groupby('Categoría')['Monto'].sum().reset_index()
                category_data['Monto'] = abs(category_data['Monto'])
                category_data = category_data.sort_values('Monto', ascending=False)  # Ordenar por monto
                
                # Colores para categorías
                colors = ['#ef4444', '#f97316', '#eab308', '#84cc16', '#22c55e', '#06b6d4', '#8b5cf6']
                
                fig_expenses = px.bar(
                    category_data,
                    x='Categoría',
                    y='Monto',
                    title=f"Categorías de Gastos - {st.session_state.selected_company}",
                    color='Categoría',
                    color_discrete_sequence=colors,
                    text=category_data['Monto'].apply(lambda x: f"${x:,.0f}")
                )
                fig_expenses.update_traces(textposition='outside')
                fig_expenses.update_layout(
                    xaxis_title="Categoría",
                    yaxis_title="Monto Total ($)",
                    showlegend=False,
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    xaxis={'tickangle': 45}
                )
                st.plotly_chart(fig_expenses, use_container_width=True)
            else:
                st.info("No hay gastos registrados para mostrar categorías.")
        
        with col2:
            # Gráfico de barras por categorías de gastos
            if not expenses_df.empty:
                category_data = expenses_df.groupby('Categoría')['Monto'].sum().reset_index()
                category_data['Monto'] = abs(category_data['Monto'])
                category_data = category_data.sort_values('Monto', ascending=True)
                
                fig_bars = px.bar(
                    category_data,
                    x='Monto',
                    y='Categoría',
                    orientation='h',
                    title=f"Gastos por Categoría - {st.session_state.selected_company}",
                    color='Monto',
                    color_continuous_scale='Reds'
                )
                fig_bars.update_layout(
                    xaxis_title="Monto ($)",
                    yaxis_title="Categoría",
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)'
                )
                st.plotly_chart(fig_bars, use_container_width=True)
            else:
                st.info("No hay gastos registrados para mostrar gráfico de barras.")
        
        # Estadísticas adicionales
        st.markdown('<h3 class="section-title">📊 Estadísticas Detalladas</h3>', unsafe_allow_html=True)
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            total_transactions = len(df_transactions)
            st.metric("Total Transacciones", f"{total_transactions:,}")
        
        with col2:
            avg_income = df_transactions[df_transactions['Monto'] > 0]['Monto'].mean()
            st.metric("Promedio Ingresos", f"${avg_income:,.0f}")
        
        with col3:
            avg_expense = abs(df_transactions[df_transactions['Monto'] < 0]['Monto'].mean())
            st.metric("Promedio Gastos", f"${avg_expense:,.0f}")
        
        with col4:
            profit_margin = ((total_income - total_expenses) / total_income * 100) if total_income > 0 else 0
            st.metric("Margen de Ganancia", f"{profit_margin:.1f}%")
        
        # Tabla de resumen por categorías
        if not expenses_df.empty:
            st.markdown('<h3 class="section-title">📋 Resumen de Gastos por Categoría</h3>', unsafe_allow_html=True)
            
            summary_data = expenses_df.groupby('Categoría').agg({
                'Monto': ['sum', 'count'],
                'Descripción': lambda x: ', '.join(x.head(3).tolist()) + ('...' if len(x) > 3 else '')
            }).reset_index()
            
            summary_data.columns = ['Categoría', 'Total Gastos', 'Cantidad', 'Ejemplos']
            summary_data['Total Gastos'] = abs(summary_data['Total Gastos'])
            summary_data = summary_data.sort_values('Total Gastos', ascending=False)
            
            # Formatear para display
            display_summary = summary_data.copy()
            display_summary['Total Gastos'] = display_summary['Total Gastos'].apply(lambda x: f"${x:,.0f}")
            
            st.dataframe(display_summary, use_container_width=True)

# Footer mejorado
st.markdown("---")
st.markdown(f"""
<div style="text-align: center; color: #666; padding: 2rem; background: {get_company_theme(st.session_state.selected_company)['light']}; border-radius: 10px; margin-top: 2rem;">
    <p style="font-size: 1.1rem; font-weight: bold; color: {get_company_theme(st.session_state.selected_company)['primary']};">
        Tri-Ledger V2 - Dashboard Financiero Avanzado
    </p>
    <p>Desarrollado con Streamlit y principios de diseño moderno</p>
    <p style="font-size: 0.9rem; margin-top: 1rem;">
        🌟 Versión 2.0 - Tema personalizado para {st.session_state.selected_company}
    </p>
</div>
""", unsafe_allow_html=True) 