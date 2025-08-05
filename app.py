import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import random

# Configuración de la página
st.set_page_config(
    page_title="Tri-Ledger - Dashboard Financiero",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Estilos CSS personalizados
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .company-card {
        background-color: #f8f9fa;
        padding: 1rem;
        border-radius: 10px;
        border-left: 4px solid #1f77b4;
        margin: 0.5rem 0;
        cursor: pointer;
        transition: all 0.3s ease;
        text-align: center;
        font-weight: bold;
    }
    .company-card:hover {
        background-color: #e3f2fd;
        transform: translateY(-2px);
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
    }
    .company-card.selected {
        background-color: #1f77b4;
        color: white;
        border-left: 4px solid #1565c0;
    }
    
    /* Estilos para los botones de empresa */
    .stButton > button {
        background-color: #f8f9fa !important;
        color: #333 !important;
        border: 2px solid #1f77b4 !important;
        border-radius: 10px !important;
        padding: 1rem !important;
        font-weight: bold !important;
        text-align: center !important;
        transition: all 0.3s ease !important;
        width: 100% !important;
        height: auto !important;
        min-height: 60px !important;
    }
    .stButton > button:hover {
        background-color: #e3f2fd !important;
        transform: translateY(-2px) !important;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1) !important;
        border-color: #1565c0 !important;
    }
    .stButton > button:focus {
        background-color: #1f77b4 !important;
        color: white !important;
        border-color: #1565c0 !important;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2) !important;
    }
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1.5rem;
        border-radius: 15px;
        text-align: center;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    .income-card {
        background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%);
        color: white;
        padding: 1.5rem;
        border-radius: 15px;
        text-align: center;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    .expense-card {
        background: linear-gradient(135deg, #ff416c 0%, #ff4b2b 100%);
        color: white;
        padding: 1.5rem;
        border-radius: 15px;
        text-align: center;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    .section-title {
        font-size: 1.5rem;
        font-weight: bold;
        color: #333;
        margin-bottom: 1rem;
    }
    .transaction-table {
        background-color: white;
        border-radius: 10px;
        padding: 1rem;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    }
</style>
""", unsafe_allow_html=True)

# Datos de ejemplo
def generate_sample_data():
    companies = ["W TRAVEL CHILE", "WOLF TRAVEL CHILE", "HELPMETRAVEL SPA"]
    
    # Datos de transacciones - 2 años de datos
    transactions_data = [
        # 2023 - W TRAVEL CHILE
        {"Descripción": "Venta paquete turístico Europa", "Tipo": "Ingreso", "Fecha": "15/01/2023", "Monto": 8500, "Empresa": "W TRAVEL CHILE"},
        {"Descripción": "Pago arriendo oficina", "Tipo": "Gasto", "Fecha": "05/01/2023", "Monto": -1200, "Empresa": "W TRAVEL CHILE"},
        {"Descripción": "Comisión agencia aérea", "Tipo": "Ingreso", "Fecha": "20/01/2023", "Monto": 1200, "Empresa": "W TRAVEL CHILE"},
        {"Descripción": "Compra equipos computación", "Tipo": "Gasto", "Fecha": "25/01/2023", "Monto": -2500, "Empresa": "W TRAVEL CHILE"},
        
        {"Descripción": "Reserva hotel Cancún", "Tipo": "Ingreso", "Fecha": "10/02/2023", "Monto": 3200, "Empresa": "W TRAVEL CHILE"},
        {"Descripción": "Pago servicios básicos", "Tipo": "Gasto", "Fecha": "15/02/2023", "Monto": -450, "Empresa": "W TRAVEL CHILE"},
        {"Descripción": "Venta paquete Disney", "Tipo": "Ingreso", "Fecha": "28/02/2023", "Monto": 6800, "Empresa": "W TRAVEL CHILE"},
        
        {"Descripción": "Comisión crucero Caribe", "Tipo": "Ingreso", "Fecha": "12/03/2023", "Monto": 1800, "Empresa": "W TRAVEL CHILE"},
        {"Descripción": "Mantenimiento equipos", "Tipo": "Gasto", "Fecha": "20/03/2023", "Monto": -800, "Empresa": "W TRAVEL CHILE"},
        {"Descripción": "Venta paquete Asia", "Tipo": "Ingreso", "Fecha": "30/03/2023", "Monto": 12500, "Empresa": "W TRAVEL CHILE"},
        
        {"Descripción": "Pago impuestos", "Tipo": "Gasto", "Fecha": "15/04/2023", "Monto": -3500, "Empresa": "W TRAVEL CHILE"},
        {"Descripción": "Comisión hotel premium", "Tipo": "Ingreso", "Fecha": "22/04/2023", "Monto": 950, "Empresa": "W TRAVEL CHILE"},
        {"Descripción": "Venta paquete Sudamérica", "Tipo": "Ingreso", "Fecha": "28/04/2023", "Monto": 4200, "Empresa": "W TRAVEL CHILE"},
        
        {"Descripción": "Pago arriendo oficina", "Tipo": "Gasto", "Fecha": "05/05/2023", "Monto": -1200, "Empresa": "W TRAVEL CHILE"},
        {"Descripción": "Venta paquete Europa", "Tipo": "Ingreso", "Fecha": "18/05/2023", "Monto": 9200, "Empresa": "W TRAVEL CHILE"},
        {"Descripción": "Compra software gestión", "Tipo": "Gasto", "Fecha": "25/05/2023", "Monto": -1800, "Empresa": "W TRAVEL CHILE"},
        
        {"Descripción": "Comisión agencia aérea", "Tipo": "Ingreso", "Fecha": "08/06/2023", "Monto": 2100, "Empresa": "W TRAVEL CHILE"},
        {"Descripción": "Pago servicios básicos", "Tipo": "Gasto", "Fecha": "15/06/2023", "Monto": -450, "Empresa": "W TRAVEL CHILE"},
        {"Descripción": "Venta paquete Australia", "Tipo": "Ingreso", "Fecha": "30/06/2023", "Monto": 15800, "Empresa": "W TRAVEL CHILE"},
        
        # 2023 - WOLF TRAVEL CHILE
        {"Descripción": "Venta paquete aventura", "Tipo": "Ingreso", "Fecha": "12/01/2023", "Monto": 4200, "Empresa": "WOLF TRAVEL CHILE"},
        {"Descripción": "Compra equipos outdoor", "Tipo": "Gasto", "Fecha": "18/01/2023", "Monto": -3200, "Empresa": "WOLF TRAVEL CHILE"},
        {"Descripción": "Comisión tour guiado", "Tipo": "Ingreso", "Fecha": "25/01/2023", "Monto": 800, "Empresa": "WOLF TRAVEL CHILE"},
        
        {"Descripción": "Venta paquete montaña", "Tipo": "Ingreso", "Fecha": "08/02/2023", "Monto": 2800, "Empresa": "WOLF TRAVEL CHILE"},
        {"Descripción": "Pago seguro equipos", "Tipo": "Gasto", "Fecha": "20/02/2023", "Monto": -650, "Empresa": "WOLF TRAVEL CHILE"},
        {"Descripción": "Comisión alojamiento", "Tipo": "Ingreso", "Fecha": "28/02/2023", "Monto": 1200, "Empresa": "WOLF TRAVEL CHILE"},
        
        {"Descripción": "Venta paquete kayak", "Tipo": "Ingreso", "Fecha": "15/03/2023", "Monto": 1800, "Empresa": "WOLF TRAVEL CHILE"},
        {"Descripción": "Mantenimiento vehículos", "Tipo": "Gasto", "Fecha": "22/03/2023", "Monto": -1500, "Empresa": "WOLF TRAVEL CHILE"},
        {"Descripción": "Comisión transporte", "Tipo": "Ingreso", "Fecha": "30/03/2023", "Monto": 950, "Empresa": "WOLF TRAVEL CHILE"},
        
        {"Descripción": "Venta paquete trekking", "Tipo": "Ingreso", "Fecha": "10/04/2023", "Monto": 3500, "Empresa": "WOLF TRAVEL CHILE"},
        {"Descripción": "Pago impuestos", "Tipo": "Gasto", "Fecha": "15/04/2023", "Monto": -2800, "Empresa": "WOLF TRAVEL CHILE"},
        {"Descripción": "Comisión guía local", "Tipo": "Ingreso", "Fecha": "25/04/2023", "Monto": 600, "Empresa": "WOLF TRAVEL CHILE"},
        
        {"Descripción": "Venta paquete escalada", "Tipo": "Ingreso", "Fecha": "05/05/2023", "Monto": 5200, "Empresa": "WOLF TRAVEL CHILE"},
        {"Descripción": "Compra equipos seguridad", "Tipo": "Gasto", "Fecha": "18/05/2023", "Monto": -4200, "Empresa": "WOLF TRAVEL CHILE"},
        {"Descripción": "Comisión alojamiento", "Tipo": "Ingreso", "Fecha": "28/05/2023", "Monto": 1400, "Empresa": "WOLF TRAVEL CHILE"},
        
        {"Descripción": "Venta paquete rafting", "Tipo": "Ingreso", "Fecha": "12/06/2023", "Monto": 2200, "Empresa": "WOLF TRAVEL CHILE"},
        {"Descripción": "Pago servicios básicos", "Tipo": "Gasto", "Fecha": "20/06/2023", "Monto": -380, "Empresa": "WOLF TRAVEL CHILE"},
        {"Descripción": "Comisión transporte", "Tipo": "Ingreso", "Fecha": "30/06/2023", "Monto": 1100, "Empresa": "WOLF TRAVEL CHILE"},
        
        # 2023 - HELPMETRAVEL SPA
        {"Descripción": "Venta paquete corporativo", "Tipo": "Ingreso", "Fecha": "20/01/2023", "Monto": 15000, "Empresa": "HELPMETRAVEL SPA"},
        {"Descripción": "Pago arriendo oficina", "Tipo": "Gasto", "Fecha": "25/01/2023", "Monto": -1800, "Empresa": "HELPMETRAVEL SPA"},
        {"Descripción": "Comisión evento empresarial", "Tipo": "Ingreso", "Fecha": "30/01/2023", "Monto": 3200, "Empresa": "HELPMETRAVEL SPA"},
        
        {"Descripción": "Venta paquete incentivo", "Tipo": "Ingreso", "Fecha": "15/02/2023", "Monto": 8500, "Empresa": "HELPMETRAVEL SPA"},
        {"Descripción": "Compra equipos presentación", "Tipo": "Gasto", "Fecha": "22/02/2023", "Monto": -2800, "Empresa": "HELPMETRAVEL SPA"},
        {"Descripción": "Comisión conferencia", "Tipo": "Ingreso", "Fecha": "28/02/2023", "Monto": 1800, "Empresa": "HELPMETRAVEL SPA"},
        
        {"Descripción": "Venta paquete capacitación", "Tipo": "Ingreso", "Fecha": "10/03/2023", "Monto": 12000, "Empresa": "HELPMETRAVEL SPA"},
        {"Descripción": "Pago servicios básicos", "Tipo": "Gasto", "Fecha": "20/03/2023", "Monto": -650, "Empresa": "HELPMETRAVEL SPA"},
        {"Descripción": "Comisión seminario", "Tipo": "Ingreso", "Fecha": "30/03/2023", "Monto": 2500, "Empresa": "HELPMETRAVEL SPA"},
        
        {"Descripción": "Venta paquete team building", "Tipo": "Ingreso", "Fecha": "12/04/2023", "Monto": 6800, "Empresa": "HELPMETRAVEL SPA"},
        {"Descripción": "Pago impuestos", "Tipo": "Gasto", "Fecha": "15/04/2023", "Monto": -4200, "Empresa": "HELPMETRAVEL SPA"},
        {"Descripción": "Comisión retiro empresarial", "Tipo": "Ingreso", "Fecha": "25/04/2023", "Monto": 1900, "Empresa": "HELPMETRAVEL SPA"},
        
        {"Descripción": "Venta paquete convención", "Tipo": "Ingreso", "Fecha": "08/05/2023", "Monto": 22000, "Empresa": "HELPMETRAVEL SPA"},
        {"Descripción": "Compra equipos audiovisuales", "Tipo": "Gasto", "Fecha": "18/05/2023", "Monto": -8500, "Empresa": "HELPMETRAVEL SPA"},
        {"Descripción": "Comisión evento internacional", "Tipo": "Ingreso", "Fecha": "28/05/2023", "Monto": 4500, "Empresa": "HELPMETRAVEL SPA"},
        
        {"Descripción": "Venta paquete networking", "Tipo": "Ingreso", "Fecha": "15/06/2023", "Monto": 9500, "Empresa": "HELPMETRAVEL SPA"},
        {"Descripción": "Pago arriendo oficina", "Tipo": "Gasto", "Fecha": "25/06/2023", "Monto": -1800, "Empresa": "HELPMETRAVEL SPA"},
        {"Descripción": "Comisión workshop", "Tipo": "Ingreso", "Fecha": "30/06/2023", "Monto": 2800, "Empresa": "HELPMETRAVEL SPA"},
        
        # 2024 - W TRAVEL CHILE
        {"Descripción": "Venta paquete verano", "Tipo": "Ingreso", "Fecha": "10/01/2024", "Monto": 7200, "Empresa": "W TRAVEL CHILE"},
        {"Descripción": "Pago arriendo oficina", "Tipo": "Gasto", "Fecha": "05/01/2024", "Monto": -1200, "Empresa": "W TRAVEL CHILE"},
        {"Descripción": "Comisión agencia aérea", "Tipo": "Ingreso", "Fecha": "18/01/2024", "Monto": 1500, "Empresa": "W TRAVEL CHILE"},
        
        {"Descripción": "Venta paquete carnaval", "Tipo": "Ingreso", "Fecha": "25/02/2024", "Monto": 5800, "Empresa": "W TRAVEL CHILE"},
        {"Descripción": "Pago servicios básicos", "Tipo": "Gasto", "Fecha": "15/02/2024", "Monto": -450, "Empresa": "W TRAVEL CHILE"},
        {"Descripción": "Compra equipos computación", "Tipo": "Gasto", "Fecha": "28/02/2024", "Monto": -3200, "Empresa": "W TRAVEL CHILE"},
        
        {"Descripción": "Venta paquete primavera", "Tipo": "Ingreso", "Fecha": "15/03/2024", "Monto": 6800, "Empresa": "W TRAVEL CHILE"},
        {"Descripción": "Mantenimiento equipos", "Tipo": "Gasto", "Fecha": "20/03/2024", "Monto": -800, "Empresa": "W TRAVEL CHILE"},
        {"Descripción": "Comisión hotel premium", "Tipo": "Ingreso", "Fecha": "30/03/2024", "Monto": 1200, "Empresa": "W TRAVEL CHILE"},
        
        {"Descripción": "Venta paquete otoño", "Tipo": "Ingreso", "Fecha": "10/04/2024", "Monto": 5200, "Empresa": "W TRAVEL CHILE"},
        {"Descripción": "Pago impuestos", "Tipo": "Gasto", "Fecha": "15/04/2024", "Monto": -3800, "Empresa": "W TRAVEL CHILE"},
        {"Descripción": "Comisión crucero", "Tipo": "Ingreso", "Fecha": "25/04/2024", "Monto": 2100, "Empresa": "W TRAVEL CHILE"},
        
        {"Descripción": "Venta paquete invierno", "Tipo": "Ingreso", "Fecha": "05/05/2024", "Monto": 8900, "Empresa": "W TRAVEL CHILE"},
        {"Descripción": "Pago arriendo oficina", "Tipo": "Gasto", "Fecha": "05/05/2024", "Monto": -1200, "Empresa": "W TRAVEL CHILE"},
        {"Descripción": "Compra software gestión", "Tipo": "Gasto", "Fecha": "18/05/2024", "Monto": -2200, "Empresa": "W TRAVEL CHILE"},
        
        {"Descripción": "Venta paquete navidad", "Tipo": "Ingreso", "Fecha": "12/06/2024", "Monto": 15800, "Empresa": "W TRAVEL CHILE"},
        {"Descripción": "Pago servicios básicos", "Tipo": "Gasto", "Fecha": "15/06/2024", "Monto": -450, "Empresa": "W TRAVEL CHILE"},
        {"Descripción": "Comisión agencia aérea", "Tipo": "Ingreso", "Fecha": "30/06/2024", "Monto": 2800, "Empresa": "W TRAVEL CHILE"},
        
        # 2024 - WOLF TRAVEL CHILE
        {"Descripción": "Venta paquete aventura", "Tipo": "Ingreso", "Fecha": "08/01/2024", "Monto": 3800, "Empresa": "WOLF TRAVEL CHILE"},
        {"Descripción": "Compra equipos outdoor", "Tipo": "Gasto", "Fecha": "15/01/2024", "Monto": -2800, "Empresa": "WOLF TRAVEL CHILE"},
        {"Descripción": "Comisión tour guiado", "Tipo": "Ingreso", "Fecha": "22/01/2024", "Monto": 900, "Empresa": "WOLF TRAVEL CHILE"},
        
        {"Descripción": "Venta paquete montaña", "Tipo": "Ingreso", "Fecha": "12/02/2024", "Monto": 3200, "Empresa": "WOLF TRAVEL CHILE"},
        {"Descripción": "Pago seguro equipos", "Tipo": "Gasto", "Fecha": "20/02/2024", "Monto": -750, "Empresa": "WOLF TRAVEL CHILE"},
        {"Descripción": "Comisión alojamiento", "Tipo": "Ingreso", "Fecha": "28/02/2024", "Monto": 1400, "Empresa": "WOLF TRAVEL CHILE"},
        
        {"Descripción": "Venta paquete kayak", "Tipo": "Ingreso", "Fecha": "18/03/2024", "Monto": 2100, "Empresa": "WOLF TRAVEL CHILE"},
        {"Descripción": "Mantenimiento vehículos", "Tipo": "Gasto", "Fecha": "25/03/2024", "Monto": -1800, "Empresa": "WOLF TRAVEL CHILE"},
        {"Descripción": "Comisión transporte", "Tipo": "Ingreso", "Fecha": "30/03/2024", "Monto": 1100, "Empresa": "WOLF TRAVEL CHILE"},
        
        {"Descripción": "Venta paquete trekking", "Tipo": "Ingreso", "Fecha": "15/04/2024", "Monto": 4200, "Empresa": "WOLF TRAVEL CHILE"},
        {"Descripción": "Pago impuestos", "Tipo": "Gasto", "Fecha": "15/04/2024", "Monto": -3200, "Empresa": "WOLF TRAVEL CHILE"},
        {"Descripción": "Comisión guía local", "Tipo": "Ingreso", "Fecha": "25/04/2024", "Monto": 700, "Empresa": "WOLF TRAVEL CHILE"},
        
        {"Descripción": "Venta paquete escalada", "Tipo": "Ingreso", "Fecha": "08/05/2024", "Monto": 6800, "Empresa": "WOLF TRAVEL CHILE"},
        {"Descripción": "Compra equipos seguridad", "Tipo": "Gasto", "Fecha": "18/05/2024", "Monto": -5200, "Empresa": "WOLF TRAVEL CHILE"},
        {"Descripción": "Comisión alojamiento", "Tipo": "Ingreso", "Fecha": "28/05/2024", "Monto": 1600, "Empresa": "WOLF TRAVEL CHILE"},
        
        {"Descripción": "Venta paquete rafting", "Tipo": "Ingreso", "Fecha": "15/06/2024", "Monto": 2800, "Empresa": "WOLF TRAVEL CHILE"},
        {"Descripción": "Pago servicios básicos", "Tipo": "Gasto", "Fecha": "20/06/2024", "Monto": -420, "Empresa": "WOLF TRAVEL CHILE"},
        {"Descripción": "Comisión transporte", "Tipo": "Ingreso", "Fecha": "30/06/2024", "Monto": 1300, "Empresa": "WOLF TRAVEL CHILE"},
        
        # 2024 - HELPMETRAVEL SPA
        {"Descripción": "Venta paquete corporativo", "Tipo": "Ingreso", "Fecha": "25/01/2024", "Monto": 18000, "Empresa": "HELPMETRAVEL SPA"},
        {"Descripción": "Pago arriendo oficina", "Tipo": "Gasto", "Fecha": "25/01/2024", "Monto": -1800, "Empresa": "HELPMETRAVEL SPA"},
        {"Descripción": "Comisión evento empresarial", "Tipo": "Ingreso", "Fecha": "30/01/2024", "Monto": 3800, "Empresa": "HELPMETRAVEL SPA"},
        
        {"Descripción": "Venta paquete incentivo", "Tipo": "Ingreso", "Fecha": "18/02/2024", "Monto": 9500, "Empresa": "HELPMETRAVEL SPA"},
        {"Descripción": "Compra equipos presentación", "Tipo": "Gasto", "Fecha": "25/02/2024", "Monto": -3200, "Empresa": "HELPMETRAVEL SPA"},
        {"Descripción": "Comisión conferencia", "Tipo": "Ingreso", "Fecha": "28/02/2024", "Monto": 2100, "Empresa": "HELPMETRAVEL SPA"},
        
        {"Descripción": "Venta paquete capacitación", "Tipo": "Ingreso", "Fecha": "12/03/2024", "Monto": 14000, "Empresa": "HELPMETRAVEL SPA"},
        {"Descripción": "Pago servicios básicos", "Tipo": "Gasto", "Fecha": "20/03/2024", "Monto": -750, "Empresa": "HELPMETRAVEL SPA"},
        {"Descripción": "Comisión seminario", "Tipo": "Ingreso", "Fecha": "30/03/2024", "Monto": 2900, "Empresa": "HELPMETRAVEL SPA"},
        
        {"Descripción": "Venta paquete team building", "Tipo": "Ingreso", "Fecha": "15/04/2024", "Monto": 7800, "Empresa": "HELPMETRAVEL SPA"},
        {"Descripción": "Pago impuestos", "Tipo": "Gasto", "Fecha": "15/04/2024", "Monto": -4800, "Empresa": "HELPMETRAVEL SPA"},
        {"Descripción": "Comisión retiro empresarial", "Tipo": "Ingreso", "Fecha": "25/04/2024", "Monto": 2200, "Empresa": "HELPMETRAVEL SPA"},
        
        {"Descripción": "Venta paquete convención", "Tipo": "Ingreso", "Fecha": "10/05/2024", "Monto": 25000, "Empresa": "HELPMETRAVEL SPA"},
        {"Descripción": "Compra equipos audiovisuales", "Tipo": "Gasto", "Fecha": "18/05/2024", "Monto": -9500, "Empresa": "HELPMETRAVEL SPA"},
        {"Descripción": "Comisión evento internacional", "Tipo": "Ingreso", "Fecha": "28/05/2024", "Monto": 5200, "Empresa": "HELPMETRAVEL SPA"},
        
        {"Descripción": "Venta paquete networking", "Tipo": "Ingreso", "Fecha": "18/06/2024", "Monto": 11000, "Empresa": "HELPMETRAVEL SPA"},
        {"Descripción": "Pago arriendo oficina", "Tipo": "Gasto", "Fecha": "25/06/2024", "Monto": -1800, "Empresa": "HELPMETRAVEL SPA"},
        {"Descripción": "Comisión workshop", "Tipo": "Ingreso", "Fecha": "30/06/2024", "Monto": 3200, "Empresa": "HELPMETRAVEL SPA"},
        
        # Datos recientes (Julio 2024) - Para mostrar en el dashboard actual
        {"Descripción": "Pago de cliente #1", "Tipo": "Ingreso", "Fecha": "15/07/2024", "Monto": 3500, "Empresa": "W TRAVEL CHILE"},
        {"Descripción": "Compra de Tasas Gubernamentales", "Tipo": "Gasto", "Fecha": "15/07/2024", "Monto": -120, "Empresa": "W TRAVEL CHILE"},
        {"Descripción": "Supermercado - Provisiones", "Tipo": "Gasto", "Fecha": "14/07/2024", "Monto": -150, "Empresa": "W TRAVEL CHILE"},
        {"Descripción": "Venta de paquete turístico", "Tipo": "Ingreso", "Fecha": "13/07/2024", "Monto": 2800, "Empresa": "WOLF TRAVEL CHILE"},
        {"Descripción": "Pago de servicios básicos", "Tipo": "Gasto", "Fecha": "12/07/2024", "Monto": -200, "Empresa": "HELPMETRAVEL SPA"},
        {"Descripción": "Comisión por reserva", "Tipo": "Ingreso", "Fecha": "11/07/2024", "Monto": 450, "Empresa": "W TRAVEL CHILE"},
        {"Descripción": "Mantenimiento de equipos", "Tipo": "Gasto", "Fecha": "10/07/2024", "Monto": -300, "Empresa": "WOLF TRAVEL CHILE"},
    ]
    
    return companies, transactions_data

# Generar datos
companies, transactions_data = generate_sample_data()
df_transactions = pd.DataFrame(transactions_data)

# Inicializar session state para empresa seleccionada
if 'selected_company' not in st.session_state:
    st.session_state.selected_company = companies[0]  # Seleccionar la primera empresa por defecto

# Función para filtrar datos por empresa
def filter_data_by_company(df, company):
    return df[df['Empresa'] == company]

# Filtrar datos por empresa seleccionada
filtered_df = filter_data_by_company(df_transactions, st.session_state.selected_company)

# Cálculos financieros
total_income = filtered_df[filtered_df['Monto'] > 0]['Monto'].sum()
total_expenses = abs(filtered_df[filtered_df['Monto'] < 0]['Monto'].sum())
current_balance = total_income - total_expenses

# Sidebar
with st.sidebar:
    st.markdown('<h1 style="color: #1f77b4; font-size: 2rem;">Tri-Ledger</h1>', unsafe_allow_html=True)
    
    # Navegación
    st.markdown("### Navegación")
    page = st.radio("Seleccionar página", ["Dashboard", "Transacciones", "Reportes"], label_visibility="collapsed")
    
    # Filtros
    st.markdown("### Filtros")
    selected_company = st.selectbox("Empresa", companies)
    date_range = st.date_input(
        "Rango de fechas",
        value=(datetime.now() - timedelta(days=30), datetime.now()),
        max_value=datetime.now()
    )

# Contenido principal
if page == "Dashboard":
    # Header
    st.markdown('<h1 class="main-header">Dashboard Financiero</h1>', unsafe_allow_html=True)
    
    # Mostrar empresa seleccionada
    st.markdown(f'<h3 style="text-align: center; color: #1f77b4; margin-bottom: 1rem;">📊 Datos de: {st.session_state.selected_company}</h3>', unsafe_allow_html=True)
    
    # Empresas clickables
    st.markdown("### Empresas")
    st.markdown("Haz clic en una empresa para ver sus datos específicos:")
    
    # Indicador de empresa seleccionada
    st.markdown(f'<div style="background-color: #e3f2fd; padding: 0.5rem; border-radius: 5px; margin-bottom: 1rem; text-align: center; border-left: 4px solid #1f77b4;"><strong>📊 Empresa activa: {st.session_state.selected_company}</strong></div>', unsafe_allow_html=True)
    
    cols = st.columns(len(companies))
    
    # Tarjetas para cada empresa
    for i, company in enumerate(companies):
        with cols[i]:
            if st.button(company, key=f"btn_{i}", use_container_width=True):
                st.session_state.selected_company = company
    
    # Métricas principales
    st.markdown("### Resumen Financiero")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown(f'''
        <div class="metric-card">
            <h3>💰 Saldo Actual</h3>
            <h2>${current_balance:,.0f}</h2>
            <p>Basado en todas las transacciones</p>
        </div>
        ''', unsafe_allow_html=True)
    
    with col2:
        st.markdown(f'''
        <div class="income-card">
            <h3>📈 Ingresos Totales</h3>
            <h2>${total_income:,.0f}</h2>
            <p>Este mes</p>
        </div>
        ''', unsafe_allow_html=True)
    
    with col3:
        st.markdown(f'''
        <div class="expense-card">
            <h3>📉 Gastos Totales</h3>
            <h2>${total_expenses:,.0f}</h2>
            <p>Este mes</p>
        </div>
        ''', unsafe_allow_html=True)
    
    # Gráficos y tablas
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown('<h3 class="section-title">Ingresos vs. Gastos (Últimos 7 días)</h3>', unsafe_allow_html=True)
        st.markdown("Un resumen visual de tu flujo de caja.")
        
        # Gráfico de ingresos vs gastos usando datos reales
        fig = go.Figure()
        
        # Procesar datos reales de las transacciones para los últimos 7 días
        recent_data = filtered_df.copy()
        recent_data['Fecha'] = pd.to_datetime(recent_data['Fecha'], format='%d/%m/%Y')
        
        # Obtener las fechas de los últimos 7 días
        end_date = datetime.now()
        start_date = end_date - timedelta(days=6)
        
        # Crear rango de fechas
        date_range = pd.date_range(start=start_date, end=end_date, freq='D')
        
        # Agrupar datos por fecha
        daily_income = []
        daily_expenses = []
        dates_formatted = []
        
        for date in date_range:
            date_str = date.strftime('%d/%m')
            dates_formatted.append(date_str)
            
            # Filtrar transacciones para esta fecha
            day_data = recent_data[recent_data['Fecha'].dt.date == date.date()]
            
            # Calcular ingresos y gastos del día
            day_income = day_data[day_data['Monto'] > 0]['Monto'].sum()
            day_expenses = abs(day_data[day_data['Monto'] < 0]['Monto'].sum())
            
            daily_income.append(day_income)
            daily_expenses.append(day_expenses)
        
        fig.add_trace(go.Bar(
            name='Ingresos',
            x=dates_formatted,
            y=daily_income,
            marker_color='#11998e'
        ))
        
        fig.add_trace(go.Bar(
            name='Gastos',
            x=dates_formatted,
            y=daily_expenses,
            marker_color='#ff416c'
        ))
        
        fig.update_layout(
            title="Flujo de Caja - Últimos 7 días",
            xaxis_title="Fecha",
            yaxis_title="Monto ($)",
            barmode='group',
            height=400
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.markdown('<h3 class="section-title">Transacciones Recientes</h3>', unsafe_allow_html=True)
        st.markdown("Una lista de tus transacciones más recientes.")
        
        # Tabla de transacciones
        st.markdown('<div class="transaction-table">', unsafe_allow_html=True)
        
        # Crear tabla con formato
        for _, row in filtered_df.head(5).iterrows():
            amount_color = "green" if row['Monto'] > 0 else "red"
            amount_sign = "+" if row['Monto'] > 0 else ""
            type_color = "#4CAF50" if row['Tipo'] == "Ingreso" else "#9E9E9E"
            
            col1, col2, col3, col4 = st.columns([3, 1, 1, 1])
            
            with col1:
                st.write(f"**{row['Descripción']}**")
            with col2:
                st.markdown(f'<span style="background-color: {type_color}; color: white; padding: 2px 8px; border-radius: 12px; font-size: 0.8em;">{row["Tipo"]}</span>', unsafe_allow_html=True)
            with col3:
                st.write(row['Fecha'])
            with col4:
                st.markdown(f'<span style="color: {amount_color}; font-weight: bold;">{amount_sign}${abs(row["Monto"]):,.0f}</span>', unsafe_allow_html=True)
            
            st.markdown("---")
        
        st.markdown('</div>', unsafe_allow_html=True)

elif page == "Transacciones":
    st.markdown('<h1 class="main-header">Gestión de Transacciones</h1>', unsafe_allow_html=True)
    
    # Formulario para nueva transacción
    with st.expander("➕ Agregar Nueva Transacción", expanded=False):
        col1, col2 = st.columns(2)
        
        with col1:
            description = st.text_input("Descripción")
            transaction_type = st.selectbox("Tipo", ["Ingreso", "Gasto"])
            company = st.selectbox("Empresa", companies)
        
        with col2:
            amount = st.number_input("Monto", min_value=0.0, value=0.0, step=0.01)
            date = st.date_input("Fecha", value=datetime.now())
        
        if st.button("Guardar Transacción"):
            st.success("Transacción guardada exitosamente!")
    
    # Tabla completa de transacciones
    st.markdown('<h3 class="section-title">Transacciones</h3>', unsafe_allow_html=True)
    st.markdown(f'<p style="color: #666;">Mostrando transacciones de: <strong>{st.session_state.selected_company}</strong></p>', unsafe_allow_html=True)
    st.dataframe(filtered_df, use_container_width=True)

elif page == "Reportes":
    st.markdown('<h1 class="main-header">Reportes Financieros</h1>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown('<h3 class="section-title">Análisis por Empresa</h3>', unsafe_allow_html=True)
        
        # Gráfico de torta por empresa
        # Mostrar distribución por tipo de transacción para la empresa seleccionada
        type_data = filtered_df.groupby('Tipo')['Monto'].sum().reset_index()
        fig_pie = px.pie(type_data, values='Monto', names='Tipo', title=f"Distribución por Tipo - {st.session_state.selected_company}")
        st.plotly_chart(fig_pie, use_container_width=True)
    
    with col2:
        st.markdown('<h3 class="section-title">Tendencia Mensual</h3>', unsafe_allow_html=True)
        
        # Gráfico de línea de tendencia
        monthly_data = filtered_df.copy()
        monthly_data['Fecha'] = pd.to_datetime(monthly_data['Fecha'], format='%d/%m/%Y')
        monthly_summary = monthly_data.groupby(monthly_data['Fecha'].dt.to_period('M'))['Monto'].sum().reset_index()
        monthly_summary['Fecha'] = monthly_summary['Fecha'].astype(str)
        
        title = f"Tendencia de Flujo de Caja - {st.session_state.selected_company}"
        
        fig_line = px.line(monthly_summary, x='Fecha', y='Monto', title=title)
        st.plotly_chart(fig_line, use_container_width=True)

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666; padding: 1rem;">
    <p>Tri-Ledger Dashboard - Sistema de Gestión Financiera</p>
    <p>Desarrollado con Streamlit</p>
</div>
""", unsafe_allow_html=True) 