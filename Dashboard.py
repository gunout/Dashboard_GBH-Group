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

# Importer notre simulateur premium
from NinjaGBHData import NinjaGBHDataSimulator

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

# Initialisation
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
        transition: all 0.3s ease;
    }}
    
    .metric-card:hover {{
        transform: translateY(-5px);
        box-shadow: 0 8px 25px rgba(0,0,0,0.3);
    }}
    
    .section-header {{
        border-left: 4px solid {COLORS['primary']};
        padding-left: 15px;
        margin-bottom: 25px;
        margin-top: 10px;
    }}
    
    .stButton > button {{
        background-color: {COLORS['primary']};
        color: white;
        border: none;
        border-radius: 8px;
        padding: 10px 20px;
        font-weight: 600;
        transition: all 0.3s ease;
    }}
    
    .stButton > button:hover {{
        background-color: {COLORS['primary']};
        opacity: 0.9;
        transform: translateY(-2px);
    }}
    
    .active-tab {{
        background-color: {COLORS['primary']} !important;
        border-color: {COLORS['primary']} !important;
        box-shadow: 0 0 0 0.2rem {COLORS['primary']}44 !important;
    }}
    </style>
""", unsafe_allow_html=True)

@st.cache_resource
def init_data():
    """Initialiser les données une seule fois"""
    print("🎨 Initialisation du Dashboard GBH Premium...")
    ninja_simulator = NinjaGBHDataSimulator()
    COLORS.update(ninja_simulator.territory_colors)
    
    financial_data = ninja_simulator.generate_financial_data()
    territory_data = ninja_simulator.generate_territory_performance()
    store_stats = ninja_simulator.get_store_statistics()
    kpi_summary = ninja_simulator.get_kpi_summary()
    transactions_data = ninja_simulator.generate_real_transactions(15)
    
    return ninja_simulator, financial_data, territory_data, store_stats, kpi_summary, transactions_data

# Initialiser les données
ninja_simulator, financial_data, territory_data, store_stats, kpi_summary, transactions_data = init_data()

# Fonctions de création de graphiques
def create_financial_trend_chart():
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=financial_data['Date'],
        y=financial_data['Chiffre_d_affaires'],
        mode='lines',
        name='CA Cumulé',
        line=dict(color=COLORS['success'], width=4, shape='spline'),
        fill='tozeroy',
        fillcolor=f'rgba({int(COLORS["success"][1:3], 16)}, {int(COLORS["success"][3:5], 16)}, {int(COLORS["success"][5:7], 16)}, 0.1)'
    ))
    
    fig.add_trace(go.Scatter(
        x=financial_data['Date'],
        y=financial_data['Bénéfice_net'],
        mode='lines',
        name='Bénéfice Net',
        line=dict(color=COLORS['primary'], width=3, shape='spline')
    ))
    
    fig.update_layout(
        title=dict(
            text='Évolution Financière GBH Group',
            x=0.5,
            font=dict(color=COLORS['text_primary'], size=18)
        ),
        xaxis=dict(
            title='Date',
            gridcolor=COLORS['card_border'],
            tickfont=dict(color=COLORS['text_secondary'])
        ),
        yaxis=dict(
            title='Montant (€)',
            gridcolor=COLORS['card_border'],
            tickformat=',.0f',
            tickfont=dict(color=COLORS['text_secondary'])
        ),
        template='plotly_dark',
        paper_bgcolor=COLORS['card_bg'],
        plot_bgcolor=COLORS['card_bg'],
        font=dict(color=COLORS['text_secondary']),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1,
            bgcolor=COLORS['card_bg'],
            bordercolor=COLORS['card_border']
        ),
        hovermode='x unified',
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
        textinfo='label+percent',
        insidetextorientation='radial',
        hovertemplate='<b>%{label}</b><br>CA: %{value:,.0f}€<br>Part: %{percent}<extra></extra>',
        textfont=dict(color=COLORS['text_primary'], size=12)
    )])
    
    fig.update_layout(
        title=dict(
            text='Répartition du CA par Zone',
            x=0.5,
            font=dict(color=COLORS['text_primary'], size=16)
        ),
        template='plotly_dark',
        paper_bgcolor=COLORS['card_bg'],
        plot_bgcolor=COLORS['card_bg'],
        font=dict(color=COLORS['text_secondary']),
        height=400,
        showlegend=False,
        annotations=[dict(
            text=f"Total<br>{drom_ca + com_ca + metro_ca:,.0f}€".replace(',', ' '),
            x=0.5, y=0.5,
            font=dict(size=16, color=COLORS['text_primary']),
            showarrow=False
        )]
    )
    
    return fig

def create_territory_performance_chart():
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
            marker_color=color_map[ter_type],
            text=df_type.apply(lambda x: f"{x['Chiffre_affaires']:,.0f}€<br>(+{x['Croissance']:.1f}%)", axis=1),
            textposition='auto',
            hovertemplate='<b>%{y}</b><br>CA: %{x:,.0f}€<br>Croissance: +%{customdata[0]:.1f}%<br>Satisfaction: %{customdata[1]:.1f}/5<extra></extra>',
            customdata=df_type[['Croissance', 'Satisfaction']].values
        ))
    
    fig.update_layout(
        title=dict(
            text='Performance Détaillée par Territoire',
            x=0.5,
            font=dict(color=COLORS['text_primary'], size=18)
        ),
        xaxis=dict(
            title='Chiffre d\'affaires (€)',
            gridcolor=COLORS['card_border'],
            tickformat=',.0f',
            tickfont=dict(color=COLORS['text_secondary'])
        ),
        yaxis=dict(
            title='Territoire',
            gridcolor=COLORS['card_border'],
            tickfont=dict(color=COLORS['text_secondary'])
        ),
        template='plotly_dark',
        paper_bgcolor=COLORS['card_bg'],
        plot_bgcolor=COLORS['card_bg'],
        font=dict(color=COLORS['text_secondary']),
        height=450,
        barmode='group',
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1,
            bgcolor=COLORS['card_bg']
        )
    )
    
    return fig

def create_type_comparison_chart():
    type_metrics = territory_data.groupby('Type').agg({
        'Chiffre_affaires': 'mean',
        'Satisfaction': 'mean',
        'Rentabilité': 'mean',
        'Panier_moyen': 'mean'
    }).reset_index()
    
    fig = go.Figure(data=[
        go.Bar(
            name='CA Moyen (M€)',
            x=type_metrics['Type'],
            y=type_metrics['Chiffre_affaires'] / 1000000,
            marker_color=[COLORS['drom'], COLORS['com'], COLORS['metro']],
            text=type_metrics['Chiffre_affaires'].apply(lambda x: f'{x/1000000:.1f}M'),
            textposition='auto'
        )
    ])
    
    fig.update_layout(
        title=dict(
            text='CA Moyen par Type (M€)',
            x=0.5,
            font=dict(color=COLORS['text_primary'], size=14)
        ),
        xaxis=dict(
            tickfont=dict(color=COLORS['text_secondary'])
        ),
        yaxis=dict(
            gridcolor=COLORS['card_border'],
            tickfont=dict(color=COLORS['text_secondary'])
        ),
        template='plotly_dark',
        paper_bgcolor=COLORS['card_bg'],
        plot_bgcolor=COLORS['card_bg'],
        font=dict(color=COLORS['text_secondary']),
        height=300,
        showlegend=False
    )
    
    return fig

def create_stores_analysis_chart():
    fig = go.Figure(data=[
        go.Scatter(
            x=store_stats['Type'],
            y=store_stats['Nombre_Magasins'],
            mode='lines+markers+text',
            line=dict(color=COLORS['warning'], width=3),
            marker=dict(size=12, color=store_stats['Type'].map({
                'DROM': COLORS['drom'], 
                'COM': COLORS['com'], 
                'Métropole': COLORS['metro']
            })),
            text=store_stats['Nombre_Magasins'],
            textposition='top center'
        )
    ])
    
    fig.update_layout(
        title=dict(
            text='Nombre de Magasins par Type',
            x=0.5,
            font=dict(color=COLORS['text_primary'], size=14)
        ),
        xaxis=dict(
            tickfont=dict(color=COLORS['text_secondary'])
        ),
        yaxis=dict(
            gridcolor=COLORS['card_border'],
            tickfont=dict(color=COLORS['text_secondary'])
        ),
        template='plotly_dark',
        paper_bgcolor=COLORS['card_bg'],
        plot_bgcolor=COLORS['card_bg'],
        font=dict(color=COLORS['text_secondary']),
        height=300,
        showlegend=False
    )
    
    return fig

def create_performance_gauges_chart():
    fig = make_subplots(
        rows=1, cols=3,
        specs=[[{"type": "indicator"}, {"type": "indicator"}, {"type": "indicator"}]],
        subplot_titles=('Satisfaction', 'Rentabilité', 'Croissance')
    )
    
    # Satisfaction moyenne
    fig.add_trace(go.Indicator(
        mode="gauge+number",
        value=territory_data['Satisfaction'].mean(),
        number=dict(suffix="/5", font=dict(size=20)),
        gauge=dict(
            axis=dict(range=[None, 5], tickwidth=2, tickcolor=COLORS['text_primary']),
            bar=dict(color=COLORS['drom']),
            bgcolor=COLORS['card_bg'],
            borderwidth=2,
            bordercolor=COLORS['card_border'],
            steps=[
                dict(range=[0, 3], color=COLORS['danger']),
                dict(range=[3, 4], color=COLORS['warning']),
                dict(range=[4, 5], color=COLORS['success'])
            ]
        )
    ), row=1, col=1)
    
    # Rentabilité moyenne
    fig.add_trace(go.Indicator(
        mode="gauge+number",
        value=territory_data['Rentabilité'].mean(),
        number=dict(suffix="%", font=dict(size=20)),
        gauge=dict(
            axis=dict(range=[None, 25], tickwidth=2, tickcolor=COLORS['text_primary']),
            bar=dict(color=COLORS['com']),
            bgcolor=COLORS['card_bg'],
            borderwidth=2,
            bordercolor=COLORS['card_border'],
            steps=[
                dict(range=[0, 8], color=COLORS['danger']),
                dict(range=[8, 15], color=COLORS['warning']),
                dict(range=[15, 25], color=COLORS['success'])
            ]
        )
    ), row=1, col=2)
    
    # Croissance moyenne
    fig.add_trace(go.Indicator(
        mode="gauge+number",
        value=territory_data['Croissance'].mean(),
        number=dict(suffix="%", font=dict(size=20)),
        gauge=dict(
            axis=dict(range=[None, 20], tickwidth=2, tickcolor=COLORS['text_primary']),
            bar=dict(color=COLORS['metro']),
            bgcolor=COLORS['card_bg'],
            borderwidth=2,
            bordercolor=COLORS['card_border'],
            steps=[
                dict(range=[0, 5], color=COLORS['danger']),
                dict(range=[5, 10], color=COLORS['warning']),
                dict(range=[10, 20], color=COLORS['success'])
            ]
        )
    ), row=1, col=3)
    
    fig.update_layout(
        template='plotly_dark',
        paper_bgcolor=COLORS['card_bg'],
        font=dict(color=COLORS['text_secondary']),
        height=300,
        margin=dict(l=20, r=20, t=60, b=20)
    )
    
    return fig

def create_drom_performance_chart(drom_data):
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        x=drom_data['Territoire'],
        y=drom_data['Chiffre_affaires'],
        name='Chiffre d\'affaires',
        marker_color=COLORS['drom']
    ))
    
    fig.add_trace(go.Scatter(
        x=drom_data['Territoire'],
        y=drom_data['Satisfaction'] * 1000000,
        name='Satisfaction (x1M)',
        yaxis='y2',
        line=dict(color=COLORS['warning'], width=3),
        marker=dict(size=8)
    ))
    
    fig.update_layout(
        title='Performance des Territoires DROM',
        xaxis_title='Territoire',
        yaxis_title='Chiffre d\'affaires (€)',
        yaxis2=dict(
            title='Satisfaction (/5)',
            overlaying='y',
            side='right',
            range=[0, 5]
        ),
        template='plotly_dark',
        paper_bgcolor=COLORS['card_bg'],
        plot_bgcolor=COLORS['card_bg']
    )
    
    return fig

def create_drom_metrics_chart(drom_data):
    metrics = ['Croissance', 'Satisfaction', 'Part_marche', 'Rentabilité']
    values = [drom_data[metric].mean() for metric in metrics]
    
    fig = go.Figure(data=[go.Bar(
        x=metrics,
        y=values,
        marker_color=[COLORS['success'], COLORS['warning'], COLORS['info'], COLORS['primary']]
    )])
    
    fig.update_layout(
        title='Métriques Moyennes DROM',
        template='plotly_dark',
        paper_bgcolor=COLORS['card_bg'],
        plot_bgcolor=COLORS['card_bg']
    )
    
    return fig

def create_com_comparison_chart(com_data):
    fig = go.Figure()
    
    fig.add_trace(go.Bar(
        x=com_data['Territoire'],
        y=com_data['Chiffre_affaires'],
        name='CA',
        marker_color=COLORS['com']
    ))
    
    fig.add_trace(go.Bar(
        x=com_data['Territoire'],
        y=com_data['Panier_moyen'] * 1000,
        name='Panier moyen (x1000)',
        marker_color=COLORS['warning']
    ))
    
    fig.update_layout(
        title='Comparaison des Territoires COM',
        barmode='group',
        template='plotly_dark',
        paper_bgcolor=COLORS['card_bg'],
        plot_bgcolor=COLORS['card_bg']
    )
    
    return fig

def create_metro_performance_chart(metro_data):
    metro_sorted = metro_data.sort_values('Chiffre_affaires', ascending=True)
    
    fig = go.Figure(data=[go.Bar(
        y=metro_sorted['Territoire'],
        x=metro_sorted['Chiffre_affaires'],
        orientation='h',
        marker_color=COLORS['metro'],
        text=metro_sorted['Chiffre_affaires'].apply(lambda x: f'{x:,.0f}€'),
        textposition='auto'
    )])
    
    fig.update_layout(
        title='Performance par Région Métropolitaine',
        xaxis_title='Chiffre d\'affaires (€)',
        template='plotly_dark',
        paper_bgcolor=COLORS['card_bg'],
        plot_bgcolor=COLORS['card_bg'],
        height=500
    )
    
    return fig

def create_profitability_analysis():
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=financial_data['Date'],
        y=financial_data['Chiffre_d_affaires'],
        name='Chiffre d\'affaires',
        line=dict(color=COLORS['success'], width=3)
    ))
    
    fig.add_trace(go.Scatter(
        x=financial_data['Date'],
        y=financial_data['Bénéfice_net'],
        name='Bénéfice net',
        line=dict(color=COLORS['primary'], width=3)
    ))
    
    fig.update_layout(
        title='Évolution CA vs Bénéfices',
        template='plotly_dark',
        paper_bgcolor=COLORS['card_bg'],
        plot_bgcolor=COLORS['card_bg']
    )
    
    return fig

def create_expenses_breakdown():
    categories = ['Personnel', 'Logistique', 'Marketing', 'Loyers', 'Autres']
    values = [45, 25, 15, 10, 5]
    
    fig = go.Figure(data=[go.Pie(
        labels=categories,
        values=values,
        hole=0.4,
        marker_colors=[COLORS['drom'], COLORS['com'], COLORS['metro'], COLORS['warning'], COLORS['info']]
    )])
    
    fig.update_layout(
        title='Répartition des Dépenses',
        template='plotly_dark',
        paper_bgcolor=COLORS['card_bg'],
        plot_bgcolor=COLORS['card_bg']
    )
    
    return fig

def create_investments_chart():
    investments = financial_data[financial_data['Investissements'] > 0]
    
    fig = go.Figure(data=[go.Bar(
        x=investments['Date'],
        y=investments['Investissements'],
        marker_color=COLORS['primary']
    )])
    
    fig.update_layout(
        title='Investissements par Date',
        template='plotly_dark',
        paper_bgcolor=COLORS['card_bg'],
        plot_bgcolor=COLORS['card_bg']
    )
    
    return fig

def display_transactions_table(territory_type=None):
    if territory_type:
        filtered_data = [t for t in transactions_data if t['Type_Territoire'] == territory_type]
    else:
        filtered_data = transactions_data
    
    # Convertir en DataFrame pour Streamlit
    df = pd.DataFrame(filtered_data)
    st.dataframe(
        df,
        column_config={
            'Date': st.column_config.DateColumn('Date'),
            'Type': st.column_config.TextColumn('Type'),
            'Catégorie': st.column_config.TextColumn('Catégorie'),
            'Territoire': st.column_config.TextColumn('Territoire'),
            'Type_Territoire': st.column_config.TextColumn('Type Territoire'),
            'Montant': st.column_config.NumberColumn('Montant', format="%.2f€")
        },
        hide_index=True,
        use_container_width=True
    )

def display_territory_detail_table(data):
    st.dataframe(
        data,
        column_config={
            'Territoire': st.column_config.TextColumn('Territoire'),
            'Type': st.column_config.TextColumn('Type'),
            'Chiffre_affaires': st.column_config.NumberColumn('CA (€)', format="%.0f"),
            'Croissance': st.column_config.NumberColumn('Croissance (%)', format="%.1f"),
            'Satisfaction': st.column_config.NumberColumn('Satisfaction', format="%.1f/5"),
            'Part_marche': st.column_config.NumberColumn('Part de marché (%)', format="%.1f"),
            'Panier_moyen': st.column_config.NumberColumn('Panier moyen (€)', format="%.1f"),
            'Rentabilité': st.column_config.NumberColumn('Rentabilité (%)', format="%.1f"),
            'Magasins': st.column_config.NumberColumn('Magasins'),
            'Nouveaux_clients_mois': st.column_config.NumberColumn('Nouveaux clients/mois')
        },
        hide_index=True,
        use_container_width=True
    )

# Initialiser l'état de la session pour la navigation
if 'current_view' not in st.session_state:
    st.session_state.current_view = 'overview'

# Fonction pour changer la vue
def set_view(view):
    st.session_state.current_view = view

# Header
st.markdown("""
<div class="main-header">
    <h1 style="color: white; font-weight: 700; text-shadow: 2px 2px 4px rgba(0,0,0,0.3);">🏬 GBH GROUP</h1>
    <h4 style="color: #B0B8C5; font-weight: 300;">Tableau de Bord Exécutif - Tous Territoires</h4>
    <div style="text-align: center; margin-top: 15px;">
        <span style="font-size: 24px; margin-right: 10px;">🌍</span>
        <span style="color: white; font-weight: 600;">{kpi_summary['total_territoires']} Territoires</span>
        <span style="color: #8A94A6;"> • </span>
        <span style="color: white; font-weight: 600;">{kpi_summary['total_magasins']} Magasins</span>
    </div>
