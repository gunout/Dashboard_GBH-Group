import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

# Import du simulateur
from NinjaGBHData import NinjaGBHDataSimulator

# Configuration de la page
st.set_page_config(
    page_title="GBH Group Dashboard Premium",
    page_icon="🏬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Thème couleurs
COLORS = {
    'drom': '#FF6B6B',
    'com': '#FFA500', 
    'metro': '#00CED1',
    'success': '#00D26A',
    'warning': '#FFB800',
    'primary': '#6C5CE7'
}

# Cache des données pour de meilleures performances
@st.cache_resource
def get_simulator():
    return NinjaGBHDataSimulator()

@st.cache_data(ttl=3600)  # Cache pour 1 heure
def get_data():
    simulator = get_simulator()
    financial_data = simulator.generate_financial_data()
    territory_data = simulator.generate_territory_performance()
    kpi_summary = simulator.get_kpi_summary()
    transactions = simulator.generate_real_transactions(20)
    return financial_data, territory_data, kpi_summary, transactions

# Initialisation
ninja_simulator = get_simulator()
financial_data, territory_data, kpi_summary, transactions_data = get_data()

# CSS personnalisé
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: 700;
        background: linear-gradient(135deg, #667eea, #764ba2);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        margin-bottom: 0;
    }
    .metric-card {
        background-color: #1A2234;
        padding: 20px;
        border-radius: 12px;
        border: 1px solid #2A3B5C;
        text-align: center;
    }
    .section-header {
        border-left: 4px solid #6C5CE7;
        padding-left: 15px;
        margin: 30px 0 20px 0;
    }
</style>
""", unsafe_allow_html=True)

# Header principal
st.markdown('<h1 class="main-header">🏬 GBH GROUP</h1>', unsafe_allow_html=True)
st.markdown("### Tableau de Bord Exécutif Premium - Tous Territoires")

# KPI Principaux en haut
st.markdown("---")
col1, col2, col3, col4, col5, col6 = st.columns(6)

with col1:
    st.metric(
        "💰 Chiffre d'Affaires",
        f"{financial_data['Chiffre_d_affaires'].iloc[-1]:,.0f}€".replace(',', ' '),
        delta=f"+{((financial_data['Chiffre_d_affaires'].iloc[-1] - financial_data['Chiffre_d_affaires'].iloc[-2]) / financial_data['Chiffre_d_affaires'].iloc[-2] * 100):.1f}%" if len(financial_data) > 1 else "+5.2%"
    )

with col2:
    st.metric(
        "💼 Bénéfice Net", 
        f"{financial_data['Bénéfice_net'].iloc[-1]:,.0f}€".replace(',', ' '),
        delta="+12.8%"
    )

with col3:
    st.metric(
        "👥 Effectifs", 
        f"{financial_data['Effectifs'].iloc[-1]:.0f}",
        delta="+2.3%"
    )

with col4:
    st.metric(
        "🏪 Magasins", 
        f"{financial_data['Nbre_magasins'].iloc[-1]:.0f}",
        delta="+1"
    )

with col5:
    st.metric(
        "⭐ Satisfaction", 
        f"{financial_data['Satisfaction_client'].iloc[-1]:.1f}/5.0"
    )

with col6:
    st.metric(
        "🛒 Panier Moyen", 
        f"{financial_data['Panier_moyen'].iloc[-1]:.1f}€",
        delta="+3.5%"
    )

st.markdown("---")

# Navigation par onglets
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📊 Vue Globale", 
    "🏝️ Analyse DROM", 
    "🏖️ Analyse COM", 
    "🏙️ Analyse Métropole",
    "📈 Performance Financière"
])

with tab1:
    st.markdown('<h2 class="section-header">📈 Vue d\'Ensemble GBH Group</h2>', unsafe_allow_html=True)
    
    # Graphiques principaux
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # Évolution financière
        fig_finance = go.Figure()
        fig_finance.add_trace(go.Scatter(
            x=financial_data['Date'],
            y=financial_data['Chiffre_d_affaires'],
            mode='lines',
            name='CA Cumulé',
            line=dict(color=COLORS['success'], width=4),
            fill='tozeroy',
            fillcolor=f'rgba(0, 210, 106, 0.1)'
        ))
        fig_finance.add_trace(go.Scatter(
            x=financial_data['Date'],
            y=financial_data['Bénéfice_net'],
            mode='lines',
            name='Bénéfice Net',
            line=dict(color=COLORS['primary'], width=3)
        ))
        fig_finance.update_layout(
            title='Évolution Financière GBH Group',
            template='plotly_dark',
            height=400,
            showlegend=True
        )
        st.plotly_chart(fig_finance, use_container_width=True)
    
    with col2:
        # Répartition territoriale
        drom_ca = territory_data[territory_data['Type'] == 'DROM']['Chiffre_affaires'].sum()
        com_ca = territory_data[territory_data['Type'] == 'COM']['Chiffre_affaires'].sum()
        metro_ca = territory_data[territory_data['Type'] == 'Métropole']['Chiffre_affaires'].sum()
        
        fig_pie = go.Figure(data=[go.Pie(
            labels=['DROM', 'COM', 'Métropole'],
            values=[drom_ca, com_ca, metro_ca],
            hole=0.6,
            marker_colors=[COLORS['drom'], COLORS['com'], COLORS['metro']],
            textinfo='label+percent'
        )])
        fig_pie.update_layout(
            title='Répartition du CA par Zone',
            template='plotly_dark',
            height=400,
            annotations=[dict(
                text=f"Total<br>{drom_ca + com_ca + metro_ca:,.0f}€".replace(',', ' '),
                x=0.5, y=0.5, font_size=16, showarrow=False
            )]
        )
        st.plotly_chart(fig_pie, use_container_width=True)
    
    # Performance par territoire
    st.markdown('<h3 class="section-header">🏆 Performance par Territoire</h3>', unsafe_allow_html=True)
    
    territory_sorted = territory_data.sort_values('Chiffre_affaires', ascending=True)
    fig_performance = go.Figure()
    
    color_map = {'DROM': COLORS['drom'], 'COM': COLORS['com'], 'Métropole': COLORS['metro']}
    
    for ter_type in territory_sorted['Type'].unique():
        df_type = territory_sorted[territory_sorted['Type'] == ter_type]
        fig_performance.add_trace(go.Bar(
            y=df_type['Territoire'],
            x=df_type['Chiffre_affaires'],
            name=ter_type,
            orientation='h',
            marker_color=color_map[ter_type],
            text=df_type['Chiffre_affaires'].apply(lambda x: f'{x:,.0f}€'),
            textposition='auto'
        ))
    
    fig_performance.update_layout(
        title='Performance Détaillée par Territoire',
        template='plotly_dark',
        height=500,
        showlegend=True
    )
    st.plotly_chart(fig_performance, use_container_width=True)

with tab2:
    st.markdown('<h2 class="section-header">🏝️ Analyse DROM</h2>', unsafe_allow_html=True)
    
    drom_data = territory_data[territory_data['Type'] == 'DROM']
    
    # KPI DROM
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Territoires DROM", f"{len(drom_data)}")
    with col2:
        st.metric("CA Total", f"{drom_data['Chiffre_affaires'].sum():,.0f}€".replace(',', ' '))
    with col3:
        st.metric("Croissance Moyenne", f"+{drom_data['Croissance'].mean():.1f}%")
    with col4:
        st.metric("Satisfaction Moyenne", f"{drom_data['Satisfaction'].mean():.1f}/5")
    
    # Graphiques DROM
    col1, col2 = st.columns(2)
    
    with col1:
        fig_drom_bar = go.Figure(data=[go.Bar(
            x=drom_data['Territoire'],
            y=drom_data['Chiffre_affaires'],
            marker_color=COLORS['drom'],
            text=drom_data['Chiffre_affaires'].apply(lambda x: f'{x:,.0f}€')
        )])
        fig_drom_bar.update_layout(
            title='Chiffre d\'Affaires par Territoire DROM',
            template='plotly_dark',
            height=400
        )
        st.plotly_chart(fig_drom_bar, use_container_width=True)
    
    with col2:
        fig_drom_radar = go.Figure()
        fig_drom_radar.add_trace(go.Scatterpolar(
            r=[drom_data['Croissance'].mean(), drom_data['Satisfaction'].mean()*20, 
               drom_data['Rentabilité'].mean(), drom_data['Part_marche'].mean()/5],
            theta=['Croissance', 'Satisfaction', 'Rentabilité', 'Part de Marché'],
            fill='toself',
            name='Performance DROM',
            line_color=COLORS['drom']
        ))
        fig_drom_radar.update_layout(
            title='Indicateurs de Performance DROM',
            template='plotly_dark',
            height=400,
            polar=dict(radialaxis=dict(visible=True, range=[0, 25]))
        )
        st.plotly_chart(fig_drom_radar, use_container_width=True)

with tab3:
    st.markdown('<h2 class="section-header">🏖️ Analyse COM</h2>', unsafe_allow_html=True)
    
    com_data = territory_data[territory_data['Type'] == 'COM']
    
    # KPI COM
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Territoires COM", f"{len(com_data)}")
    with col2:
        st.metric("CA Total", f"{com_data['Chiffre_affaires'].sum():,.0f}€".replace(',', ' '))
    with col3:
        st.metric("Panier Moyen", f"{com_data['Panier_moyen'].mean():.1f}€")
    with col4:
        st.metric("Rentabilité Moyenne", f"{com_data['Rentabilité'].mean():.1f}%")
    
    # Graphique COM
    fig_com = go.Figure(data=[go.Bar(
        x=com_data['Territoire'],
        y=com_data['Chiffre_affaires'],
        marker_color=COLORS['com'],
        text=com_data['Chiffre_affaires'].apply(lambda x: f'{x:,.0f}€'),
        textposition='auto'
    )])
    fig_com.update_layout(
        title='Performance des Territoires COM',
        template='plotly_dark',
        height=400
    )
    st.plotly_chart(fig_com, use_container_width=True)
    
    # Tableau détaillé COM
    st.dataframe(
        com_data[['Territoire', 'Chiffre_affaires', 'Croissance', 'Satisfaction', 'Panier_moyen']],
        use_container_width=True
    )

with tab4:
    st.markdown('<h2 class="section-header">🏙️ Analyse Métropole</h2>', unsafe_allow_html=True)
    
    metro_data = territory_data[territory_data['Type'] == 'Métropole']
    
    # KPI Métropole
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Régions", f"{len(metro_data)}")
    with col2:
        st.metric("CA Total", f"{metro_data['Chiffre_affaires'].sum():,.0f}€".replace(',', ' '))
    with col3:
        st.metric("Part du CA Total", f"{(metro_data['Chiffre_affaires'].sum() / territory_data['Chiffre_affaires'].sum() * 100):.1f}%")
    with col4:
        st.metric("Nouveaux Clients/mois", f"{metro_data['Nouveaux_clients_mois'].sum():,}")
    
    # Graphique Métropole
    metro_sorted = metro_data.sort_values('Chiffre_affaires', ascending=True)
    fig_metro = go.Figure(data=[go.Bar(
        y=metro_sorted['Territoire'],
        x=metro_sorted['Chiffre_affaires'],
        orientation='h',
        marker_color=COLORS['metro'],
        text=metro_sorted['Chiffre_affaires'].apply(lambda x: f'{x:,.0f}€'),
        textposition='auto'
    )])
    fig_metro.update_layout(
        title='Performance par Région Métropolitaine',
        template='plotly_dark',
        height=500
    )
    st.plotly_chart(fig_metro, use_container_width=True)

with tab5:
    st.markdown('<h2 class="section-header">📈 Analyse Financière Détaillée</h2>', unsafe_allow_html=True)
    
    # KPI Financiers
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        daily_margin = ((financial_data['Bénéfice_net'].iloc[-1] - financial_data['Bénéfice_net'].iloc[-2]) / 
                       (financial_data['Chiffre_d_affaires'].iloc[-1] - financial_data['Chiffre_d_affaires'].iloc[-2]) * 100) if len(financial_data) > 1 else 12.5
        st.metric("Marge Nette Journalière", f"{daily_margin:.1f}%")
    
    with col2:
        st.metric("ROI Mensuel", "8.2%")
    
    with col3:
        st.metric("Trésorerie Disponible", f"{(financial_data['Bénéfice_net'].iloc[-1] * 0.3):,.0f}€".replace(',', ' '))
    
    with col4:
        st.metric("Investissements Total", f"{financial_data['Investissements'].sum():,.0f}€".replace(',', ' '))
    
    # Graphiques financiers
    col1, col2 = st.columns(2)
    
    with col1:
        # Productivité et satisfaction
        fig_metrics = go.Figure()
        fig_metrics.add_trace(go.Scatter(
            x=financial_data['Date'],
            y=financial_data['Productivité'],
            name='Productivité',
            line=dict(color=COLORS['success'], width=3)
        ))
        fig_metrics.add_trace(go.Scatter(
            x=financial_data['Date'],
            y=financial_data['Satisfaction_client'] * 20,
            name='Satisfaction (x20)',
            line=dict(color=COLORS['warning'], width=3),
            yaxis='y2'
        ))
        fig_metrics.update_layout(
            title='Productivité vs Satisfaction Clients',
            template='plotly_dark',
            height=400,
            yaxis2=dict(
                title='Satisfaction',
                overlaying='y',
                side='right',
                range=[0, 100]
            )
        )
        st.plotly_chart(fig_metrics, use_container_width=True)
    
    with col2:
        # Nouveaux clients
        fig_clients = go.Figure(data=[go.Scatter(
            x=financial_data['Date'],
            y=financial_data['Nouveaux_clients'],
            mode='lines+markers',
            line=dict(color=COLORS['primary'], width=3),
            marker=dict(size=4)
        )])
        fig_clients.update_layout(
            title='Évolution des Nouveaux Clients',
            template='plotly_dark',
            height=400
        )
        st.plotly_chart(fig_clients, use_container_width=True)

# Transactions récentes
st.markdown("---")
st.markdown('<h2 class="section-header">💳 Transactions Récentes</h2>', unsafe_allow_html=True)

# Convertir les transactions en DataFrame pour un meilleur affichage
transactions_df = pd.DataFrame(transactions_data)
if not transactions_df.empty:
    st.dataframe(
        transactions_df,
        use_container_width=True,
        height=400
    )

# Footer
st.markdown("---")
st.markdown(
    f"""
    <div style='text-align: center; color: #666;'>
        <p>🔄 Dernière mise à jour: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')} | 
        GBH Group Dashboard Premium v2.0 | 
        <em>Powered by Streamlit</em></p>
    </div>
    """, 
    unsafe_allow_html=True
)

# Bouton de rafraîchissement dans la sidebar
with st.sidebar:
    st.title("🔧 Contrôles")
    if st.button("🔄 Actualiser les Données"):
        st.cache_data.clear()
        st.cache_resource.clear()
        st.rerun()
    
    st.markdown("---")
    st.subheader("📊 Statistiques Globales")
    st.metric("Total Territoires", kpi_summary['total_territoires'])
    st.metric("Total Magasins", kpi_summary['total_magasins'])
    st.metric("Satisfaction Moyenne", f"{kpi_summary['satisfaction_moyenne']:.1f}/5")
    st.metric("Croissance Moyenne", f"+{kpi_summary['croissance_moyenne']:.1f}%")