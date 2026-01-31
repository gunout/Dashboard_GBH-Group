# Dashboard.py - Édition Futuriste Neon CORRIGÉE
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import streamlit as st
from datetime import datetime, timedelta
import warnings
import time
warnings.filterwarnings('ignore')

# ========== CONFIGURATION FUTURISTE ==========
NEON_BLUE = '#00f3ff'
NEON_CYAN = '#00fff9'
NEON_PURPLE = '#b967ff'
NEON_PINK = '#ff00ff'
NEON_GREEN = '#00ff9d'
NEON_YELLOW = '#fff000'

COLORS = {
    'background': '#0a0e17',
    'card_bg': '#0d1220',
    'card_border': '#1a2234',
    'text_primary': '#ffffff',
    'text_secondary': '#8a94a6',
    'text_neon': NEON_BLUE,
    
    'gradient_start': '#0066ff',
    'gradient_mid': '#00f3ff',
    'gradient_end': '#b967ff',
    
    'success': NEON_GREEN,
    'warning': NEON_YELLOW,
    'danger': NEON_PINK,
    'info': NEON_CYAN,
    'primary': NEON_BLUE,
    'accent': NEON_PURPLE,
    
    'drom': '#ff4d94',
    'com': '#ffcc00',
    'metro': '#00e6ff'
}

