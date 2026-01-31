# Dashboard.py - Édition Futuriste Neon
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
    
    # Gradients néon
    'gradient_start': '#0066ff',
    'gradient_mid': '#00f3ff',
    'gradient_end': '#b967ff',
    
    # Couleurs fonctionnelles néon
    'success': NEON_GREEN,
    'warning': NEON_YELLOW,
    'danger': NEON_PINK,
    'info': NEON_CYAN,
    'primary': NEON_BLUE,
    'accent': NEON_PURPLE,
    
    # Couleurs territoires néon
    'drom': '#ff4d94',  # Rose néon
    'com': '#ffcc00',   # Jaune néon
    'metro': '#00e6ff'  # Cyan néon
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

@keyframes float {{
    0%, 100% {{ transform: translateY(0); }}
    50% {{ transform: translateY(-10px); }}
}}

@keyframes neonBorder {{
    0%, 100% {{ border-color: {NEON_BLUE}; }}
    50% {{ border-color: {NEON_CYAN}; }}
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

/* Application principale */
.stApp {{
    background: linear-gradient(135deg, #0a0e17 0%, #0d1220 50%, #0a0e17 100%);
    background-attachment: fixed;
    color: {COLORS['text_primary']};
    font-family: 'Segoe UI', 'Roboto', 'Arial', sans-serif;
}}

/* Header futuriste avec effets */
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
    animation: neonBorder 3s infinite;
}}

@keyframes gradientShift {{
    0% {{ background-position: 0% 50%; }}
    50% {{ background-position: 100% 50%; }}
    100% {{ background-position: 0% 50%; }}
}}

.main-header::before {{
    content: '';
    position: absolute;
    top: -50%;
    left: -50%;
    width: 200%;
    height: 200%;
    background: radial-gradient(circle, rgba(0, 243, 255, 0.1) 0%, transparent 70%);
    animation: float 20s infinite linear;
}}

/* Cartes de métriques avec effets néon */
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

.metric-card::before {{
    content: '';
    position: absolute;
    top: 0;
    left: -100%;
    width: 100%;
    height: 100%;
    background: linear-gradient(90deg, transparent, rgba(0, 243, 255, 0.1), transparent);
    transition: left 0.5s;
}}

.metric-card:hover::before {{
    left: 100%;
}}

.metric-card:hover {{
    transform: translateY(-10px) scale(1.02);
    border-color: {NEON_BLUE};
    box-shadow: 0 15px 30px rgba(0, 243, 255, 0.3),
                0 0 20px rgba(0, 243, 255, 0.2),
                inset 0 0 20px rgba(0, 243, 255, 0.1);
}}

/* Boutons futuristes */
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
    animation: pulse 2s infinite;
}}

.stButton > button:hover {{
    transform: translateY(-3px);
    box-shadow: 0 10px 20px rgba(0, 243, 255, 0.4),
                0 0 30px rgba(0, 243, 255, 0.3);
    animation: none;
}}

.stButton > button::before {{
    content: '';
    position: absolute;
    top: 0;
    left: -100%;
    width: 100%;
    height: 100%;
    background: linear-gradient(90deg, transparent, rgba(255, 255, 255, 0.2), transparent);
    transition: left 0.5s;
}}

.stButton > button:hover::before {{
    left: 100%;
}}

/* Navigation futuriste */
.stRadio > div {{
    background: rgba(13, 18, 32, 0.8);
    border: 1px solid {COLORS['card_border']};
    border-radius: 12px;
    padding: 10px;
    backdrop-filter: blur(10px);
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

.stRadio > div > label[data-testid="stRadio"]:checked + span {{
    color: {NEON_BLUE} !important;
    font-weight: 600;
    text-shadow: 0 0 10px {NEON_BLUE};
}}

/* Titres avec effet néon */
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

/* Cartes de données avec effet holographique */
.data-card {{
    background: linear-gradient(135deg, 
        rgba(13, 18, 32, 0.9) 0%,
        rgba(26, 34, 52, 0.7) 100%);
    border: 1px solid rgba(0, 243, 255, 0.3);
    border-radius: 15px;
    padding: 25px;
    backdrop-filter: blur(10px);
    position: relative;
    overflow: hidden;
}}

.data-card::before {{
    content: '';
    position: absolute;
    top: -2px;
    left: -2px;
    right: -2px;
    bottom: -2px;
    background: linear-gradient(45deg, {NEON_BLUE}, {NEON_CYAN}, {NEON_PURPLE}, {NEON_BLUE});
    background-size: 400% 400%;
    border-radius: 17px;
    z-index: -1;
    animation: gradientShift 6s ease infinite;
    opacity: 0.5;
}}

/* Animation de particules */
.particles {{
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    pointer-events: none;
    z-index: -1;
}}

.particle {{
    position: absolute;
    background: {NEON_BLUE};
    border-radius: 50%;
    animation: floatParticle 20s infinite linear;
}}

@keyframes floatParticle {{
    0% {{ transform: translateY(100vh) translateX(0) scale(0.5); opacity: 0; }}
    10% {{ opacity: 0.3; }}
    90% {{ opacity: 0.3; }}
    100% {{ transform: translateY(-100px) translateX(100px) scale(1); opacity: 0; }}
}}

/* Scrollbar stylisée */
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
    border: 2px solid {COLORS['card_bg']};
}}