</div>
""".format(kpi_summary=kpi_summary), unsafe_allow_html=True)

# Navigation
cols = st.columns(5)
with cols[0]:
    if st.button("📊 Vue d'Ensemble", key="btn-overview", use_container_width=True):
        set_view('overview')
with cols[1]:
    if st.button("🏝️ Analyse DROM", key="btn-drom", use_container_width=True):
        set_view('drom')
with cols[2]:
    if st.button("🏖️ Analyse COM", key="btn-com", use_container_width=True):
        set_view('com')
with cols[3]:
    if st.button("🏙️ Analyse Métropole", key="btn-metro", use_container_width=True):
        set_view('metro')
with cols[4]:
    if st.button("📈 Performance Financière", key="btn-finance", use_container_width=True):
        set_view('finance')

st.markdown("---")

# Afficher la vue actuelle
if st.session_state.current_view == 'overview':
    # KPI Principaux
    latest = financial_data.iloc[-1]
    kpi_cols = st.columns(6)
    
    with kpi_cols[0]:
        st.markdown(f"""
        <div class="metric-card">
            <div style="text-align: center;">
                <div style="margin-bottom: 15px; color: {COLORS['success']};">💰</div>
                <h4 style="color: {COLORS['text_secondary']}; font-size: 14px; font-weight: 600;">Chiffre d'Affaires</h4>
                <h2 style="color: {COLORS['success']}; font-weight: 700; margin: 10px 0;">{latest['Chiffre_d_affaires']:,.0f}€</h2>
                <div style="color: {COLORS['text_muted']}; font-size: 12px;">↗️ {latest['Chiffre_d_affaires'] - financial_data.iloc[-2]['Chiffre_d_affaires']:,.0f}€/jour</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with kpi_cols[1]:
        st.markdown(f"""
        <div class="metric-card">
            <div style="text-align: center;">
                <div style="margin-bottom: 15px; color: {COLORS['primary']};">📈</div>
                <h4 style="color: {COLORS['text_secondary']}; font-size: 14px; font-weight: 600;">Bénéfice Net</h4>
                <h2 style="color: {COLORS['primary']}; font-weight: 700; margin: 10px 0;">{latest['Bénéfice_net']:,.0f}€</h2>
                <div style="color: {COLORS['text_muted']}; font-size: 12px;">↗️ {latest['Bénéfice_net'] - financial_data.iloc[-2]['Bénéfice_net']:,.0f}€/jour</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with kpi_cols[2]:
        st.markdown(f"""
        <div class="metric-card">
            <div style="text-align: center;">
                <div style="margin-bottom: 15px; color: {COLORS['info']};">👥</div>
                <h4 style="color: {COLORS['text_secondary']}; font-size: 14px; font-weight: 600;">Effectifs</h4>
                <h2 style="color: {COLORS['info']}; font-weight: 700; margin: 10px 0;">{latest['Effectifs']:.0f}</h2>
                <div style="color: {COLORS['text_muted']}; font-size: 12px;">Employés</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with kpi_cols[3]:
        st.markdown(f"""
        <div class="metric-card">
            <div style="text-align: center;">
                <div style="margin-bottom: 15px; color: {COLORS['warning']};">🏪</div>
                <h4 style="color: {COLORS['text_secondary']}; font-size: 14px; font-weight: 600;">Magasins</h4>
                <h2 style="color: {COLORS['warning']}; font-weight: 700; margin: 10px 0;">{latest['Nbre_magasins']:.0f}</h2>
                <div style="color: {COLORS['text_muted']}; font-size: 12px;">Points de vente</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with kpi_cols[4]:
        st.markdown(f"""
        <div class="metric-card">
            <div style="text-align: center;">
                <div style="margin-bottom: 15px; color: {COLORS['drom']};">⭐</div>
                <h4 style="color: {COLORS['text_secondary']}; font-size: 14px; font-weight: 600;">Satisfaction</h4>
                <h2 style="color: {COLORS['drom']}; font-weight: 700; margin: 10px 0;">{latest['Satisfaction_client']:.1f}</h2>
                <div style="color: {COLORS['text_muted']}; font-size: 12px;">/ 5.0</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with kpi_cols[5]:
        st.markdown(f"""
        <div class="metric-card">
            <div style="text-align: center;">
                <div style="margin-bottom: 15px; color: {COLORS['com']};">🛒</div>
                <h4 style="color: {COLORS['text_secondary']}; font-size: 14px; font-weight: 600;">Panier Moyen</h4>
                <h2 style="color: {COLORS['com']}; font-weight: 700; margin: 10px 0;">{latest['Panier_moyen']:.1f}€</h2>
                <div style="color: {COLORS['text_muted']}; font-size: 12px;">Montant moyen</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # Graphiques
    st.markdown("### 📈 Évolution Financière - Vue Globale")
    st.plotly_chart(create_financial_trend_chart(), use_container_width=True)
    
    col1, col2 = st.columns([2, 1])
    with col1:
        st.markdown("### 🌍 Répartition Territoriale")
        st.plotly_chart(create_territory_breakdown_chart(), use_container_width=True)
    with col2:
        st.markdown("### 📊 Métriques Globales")
        st.plotly_chart(create_performance_gauges_chart(), use_container_width=True)
    
    st.markdown("### 🏆 Performance par Territoire - Tous Types")
    st.plotly_chart(create_territory_performance_chart(), use_container_width=True)
    
    st.markdown("### 📊 Analyse Comparative")
    comp_cols = st.columns(3)
    with comp_cols[0]:
        st.plotly_chart(create_type_comparison_chart(), use_container_width=True)
    with comp_cols[1]:
        st.plotly_chart(create_stores_analysis_chart(), use_container_width=True)
    with comp_cols[2]:
        st.plotly_chart(create_performance_gauges_chart(), use_container_width=True)
    
    st.markdown("### 💳 Transactions Récentes - Tous Territoires")
    display_transactions_table()

elif st.session_state.current_view == 'drom':
    drom_data = territory_data[territory_data['Type'] == 'DROM']
    
    st.markdown(f"<h2 style='color: {COLORS['drom']}; border-bottom: 2px solid {COLORS['drom']}; padding-bottom: 10px;'>🏝️ Analyse DROM</h2>", unsafe_allow_html=True)
    
    # KPI DROM
    kpi_cols = st.columns(4)
    with kpi_cols[0]:
        st.markdown(f"""
        <div class="metric-card">
            <h4 style="color: {COLORS['text_primary']};">{len(drom_data)} Territoires DROM</h4>
            <h2 style="color: {COLORS['drom']};">{drom_data['Chiffre_affaires'].sum():,.0f}€</h2>
            <p style="color: {COLORS['text_secondary']};">Chiffre d'affaires total</p>
        </div>
        """, unsafe_allow_html=True)
    
    with kpi_cols[1]:
        st.markdown(f"""
        <div class="metric-card">
            <h4 style="color: {COLORS['text_primary']};">Croissance Moyenne</h4>
            <h2 style="color: {COLORS['success']};">+{drom_data['Croissance'].mean():.1f}%</h2>
            <p style="color: {COLORS['text_secondary']};">vs période précédente</p>
        </div>
        """, unsafe_allow_html=True)
    
    with kpi_cols[2]:
        st.markdown(f"""
        <div class="metric-card">
            <h4 style="color: {COLORS['text_primary']};">Satisfaction Moyenne</h4>
            <h2 style="color: {COLORS['warning']};">{drom_data['Satisfaction'].mean():.1f}/5</h2>
            <p style="color: {COLORS['text_secondary']};">Score client</p>
        </div>
        """, unsafe_allow_html=True)
    
    with kpi_cols[3]:
        st.markdown(f"""
        <div class="metric-card">
            <h4 style="color: {COLORS['text_primary']};">Part de Marché Moyenne</h4>
            <h2 style="color: {COLORS['info']};">{drom_data['Part_marche'].mean():.1f}%</h2>
            <p style="color: {COLORS['text_secondary']};">Dans chaque territoire</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Graphiques DROM
    col1, col2 = st.columns([2, 1])
    with col1:
        st.markdown("### 📊 Performance des Territoires DROM")
        st.plotly_chart(create_drom_performance_chart(drom_data), use_container_width=True)
    with col2:
        st.markdown("### 🎯 Métriques Clés DROM")
        st.plotly_chart(create_drom_metrics_chart(drom_data), use_container_width=True)
    
    st.markdown("### 💳 Transactions DROM Récentes")
    display_transactions_table(territory_type='DROM')

elif st.session_state.current_view == 'com':
    com_data = territory_data[territory_data['Type'] == 'COM']
    
    st.markdown(f"<h2 style='color: {COLORS['com']}; border-bottom: 2px solid {COLORS['com']}; padding-bottom: 10px;'>🏖️ Analyse COM</h2>", unsafe_allow_html=True)
    
    # KPI COM
    kpi_cols = st.columns(4)
    with kpi_cols[0]:
        st.markdown(f"""
        <div class="metric-card">
            <h4 style="color: {COLORS['text_primary']};">{len(com_data)} Territoires COM</h4>
            <h2 style="color: {COLORS['com']};">{com_data['Chiffre_affaires'].sum():,.0f}€</h2>
            <p style="color: {COLORS['text_secondary']};">Chiffre d'affaires total</p>
        </div>
        """, unsafe_allow_html=True)
    
    with kpi_cols[1]:
        st.markdown(f"""
        <div class="metric-card">
            <h4 style="color: {COLORS['text_primary']};">Croissance Moyenne</h4>
            <h2 style="color: {COLORS['success']};">+{com_data['Croissance'].mean():.1f}%</h2>
            <p style="color: {COLORS['text_secondary']};">vs période précédente</p>
        </div>
        """, unsafe_allow_html=True)
    
    with kpi_cols[2]:
        st.markdown(f"""
        <div class="metric-card">
            <h4 style="color: {COLORS['text_primary']};">Panier Moyen</h4>
            <h2 style="color: {COLORS['warning']};">{com_data['Panier_moyen'].mean():.1f}€</h2>
            <p style="color: {COLORS['text_secondary']};">Montant moyen par transaction</p>
        </div>
        """, unsafe_allow_html=True)
    
    with kpi_cols[3]:
        st.markdown(f"""
        <div class="metric-card">
            <h4 style="color: {COLORS['text_primary']};">Rentabilité Moyenne</h4>
            <h2 style="color: {COLORS['info']};">{com_data['Rentabilité'].mean():.1f}%</h2>
            <p style="color: {COLORS['text_secondary']};">Marge nette moyenne</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Graphiques COM
    st.markdown("### 📊 Analyse Comparative COM")
    st.plotly_chart(create_com_comparison_chart(com_data), use_container_width=True)
    
    st.markdown("### 🏝️ Détail par Territoire COM")
    display_territory_detail_table(com_data)

elif st.session_state.current_view == 'metro':
    metro_data = territory_data[territory_data['Type'] == 'Métropole']
    
    st.markdown(f"<h2 style='color: {COLORS['metro']}; border-bottom: 2px solid {COLORS['metro']}; padding-bottom: 10px;'>🏙️ Analyse Métropole</h2>", unsafe_allow_html=True)
    
    # KPI Métropole
    kpi_cols = st.columns(4)
    with kpi_cols[0]:
        st.markdown(f"""
        <div class="metric-card">
            <h4 style="color: {COLORS['text_primary']};">{len(metro_data)} Régions Métropolitaines</h4>
            <h2 style="color: {COLORS['metro']};">{metro_data['Chiffre_affaires'].sum():,.0f}€</h2>
            <p style="color: {COLORS['text_secondary']};">Chiffre d'affaires total</p>
        </div>
        """, unsafe_allow_html=True)
    
    with kpi_cols[1]:
        st.markdown(f"""
        <div class="metric-card">
            <h4 style="color: {COLORS['text_primary']};">Performance Relative</h4>
            <h2 style="color: {COLORS['primary']};">{(metro_data['Chiffre_affaires'].sum() / territory_data['Chiffre_affaires'].sum() * 100):.1f}%</h2>
            <p style="color: {COLORS['text_secondary']};">Part du CA total</p>
        </div>
        """, unsafe_allow_html=True)
    
    with kpi_cols[2]:
        st.markdown(f"""
        <div class="metric-card">
            <h4 style="color: {COLORS['text_primary']};">Densité de Magasins</h4>
            <h2 style="color: {COLORS['warning']};">{metro_data['Magasins'].sum() / len(metro_data):.1f}</h2>
            <p style="color: {COLORS['text_secondary']};">Magasins par région</p>
        </div>
        """, unsafe_allow_html=True)
    
    with kpi_cols[3]:
        st.markdown(f"""
        <div class="metric-card">
            <h4 style="color: {COLORS['text_primary']};">Nouveaux Clients</h4>
            <h2 style="color: {COLORS['success']};">{metro_data['Nouveaux_clients_mois'].sum():,}</h2>
            <p style="color: {COLORS['text_secondary']};">Par mois</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Graphiques Métropole
    st.markdown("### 📈 Performance par Région Métropolitaine")
    st.plotly_chart(create_metro_performance_chart(metro_data), use_container_width=True)

elif st.session_state.current_view == 'finance':
    st.markdown(f"<h2 style='color: {COLORS['success']}; border-bottom: 2px solid {COLORS['success']}; padding-bottom: 10px;'>📈 Analyse Financière Détaillée</h2>", unsafe_allow_html=True)
    
    # KPI Financiers
    kpi_cols = st.columns(4)
    with kpi_cols[0]:
        profit_margin = ((financial_data['Bénéfice_net'].iloc[-1] - financial_data['Bénéfice_net'].iloc[-2]) / 
                        (financial_data['Chiffre_d_affaires'].iloc[-1] - financial_data['Chiffre_d_affaires'].iloc[-2]) * 100) if len(financial_data) > 1 else 12.5
        st.markdown(f"""
        <div class="metric-card">
            <h4 style="color: {COLORS['text_primary']};">Marge Nette</h4>
            <h2 style="color: {COLORS['success']};">{profit_margin:.1f}%</h2>
            <p style="color: {COLORS['text_secondary']};">Dernier jour</p>
        </div>
        """, unsafe_allow_html=True)
    
    with kpi_cols[1]:
        st.markdown(f"""
        <div class="metric-card">
            <h4 style="color: {COLORS['text_primary']};">ROI Mensuel</h4>
            <h2 style="color: {COLORS['primary']};">8.2%</h2>
            <p style="color: {COLORS['text_secondary']};">Return on Investment</p>
        </div>
        """, unsafe_allow_html=True)
    
    with kpi_cols[2]:
        st.markdown(f"""
        <div class="metric-card">
            <h4 style="color: {COLORS['text_primary']};">Trésorerie</h4>
            <h2 style="color: {COLORS['info']};">{financial_data['Bénéfice_net'].iloc[-1] * 0.3:,.0f}€</h2>
            <p style="color: {COLORS['text_secondary']};">Disponible</p>
        </div>
        """, unsafe_allow_html=True)
    
    with kpi_cols[3]:
        st.markdown(f"""
        <div class="metric-card">
            <h4 style="color: {COLORS['text_primary']};">Dettes</h4>
            <h2 style="color: {COLORS['warning']};">{financial_data['Investissements'].sum() * 0.6:,.0f}€</h2>
            <p style="color: {COLORS['text_secondary']};">Encours</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Graphiques Financiers
    col1, col2 = st.columns([2, 1])
    with col1:
        st.markdown("### 💰 Analyse de Rentabilité")
        st.plotly_chart(create_profitability_analysis(), use_container_width=True)
    with col2:
        st.markdown("### 📊 Répartition des Dépenses")
        st.plotly_chart(create_expenses_breakdown(), use_container_width=True)
    
    st.markdown("### 🏗️ Historique des Investissements")
    st.plotly_chart(create_investments_chart(), use_container_width=True)

# Pied de page
st.markdown("---")
col1, col2, col3 = st.columns([2, 1, 1])
with col1:
    st.markdown(f"<span style='color: {COLORS['text_secondary']}'>Dernière mise à jour: </span><span style='color: {COLORS['text_primary']}; font-weight: bold;'>{datetime.now().strftime('%d/%m/%Y %H:%M:%S')}</span>", unsafe_allow_html=True)
with col2:
    if st.button("🔄 Actualiser les Données", key="refresh-btn"):
        st.cache_resource.clear()
        st.rerun()
with col3:
    st.markdown(f"<span style='color: {COLORS['text_muted']}; font-size: 12px;'>GBH Group Dashboard Premium v2.0</span>", unsafe_allow_html=True)
