# Dashboard.py - Streamlit version
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import streamlit as st
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore')

# Thème couleurs premium
COLORS = {
    'background': '#0F1421',
    'card_bg': '#1A2234',
    'card_border': '#2A3B5C',
    'text_primary': '#FFFFFF',
    'text_secondary': '#B0B8C5',
    'text_muted': '#8A94A6',
    
    # Couleurs territoires
    'drom': '#FF6B6B',
    'com': '#FFA500', 
    'metro': '#00CED1',
    
    # Couleurs fonctionnelles
    'success': '#00D26A',
    'warning': '#FFB800',
    'danger': '#FF4757',
    'info': '#0095FF',
    'primary': '#6C5CE7',
    
    # Dégradés
    'gradient_start': '#667eea',
    'gradient_end': '#764ba2'
}

# Configuration de la page Streamlit
st.set_page_config(
    page_title="GBH Group Dashboard",
    page_icon="🏬",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Appliquer le style CSS personnalisé
st.markdown(f"""
    <style>
    .stApp {{
        background-color: {COLORS['background']};
        color: {COLORS['text_primary']};
    }}
    
    .main-header {{
        background: linear-gradient(135deg, {COLORS['gradient_start']}, {COLORS['gradient_end']});
        border-radius: 15px;
        padding: 30px;
        margin-bottom: 30px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.3);
    }}
    
    .metric-card {{
        background-color: {COLORS['card_bg']};
        border: 1px solid {COLORS['card_border']};
        border-radius: 12px;
        padding: 20px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.2);
    }}
    
    .section-header {{
        border-left: 4px solid {COLORS['primary']};
        padding-left: 15px;
        margin-bottom: 25px;
        margin-top: 10px;
    }}
    </style>
""", unsafe_allow_html=True)

# Fonctions pour générer des données de démonstration
def generate_sample_data():
    """Générer des données de démonstration si NinjaGBHData n'est pas disponible"""
    
    # Données financières
    dates = pd.date_range(start='2024-01-01', end='2024-03-15', freq='D')
    financial_data = pd.DataFrame({
        'Date': dates,
        'Chiffre_d_affaires': np.cumsum(np.random.normal(50000, 10000, len(dates))) + 1000000,
        'Bénéfice_net': np.cumsum(np.random.normal(5000, 1000, len(dates))) + 100000,
        'Effectifs': np.random.randint(200, 300, len(dates)),
        'Nbre_magasins': np.random.randint(45, 55, len(dates)),
        'Satisfaction_client': np.random.uniform(3.5, 4.8, len(dates)),
        'Panier_moyen': np.random.uniform(45, 85, len(dates)),
        'Investissements': np.random.choice([0, 50000, 100000, 150000], len(dates), p=[0.7, 0.15, 0.1, 0.05])
    })
    
    # Données territoriales
    territories = {
        'DROM': ['Martinique', 'Guadeloupe', 'Guyane', 'Réunion', 'Mayotte'],
        'COM': ['Polynésie', 'Nouvelle-Calédonie', 'Wallis-et-Futuna', 'Saint-Pierre-et-Miquelon'],
        'Métropole': ['Île-de-France', 'Auvergne-Rhône-Alpes', 'Occitanie', 'Nouvelle-Aquitaine', 
                     'Hauts-de-France', 'Provence-Alpes-Côte d\'Azur', 'Grand Est', 'Normandie']
    }
    
    territory_rows = []
    for ter_type, ter_list in territories.items():
        for ter in ter_list:
            territory_rows.append({
                'Territoire': ter,
                'Type': ter_type,
                'Chiffre_affaires': np.random.uniform(50000, 500000),
                'Croissance': np.random.uniform(5, 25),
                'Satisfaction': np.random.uniform(3.5, 4.9),
                'Part_marche': np.random.uniform(15, 45),
                'Panier_moyen': np.random.uniform(40, 90),
                'Rentabilité': np.random.uniform(8, 22),
                'Magasins': np.random.randint(2, 15),
                'Nouveaux_clients_mois': np.random.randint(50, 500)
            })
    
    territory_data = pd.DataFrame(territory_rows)
    
    # Statistiques magasins
    store_stats = pd.DataFrame({
        'Type': ['DROM', 'COM', 'Métropole'],
        'Nombre_Magasins': [territory_data[territory_data['Type'] == 'DROM']['Magasins'].sum(),
                           territory_data[territory_data['Type'] == 'COM']['Magasins'].sum(),
                           territory_data[territory_data['Type'] == 'Métropole']['Magasins'].sum()]
    })
    
    # Résumé KPI
    kpi_summary = {
        'total_territoires': len(territory_data),
        'total_magasins': store_stats['Nombre_Magasins'].sum()
    }
    
    # Transactions
    transactions = []
    transaction_types = ['Vente', 'Retour', 'Remise', 'Service']
    categories = ['Électronique', 'Alimentation', 'Vêtements', 'Maison', 'Sport']
    
    for i in range(50):
        transactions.append({
            'Date': (datetime.now() - timedelta(days=np.random.randint(0, 30))).strftime('%Y-%m-%d'),
            'Type': np.random.choice(transaction_types),
            'Catégorie': np.random.choice(categories),
            'Territoire': np.random.choice(territory_data['Territoire'].tolist()),
            'Type_Territoire': territory_data[territory_data['Territoire'] == _]['Type'].iloc[0] if _ in territory_data['Territoire'].values else np.random.choice(['DROM', 'COM', 'Métropole']),
            'Montant': np.random.uniform(10, 500) * (1 if np.random.random() > 0.2 else -1)
        })
    
    return financial_data, territory_data, store_stats, kpi_summary, transactions

# Charger les données
try:
    from NinjaGBHData import NinjaGBHDataSimulator
    ninja_simulator = NinjaGBHDataSimulator()
    COLORS.update(ninja_simulator.territory_colors)
    financial_data = ninja_simulator.generate_financial_data()
    territory_data = ninja_simulator.generate_territory_performance()
    store_stats = ninja_simulator.get_store_statistics()
    kpi_summary = ninja_simulator.get_kpi_summary()
    transactions_data = ninja_simulator.generate_real_transactions(15)
    print("✅ Données NinjaGBH chargées avec succès")
except Exception as e:
    print(f"⚠️ NinjaGBHData non disponible, utilisation des données de démo: {e}")
    financial_data, territory_data, store_stats, kpi_summary, transactions_data = generate_sample_data()

# Fonctions de création de graphiques
def create_financial_trend_chart():
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=financial_data['Date'],
        y=financial_data['Chiffre_d_affaires'],
        mode='lines',
        name='CA Cumulé',
        line=dict(color=COLORS['success'], width=3),
        fill='tozeroy',
        fillcolor=f'rgba({int(COLORS["success"][1:3], 16)}, {int(COLORS["success"][3:5], 16)}, {int(COLORS["success"][5:7], 16)}, 0.1)'
    ))
    
    fig.add_trace(go.Scatter(
        x=financial_data['Date'],
        y=financial_data['Bénéfice_net'],
        mode='lines',
        name='Bénéfice Net',
        line=dict(color=COLORS['primary'], width=2)
    ))
    
    fig.update_layout(
        title='Évolution Financière GBH Group',
        xaxis_title='Date',
        yaxis_title='Montant (€)',
        template='plotly_dark',
        paper_bgcolor=COLORS['card_bg'],
        plot_bgcolor=COLORS['card_bg'],
        height=400
    )
    
    return fig