::-webkit-scrollbar-thumb:hover {{
    background: linear-gradient({NEON_CYAN}, {NEON_BLUE});
    box-shadow: 0 0 10px {NEON_BLUE};
}}

/* Effet de texte défilant */
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

/* Badges néon */
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
    animation: pulse 2s infinite;
}}

/* État de chargement */
.loading {{
    position: relative;
}}

.loading::after {{
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: linear-gradient(90deg, transparent, rgba(0, 243, 255, 0.1), transparent);
    animation: loading 1.5s infinite;
}}

@keyframes loading {{
    0% {{ transform: translateX(-100%); }}
    100% {{ transform: translateX(100%); }}
}}
</style>

<script>
// Ajout de particules animées
function createParticles() {{
    const container = document.createElement('div');
    container.className = 'particles';
    document.querySelector('.stApp').appendChild(container);
    
    for(let i = 0; i < 30; i++) {{
        const particle = document.createElement('div');
        particle.className = 'particle';
        particle.style.left = Math.random() * 100 + '%';
        particle.style.width = Math.random() * 4 + 2 + 'px';
        particle.style.height = particle.style.width;
        particle.style.animationDelay = Math.random() * 20 + 's';
        particle.style.animationDuration = Math.random() * 10 + 20 + 's';
        container.appendChild(particle);
    }}
}}