# ========== CONFIGURATION STREAMLIT ==========
st.set_page_config(
    page_title="GBH Group | Dashboard Futuriste",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ========== STYLES CSS ANIMÉS ==========
st.markdown(f"""
<style>
@keyframes glow {{
    0%, 100% {{ 
        box-shadow: 0 0 10px {NEON_BLUE}, 0 0 20px {NEON_BLUE}, 0 0 30px {NEON_BLUE};
    }}
    50% {{ 
        box-shadow: 0 0 20px {NEON_CYAN}, 0 0 40px {NEON_CYAN}, 0 0 60px {NEON_CYAN};
    }}
}}

@keyframes pulse {{
    0%, 100% {{ opacity: 1; }}
    50% {{ opacity: 0.7; }}
}}

@keyframes slideIn {{
    from {{ transform: translateX(-20px); opacity: 0; }}
    to {{ transform: translateX(0); opacity: 1; }}
}}

@keyframes textGlow {{
    0%, 100% {{ 
        text-shadow: 0 0 5px {NEON_BLUE}, 0 0 10px {NEON_BLUE};
        color: {NEON_BLUE};
    }}
    50% {{ 
        text-shadow: 0 0 10px {NEON_CYAN}, 0 0 20px {NEON_CYAN};
        color: {NEON_CYAN};
    }}
}}

.stApp {{
    background: linear-gradient(135deg, #0a0e17 0%, #0d1220 50%, #0a0e17 100%);
    background-attachment: fixed;
    color: {COLORS['text_primary']};
    font-family: 'Segoe UI', 'Roboto', 'Arial', sans-serif;
}}

.main-header {{
    background: linear-gradient(135deg, {COLORS['gradient_start']} 0%, {COLORS['gradient_mid']} 50%, {COLORS['gradient_end']} 100%);
    background-size: 200% 200%;
    animation: gradientShift 5s ease infinite;
    border-radius: 20px;
    padding: 40px;
    margin-bottom: 40px;
    position: relative;
    overflow: hidden;
    box-shadow: 0 20px 40px rgba(0, 243, 255, 0.2);
    border: 2px solid {NEON_BLUE};
}}

@keyframes gradientShift {{
    0% {{ background-position: 0% 50%; }}
    50% {{ background-position: 100% 50%; }}
    100% {{ background-position: 0% 50%; }}
}}

.metric-card {{
    background: {COLORS['card_bg']};
    border: 1px solid {COLORS['card_border']};
    border-radius: 15px;
    padding: 25px;
    position: relative;
    overflow: hidden;
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    animation: slideIn 0.6s ease-out;
}}

.metric-card:hover {{
    transform: translateY(-10px) scale(1.02);
    border-color: {NEON_BLUE};
    box-shadow: 0 15px 30px rgba(0, 243, 255, 0.3),
                0 0 20px rgba(0, 243, 255, 0.2);
}}

.stButton > button {{
    background: linear-gradient(135deg, {COLORS['gradient_start']}, {COLORS['gradient_end']});
    color: white !important;
    border: none;
    border-radius: 10px;
    padding: 12px 24px;
    font-weight: 600;
    font-size: 16px;
    transition: all 0.3s ease;
    position: relative;
    overflow: hidden;
    text-transform: uppercase;
    letter-spacing: 1px;
}}

.stButton > button:hover {{
    transform: translateY(-3px);
    box-shadow: 0 10px 20px rgba(0, 243, 255, 0.4),
                0 0 30px rgba(0, 243, 255, 0.3);
}}

.stRadio > div {{
    background: rgba(13, 18, 32, 0.8);
    border: 1px solid {COLORS['card_border']};
    border-radius: 12px;
    padding: 10px;
}}

.stRadio > div > label {{
    color: {COLORS['text_secondary']};
    font-weight: 500;
    transition: all 0.3s ease;
    padding: 8px 16px;
    border-radius: 8px;
}}

.stRadio > div > label:hover {{
    color: {NEON_BLUE};
    background: rgba(0, 243, 255, 0.1);
}}

.neon-title {{
    animation: textGlow 3s infinite;
    font-weight: 800;
    letter-spacing: 1px;
    margin-bottom: 30px;
    position: relative;
    display: inline-block;
}}

.neon-title::after {{
    content: '';
    position: absolute;
    bottom: -10px;
    left: 0;
    width: 100%;
    height: 3px;
    background: linear-gradient(90deg, {NEON_BLUE}, {NEON_CYAN}, {NEON_BLUE});
    background-size: 200% 100%;
    animation: gradientShift 3s infinite;
    border-radius: 2px;
}}

.data-card {{
    background: linear-gradient(135deg, 
        rgba(13, 18, 32, 0.9) 0%,
        rgba(26, 34, 52, 0.7) 100%);
    border: 1px solid rgba(0, 243, 255, 0.3);
    border-radius: 15px;
    padding: 25px;
    position: relative;
    overflow: hidden;
}}

::-webkit-scrollbar {{
    width: 10px;
}}

::-webkit-scrollbar-track {{
    background: {COLORS['card_bg']};
    border-radius: 5px;
}}

::-webkit-scrollbar-thumb {{
    background: linear-gradient({NEON_BLUE}, {NEON_CYAN});
    border-radius: 5px;
}}

.marquee {{
    white-space: nowrap;
    overflow: hidden;
    position: relative;
    background: linear-gradient(90deg, transparent, {COLORS['card_bg']} 20%, {COLORS['card_bg']} 80%, transparent);
    padding: 15px 0;
    margin: 20px 0;
    border-top: 1px solid rgba(0, 243, 255, 0.3);
    border-bottom: 1px solid rgba(0, 243, 255, 0.3);
}}

.marquee-content {{
    display: inline-block;
    animation: marquee 30s linear infinite;
    padding-left: 100%;
}}

@keyframes marquee {{
    0% {{ transform: translateX(0); }}
    100% {{ transform: translateX(-100%); }}
}}

.neon-badge {{
    display: inline-block;
    padding: 5px 15px;
    background: rgba(0, 243, 255, 0.1);
    border: 1px solid {NEON_BLUE};
    border-radius: 20px;
    color: {NEON_BLUE};
    font-size: 12px;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 1px;
}}
</style>
""", unsafe_allow_html=True)

# ========== FONCTIONS DE GÉNÉRATION DE DONNÉES ==========
def generate_futuristic_data():
    """Générer des données de démonstration"""
    
    dates = pd.date_range(start='2024-01-01', end='2024-03-15', freq='D')
    
    financial_data = pd.DataFrame({
        'Date': dates,
        'Chiffre_d_affaires': 1000000 + np.cumsum(np.random.normal(50000, 15000, len(dates))),
        'Bénéfice_net': 100000 + np.cumsum(np.random.normal(5000, 2000, len(dates))),
        'Effectifs': np.random.randint(200, 300, len(dates)),
        'Nbre_magasins': np.random.randint(45, 55, len(dates)),
        'Satisfaction_client': np.random.uniform(3.5, 4.8, len(dates)),
        'Panier_moyen': np.random.uniform(45, 85, len(dates)),
        'Investissements': np.random.choice([0, 75000, 150000, 250000], len(dates), p=[0.6, 0.2, 0.15, 0.05]),
        'Clients_actifs': np.random.randint(4000, 6000, len(dates))
    })
    
    # Noms de territoires futuristes
    territories = {
        'DROM': ['Matrix Martinique', 'Nexus Guadeloupe', 'Quantum Guyane', 'Cyber Réunion'],
        'COM': ['Neo Polynésie', 'Digital Calédonie', 'Holo Wallis'],
        'Métropole': ['Paris 2.0', 'Lyon Digital', 'Mars Tech Valley', 'Neo Bordeaux', 'Quantum Lille']
    }
    
    territory_rows = []
    for ter_type, ter_list in territories.items():
        for ter in ter_list:
            territory_rows.append({
                'Territoire': ter,
                'Type': ter_type,
                'Chiffre_affaires': np.random.uniform(100000, 800000),
                'Croissance': np.random.uniform(5, 25),
                'Satisfaction': np.random.uniform(3.5, 4.9),
                'Part_marche': np.random.uniform(15, 45),
                'Panier_moyen': np.random.uniform(50, 120),
                'Rentabilité': np.random.uniform(8, 22),
                'Magasins': np.random.randint(3, 15),
                'Nouveaux_clients_mois': np.random.randint(100, 500),
                'Digital_score': np.random.uniform(40, 85)  # Colonne corrigée
            })
    
    territory_data = pd.DataFrame(territory_rows)
    
    store_stats = pd.DataFrame({
        'Type': ['DROM', 'COM', 'Métropole'],
        'Nombre_Magasins': [territory_data[territory_data['Type'] == 'DROM']['Magasins'].sum(),
                           territory_data[territory_data['Type'] == 'COM']['Magasins'].sum(),
                           territory_data[territory_data['Type'] == 'Métropole']['Magasins'].sum()]
    })
    
    kpi_summary = {
        'total_territoires': len(territory_data),
        'total_magasins': store_stats['Nombre_Magasins'].sum(),
        'ca_total': territory_data['Chiffre_affaires'].sum(),
        'croissance_moyenne': territory_data['Croissance'].mean(),
        'satisfaction_moyenne': territory_data['Satisfaction'].mean()
    }
    
    transactions = []
    transaction_types = ['VENTE', 'SERVICE', 'FORMATION', 'ABONNEMENT']
    categories = ['TECH', 'BIOTECH', 'ROBOTIQUE', 'IA']
    
    for i in range(30):
        territory = np.random.choice(territory_data['Territoire'].tolist())
        ter_type = territory_data[territory_data['Territoire'] == territory]['Type'].iloc[0]
        
        transactions.append({
            'Timestamp': (datetime.now() - timedelta(hours=np.random.randint(0, 72))).strftime('%Y-%m-%d %H:%M:%S'),
            'Type': np.random.choice(transaction_types),
            'Catégorie': np.random.choice(categories),
            'Territoire': territory,
            'Type_Territoire': ter_type,
            'Montant': np.random.uniform(100, 2000)
        })
    
    return financial_data, territory_data, store_stats, kpi_summary, transactions

# ========== CHARGEMENT DES DONNÉES ==========
with st.spinner('🚀 Initialisation du système...'):
    time.sleep(0.5)
    
    try:
        from NinjaGBHData import NinjaGBHDataSimulator
        ninja_simulator = NinjaGBHDataSimulator()
        financial_data = ninja_simulator.generate_financial_data()
        territory_data = ninja_simulator.generate_territory_performance()
        store_stats = ninja_simulator.get_store_statistics()
        kpi_summary = ninja_simulator.get_kpi_summary()
        transactions_data = ninja_simulator.generate_real_transactions(15)
        
        # Ajouter les colonnes manquantes si elles n'existent pas
        if 'Digital_score' not in territory_data.columns:
            territory_data['Digital_score'] = np.random.uniform(40, 85, len(territory_data))
        
        st.success('✅ Données chargées avec succès')
    except Exception as e:
        st.warning(f'⚠️ Utilisation des données de démo')
        financial_data, territory_data, store_stats, kpi_summary, transactions_data = generate_futuristic_data()

# ========== FONCTIONS DE GRAPHIQUES ==========
def create_cyber_trend_chart():
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=financial_data['Date'],
        y=financial_data['Chiffre_d_affaires'],
        mode='lines',
        name='CA',
        line=dict(color=NEON_BLUE, width=3)
    ))
    
    fig.add_trace(go.Scatter(
        x=financial_data['Date'],
        y=financial_data['Bénéfice_net'],
        mode='lines',
        name='Bénéfice',
        line=dict(color=NEON_PURPLE, width=2)
    ))
    
    fig.update_layout(
        title='📈 ÉVOLUTION FINANCIÈRE',
        xaxis_title='Date',
        yaxis_title='Montant (€)',
        template='plotly_dark',
        paper_bgcolor=COLORS['card_bg'],
        plot_bgcolor=COLORS['card_bg'],
        height=400
    )
    
    return fig