def create_territory_breakdown_chart():
    drom_ca = territory_data[territory_data['Type'] == 'DROM']['Chiffre_affaires'].sum()
    com_ca = territory_data[territory_data['Type'] == 'COM']['Chiffre_affaires'].sum()
    metro_ca = territory_data[territory_data['Type'] == 'Métropole']['Chiffre_affaires'].sum()
    
    fig = go.Figure(data=[go.Pie(
        labels=['DROM', 'COM', 'Métropole'],
        values=[drom_ca, com_ca, metro_ca],
        hole=0.6,
        marker=dict(colors=[COLORS['drom'], COLORS['com'], COLORS['metro']]),
        textinfo='label+percent'
    )])
    
    fig.update_layout(
        title='Répartition du CA par Zone',
        template='plotly_dark',
        paper_bgcolor=COLORS['card_bg'],
        plot_bgcolor=COLORS['card_bg'],
        height=400,
        showlegend=False
    )
    
    return fig

# Interface principale
st.markdown(f"""
<div class="main-header">
    <h1 style="color: white; font-weight: 700;">🏬 GBH GROUP</h1>
    <h4 style="color: #B0B8C5; font-weight: 300;">Tableau de Bord Exécutif</h4>
    <div style="text-align: center; margin-top: 15px;">
        <span style="font-size: 24px; margin-right: 10px;">🌍</span>
        <span style="color: white; font-weight: 600;">{kpi_summary.get('total_territoires', len(territory_data))} Territoires</span>
        <span style="color: #8A94A6;"> • </span>
        <span style="color: white; font-weight: 600;">{kpi_summary.get('total_magasins', territory_data['Magasins'].sum())} Magasins</span>
    </div>
</div>
""", unsafe_allow_html=True)