window.addEventListener('load', createParticles);
</script>
""", unsafe_allow_html=True)

# ========== FONCTIONS DE GÉNÉRATION DE DONNÉES FUTURISTES ==========
def generate_futuristic_data():
    """Générer des données de démonstration avec tendances futuristes"""
    
    dates = pd.date_range(start='2024-01-01', end='2024-03-15', freq='D')
    
    # Tendances exponentielles pour effet futuriste
    growth_factor = np.exp(np.linspace(0, 2, len(dates)))
    
    financial_data = pd.DataFrame({
        'Date': dates,
        'Chiffre_d_affaires': 1000000 + np.cumsum(np.random.normal(50000, 15000, len(dates))) * growth_factor,
        'Bénéfice_net': 100000 + np.cumsum(np.random.normal(5000, 2000, len(dates))) * growth_factor,
        'Effectifs': np.random.normal(250, 20, len(dates)).astype(int) + (np.arange(len(dates)) * 0.5).astype(int),
        'Nbre_magasins': np.random.normal(50, 5, len(dates)).astype(int) + (np.arange(len(dates)) * 0.2).astype(int),
        'Satisfaction_client': np.clip(np.random.normal(4.2, 0.3, len(dates)) + (np.arange(len(dates)) * 0.002), 3.5, 5.0),
        'Panier_moyen': np.random.normal(65, 15, len(dates)) + (np.arange(len(dates)) * 0.3),
        'Investissements': np.random.choice([0, 75000, 150000, 250000], len(dates), p=[0.6, 0.2, 0.15, 0.05]) * growth_factor[:len(dates)],
        'Clients_actifs': np.random.normal(5000, 1000, len(dates)).astype(int) + (np.arange(len(dates)) * 20).astype(int),
        'CA_digital': np.random.normal(200000, 50000, len(dates)) + np.cumsum(np.random.normal(10000, 3000, len(dates)))
    })
    
    # Données territoriales futuristes
    territories = {
        'DROM': ['Matrix Martinique', 'Nexus Guadeloupe', 'Quantum Guyane', 'Cyber Réunion', 'Synthwave Mayotte'],
        'COM': ['Neo Polynésie', 'Digital Calédonie', 'Holo Wallis', 'Virtual Saint-Pierre'],
        'Métropole': ['Paris 2.0', 'Lyon Digital', 'Mars Tech Valley', 'Neo Bordeaux', 
                     'Quantum Lille', 'Cyber Marseille', 'AI Strasbourg', 'Holo Nantes']
    }
    
    territory_rows = []
    for ter_type, ter_list in territories.items():
        for ter in ter_list:
            base_ca = np.random.uniform(100000, 800000)
            growth = np.random.uniform(15, 40)  # Croissance forte pour effet futuriste
            
            territory_rows.append({
                'Territoire': ter,
                'Type': ter_type,
                'Chiffre_affaires': base_ca,
                'Croissance': growth,
                'Satisfaction': np.random.uniform(4.0, 4.9),
                'Part_marche': np.random.uniform(25, 60),
                'Panier_moyen': np.random.uniform(50, 120),
                'Rentabilité': np.random.uniform(12, 30),
                'Magasins': np.random.randint(3, 20),
                'Nouveaux_clients_mois': np.random.randint(100, 800),
                'Digital_penetration': np.random.uniform(40, 85),
                'Tech_score': np.random.uniform(60, 95)
            })
    
    territory_data = pd.DataFrame(territory_rows)
    
    # Statistiques magasins
    store_stats = pd.DataFrame({
        'Type': ['DROM', 'COM', 'Métropole'],
        'Nombre_Magasins': [territory_data[territory_data['Type'] == 'DROM']['Magasins'].sum(),
                           territory_data[territory_data['Type'] == 'COM']['Magasins'].sum(),
                           territory_data[territory_data['Type'] == 'Métropole']['Magasins'].sum()],
        'CA_Moyen_Magasin': [territory_data[territory_data['Type'] == 'DROM']['Chiffre_affaires'].sum() / 
                            territory_data[territory_data['Type'] == 'DROM']['Magasins'].sum(),
                           territory_data[territory_data['Type'] == 'COM']['Chiffre_affaires'].sum() / 
                            territory_data[territory_data['Type'] == 'COM']['Magasins'].sum(),
                           territory_data[territory_data['Type'] == 'Métropole']['Chiffre_affaires'].sum() / 
                            territory_data[territory_data['Type'] == 'Métropole']['Magasins'].sum()]
    })
    
    # KPI résumé futuriste
    kpi_summary = {
        'total_territoires': len(territory_data),
        'total_magasins': store_stats['Nombre_Magasins'].sum(),
        'ca_total': territory_data['Chiffre_affaires'].sum(),
        'croissance_moyenne': territory_data['Croissance'].mean(),
        'satisfaction_moyenne': territory_data['Satisfaction'].mean(),
        'rentabilite_moyenne': territory_data['Rentabilité'].mean(),
        'penetration_digitale': territory_data['Digital_penetration'].mean()
    }
    
    # Transactions futuristes
    transactions = []
    transaction_types = ['VENTE QUANTUM', 'ECHANGE HOLO', 'SERVICE AI', 'ABONNEMENT PREMIUM', 'FORMATION VR']
    categories = ['TECH ULTRA', 'BIOTECH', 'ROBOTIQUE', 'INTELLIGENCE ARTIFICIELLE', 'QUANTUM COMPUTING', 'NEUROTECH']
    
    for i in range(50):
        amount = np.random.uniform(100, 2000)
        territory = np.random.choice(territory_data['Territoire'].tolist())
        ter_type = territory_data[territory_data['Territoire'] == territory]['Type'].iloc[0]
        
        transactions.append({
            'Timestamp': (datetime.now() - timedelta(hours=np.random.randint(0, 72))).strftime('%Y-%m-%d %H:%M:%S'),
            'Type': np.random.choice(transaction_types),
            'Catégorie': np.random.choice(categories),
            'Territoire': territory,
            'Type_Territoire': ter_type,
            'Montant': amount * (1.5 if ter_type == 'Métropole' else 1.2 if ter_type == 'COM' else 1),
            'Client_ID': f"CUST-{np.random.randint(10000, 99999)}",
            'Mode_Paiement': np.random.choice(['CRYPTO', 'TOKEN', 'BIOMETRIE', 'VR WALLET']),
            'Score_Futur': np.random.uniform(0.7, 1.3)
        })
    
    return financial_data, territory_data, store_stats, kpi_summary, transactions

# ========== CHARGEMENT DES DONNÉES ==========
with st.spinner('🚀 Initialisation du système quantique...'):
    time.sleep(0.5)
    
    try:
        from NinjaGBHData import NinjaGBHDataSimulator
        ninja_simulator = NinjaGBHDataSimulator()
        financial_data = ninja_simulator.generate_financial_data()
        territory_data = ninja_simulator.generate_territory_performance()
        store_stats = ninja_simulator.get_store_statistics()
        kpi_summary = ninja_simulator.get_kpi_summary()
        transactions_data = ninja_simulator.generate_real_transactions(15)
        st.success('✅ Système quantique connecté | Données réelles chargées')
    except:
        financial_data, territory_data, store_stats, kpi_summary, transactions_data = generate_futuristic_data()
        st.success('✨ Mode démo activé | Données futuristes générées')

# ========== FONCTIONS DE GRAPHIQUES FUTURISTES ==========
def create_cyber_trend_chart():
    """Graphique de tendance avec style cyberpunk"""
    fig = go.Figure()
    
    # Ligne principale avec effet glow
    fig.add_trace(go.Scatter(
        x=financial_data['Date'],
        y=financial_data['Chiffre_d_affaires'],
        mode='lines',
        name='CA QUANTUM',
        line=dict(
            color=NEON_BLUE,
            width=4,
            shape='spline'
        ),
        fill='tozeroy',
        fillcolor=f'rgba(0, 243, 255, 0.1)'
    ))
    
    # Ligne secondaire
    fig.add_trace(go.Scatter(
        x=financial_data['Date'],
        y=financial_data['Bénéfice_net'],
        mode='lines',
        name='PROFIT SYNTHWAVE',
        line=dict(
            color=NEON_PURPLE,
            width=3,
            shape='spline',
            dash='dot'
        )
    ))
    
    # Points de données avec effet
    fig.add_trace(go.Scatter(
        x=financial_data['Date'][::7],
        y=financial_data['Chiffre_d_affaires'][::7],
        mode='markers',
        name='POINTS DATA',
        marker=dict(
            size=10,
            color=NEON_CYAN,
            line=dict(width=2, color='white'),
            symbol='diamond'
        )
    ))
    
    fig.update_layout(
        title=dict(
            text='📈 ÉVOLUTION QUANTUM 2024',
            font=dict(size=24, color=NEON_BLUE, family='Courier New'),
            x=0.5
        ),
        xaxis=dict(
            title='TIMELINE',
            gridcolor='rgba(0, 243, 255, 0.1)',
            tickfont=dict(color=NEON_CYAN, family='Courier New'),
            linecolor=NEON_BLUE,
            linewidth=2,
            showgrid=True,
            gridwidth=1
        ),
        yaxis=dict(
            title='VALUE (M€)',
            gridcolor='rgba(0, 243, 255, 0.1)',
            tickfont=dict(color=NEON_CYAN, family='Courier New'),
            linecolor=NEON_BLUE,
            linewidth=2
        ),
        template='plotly_dark',
        paper_bgcolor='rgba(13, 18, 32, 0.9)',
        plot_bgcolor='rgba(13, 18, 32, 0.5)',
        font=dict(color=COLORS['text_primary'], family='Arial'),
        legend=dict(
            bgcolor='rgba(13, 18, 32, 0.8)',
            bordercolor=NEON_BLUE,
            borderwidth=1,
            font=dict(color=NEON_CYAN, family='Courier New')
        ),
        hovermode='x unified',
        height=450,
        margin=dict(l=50, r=50, t=80, b=50)
    )
    
    return fig

def create_neon_gauge(value, title, color):
    """Jauge néon interactive"""
    fig = go.Figure(go.Indicator(
        mode="gauge+number+delta",
        value=value,
        title={'text': title, 'font': {'size': 16, 'color': color, 'family': 'Courier New'}},
        delta={'reference': value * 0.8, 'increasing': {'color': NEON_GREEN}},
        gauge={
            'axis': {'range': [None, 100], 'tickwidth': 1, 'tickcolor': color},
            'bar': {'color': color},
            'bgcolor': COLORS['card_bg'],
            'borderwidth': 2,
            'bordercolor': color,
            'steps': [
                {'range': [0, 33], 'color': f'rgba{tuple(int(color.lstrip("#")[i:i+2], 16) for i in (0, 2, 4)) + (0.1,)}'},
                {'range': [33, 66], 'color': f'rgba{tuple(int(color.lstrip("#")[i:i+2], 16) for i in (0, 2, 4)) + (0.3,)}'},
                {'range': [66, 100], 'color': f'rgba{tuple(int(color.lstrip("#")[i:i+2], 16) for i in (0, 2, 4)) + (0.5,)}'}
            ],
            'threshold': {
                'line': {'color': "white", 'width': 4},
                'thickness': 0.75,
                'value': value
            }
        }
    ))
    
    fig.update_layout(
        paper_bgcolor=COLORS['card_bg'],
        font={'color': "white", 'family': "Arial"},
        height=250,
        margin=dict(t=50, b=10, l=10, r=10)
    )
    
    return fig

def create_3d_scatter():
    """Graphique 3D futuriste"""
    fig = go.Figure(data=[go.Scatter3d(
        x=territory_data['Chiffre_affaires'],
        y=territory_data['Croissance'],
        z=territory_data['Satisfaction'],
        mode='markers',
        marker=dict(
            size=territory_data['Rentabilité'] / 2,
            color=territory_data['Tech_score'],
            colorscale=[[0, NEON_BLUE], [0.5, NEON_PURPLE], [1, NEON_PINK]],
            showscale=True,
            opacity=0.8,
            line=dict(color='white', width=1)
        ),
        text=territory_data['Territoire'],
        hovertemplate='<b>%{text}</b><br>CA: %{x:,.0f}€<br>Croissance: %{y:.1f}%<br>Satisfaction: %{z:.1f}/5<extra></extra>'
    )])
    
    fig.update_layout(
        title=dict(
            text='🌐 MATRICE DES PERFORMANCES 3D',
            font=dict(size=20, color=NEON_BLUE)
        ),
        scene=dict(
            xaxis_title='CA (€)',
            yaxis_title='CROISSANCE (%)',
            zaxis_title='SATISFACTION',
            bgcolor=COLORS['card_bg'],
            camera=dict(eye=dict(x=1.5, y=1.5, z=1))
        ),
        height=500,
        margin=dict(l=0, r=0, t=50, b=0)
    )
    
    return fig

def create_radar_chart():
    """Graphique radar pour analyse multidimensionnelle"""
    categories = ['CA', 'CROISSANCE', 'SATISFACTION', 'RENTABILITÉ', 'DIGITAL', 'TECH']
    
    fig = go.Figure()
    
    for ter_type in territory_data['Type'].unique():
        data = territory_data[territory_data['Type'] == ter_type].mean()
        values = [
            data['Chiffre_affaires'] / 1000000,
            data['Croissance'],
            data['Satisfaction'] * 20,
            data['Rentabilité'],
            data['Digital_penetration'],
            data['Tech_score']
        ]
        
        fig.add_trace(go.Scatterpolar(
            r=values,
            theta=categories,
            fill='toself',
            name=ter_type,
            line=dict(color=COLORS[ter_type.lower()], width=2)
        ))
    
    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 100]
            ),
            bgcolor=COLORS['card_bg']
        ),
        showlegend=True,
        title='📡 ANALYSE MULTIDIMENSIONNELLE',
        height=400
    )
    
    return fig

# ========== INTERFACE UTILISATEUR ==========

# Header futuriste
st.markdown(f"""
<div class="main-header">
    <h1 style="font-size: 48px; margin: 0; background: linear-gradient(90deg, {NEON_BLUE}, {NEON_CYAN}, {NEON_PURPLE});
               -webkit-background-clip: text;
               -webkit-text-fill-color: transparent;
               text-shadow: 0 0 30px rgba(0, 243, 255, 0.5);
               font-family: 'Courier New', monospace;">
        ⚡ GBH GROUP | QUANTUM DASHBOARD
    </h1>
    <div style="display: flex; justify-content: space-between; align-items: center; margin-top: 20px;">
        <div>
            <h3 style="color: {NEON_CYAN}; margin: 5px 0;">🌌 SYSTÈME DE SURVEILLANCE FINANCIÈRE</h3>
            <p style="color: rgba(255, 255, 255, 0.7); margin: 0;">Version 3.14 | Interface neuronale active</p>
        </div>
        <div style="text-align: right;">
            <div style="font-size: 24px; color: {NEON_GREEN}; font-family: 'Courier New';">
                {datetime.now().strftime('%H:%M:%S')}
            </div>
            <div style="font-size: 14px; color: {NEON_CYAN};">
                {datetime.now().strftime('%d/%m/%Y')}
            </div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# Barre de navigation