def create_neon_gauge(value, title, color):
    """Jauge néon - VERSION SIMPLIFIÉE"""
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=value,
        title={'text': title},
        gauge={
            'axis': {'range': [None, 100]},
            'bar': {'color': color},
            'bgcolor': COLORS['card_bg'],
            'borderwidth': 2,
            'bordercolor': color
        }
    ))
    
    fig.update_layout(
        paper_bgcolor=COLORS['card_bg'],
        font={'color': "white"},
        height=250
    )
    
    return fig

def create_territory_chart():
    territory_sorted = territory_data.sort_values('Chiffre_affaires', ascending=True)
    
    fig = go.Figure()
    
    color_map = {'DROM': COLORS['drom'], 'COM': COLORS['com'], 'Métropole': COLORS['metro']}
    
    for ter_type in territory_sorted['Type'].unique():
        df_type = territory_sorted[territory_sorted['Type'] == ter_type]
        fig.add_trace(go.Bar(
            y=df_type['Territoire'],
            x=df_type['Chiffre_affaires'],
            name=ter_type,
            orientation='h',
            marker_color=color_map[ter_type]
        ))
    
    fig.update_layout(
        title='PERFORMANCE PAR TERRITOIRE',
        template='plotly_dark',
        paper_bgcolor=COLORS['card_bg'],
        plot_bgcolor=COLORS['card_bg'],
        height=500
    )
    
    return fig