# Navigation
view = st.radio(
    "Navigation",
    ["📊 Vue d'Ensemble", "🏝️ Analyse DROM", "🏖️ Analyse COM", "🏙️ Analyse Métropole", "📈 Performance Financière"],
    horizontal=True,
    label_visibility="collapsed"
)

st.markdown("---")

if "Vue d'Ensemble" in view:
    # KPI Principaux
    latest = financial_data.iloc[-1]
    
    col1, col2, col3, col4, col5, col6 = st.columns(6)
    
    with col1:
        st.metric("Chiffre d'Affaires", f"{latest['Chiffre_d_affaires']:,.0f}€", 
                 delta=f"{latest['Chiffre_d_affaires'] - financial_data.iloc[-2]['Chiffre_d_affaires']:,.0f}€/jour")
    
    with col2:
        st.metric("Bénéfice Net", f"{latest['Bénéfice_net']:,.0f}€",
                 delta=f"{latest['Bénéfice_net'] - financial_data.iloc[-2]['Bénéfice_net']:,.0f}€/jour")
    
    with col3:
        st.metric("Effectifs", f"{latest['Effectifs']:.0f}", "Employés")
    
    with col4:
        st.metric("Magasins", f"{latest['Nbre_magasins']:.0f}", "Points de vente")
    
    with col5:
        st.metric("Satisfaction", f"{latest['Satisfaction_client']:.1f}/5.0")
    
    with col6:
        st.metric("Panier Moyen", f"{latest['Panier_moyen']:.1f}€")
    
    # Graphiques
    st.subheader("📈 Évolution Financière - Vue Globale")
    st.plotly_chart(create_financial_trend_chart(), use_container_width=True)
    
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("🌍 Répartition Territoriale")
        st.plotly_chart(create_territory_breakdown_chart(), use_container_width=True)
    
    with col2:
        st.subheader("🏆 Top 5 Territoires")
        top_5 = territory_data.nlargest(5, 'Chiffre_affaires')
        fig = go.Figure(data=[go.Bar(
            x=top_5['Territoire'],
            y=top_5['Chiffre_affaires'],
            marker_color=[COLORS['drom'] if t == 'DROM' else COLORS['com'] if t == 'COM' else COLORS['metro'] 
                         for t in top_5['Type']]
        )])
        fig.update_layout(
            template='plotly_dark',
            paper_bgcolor=COLORS['card_bg'],
            plot_bgcolor=COLORS['card_bg'],
            height=400
        )
        st.plotly_chart(fig, use_container_width=True)
    
    # Transactions récentes
    st.subheader("💳 Transactions Récentes")
    transactions_df = pd.DataFrame(transactions_data)
    st.dataframe(transactions_df.head(10), use_container_width=True)

elif "DROM" in view:
    drom_data = territory_data[territory_data['Type'] == 'DROM']
    
    st.subheader(f"🏝️ Analyse DROM ({len(drom_data)} territoires)")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("CA Total", f"{drom_data['Chiffre_affaires'].sum():,.0f}€")
    
    with col2:
        st.metric("Croissance Moy", f"+{drom_data['Croissance'].mean():.1f}%")
    
    with col3:
        st.metric("Satisfaction", f"{drom_data['Satisfaction'].mean():.1f}/5")
    
    with col4:
        st.metric("Part de Marché", f"{drom_data['Part_marche'].mean():.1f}%")
    
    # Graphique DROM
    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=drom_data['Territoire'],
        y=drom_data['Chiffre_affaires'],
        name='CA',
        marker_color=COLORS['drom']
    ))
    fig.update_layout(
        title='Performance des Territoires DROM',
        template='plotly_dark',
        paper_bgcolor=COLORS['card_bg'],
        plot_bgcolor=COLORS['card_bg'],
        height=400
    )
    st.plotly_chart(fig, use_container_width=True)

