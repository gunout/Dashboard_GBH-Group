# Dashboard.py - VERSION TEMPS RÉEL avec NinjaGBHData
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import streamlit as st
from datetime import datetime, timedelta
import time
import warnings
warnings.filterwarnings('ignore')

# ========== CONFIGURATION STREAMLIT ==========
st.set_page_config(
    page_title="GBH Group | Dashboard Temps Réel",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ========== STYLE CSS ANIMÉ ==========
st.markdown("""
<style>
@keyframes pulse {
    0% { opacity: 1; }
    50% { opacity: 0.7; }
    100% { opacity: 1; }
}

@keyframes slideIn {
    from { transform: translateY(-20px); opacity: 0; }
    to { transform: translateY(0); opacity: 1; }
}

.real-time-badge {
    background: linear-gradient(90deg, #ff0080, #00f3ff);
    color: white;
    padding: 5px 15px;
    border-radius: 20px;
    font-weight: bold;
    font-size: 12px;
    animation: pulse 2s infinite;
    display: inline-block;
    margin-right: 10px;
}

.metric-card {
    background: #0d1220;
    border: 1px solid #2a3b5c;
    border-radius: 15px;
    padding: 20px;
    margin-bottom: 20px;
    transition: all 0.3s ease;
    animation: slideIn 0.6s ease-out;
}

.metric-card:hover {
    transform: translateY(-5px);
    box-shadow: 0 10px 30px rgba(0, 243, 255, 0.2);
    border-color: #00f3ff;
}

.live-indicator {
    display: inline-block;
    width: 10px;
    height: 10px;
    background-color: #00ff9d;
    border-radius: 50%;
    margin-right: 5px;
    animation: pulse 1s infinite;
}

.stButton > button {
    background: linear-gradient(90deg, #0066ff, #00f3ff);
    color: white;
    border: none;
    border-radius: 10px;
    padding: 12px 24px;
    font-weight: 600;
    transition: all 0.3s ease;
}

.stButton > button:hover {
    transform: translateY(-2px);
    box-shadow: 0 5px 15px rgba(0, 243, 255, 0.4);
}
</style>
""", unsafe_allow_html=True)

# ========== FONCTIONS D'ANALYSE TEMPS RÉEL ==========
def calculate_real_time_metrics(financial_data, territory_data):
    """Calcule des métriques en temps réel"""
    
    metrics = {}
    
    # Dernière heure de mise à jour
    metrics['last_update'] = datetime.now().strftime('%H:%M:%S')
    
    # Analyse en temps réel
    if len(financial_data) > 0:
        latest = financial_data.iloc[-1]
        
        # CA des dernières 24h
        if len(financial_data) >= 2:
            last_24h = financial_data.tail(2)
            metrics['revenue_last_24h'] = last_24h['Chiffre_d_affaires'].iloc[-1] - last_24h['Chiffre_d_affaires'].iloc[0]
            
            # Taux de croissance instantané
            if len(financial_data) >= 10:
                last_10_days = financial_data.tail(10)
                growth_rates = []
                for i in range(1, len(last_10_days)):
                    daily_growth = ((last_10_days['Chiffre_d_affaires'].iloc[i] - last_10_days['Chiffre_d_affaires'].iloc[i-1]) / 
                                   last_10_days['Chiffre_d_affaires'].iloc[i-1]) * 100
                    growth_rates.append(daily_growth)
                
                metrics['instant_growth_rate'] = np.mean(growth_rates) if growth_rates else 0
                metrics['growth_volatility'] = np.std(growth_rates) if len(growth_rates) > 1 else 0
        
        # Alertes en temps réel
        alerts = []
        
        if 'Satisfaction_client' in financial_data.columns:
            current_satisfaction = latest['Satisfaction_client']
            if current_satisfaction < 4.0:
                alerts.append({
                    'type': 'warning',
                    'message': f'Satisfaction client basse: {current_satisfaction:.1f}/5',
                    'priority': 'Haute'
                })
        
        if 'CA_Quotidien' in financial_data.columns and len(financial_data) >= 2:
            current_daily_ca = latest['CA_Quotidien']
            avg_daily_ca = financial_data['CA_Quotidien'].mean()
            
            if current_daily_ca < avg_daily_ca * 0.7:
                alerts.append({
                    'type': 'danger',
                    'message': f'CA quotidien en baisse: -{((avg_daily_ca - current_daily_ca)/avg_daily_ca*100):.0f}% vs moyenne',
                    'priority': 'Moyenne'
                })
        
        metrics['alerts'] = alerts
    
    # Analyse territoriale dynamique
    if len(territory_data) > 0:
        # Top performers du moment
        metrics['top_performer'] = territory_data.loc[territory_data['Chiffre_affaires'].idxmax()]['Territoire']
        metrics['top_growth'] = territory_data.loc[territory_data['Croissance'].idxmax()]['Territoire']
        metrics['top_satisfaction'] = territory_data.loc[territory_data['Satisfaction'].idxmax()]['Territoire']
        
        # Performance par type en temps réel
        type_performance = territory_data.groupby('Type').agg({
            'Chiffre_affaires': 'mean',
            'Croissance': 'mean',
            'Satisfaction': 'mean'
        }).round(2)
        
        metrics['type_performance'] = type_performance
        
        # Territoires nécessitant attention
        attention_needed = territory_data[
            (territory_data['Croissance'] < territory_data['Croissance'].mean()) &
            (territory_data['Satisfaction'] < territory_data['Satisfaction'].mean())
        ]
        metrics['attention_territories'] = attention_needed['Territoire'].tolist()[:3]
    
    return metrics

def generate_realtime_forecast(financial_data, horizon_hours=24):
    """Génère des prévisions en temps réel"""
    
    forecast = {}
    
    if len(financial_data) >= 10:
        # Utilise les dernières données pour la prévision
        recent_data = financial_data.tail(24)  # Dernières 24 heures
        
        if len(recent_data) > 1:
            # Prévision simple basée sur la tendance récente
            X = np.arange(len(recent_data))
            y = recent_data['CA_Quotidien'].values
            
            # Régression linéaire manuelle
            n = len(X)
            mean_x = np.mean(X)
            mean_y = np.mean(y)
            
            SS_xy = np.sum(y * X) - n * mean_y * mean_x
            SS_xx = np.sum(X * X) - n * mean_x * mean_x
            
            if SS_xx != 0:
                slope = SS_xy / SS_xx
                intercept = mean_y - slope * mean_x
                
                # Prévision pour les prochaines heures
                future_X = np.arange(len(recent_data), len(recent_data) + horizon_hours)
                future_y = intercept + slope * future_X
                
                forecast['next_hours'] = future_y
                forecast['trend_direction'] = '↗️ Hausse' if slope > 0 else '↘️ Baisse' if slope < 0 else '→ Stable'
                forecast['trend_strength'] = abs(slope) / mean_y * 100 if mean_y > 0 else 0
                
                # Estimation du CA pour la prochaine heure
                forecast['next_hour_estimate'] = intercept + slope * (len(recent_data) + 1)
    
    return forecast

def monitor_real_time_transactions(transactions_data):
    """Analyse des transactions en temps réel"""
    
    monitoring = {}
    
    if len(transactions_data) > 0:
        # Convertir les dates
        df_transactions = pd.DataFrame(transactions_data)
        
        if 'Date' in df_transactions.columns:
            # Dernières transactions (15 dernières minutes)
            now = datetime.now()
            df_transactions['Timestamp'] = pd.to_datetime(df_transactions['Date'], errors='coerce')
            
            recent_transactions = df_transactions[
                df_transactions['Timestamp'] > (now - timedelta(minutes=15))
            ]
            
            monitoring['recent_transactions_count'] = len(recent_transactions)
            
            if len(recent_transactions) > 0:
                # Montant total des dernières transactions
                def parse_amount(amount_str):
                    try:
                        # Nettoyer le string
                        clean_str = str(amount_str).replace('€', '').replace(' ', '').replace(',', '')
                        return float(clean_str)
                    except:
                        return 0
                
                recent_transactions['Montant_Numeric'] = recent_transactions['Montant'].apply(parse_amount)
                monitoring['recent_revenue'] = recent_transactions['Montant_Numeric'].sum()
                
                # Distribution par type de territoire
                if 'Type_Territoire' in recent_transactions.columns:
                    territory_dist = recent_transactions.groupby('Type_Territoire').agg({
                        'Montant_Numeric': 'sum',
                        'Date': 'count'
                    }).round(2)
                    monitoring['territory_distribution'] = territory_dist
                
                # Transactions suspectes
                high_value_transactions = recent_transactions[
                    abs(recent_transactions['Montant_Numeric']) > 10000
                ]
                monitoring['high_value_count'] = len(high_value_transactions)
        
        # Statistiques globales
        monitoring['total_transactions'] = len(df_transactions)
        
        if 'Type_Territoire' in df_transactions.columns:
            monitoring['territory_coverage'] = df_transactions['Type_Territoire'].nunique()
    
    return monitoring

# ========== INTERFACE TEMPS RÉEL ==========
st.title("⚡ GBH Group - Dashboard Temps Réel")

# En-tête temps réel
col1, col2, col3 = st.columns([3, 2, 2])

with col1:
    st.markdown(f"""
    <div style="display: flex; align-items: center; margin-bottom: 20px;">
        <span class="live-indicator"></span>
        <span class="real-time-badge">EN DIRECT</span>
        <span style="color: #8a94a6; font-size: 14px; margin-left: 10px;">
            Données mises à jour en temps réel
        </span>
    </div>
    """, unsafe_allow_html=True)

with col2:
    current_time = datetime.now().strftime('%H:%M:%S')
    st.markdown(f"""
    <div style="text-align: center;">
        <div style="font-size: 24px; color: #00f3ff; font-family: monospace; font-weight: bold;">
            {current_time}
        </div>
        <div style="color: #8a94a6; font-size: 12px;">
            Heure serveur
        </div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    if st.button("🔄 Actualiser Maintenant", use_container_width=True):
        st.rerun()

st.divider()

# ========== CHARGEMENT DES DONNÉES ==========
@st.cache_resource(ttl=60)  # Cache de 60 secondes pour données "temps réel"
def load_ninja_data():
    """Charge les données depuis NinjaGBHData avec rafraîchissement automatique"""
    
    try:
        # Import dynamique de NinjaGBHData
        import importlib
        import sys
        import os
        
        # Essayer d'importer le module
        try:
            from NinjaGBHData import NinjaGBHDataSimulator
            ninja = NinjaGBHDataSimulator()
            print("✅ NinjaGBHData chargé avec succès")
            
        except ImportError as e:
            print(f"⚠️ NinjaGBHData non trouvé, création d'un simulateur local: {e}")
            # Créer un simulateur local si le module n'existe pas
            class LocalNinjaSimulator:
                def __init__(self):
                    self.territory_colors = {
                        'DROM': '#FF6B6B',
                        'COM': '#FFA500',
                        'Métropole': '#00CED1'
                    }
                
                def generate_financial_data(self, start_date='2023-01-01', end_date=None):
                    if end_date is None:
                        end_date = datetime.now()
                    
                    dates = pd.date_range(start=start_date, end=end_date, freq='D')
                    n_days = len(dates)
                    
                    # CA avec variations réalistes
                    base_ca = 280000
                    trend = np.arange(n_days) * 150
                    seasonal = np.sin(np.arange(n_days) * 2 * np.pi / 365) * 50000
                    noise = np.random.normal(0, 20000, n_days)
                    
                    daily_revenue = base_ca + trend + seasonal + noise
                    daily_revenue = np.maximum(daily_revenue, 120000)
                    
                    return pd.DataFrame({
                        'Date': dates,
                        'Chiffre_d_affaires': np.cumsum(daily_revenue),
                        'CA_Quotidien': daily_revenue,
                        'Bénéfice_net': np.cumsum(daily_revenue * 0.12),
                        'Investissements': np.random.choice([0, 50000, 100000, 200000], n_days, p=[0.7, 0.15, 0.1, 0.05]),
                        'Effectifs': np.random.randint(2500, 3000, n_days),
                        'Satisfaction_client': np.random.uniform(4.0, 4.8, n_days),
                        'Panier_moyen': np.random.uniform(50, 80, n_days),
                        'Nbre_magasins': np.random.randint(45, 55, n_days)
                    })
                
                def generate_territory_performance(self):
                    territories = {
                        'DROM': ['Martinique', 'Guadeloupe', 'Réunion', 'Guyane', 'Mayotte'],
                        'COM': ['Saint-Martin', 'Saint-Barthélemy', 'Polynésie française', 'Nouvelle-Calédonie'],
                        'Métropole': ['Île-de-France', 'Auvergne-Rhône-Alpes', 'Provence-Alpes-Côte d\'Azur', 
                                     'Nouvelle-Aquitaine', 'Occitanie', 'Hauts-de-France']
                    }
                    
                    territory_rows = []
                    for ter_type, ter_list in territories.items():
                        for territory in ter_list:
                            if ter_type == 'DROM':
                                ca_base = np.random.uniform(2000000, 5000000)
                                growth = np.random.uniform(8, 20)
                                satisfaction = np.random.uniform(4.2, 4.8)
                            elif ter_type == 'COM':
                                ca_base = np.random.uniform(1000000, 3000000)
                                growth = np.random.uniform(5, 15)
                                satisfaction = np.random.uniform(4.1, 4.7)
                            else:
                                ca_base = np.random.uniform(5000000, 12000000)
                                growth = np.random.uniform(3, 10)
                                satisfaction = np.random.uniform(4.0, 4.6)
                            
                            territory_rows.append({
                                'Territoire': territory,
                                'Type': ter_type,
                                'Chiffre_affaires': ca_base,
                                'Croissance': growth,
                                'Satisfaction': satisfaction,
                                'Part_marche': np.random.uniform(15, 40),
                                'Rentabilité': np.random.uniform(10, 20),
                                'Panier_moyen': np.random.uniform(50, 90),
                                'Magasins': np.random.randint(2, 6),
                                'Nouveaux_clients_mois': np.random.randint(500, 3000)
                            })
                    
                    return pd.DataFrame(territory_rows)
                
                def generate_real_transactions(self, n=50):
                    transactions = []
                    territories = ['Martinique', 'Guadeloupe', 'Île-de-France', 'Auvergne-Rhône-Alpes']
                    
                    for i in range(n):
                        transaction_time = datetime.now() - timedelta(
                            minutes=np.random.randint(0, 1440),
                            seconds=np.random.randint(0, 60)
                        )
                        
                        amount = np.random.uniform(50, 5000)
                        territory = np.random.choice(territories)
                        
                        if territory in ['Martinique', 'Guadeloupe']:
                            ter_type = 'DROM'
                        elif territory == 'Île-de-France':
                            ter_type = 'Métropole'
                        else:
                            ter_type = 'Métropole'
                        
                        transactions.append({
                            'Date': transaction_time.strftime('%d/%m/%Y %H:%M'),
                            'Type': np.random.choice(['Vente', 'Achat', 'Service']),
                            'Catégorie': np.random.choice(['Alimentation', 'Bricolage', 'Textile', 'Électronique']),
                            'Magasin': f"GBH {np.random.choice(['Paris', 'Lyon', 'Marseille', 'Fort-de-France'])}",
                            'Montant': f"{amount:+,.2f} €",
                            'Territoire': territory,
                            'Type_Territoire': ter_type,
                            'ID_Transaction': f"GBH{np.random.randint(10000, 99999)}"
                        })
                    
                    return transactions
                
                def get_store_statistics(self):
                    return pd.DataFrame({
                        'Type': ['DROM', 'COM', 'Métropole'],
                        'Nombre_Magasins': [15, 8, 35],
                        'CA_Total': [18000000, 8000000, 60000000]
                    })
                
                def get_kpi_summary(self):
                    return {
                        'total_territoires': 15,
                        'total_magasins': 58,
                        'ca_total': 86000000,
                        'satisfaction_moyenne': 4.3,
                        'croissance_moyenne': 8.5
                    }
            
            ninja = LocalNinjaSimulator()
        
        # Générer les données avec timestamp récent
        financial_data = ninja.generate_financial_data(
            start_date='2024-01-01',  # Dernière année seulement
            end_date=datetime.now()
        )
        
        # Ajouter des données du jour en cours (simulation temps réel)
        today = datetime.now().strftime('%Y-%m-%d')
        if financial_data['Date'].iloc[-1].strftime('%Y-%m-%d') != today:
            # Ajouter une entrée pour aujourd'hui
            last_entry = financial_data.iloc[-1].copy()
            last_entry['Date'] = datetime.now()
            last_entry['Chiffre_d_affaires'] += np.random.normal(250000, 50000)
            last_entry['Bénéfice_net'] += np.random.normal(30000, 5000)
            last_entry['CA_Quotidien'] = np.random.normal(280000, 30000)
            
            financial_data = pd.concat([financial_data, pd.DataFrame([last_entry])], ignore_index=True)
        
        territory_data = ninja.generate_territory_performance()
        transactions = ninja.generate_real_transactions(100)
        store_stats = ninja.get_store_statistics()
        kpi_summary = ninja.get_kpi_summary()
        
        # Calculer les métriques temps réel
        real_time_metrics = calculate_real_time_metrics(financial_data, territory_data)
        real_time_forecast = generate_realtime_forecast(financial_data)
        transaction_monitoring = monitor_real_time_transactions(transactions)
        
        return {
            'ninja': ninja,
            'financial_data': financial_data,
            'territory_data': territory_data,
            'transactions': transactions,
            'store_stats': store_stats,
            'kpi_summary': kpi_summary,
            'real_time_metrics': real_time_metrics,
            'real_time_forecast': real_time_forecast,
            'transaction_monitoring': transaction_monitoring,
            'last_updated': datetime.now()
        }
        
    except Exception as e:
        st.error(f"❌ Erreur de chargement: {str(e)}")
        return None

# Chargement initial des données
data = load_ninja_data()

if data is None:
    st.error("Impossible de charger les données. Vérifiez le module NinjaGBHData.")
    st.stop()

# ========== AFFICHAGE DES DONNÉES TEMPS RÉEL ==========

# Section 1: Métriques en direct
st.subheader("📊 Métriques en Direct")

col1, col2, col3, col4 = st.columns(4)

with col1:
    latest_ca = data['financial_data']['Chiffre_d_affaires'].iloc[-1]
    previous_ca = data['financial_data']['Chiffre_d_affaires'].iloc[-2] if len(data['financial_data']) > 1 else latest_ca
    daily_growth = ((latest_ca - previous_ca) / previous_ca * 100) if previous_ca > 0 else 0
    
    st.markdown(f"""
    <div class="metric-card">
        <div style="display: flex; justify-content: space-between; align-items: center;">
            <div>
                <div style="color: #8a94a6; font-size: 14px; margin-bottom: 5px;">CA Cumulé</div>
                <div style="color: #00f3ff; font-size: 28px; font-weight: bold;">{latest_ca:,.0f}€</div>
            </div>
            <div style="color: {'#00ff9d' if daily_growth > 0 else '#ff4757'}; font-size: 16px;">
                {'↗' if daily_growth > 0 else '↘'} {abs(daily_growth):.1f}%
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    if 'real_time_metrics' in data and 'revenue_last_24h' in data['real_time_metrics']:
        revenue_24h = data['real_time_metrics']['revenue_last_24h']
        st.markdown(f"""
        <div class="metric-card">
            <div style="color: #8a94a6; font-size: 14px; margin-bottom: 5px;">Dernières 24h</div>
            <div style="color: #00ff9d; font-size: 28px; font-weight: bold;">{revenue_24h:,.0f}€</div>
            <div style="color: #8a94a6; font-size: 12px; margin-top: 5px;">CA généré</div>
        </div>
        """, unsafe_allow_html=True)

with col3:
    current_satisfaction = data['financial_data']['Satisfaction_client'].iloc[-1]
    st.markdown(f"""
    <div class="metric-card">
        <div style="display: flex; justify-content: space-between; align-items: center;">
            <div>
                <div style="color: #8a94a6; font-size: 14px; margin-bottom: 5px;">Satisfaction</div>
                <div style="color: #ffcc00; font-size: 28px; font-weight: bold;">{current_satisfaction:.1f}/5.0</div>
            </div>
            <div style="font-size: 24px;">
                {'⭐' if current_satisfaction >= 4.5 else '✨' if current_satisfaction >= 4.0 else '💫'}
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

with col4:
    if 'real_time_forecast' in data and 'next_hour_estimate' in data['real_time_forecast']:
        next_hour = data['real_time_forecast']['next_hour_estimate']
        st.markdown(f"""
        <div class="metric-card">
            <div style="color: #8a94a6; font-size: 14px; margin-bottom: 5px;">Prévision prochaine heure</div>
            <div style="color: #b967ff; font-size: 28px; font-weight: bold;">{next_hour:,.0f}€</div>
            <div style="color: #8a94a6; font-size: 12px; margin-top: 5px;">Estimation IA</div>
        </div>
        """, unsafe_allow_html=True)

# Section 2: Graphique temps réel
st.subheader("📈 Évolution Temps Réel")

tab1, tab2, tab3 = st.tabs(["CA Quotidien", "Bénéfices", "Transactions"])

with tab1:
    # Graphique des dernières 48 heures
    recent_data = data['financial_data'].tail(48)
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=recent_data['Date'],
        y=recent_data['CA_Quotidien'],
        mode='lines+markers',
        name='CA Quotidien',
        line=dict(color='#00f3ff', width=3),
        marker=dict(size=6, color='white'),
        fill='tozeroy',
        fillcolor='rgba(0, 243, 255, 0.1)'
    ))
    
    # Dernier point en évidence
    last_point = recent_data.iloc[-1]
    fig.add_trace(go.Scatter(
        x=[last_point['Date']],
        y=[last_point['CA_Quotidien']],
        mode='markers',
        name='En ce moment',
        marker=dict(size=12, color='#00ff9d', symbol='diamond'),
        hoverinfo='text',
        text=[f"Maintenant: {last_point['CA_Quotidien']:,.0f}€"]
    ))
    
    fig.update_layout(
        title='Activité Commerciale - Dernières 48 Heures',
        xaxis_title='Heure',
        yaxis_title='CA (€)',
        template='plotly_dark',
        height=400,
        hovermode='x unified'
    )
    
    st.plotly_chart(fig, use_container_width=True)

with tab2:
    # Graphique des bénéfices
    fig = go.Figure()
    
    # Calcul du bénéfice quotidien
    financial_data = data['financial_data']
    if len(financial_data) > 1:
        daily_profit = financial_data['Bénéfice_net'].diff().tail(48)
        dates = financial_data['Date'].tail(48)
        
        fig.add_trace(go.Bar(
            x=dates,
            y=daily_profit,
            name='Bénéfice Quotidien',
            marker_color='#00ff9d',
            opacity=0.8
        ))
        
        fig.update_layout(
            title='Bénéfices Journaliers - Dernières 48 Heures',
            xaxis_title='Date',
            yaxis_title='Bénéfice (€)',
            template='plotly_dark',
            height=400
        )
        
        st.plotly_chart(fig, use_container_width=True)

with tab3:
    # Monitoring des transactions
    if 'transaction_monitoring' in data:
        monitoring = data['transaction_monitoring']
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric(
                "Transactions récentes (15min)",
                monitoring.get('recent_transactions_count', 0),
                "opérations"
            )
        
        with col2:
            st.metric(
                "Revenu récent",
                f"{monitoring.get('recent_revenue', 0):,.0f}€",
                "15 dernières minutes"
            )
        
        with col3:
            st.metric(
                "Transactions haute valeur",
                monitoring.get('high_value_count', 0),
                "> 10,000€"
            )
        
        # Timeline des transactions
        if 'transactions' in data and len(data['transactions']) > 0:
            df_transactions = pd.DataFrame(data['transactions'])
            
            # Limiter aux 20 dernières transactions
            recent_transactions = df_transactions.head(20)
            
            st.dataframe(
                recent_transactions[['Date', 'Type', 'Territoire', 'Montant']],
                column_config={
                    'Date': 'Heure',
                    'Type': 'Type',
                    'Territoire': 'Territoire',
                    'Montant': st.column_config.NumberColumn(
                        'Montant',
                        format="%.2f€"
                    )
                },
                hide_index=True,
                use_container_width=True
            )

# Section 3: Alertes et notifications
st.subheader("🚨 Alertes Temps Réel")

if 'real_time_metrics' in data and 'alerts' in data['real_time_metrics']:
    alerts = data['real_time_metrics']['alerts']
    
    if alerts:
        for alert in alerts:
            if alert['type'] == 'danger':
                st.error(f"🔴 **{alert['priority']}**: {alert['message']}")
            elif alert['type'] == 'warning':
                st.warning(f"🟡 **{alert['priority']}**: {alert['message']}")
            else:
                st.info(f"🔵 **{alert['priority']}**: {alert['message']}")
    else:
        st.success("✅ Aucune alerte critique - Tous les systèmes fonctionnent normalement")
else:
    st.info("📡 Surveillance des alertes en cours...")

# Section 4: Performance territoriale en direct
st.subheader("🌍 Performance Territoriale - Live")

if 'real_time_metrics' in data:
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric(
            "🏆 Meilleur Performer",
            data['real_time_metrics'].get('top_performer', 'N/A'),
            "Plus haut CA"
        )
    
    with col2:
        st.metric(
            "🚀 Plus forte croissance",
            data['real_time_metrics'].get('top_growth', 'N/A'),
            "Taux de croissance"
        )
    
    with col3:
        st.metric(
            "⭐ Meilleure satisfaction",
            data['real_time_metrics'].get('top_satisfaction', 'N/A'),
            "Score client"
        )

# Section 5: Dashboard de contrôle
st.subheader("🎮 Contrôle Temps Réel")

col1, col2, col3 = st.columns(3)

with col1:
    refresh_rate = st.select_slider(
        "Fréquence de rafraîchissement",
        options=['30s', '1min', '5min', '10min', 'Manuel'],
        value='1min'
    )
    
    # Convertir en secondes
    refresh_seconds = {
        '30s': 30,
        '1min': 60,
        '5min': 300,
        '10min': 600,
        'Manuel': 0
    }[refresh_rate]

with col2:
    auto_refresh = st.checkbox("Rafraîchissement automatique", value=True)
    
    if auto_refresh and refresh_seconds > 0:
        st.info(f"🔄 Prochain rafraîchissement dans {refresh_seconds} secondes")
        time.sleep(0.1)  # Petite pause pour l'effet
        # En production, utiliser st.rerun() dans une boucle

with col3:
    if st.button("📊 Générer Rapport Instantané", use_container_width=True):
        # Créer un rapport instantané
        report_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        st.success(f"📄 Rapport généré à {report_time}")
        
        # Afficher un résumé
        with st.expander("📋 Voir le rapport"):
            st.write("### 📊 Rapport Instantané GBH Group")
            st.write(f"**Heure de génération:** {report_time}")
            st.write(f"**CA total:** {data['financial_data']['Chiffre_d_affaires'].iloc[-1]:,.0f}€")
            st.write(f"**Satisfaction actuelle:** {data['financial_data']['Satisfaction_client'].iloc[-1]:.1f}/5.0")
            st.write(f"**Nombre de territoires actifs:** {len(data['territory_data'])}")
            st.write(f"**Transactions récentes:** {data['transaction_monitoring'].get('recent_transactions_count', 0)}")

# Pied de page avec info temps réel
st.divider()

footer_col1, footer_col2, footer_col3 = st.columns(3)

with footer_col1:
    last_update = data['last_updated'].strftime('%H:%M:%S') if 'last_updated' in data else 'N/A'
    st.caption(f"🕒 Dernière mise à jour: {last_update}")

with footer_col2:
    total_transactions = data['transaction_monitoring'].get('total_transactions', 0)
    st.caption(f"💳 Total transactions: {total_transactions}")

with footer_col3:
    territory_coverage = data['transaction_monitoring'].get('territory_coverage', 0)
    st.caption(f"🌍 Couverture territoriale: {territory_coverage} régions")

# Rafraîchissement automatique
if auto_refresh and refresh_seconds > 0:
    time.sleep(refresh_seconds)
    st.rerun()