# ========== INTERFACE UTILISATEUR ==========
st.markdown(f"""
<div class="main-header">
    <h1 style="font-size: 48px; margin: 0; background: linear-gradient(90deg, {NEON_BLUE}, {NEON_CYAN}, {NEON_PURPLE});
               -webkit-background-clip: text;
               -webkit-text-fill-color: transparent;
               font-family: 'Courier New', monospace;">
        ⚡ GBH GROUP | DASHBOARD FUTURISTE
    </h1>
    <div style="display: flex; justify-content: space-between; align-items: center; margin-top: 20px;">
        <div>
            <h3 style="color: {NEON_CYAN}; margin: 5px 0;">Tableau de Bord Exécutif</h3>
        </div>
        <div style="text-align: right;">
            <div style="font-size: 24px; color: {NEON_GREEN}; font-family: 'Courier New';">
                {datetime.now().strftime('%H:%M:%S')}
            </div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div class="marquee">
    <div class="marquee-content">
        ⚡ SYSTÈME ACTIF • ANALYSE EN TEMPS RÉEL • PERFORMANCE OPTIMALE •
    </div>
</div>
""", unsafe_allow_html=True)

view = st.radio(
    "",
    ["🌐 DASHBOARD", "🚀 PERFORMANCE", "📊 ANALYSE", "💹 FINANCE"],
    horizontal=True
)