st.markdown("""
<div style="background: rgba(13, 18, 32, 0.8); padding: 15px; border-radius: 15px; 
            border: 1px solid rgba(0, 243, 255, 0.3); margin-bottom: 30px;
            backdrop-filter: blur(10px);">
    <div class="marquee">
        <div class="marquee-content">
            ⚡ SYSTÈME ACTIF • CHARGEMENT DES DONNÉES QUANTIQUES • ANALYSE EN TEMPS RÉEL • 
            PRÉDICTIONS IA • SURVEILLANCE 24/7 • OPTIMISATION AUTOMATIQUE •
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# Sélection de vue
view = st.radio(
    "",
    ["🌐 TABLEAU DE BORD", "🚀 PERFORMANCE", "📊 ANALYSE", "💹 FINANCE", "👥 ÉQUIPE"],
    horizontal=True,
    key="nav"
)

st.markdown("---")

# ========== VUE PRINCIPALE ==========
if "TABLEAU" in view:
    
    # KPI en temps réel
    st.markdown('<h2 class="neon-title">📊 DASHBOARD EN TEMPS RÉEL</h2>', unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        ca = financial_data['Chiffre_d_affaires'].iloc[-1]
        delta = ca - financial_data['Chiffre_d_affaires'].iloc[-2]
        st.markdown(f"""
        <div class="metric-card">
            <div style="text-align: center;">
                <div style="font-size: 32px; color: {NEON_BLUE}; margin-bottom: 10px;">⚡</div>
                <h4 style="color: {COLORS['text_secondary']}; margin: 0;">CHIFFRE D'AFFAIRES</h4>
                <h2 style="color: {NEON_BLUE}; margin: 15px 0; font-family: 'Courier New';">{ca:,.0f}€</h2>
                <div style="color: {NEON_GREEN if delta > 0 else NEON_PINK}; font-size: 14px;">
                    ↗ {delta:,.0f}€ vs hier
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        profit = financial_data['Bénéfice_net'].iloc[-1]
        profit_delta = profit - financial_data['Bénéfice_net'].iloc[-2]
        st.markdown(f"""
        <div class="metric-card">
            <div style="text-align: center;">
                <div style="font-size: 32px; color: {NEON_GREEN}; margin-bottom: 10px;">💎</div>
                <h4 style="color: {COLORS['text_secondary']}; margin: 0;">BÉNÉFICE NET</h4>
                <h2 style="color: {NEON_GREEN}; margin: 15px 0; font-family: 'Courier New';">{profit:,.0f}€</h2>
                <div style="color: {NEON_GREEN if profit_delta > 0 else NEON_PINK}; font-size: 14px;">
                    ↗ {profit_delta:,.0f}€ vs hier
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        clients = financial_data['Clients_actifs'].iloc[-1] if 'Clients_actifs' in financial_data.columns else 5250
        st.markdown(f"""
        <div class="metric-card">
            <div style="text-align: center;">
                <div style="font-size: 32px; color: {NEON_PURPLE}; margin-bottom: 10px;">👤</div>
                <h4 style="color: {COLORS['text_secondary']}; margin: 0;">CLIENTS ACTIFS</h4>
                <h2 style="color: {NEON_PURPLE}; margin: 15px 0; font-family: 'Courier New';">{clients:,.0f}</h2>
                <div style="color: {NEON_CYAN}; font-size: 14px;">
                    ↗ +2.5% ce mois
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        satisfaction = financial_data['Satisfaction_client'].iloc[-1]
        st.markdown(f"""
        <div class="metric-card">
            <div style="text-align: center;">
                <div style="font-size: 32px; color: {NEON_YELLOW}; margin-bottom: 10px;">⭐</div>
                <h4 style="color: {COLORS['text_secondary']}; margin: 0;">SATISFACTION</h4>
                <h2 style="color: {NEON_YELLOW}; margin: 15px 0; font-family: 'Courier New';">{satisfaction:.1f}/5.0</h2>
                <div style="color: {NEON_GREEN if satisfaction > 4 else NEON_YELLOW}; font-size: 14px;">
                    {('EXCELLENT' if satisfaction > 4.5 else 'BON' if satisfaction > 4 else 'MOYEN')}
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # Graphique principal
    st.markdown('<h3 class="neon-title" style="font-size: 24px;">📈 ÉVOLUTION QUANTUM</h3>', unsafe_allow_html=True)
    st.plotly_chart(create_cyber_trend_chart(), use_container_width=True)
    
    # Deuxième ligne de métriques
    col5, col6, col7, col8 = st.columns(4)
    
    with col5:
        st.plotly_chart(create_neon_gauge(
            territory_data['Digital_penetration'].mean(), 
            "DIGITAL %", 
            NEON_BLUE
        ), use_container_width=True)
    
    with col6:
        st.plotly_chart(create_neon_gauge(
            territory_data['Tech_score'].mean(), 
            "TECH SCORE", 
            NEON_PURPLE
        ), use_container_width=True)
    
    with col7:
        st.plotly_chart(create_neon_gauge(
            territory_data['Rentabilité'].mean(), 
            "RENTABILITÉ", 
            NEON_GREEN
        ), use_container_width=True)
    
    with col8:
        st.plotly_chart(create_neon_gauge(
            territory_data['Croissance'].mean(), 
            "CROISSANCE", 
            NEON_CYAN
        ), use_container_width=True)

elif "PERFORMANCE" in view:
    
    st.markdown('<h2 class="neon-title">🚀 PERFORMANCE TERRITORIALE</h2>', unsafe_allow_html=True)
    
    # Sélecteur de territoire
    territory_type = st.selectbox(
        "FILTRE TERRITORIAL",
        ["TOUS", "DROM", "COM", "MÉTROPOLE"],
        key="territory_filter"
    )
    
    filtered_data = territory_data if territory_type == "TOUS" else territory_data[territory_data['Type'] == territory_type]
    
    # Top performers
    st.markdown('<h3 style="color: #00fff9; border-left: 4px solid #00fff9; padding-left: 15px;">🏆 TOP PERFORMERS</h3>', unsafe_allow_html=True)
    
    top_cols = st.columns(3)
    
    with top_cols[0]:
        top_ca = filtered_data.nlargest(1, 'Chiffre_affaires')
        if not top_ca.empty:
            st.markdown(f"""
            <div class="data-card">
                <h4 style="color: {NEON_BLUE}; margin: 0 0 10px 0;">📊 MEILLEUR CA</h4>
                <h2 style="color: white; margin: 10px 0;">{top_ca['Territoire'].iloc[0]}</h2>
                <div style="color: {NEON_GREEN}; font-size: 24px; font-weight: bold;">
                    {top_ca['Chiffre_affaires'].iloc[0]:,.0f}€
                </div>
                <div style="color: {NEON_CYAN}; margin-top: 10px;">
                    ↗ +{top_ca['Croissance'].iloc[0]:.1f}% croissance
                </div>
            </div>
            """, unsafe_allow_html=True)
    
    with top_cols[1]:
        top_growth = filtered_data.nlargest(1, 'Croissance')
        if not top_growth.empty:
            st.markdown(f"""
            <div class="data-card">
                <h4 style="color: {NEON_GREEN}; margin: 0 0 10px 0;">🚀 CROISSANCE MAX</h4>
                <h2 style="color: white; margin: 10px 0;">{top_growth['Territoire'].iloc[0]}</h2>
                <div style="color: {NEON_GREEN}; font-size: 24px; font-weight: bold;">
                    +{top_growth['Croissance'].iloc[0]:.1f}%
                </div>
                <div style="color: {NEON_CYAN}; margin-top: 10px;">
                    🎯 CA: {top_growth['Chiffre_affaires'].iloc[0]:,.0f}€
                </div>
            </div>
            """, unsafe_allow_html=True)
    
    with top_cols[2]:
        top_satisfaction = filtered_data.nlargest(1, 'Satisfaction')
        if not top_satisfaction.empty:
            st.markdown(f"""
            <div class="data-card">
                <h4 style="color: {NEON_YELLOW}; margin: 0 0 10px 0;">⭐ SATISFACTION MAX</h4>
                <h2 style="color: white; margin: 10px 0;">{top_satisfaction['Territoire'].iloc[0]}</h2>
                <div style="color: {NEON_YELLOW}; font-size: 24px; font-weight: bold;">
                    {top_satisfaction['Satisfaction'].iloc[0]:.1f}/5.0
                </div>
                <div style="color: {NEON_CYAN}; margin-top: 10px;">
                    📈 Rentabilité: {top_satisfaction['Rentabilité'].iloc[0]:.1f}%
                </div>
            </div>
            """, unsafe_allow_html=True)
    
    # Graphiques 3D et Radar
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown('<h4 style="color: #00f3ff;">🌐 MATRICE 3D DES PERFORMANCES</h4>', unsafe_allow_html=True)
        st.plotly_chart(create_3d_scatter(), use_container_width=True)
    
    with col2:
        st.markdown('<h4 style="color: #00f3ff;">📡 ANALYSE RADAR MULTIDIMENSIONNELLE</h4>', unsafe_allow_html=True)
        st.plotly_chart(create_radar_chart(), use_container_width=True)

elif "ANALYSE" in view:
    
    st.markdown('<h2 class="neon-title">📊 ANALYSE AVANCÉE</h2>', unsafe_allow_html=True)
    
    # Analyse comparative
    st.markdown('<h3 style="color: #b967ff; border-left: 4px solid #b967ff; padding-left: 15px;">🔍 ANALYSE COMPARATIVE</h3>', unsafe_allow_html=True)
    
    # Graphique de comparaison par type
    type_comparison = territory_data.groupby('Type').agg({
        'Chiffre_affaires': 'mean',
        'Croissance': 'mean',
        'Satisfaction': 'mean',
        'Rentabilité': 'mean'
    }).reset_index()
    
    fig = go.Figure()
    
    metrics = ['Chiffre_affaires', 'Croissance', 'Satisfaction', 'Rentabilité']
    for metric in metrics:
        fig.add_trace(go.Bar(
            x=type_comparison['Type'],
            y=type_comparison[metric],
            name=metric.upper(),
            marker_color=[COLORS['drom'], COLORS['com'], COLORS['metro']]
        ))
    
    fig.update_layout(
        title='COMPARAISON PAR TYPE DE TERRITOIRE',
        barmode='group',
        template='plotly_dark',
        paper_bgcolor=COLORS['card_bg'],
        plot_bgcolor=COLORS['card_bg'],
        height=400
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Heatmap de corrélation
    st.markdown('<h3 style="color: #00ff9d; border-left: 4px solid #00ff9d; padding-left: 15px;">🎯 MATRICE DE CORRÉLATION</h3>', unsafe_allow_html=True)
    
    corr_data = territory_data[['Chiffre_affaires', 'Croissance', 'Satisfaction', 'Rentabilité', 'Panier_moyen', 'Digital_penetration', 'Tech_score']].corr()
    
    fig = go.Figure(data=go.Heatmap(
        z=corr_data.values,
        x=corr_data.columns,
        y=corr_data.columns,
        colorscale=[[0, NEON_BLUE], [0.5, NEON_PURPLE], [1, NEON_PINK]],
        showscale=True,
        hoverongaps=False
    ))
    
    fig.update_layout(
        title='ANALYSE DES CORRÉLATIONS',
        height=500,
        template='plotly_dark'
    )
    
    st.plotly_chart(fig, use_container_width=True)

elif "FINANCE" in view:
    
    st.markdown('<h2 class="neon-title">💹 ANALYSE FINANCIÈRE AVANCÉE</h2>', unsafe_allow_html=True)
    
    # Métriques financières détaillées
    col1, col2, col3 = st.columns(3)
    
    with col1:
        marge = ((financial_data['Bénéfice_net'].iloc[-1] / financial_data['Chiffre_d_affaires'].iloc[-1]) * 100) if financial_data['Chiffre_d_affaires'].iloc[-1] > 0 else 0
        st.markdown(f"""
        <div class="data-card">
            <h4 style="color: {NEON_GREEN}; margin: 0 0 10px 0;">💰 MARGE NETTE</h4>
            <h2 style="color: {NEON_GREEN}; margin: 15px 0; font-size: 36px;">{marge:.1f}%</h2>
            <div style="color: {COLORS['text_secondary']};">
                Dernière période
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        roi = 8.2
        st.markdown(f"""
        <div class="data-card">
            <h4 style="color: {NEON_BLUE}; margin: 0 0 10px 0;">📈 ROI MENSUEL</h4>
            <h2 style="color: {NEON_BLUE}; margin: 15px 0; font-size: 36px;">{roi}%</h2>
            <div style="color: {COLORS['text_secondary']};">
                Return on Investment
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        cash = financial_data['Bénéfice_net'].iloc[-1] * 0.3
        st.markdown(f"""
        <div class="data-card">
            <h4 style="color: {NEON_CYAN}; margin: 0 0 10px 0;">🏦 TRÉSORERIE</h4>
            <h2 style="color: {NEON_CYAN}; margin: 15px 0; font-size: 36px;">{cash:,.0f}€</h2>
            <div style="color: {COLORS['text_secondary']};">
                Disponible immédiatement
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # Graphique de prévision
    st.markdown('<h3 style="color: #00fff9; border-left: 4px solid #00fff9; padding-left: 15px;">🔮 PRÉVISION IA</h3>', unsafe_allow_html=True)
    
    # Simulation de prévision
    future_dates = pd.date_range(start=financial_data['Date'].iloc[-1], periods=30, freq='D')
    last_ca = financial_data['Chiffre_d_affaires'].iloc[-1]
    growth_rate = 0.015  # 1.5% de croissance journalière
    
    forecast = []
    for i in range(30):
        forecast.append(last_ca * (1 + growth_rate) ** i)
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=financial_data['Date'],
        y=financial_data['Chiffre_d_affaires'],
        mode='lines',
        name='DONNÉES RÉELLES',
        line=dict(color=NEON_BLUE, width=3)
    ))
    
    fig.add_trace(go.Scatter(
        x=future_dates,
        y=forecast,
        mode='lines',
        name='PRÉVISION IA',
        line=dict(color=NEON_GREEN, width=3, dash='dash')
    ))
    
    fig.update_layout(
        title='PRÉVISION DE CROISSANCE (30 JOURS)',
        template='plotly_dark',
        paper_bgcolor=COLORS['card_bg'],
        plot_bgcolor=COLORS['card_bg'],
        height=400
    )
    
    st.plotly_chart(fig, use_container_width=True)

else:  # ÉQUIPE
    
    st.markdown('<h2 class="neon-title">👥 INTELLIGENCE COLLECTIVE</h2>', unsafe_allow_html=True)
    
    # Statistiques d'équipe
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown(f"""
        <div class="data-card">
            <h4 style="color: {NEON_BLUE}; margin: 0 0 10px 0;">👨‍💼 ÉQUIPE GBH</h4>
            <h2 style="color: white; margin: 15px 0; font-size: 48px;">{financial_data['Effectifs'].iloc[-1]}</h2>
            <div style="color: {COLORS['text_secondary']};">
                Collaborateurs actifs
            </div>
            <div style="margin-top: 20px;">
                <span class="neon-badge">+5% ce mois</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        avg_exp = 4.2
        st.markdown(f"""
        <div class="data-card">
            <h4 style="color: {NEON_GREEN}; margin: 0 0 10px 0;">📚 EXPÉRIENCE MOY.</h4>
            <h2 style="color: {NEON_GREEN}; margin: 15px 0; font-size: 48px;">{avg_exp} ans</h2>
            <div style="color: {COLORS['text_secondary']};">
                Par collaborateur
            </div>
            <div style="margin-top: 20px;">
                <span class="neon-badge">HAUT NIVEAU</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        formation = 85
        st.markdown(f"""
        <div class="data-card">
            <h4 style="color: {NEON_PURPLE}; margin: 0 0 10px 0;">🎓 FORMATION TECH</h4>
            <h2 style="color: {NEON_PURPLE}; margin: 15px 0; font-size: 48px;">{formation}%</h2>
            <div style="color: {COLORS['text_secondary']};">
                Certifiés IA & Data
            </div>
            <div style="margin-top: 20px;">
                <span class="neon-badge">ÉLITE TECH</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # Distribution des compétences
    st.markdown('<h3 style="color: #ff00ff; border-left: 4px solid #ff00ff; padding-left: 15px;">🎯 DISTRIBUTION DES COMPÉTENCES</h3>', unsafe_allow_html=True)
    
    skills = ['IA/ML', 'DATA SCIENCE', 'CYBERSECURITY', 'CLOUD', 'DEVOPS', 'BLOCKCHAIN', 'QUANTUM']
    levels = [85, 78, 92, 88, 76, 65, 45]
    
    fig = go.Figure(data=[go.Bar(
        x=skills,
        y=levels,
        marker_color=[NEON_BLUE, NEON_CYAN, NEON_GREEN, NEON_PURPLE, NEON_PINK, NEON_YELLOW, '#ffffff'],
        marker_line_color='white',
        marker_line_width=1
    )])
    
    fig.update_layout(
        title='COMPÉTENCES TECH DE L\'ÉQUIPE',
        template='plotly_dark',
        paper_bgcolor=COLORS['card_bg'],
        plot_bgcolor=COLORS['card_bg'],
        height=400
    )
    
    st.plotly_chart(fig, use_container_width=True)

# ========== PIED DE PAGE FUTURISTE ==========
st.markdown("""
<div style="margin-top: 50px; padding: 20px; background: rgba(13, 18, 32, 0.8); 
            border-radius: 15px; border: 1px solid rgba(0, 243, 255, 0.3);
            text-align: center;">
    
    <div style="display: flex; justify-content: space-between; align-items: center;">
        <div style="text-align: left;">
            <div style="color: #00f3ff; font-family: 'Courier New'; font-size: 14px;">
                ⚡ SYSTÈME GBH QUANTUM v3.14
            </div>
            <div style="color: rgba(255, 255, 255, 0.5); font-size: 12px; margin-top: 5px;">
                Interface neuronale optimisée
            </div>
        </div>
        
        <div style="text-align: center;">
            <div style="color: #00fff9; font-size: 18px; font-family: 'Courier New';">
                {timestamp}
            </div>
            <div style="color: rgba(255, 255, 255, 0.7); font-size: 12px;">
                Dernière mise à jour
            </div>
        </div>
        
        <div style="text-align: right;">
            <div style="color: #00ff9d; font-family: 'Courier New'; font-size: 14px;">
                🚀 MODE PERFORMANCE ACTIVÉ
            </div>
            <div style="color: rgba(255, 255, 255, 0.5); font-size: 12px; margin-top: 5px;">
                Latence: < 50ms
            </div>
        </div>
    </div>
    
    <div style="margin-top: 20px; padding: 10px; background: rgba(0, 243, 255, 0.1); 
                border-radius: 10px; border: 1px solid rgba(0, 243, 255, 0.2);">
        <div style="color: rgba(255, 255, 255, 0.6); font-size: 11px; letter-spacing: 1px;">
            © 2024 GBH GROUP | SYSTÈME DE GESTION QUANTUM | CONFIDENTIEL NIVEAU 5 | 
            TOUS DROITS RÉSERVÉS | VERSION CYBERPUNK
        </div>
    </div>
</div>
""".format(timestamp=datetime.now().strftime('%d/%m/%Y %H:%M:%S')), unsafe_allow_html=True)

# Bouton de rafraîchissement
if st.button('🔄 RAFRAÎCHIR LES DONNÉES QUANTIQUES', use_container_width=True):
    st.rerun()

# Message de fin
st.balloons()