elif "COM" in view:
    com_data = territory_data[territory_data['Type'] == 'COM']
    
    st.subheader(f"🏖️ Analyse COM ({len(com_data)} territoires)")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("CA Total", f"{com_data['Chiffre_affaires'].sum():,.0f}€")
    
    with col2:
        st.metric("Croissance", f"+{com_data['Croissance'].mean():.1f}%")
    
    with col3:
        st.metric("Panier Moyen", f"{com_data['Panier_moyen'].mean():.1f}€")
    
    with col4:
        st.metric("Rentabilité", f"{com_data['Rentabilité'].mean():.1f}%")
    
    # Graphique COM
    fig = go.Figure(data=[go.Bar(
        x=com_data['Territoire'],
        y=com_data['Chiffre_affaires'],
        marker_color=COLORS['com']
    )])
    fig.update_layout(
        title='Performance des Territoires COM',
        template='plotly_dark',
        paper_bgcolor=COLORS['card_bg'],
        plot_bgcolor=COLORS['card_bg'],
        height=400
    )
    st.plotly_chart(fig, use_container_width=True)

elif "Métropole" in view:
    metro_data = territory_data[territory_data['Type'] == 'Métropole']
    
    st.subheader(f"🏙️ Analyse Métropole ({len(metro_data)} régions)")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("CA Total", f"{metro_data['Chiffre_affaires'].sum():,.0f}€")
    
    with col2:
        st.metric("Part du CA Total", f"{(metro_data['Chiffre_affaires'].sum() / territory_data['Chiffre_affaires'].sum() * 100):.1f}%")
    
    with col3:
        st.metric("Magasins/Région", f"{metro_data['Magasins'].sum() / len(metro_data):.1f}")
    
    with col4:
        st.metric("Nouveaux Clients", f"{metro_data['Nouveaux_clients_mois'].sum():,}/mois")
    
    # Graphique Métropole
    metro_sorted = metro_data.sort_values('Chiffre_affaires')
    fig = go.Figure(data=[go.Bar(
        y=metro_sorted['Territoire'],
        x=metro_sorted['Chiffre_affaires'],
        orientation='h',
        marker_color=COLORS['metro']
    )])
    fig.update_layout(
        title='Performance par Région Métropolitaine',
        template='plotly_dark',
        paper_bgcolor=COLORS['card_bg'],
        plot_bgcolor=COLORS['card_bg'],
        height=500
    )
    st.plotly_chart(fig, use_container_width=True)

else:  # Performance Financière
    st.subheader("📈 Analyse Financière Détaillée")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        profit_margin = ((financial_data['Bénéfice_net'].iloc[-1] - financial_data['Bénéfice_net'].iloc[-2]) / 
                        (financial_data['Chiffre_d_affaires'].iloc[-1] - financial_data['Chiffre_d_affaires'].iloc[-2]) * 100) if len(financial_data) > 1 else 12.5
        st.metric("Marge Nette", f"{profit_margin:.1f}%")
    
    with col2:
        st.metric("ROI Mensuel", "8.2%")
    
    with col3:
        st.metric("Trésorerie", f"{financial_data['Bénéfice_net'].iloc[-1] * 0.3:,.0f}€")
    
    with col4:
        st.metric("Dettes", f"{financial_data['Investissements'].sum() * 0.6:,.0f}€")
    
    # Graphique de rentabilité
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=financial_data['Date'],
        y=financial_data['Chiffre_d_affaires'],
        name='CA',
        line=dict(color=COLORS['success'])
    ))
    fig.add_trace(go.Scatter(
        x=financial_data['Date'],
        y=financial_data['Bénéfice_net'],
        name='Bénéfice',
        line=dict(color=COLORS['primary'])
    ))
    fig.update_layout(
        title='Évolution CA vs Bénéfices',
        template='plotly_dark',
        paper_bgcolor=COLORS['card_bg'],
        plot_bgcolor=COLORS['card_bg'],
        height=400
    )
    st.plotly_chart(fig, use_container_width=True)

# Pied de page
st.markdown("---")
st.caption(f"Dernière mise à jour: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')} • GBH Group Dashboard Premium v2.0")

if st.button("🔄 Rafraîchir les données"):
    st.rerun()