st.markdown("---")

if "DASHBOARD" in view:
    
    st.markdown('<h2 class="neon-title">📊 TABLEAU DE BORD PRINCIPAL</h2>', unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        ca = financial_data['Chiffre_d_affaires'].iloc[-1]
        delta = ca - financial_data['Chiffre_d_affaires'].iloc[-2] if len(financial_data) > 1 else 0
        st.markdown(f"""
        <div class="metric-card">
            <div style="text-align: center;">
                <div style="font-size: 32px; color: {NEON_BLUE}; margin-bottom: 10px;">⚡</div>
                <h4 style="color: {COLORS['text_secondary']}; margin: 0;">CHIFFRE D'AFFAIRES</h4>
                <h2 style="color: {NEON_BLUE}; margin: 15px 0;">{ca:,.0f}€</h2>
                <div style="color: {NEON_GREEN if delta > 0 else NEON_PINK};">
                    {'↗' if delta > 0 else '↘'} {abs(delta):,.0f}€
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        profit = financial_data['Bénéfice_net'].iloc[-1]
        profit_delta = profit - financial_data['Bénéfice_net'].iloc[-2] if len(financial_data) > 1 else 0
        st.markdown(f"""
        <div class="metric-card">
            <div style="text-align: center;">
                <div style="font-size: 32px; color: {NEON_GREEN}; margin-bottom: 10px;">💎</div>
                <h4 style="color: {COLORS['text_secondary']}; margin: 0;">BÉNÉFICE NET</h4>
                <h2 style="color: {NEON_GREEN}; margin: 15px 0;">{profit:,.0f}€</h2>
                <div style="color: {NEON_GREEN if profit_delta > 0 else NEON_PINK};">
                    {'↗' if profit_delta > 0 else '↘'} {abs(profit_delta):,.0f}€
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        satisfaction = financial_data['Satisfaction_client'].iloc[-1]
        st.markdown(f"""
        <div class="metric-card">
            <div style="text-align: center;">
                <div style="font-size: 32px; color: {NEON_YELLOW}; margin-bottom: 10px;">⭐</div>
                <h4 style="color: {COLORS['text_secondary']}; margin: 0;">SATISFACTION</h4>
                <h2 style="color: {NEON_YELLOW}; margin: 15px 0;">{satisfaction:.1f}/5.0</h2>
                <div style="color: {NEON_CYAN};">
                    {'EXCELLENT' if satisfaction > 4.5 else 'BON' if satisfaction > 4 else 'MOYEN'}
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        stores = financial_data['Nbre_magasins'].iloc[-1]
        st.markdown(f"""
        <div class="metric-card">
            <div style="text-align: center;">
                <div style="font-size: 32px; color: {NEON_PURPLE}; margin-bottom: 10px;">🏪</div>
                <h4 style="color: {COLORS['text_secondary']}; margin: 0;">MAGASINS</h4>
                <h2 style="color: {NEON_PURPLE}; margin: 15px 0;">{stores}</h2>
                <div style="color: {NEON_CYAN};">
                    Points de vente actifs
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    st.plotly_chart(create_cyber_trend_chart(), use_container_width=True)
    
    # Jaunes simplifiés
    col5, col6, col7, col8 = st.columns(4)
    
    with col5:
        digital_score = territory_data['Digital_score'].mean() if 'Digital_score' in territory_data.columns else 65
        st.plotly_chart(create_neon_gauge(digital_score, "DIGITAL", NEON_BLUE), use_container_width=True)
    
    with col6:
        rentabilite = territory_data['Rentabilité'].mean()
        st.plotly_chart(create_neon_gauge(rentabilite, "RENTABILITÉ", NEON_GREEN), use_container_width=True)
    
    with col7:
        croissance = territory_data['Croissance'].mean()
        st.plotly_chart(create_neon_gauge(croissance, "CROISSANCE", NEON_CYAN), use_container_width=True)
    
    with col8:
        satisfaction_terr = territory_data['Satisfaction'].mean() * 20
        st.plotly_chart(create_neon_gauge(satisfaction_terr, "SATISFACTION", NEON_YELLOW), use_container_width=True)

elif "PERFORMANCE" in view:
    
    st.markdown('<h2 class="neon-title">🚀 PERFORMANCE TERRITORIALE</h2>', unsafe_allow_html=True)
    
    territory_type = st.selectbox(
        "FILTRE",
        ["TOUS", "DROM", "COM", "MÉTROPOLE"]
    )
    
    filtered_data = territory_data if territory_type == "TOUS" else territory_data[territory_data['Type'] == territory_type]
    
    st.plotly_chart(create_territory_chart(), use_container_width=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        top_ca = filtered_data.nlargest(1, 'Chiffre_affaires')
        if not top_ca.empty:
            st.markdown(f"""
            <div class="data-card">
                <h4 style="color: {NEON_BLUE}; margin: 0 0 10px 0;">🏆 MEILLEUR CA</h4>
                <h3 style="color: white; margin: 10px 0;">{top_ca['Territoire'].iloc[0]}</h3>
                <div style="color: {NEON_GREEN}; font-size: 24px;">
                    {top_ca['Chiffre_affaires'].iloc[0]:,.0f}€
                </div>
            </div>
            """, unsafe_allow_html=True)
    
    with col2:
        top_growth = filtered_data.nlargest(1, 'Croissance')
        if not top_growth.empty:
            st.markdown(f"""
            <div class="data-card">
                <h4 style="color: {NEON_GREEN}; margin: 0 0 10px 0;">🚀 CROISSANCE MAX</h4>
                <h3 style="color: white; margin: 10px 0;">{top_growth['Territoire'].iloc[0]}</h3>
                <div style="color: {NEON_GREEN}; font-size: 24px;">
                    +{top_growth['Croissance'].iloc[0]:.1f}%
                </div>
            </div>
            """, unsafe_allow_html=True)
    
    with col3:
        top_satisfaction = filtered_data.nlargest(1, 'Satisfaction')
        if not top_satisfaction.empty:
            st.markdown(f"""
            <div class="data-card">
                <h4 style="color: {NEON_YELLOW}; margin: 0 0 10px 0;">⭐ SATISFACTION MAX</h4>
                <h3 style="color: white; margin: 10px 0;">{top_satisfaction['Territoire'].iloc[0]}</h3>
                <div style="color: {NEON_YELLOW}; font-size: 24px;">
                    {top_satisfaction['Satisfaction'].iloc[0]:.1f}/5.0
                </div>
            </div>
            """, unsafe_allow_html=True)

elif "ANALYSE" in view:
    
    st.markdown('<h2 class="neon-title">📊 ANALYSE AVANCÉE</h2>', unsafe_allow_html=True)
    
    type_comparison = territory_data.groupby('Type').agg({
        'Chiffre_affaires': 'mean',
        'Croissance': 'mean',
        'Satisfaction': 'mean',
        'Rentabilité': 'mean'
    }).reset_index()
    
    fig = go.Figure()
    
    metrics = ['Chiffre_affaires', 'Croissance', 'Satisfaction', 'Rentabilité']
    colors = [NEON_BLUE, NEON_GREEN, NEON_YELLOW, NEON_PURPLE]
    
    for metric, color in zip(metrics, colors):
        fig.add_trace(go.Bar(
            x=type_comparison['Type'],
            y=type_comparison[metric],
            name=metric.upper(),
            marker_color=color
        ))
    
    fig.update_layout(
        title='COMPARAISON PAR TYPE',
        barmode='group',
        template='plotly_dark',
        paper_bgcolor=COLORS['card_bg'],
        plot_bgcolor=COLORS['card_bg'],
        height=400
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Tableau des données
    st.markdown('<h3 style="color: #00f3ff;">📋 DONNÉES DÉTAILLÉES</h3>', unsafe_allow_html=True)
    st.dataframe(
        territory_data,
        column_config={
            'Territoire': 'Territoire',
            'Type': 'Type',
            'Chiffre_affaires': st.column_config.NumberColumn('CA (€)', format="%.0f"),
            'Croissance': st.column_config.NumberColumn('Croissance (%)', format="%.1f"),
            'Satisfaction': st.column_config.NumberColumn('Satisfaction', format="%.1f"),
            'Rentabilité': st.column_config.NumberColumn('Rentabilité (%)', format="%.1f")
        },
        use_container_width=True
    )

else:  # FINANCE
    
    st.markdown('<h2 class="neon-title">💹 ANALYSE FINANCIÈRE</h2>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        marge = ((financial_data['Bénéfice_net'].iloc[-1] / financial_data['Chiffre_d_affaires'].iloc[-1]) * 100) if financial_data['Chiffre_d_affaires'].iloc[-1] > 0 else 0
        st.markdown(f"""
        <div class="data-card">
            <h4 style="color: {NEON_GREEN}; margin: 0 0 10px 0;">💰 MARGE NETTE</h4>
            <h2 style="color: {NEON_GREEN}; margin: 15px 0; font-size: 36px;">{marge:.1f}%</h2>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="data-card">
            <h4 style="color: {NEON_BLUE}; margin: 0 0 10px 0;">📈 ROI MENSUEL</h4>
            <h2 style="color: {NEON_BLUE}; margin: 15px 0; font-size: 36px;">8.2%</h2>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        cash = financial_data['Bénéfice_net'].iloc[-1] * 0.3
        st.markdown(f"""
        <div class="data-card">
            <h4 style="color: {NEON_CYAN}; margin: 0 0 10px 0;">🏦 TRÉSORERIE</h4>
            <h2 style="color: {NEON_CYAN}; margin: 15px 0; font-size: 36px;">{cash:,.0f}€</h2>
        </div>
        """, unsafe_allow_html=True)
    
    # Graphique de répartition
    ca_by_type = territory_data.groupby('Type')['Chiffre_affaires'].sum().reset_index()
    
    fig = go.Figure(data=[go.Pie(
        labels=ca_by_type['Type'],
        values=ca_by_type['Chiffre_affaires'],
        hole=0.4,
        marker_colors=[COLORS['drom'], COLORS['com'], COLORS['metro']]
    )])
    
    fig.update_layout(
        title='RÉPARTITION DU CA PAR TYPE',
        template='plotly_dark',
        paper_bgcolor=COLORS['card_bg'],
        plot_bgcolor=COLORS['card_bg'],
        height=400
    )
    
    st.plotly_chart(fig, use_container_width=True)

# ========== PIED DE PAGE ==========
st.markdown("""
<div style="margin-top: 50px; padding: 20px; background: rgba(13, 18, 32, 0.8); 
            border-radius: 15px; border: 1px solid rgba(0, 243, 255, 0.3);
            text-align: center;">
    
    <div style="display: flex; justify-content: space-between; align-items: center;">
        <div style="text-align: left;">
            <div style="color: #00f3ff; font-family: 'Courier New';">
                ⚡ GBH GROUP DASHBOARD
            </div>
        </div>
        
        <div style="text-align: center;">
            <div style="color: #00fff9; font-family: 'Courier New';">
                {timestamp}
            </div>
        </div>
        
        <div style="text-align: right;">
            <div style="color: #00ff9d; font-family: 'Courier New';">
                🚀 PERFORMANCE MAX
            </div>
        </div>
    </div>
</div>
""".format(timestamp=datetime.now().strftime('%d/%m/%Y %H:%M:%S')), unsafe_allow_html=True)

if st.button('🔄 RAFRAÎCHIR LES DONNÉES', use_container_width=True):
    st.rerun()

# Message de confirmation
st.success('✅ Dashboard chargé avec succès!')
