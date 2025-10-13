# Dashboard_GBH_Premium.py
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import dash
from dash import dcc, html, Input, Output, dash_table, callback_context
import dash_bootstrap_components as dbc
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
ninja_simulator = NinjaGBHDataSimulator()
COLORS.update(ninja_simulator.territory_colors)

print("🎨 Initialisation du Dashboard GBH Premium...")
financial_data = ninja_simulator.generate_financial_data()
territory_data = ninja_simulator.generate_territory_performance()
store_stats = ninja_simulator.get_store_statistics()
kpi_summary = ninja_simulator.get_kpi_summary()
transactions_data = ninja_simulator.generate_real_transactions(15)

# Application Dash avec thème personnalisé
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.DARKLY])

# Styles CSS personnalisés
CUSTOM_STYLES = {
    'header_gradient': {
        'background': f'linear-gradient(135deg, {COLORS["gradient_start"]}, {COLORS["gradient_end"]})',
        'borderRadius': '15px',
        'padding': '30px',
        'marginBottom': '30px',
        'boxShadow': '0 10px 30px rgba(0,0,0,0.3)'
    },
    'metric_card': {
        'backgroundColor': COLORS['card_bg'],
        'border': f'1px solid {COLORS["card_border"]}',
        'borderRadius': '12px',
        'padding': '20px',
        'height': '100%',
        'transition': 'all 0.3s ease',
        'boxShadow': '0 4px 15px rgba(0,0,0,0.2)'
    },
    'metric_card_hover': {
        'transform': 'translateY(-5px)',
        'boxShadow': '0 8px 25px rgba(0,0,0,0.3)'
    },
    'section_header': {
        'borderLeft': f'4px solid {COLORS["primary"]}',
        'paddingLeft': '15px',
        'marginBottom': '25px',
        'marginTop': '10px'
    }
}

app.layout = dbc.Container([
    # Header avec navigation
    dbc.Row([
        dbc.Col([
            html.Div([
                html.Div([
                    html.H1("🏬 GBH GROUP", 
                           className="display-4 mb-2",
                           style={'color': COLORS['text_primary'], 
                                  'fontWeight': '700',
                                  'textShadow': '2px 2px 4px rgba(0,0,0,0.3)'}),
                    html.H4("Tableau de Bord Exécutif - Tous Territoires", 
                           style={'color': COLORS['text_secondary'],
                                  'fontWeight': '300'}),
                    
                    dbc.Row([
                        dbc.Col([
                            html.Div([
                                html.Span("🌍", style={'fontSize': '24px', 'marginRight': '10px'}),
                                html.Span(f"{kpi_summary['total_territoires']} Territoires", 
                                         style={'color': COLORS['text_primary'], 'fontWeight': '600'}),
                                html.Span(" • ", style={'color': COLORS['text_muted']}),
                                html.Span(f"{kpi_summary['total_magasins']} Magasins", 
                                         style={'color': COLORS['text_primary'], 'fontWeight': '600'})
                            ], style={'textAlign': 'center', 'marginTop': '15px'})
                        ], width=12)
                    ])
                ], style=CUSTOM_STYLES['header_gradient'])
            ])
        ], width=12)
    ], className="mb-4"),
    
    # Navigation
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    dbc.ButtonGroup([
                        dbc.Button("📊 Vue d'Ensemble", id="btn-overview", color="primary", active=True),
                        dbc.Button("🏝️ Analyse DROM", id="btn-drom", color="danger"),
                        dbc.Button("🏖️ Analyse COM", id="btn-com", color="warning"),
                        dbc.Button("🏙️ Analyse Métropole", id="btn-metro", color="info"),
                        dbc.Button("📈 Performance Financière", id="btn-finance", color="success"),
                    ], size="lg", style={'width': '100%', 'justifyContent': 'center'})
                ])
            ], style={'backgroundColor': 'transparent', 'border': 'none'})
        ], width=12)
    ], className="mb-4"),
    
    # KPI Principaux - Ligne 1
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.Div([
                        html.Div([
                            html.I(className="fas fa-euro-sign fa-2x", 
                                  style={'color': COLORS['success']})
                        ], className="text-center mb-3"),
                        html.H4("Chiffre d'Affaires", 
                               style={'color': COLORS['text_secondary'], 
                                      'fontSize': '14px',
                                      'fontWeight': '600'}),
                        html.H2(id="ca-value", 
                               style={'color': COLORS['success'], 
                                      'fontWeight': '700',
                                      'margin': '10px 0'}),
                        html.Div(id="ca-trend",
                               style={'color': COLORS['text_muted'], 
                                      'fontSize': '12px'})
                    ], className="text-center")
                ])
            ], style=CUSTOM_STYLES['metric_card'], id="card-ca")
        ], width=2),
        
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.Div([
                        html.Div([
                            html.I(className="fas fa-chart-line fa-2x", 
                                  style={'color': COLORS['primary']})
                        ], className="text-center mb-3"),
                        html.H4("Bénéfice Net", 
                               style={'color': COLORS['text_secondary'], 
                                      'fontSize': '14px',
                                      'fontWeight': '600'}),
                        html.H2(id="profit-value", 
                               style={'color': COLORS['primary'], 
                                      'fontWeight': '700',
                                      'margin': '10px 0'}),
                        html.Div(id="profit-trend",
                               style={'color': COLORS['text_muted'], 
                                      'fontSize': '12px'})
                    ], className="text-center")
                ])
            ], style=CUSTOM_STYLES['metric_card'], id="card-profit")
        ], width=2),
        
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.Div([
                        html.Div([
                            html.I(className="fas fa-users fa-2x", 
                                  style={'color': COLORS['info']})
                        ], className="text-center mb-3"),
                        html.H4("Effectifs", 
                               style={'color': COLORS['text_secondary'], 
                                      'fontSize': '14px',
                                      'fontWeight': '600'}),
                        html.H2(id="employees-value", 
                               style={'color': COLORS['info'], 
                                      'fontWeight': '700',
                                      'margin': '10px 0'}),
                        html.Div("Employés", 
                               style={'color': COLORS['text_muted'], 
                                      'fontSize': '12px'})
                    ], className="text-center")
                ])
            ], style=CUSTOM_STYLES['metric_card'], id="card-employees")
        ], width=2),
        
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.Div([
                        html.Div([
                            html.I(className="fas fa-store fa-2x", 
                                  style={'color': COLORS['warning']})
                        ], className="text-center mb-3"),
                        html.H4("Magasins", 
                               style={'color': COLORS['text_secondary'], 
                                      'fontSize': '14px',
                                      'fontWeight': '600'}),
                        html.H2(id="stores-value", 
                               style={'color': COLORS['warning'], 
                                      'fontWeight': '700',
                                      'margin': '10px 0'}),
                        html.Div("Points de vente", 
                               style={'color': COLORS['text_muted'], 
                                      'fontSize': '12px'})
                    ], className="text-center")
                ])
            ], style=CUSTOM_STYLES['metric_card'], id="card-stores")
        ], width=2),
        
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.Div([
                        html.Div([
                            html.I(className="fas fa-star fa-2x", 
                                  style={'color': COLORS['drom']})
                        ], className="text-center mb-3"),
                        html.H4("Satisfaction", 
                               style={'color': COLORS['text_secondary'], 
                                      'fontSize': '14px',
                                      'fontWeight': '600'}),
                        html.H2(id="satisfaction-value", 
                               style={'color': COLORS['drom'], 
                                      'fontWeight': '700',
                                      'margin': '10px 0'}),
                        html.Div("/ 5.0", 
                               style={'color': COLORS['text_muted'], 
                                      'fontSize': '12px'})
                    ], className="text-center")
                ])
            ], style=CUSTOM_STYLES['metric_card'], id="card-satisfaction")
        ], width=2),
        
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.Div([
                        html.Div([
                            html.I(className="fas fa-shopping-basket fa-2x", 
                                  style={'color': COLORS['com']})
                        ], className="text-center mb-3"),
                        html.H4("Panier Moyen", 
                               style={'color': COLORS['text_secondary'], 
                                      'fontSize': '14px',
                                      'fontWeight': '600'}),
                        html.H2(id="basket-value", 
                               style={'color': COLORS['com'], 
                                      'fontWeight': '700',
                                      'margin': '10px 0'}),
                        html.Div("€", 
                               style={'color': COLORS['text_muted'], 
                                      'fontSize': '12px'})
                    ], className="text-center")
                ])
            ], style=CUSTOM_STYLES['metric_card'], id="card-basket")
        ], width=2)
    ], className="mb-4"),
    
    # Première ligne de graphiques
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardHeader([
                    html.H4("📈 Évolution Financière", 
                           style={'color': COLORS['text_primary'], 
                                  'margin': '0'})
                ], style={'backgroundColor': COLORS['card_bg'], 
                         'borderBottom': f'1px solid {COLORS["card_border"]}'}),
                dbc.CardBody([
                    dcc.Graph(id="financial-trend", style={'height': '400px'})
                ])
            ], style=CUSTOM_STYLES['metric_card'])
        ], width=8),
        
        dbc.Col([
            dbc.Card([
                dbc.CardHeader([
                    html.H4("🌍 Répartition Territoriale", 
                           style={'color': COLORS['text_primary'], 
                                  'margin': '0'})
                ], style={'backgroundColor': COLORS['card_bg'], 
                         'borderBottom': f'1px solid {COLORS["card_border"]}'}),
                dbc.CardBody([
                    dcc.Graph(id="territory-breakdown", style={'height': '400px'})
                ])
            ], style=CUSTOM_STYLES['metric_card'])
        ], width=4)
    ], className="mb-4"),
    
    # Deuxième ligne de graphiques
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardHeader([
                    html.H4("🏆 Performance par Territoire", 
                           style={'color': COLORS['text_primary'], 
                                  'margin': '0'})
                ], style={'backgroundColor': COLORS['card_bg'], 
                         'borderBottom': f'1px solid {COLORS["card_border"]}'}),
                dbc.CardBody([
                    dcc.Graph(id="territory-performance", style={'height': '450px'})
                ])
            ], style=CUSTOM_STYLES['metric_card'])
        ], width=12)
    ], className="mb-4"),
    
    # Troisième ligne : Analyse détaillée
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardHeader([
                    html.H4("📊 Analyse Comparative", 
                           style={'color': COLORS['text_primary'], 
                                  'margin': '0'})
                ], style={'backgroundColor': COLORS['card_bg'], 
                         'borderBottom': f'1px solid {COLORS["card_border"]}'}),
                dbc.CardBody([
                    dbc.Row([
                        dbc.Col([
                            dcc.Graph(id="type-comparison", style={'height': '300px'})
                        ], width=4),
                        dbc.Col([
                            dcc.Graph(id="stores-analysis", style={'height': '300px'})
                        ], width=4),
                        dbc.Col([
                            dcc.Graph(id="performance-gauges", style={'height': '300px'})
                        ], width=4)
                    ])
                ])
            ], style=CUSTOM_STYLES['metric_card'])
        ], width=12)
    ], className="mb-4"),
    
    # Quatrième ligne : Transactions et indicateurs temps réel
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardHeader([
                    html.H4("💳 Transactions en Temps Réel", 
                           style={'color': COLORS['text_primary'], 
                                  'margin': '0'})
                ], style={'backgroundColor': COLORS['card_bg'], 
                         'borderBottom': f'1px solid {COLORS["card_border"]}'}),
                dbc.CardBody([
                    dash_table.DataTable(
                        id='transaction-table',
                        columns=[
                            {'name': 'Date', 'id': 'Date'},
                            {'name': 'Type', 'id': 'Type'},
                            {'name': 'Catégorie', 'id': 'Catégorie'},
                            {'name': 'Territoire', 'id': 'Territoire'},
                            {'name': 'Type Territoire', 'id': 'Type_Territoire'},
                            {'name': 'Montant', 'id': 'Montant'}
                        ],
                        style_cell={
                            'backgroundColor': COLORS['card_bg'],
                            'color': COLORS['text_primary'],
                            'border': f'1px solid {COLORS["card_border"]}',
                            'textAlign': 'left',
                            'fontSize': '12px',
                            'fontFamily': 'Arial, sans-serif'
                        },
                        style_header={
                            'backgroundColor': COLORS['primary'],
                            'color': 'white',
                            'fontWeight': 'bold',
                            'border': f'1px solid {COLORS["card_border"]}',
                            'textAlign': 'center'
                        },
                        style_data_conditional=[
                            {
                                'if': {'row_index': 'odd'},
                                'backgroundColor': '#1E2A47'
                            },
                            {
                                'if': {'filter_query': '{Montant} contains "-"'},
                                'color': COLORS['danger'],
                                'fontWeight': '600'
                            },
                            {
                                'if': {'filter_query': '{Montant} contains "+"'},
                                'color': COLORS['success'],
                                'fontWeight': '600'
                            },
                            {
                                'if': {'column_id': 'Type_Territoire', 'filter_query': '{Type_Territoire} = "DROM"'},
                                'backgroundColor': COLORS['drom'],
                                'color': 'white',
                                'fontWeight': '600'
                            },
                            {
                                'if': {'column_id': 'Type_Territoire', 'filter_query': '{Type_Territoire} = "COM"'},
                                'backgroundColor': COLORS['com'],
                                'color': 'white',
                                'fontWeight': '600'
                            },
                            {
                                'if': {'column_id': 'Type_Territoire', 'filter_query': '{Type_Territoire} = "Métropole"'},
                                'backgroundColor': COLORS['metro'],
                                'color': 'white',
                                'fontWeight': '600'
                            }
                        ],
                        page_size=8,
                        page_action='native',
                        sort_action='native',
                        filter_action='native',
                        style_table={'overflowX': 'auto'}
                    )
                ])
            ], style=CUSTOM_STYLES['metric_card'])
        ], width=12)
    ], className="mb-4"),
    
    # Pied de page
    dbc.Row([
        dbc.Col([
            html.Div([
                html.Hr(style={'borderColor': COLORS['card_border'], 'margin': '20px 0'}),
                html.Div([
                    html.Span("🔄 ", style={'color': COLORS['primary']}),
                    html.Span("Dernière mise à jour: ", 
                             style={'color': COLORS['text_secondary']}),
                    html.Span(id="last-update", 
                             style={'color': COLORS['text_primary'], 'fontWeight': 'bold'}),
                    dbc.Button("🔄 Actualiser les Données", 
                              id="refresh-btn",
                              color="primary",
                              className="ms-3",
                              size="sm",
                              style={'backgroundColor': COLORS['primary'], 
                                     'border': 'none'}),
                    html.Span(" • ", className="ms-2", style={'color': COLORS['text_muted']}),
                    html.Span("GBH Group Dashboard Premium v2.0", 
                             style={'color': COLORS['text_muted'], 'fontSize': '12px'})
                ], className="text-center")
            ], style={'padding': '20px 0'})
        ], width=12)
    ]),
    
    # Intervalles de mise à jour
    dcc.Interval(
        id='interval-component',
        interval=60*1000,  # Mise à jour toutes les minutes
        n_intervals=0
    ),
    dcc.Store(id='view-store', data='overview')
    
], fluid=True, style={
    'backgroundColor': COLORS['background'],
    'minHeight': '100vh',
    'padding': '20px',
    'fontFamily': 'Arial, sans-serif'
})

# Callbacks pour l'interactivité
@app.callback(
    [Output('card-ca', 'style'),
     Output('card-profit', 'style'),
     Output('card-employees', 'style'),
     Output('card-stores', 'style'),
     Output('card-satisfaction', 'style'),
     Output('card-basket', 'style')],
    [Input('card-ca', 'n_clicks'),
     Input('card-profit', 'n_clicks'),
     Input('card-employees', 'n_clicks'),
     Input('card-stores', 'n_clicks'),
     Input('card-satisfaction', 'n_clicks'),
     Input('card-basket', 'n_clicks')]
)
def hover_effect(*args):
    ctx = callback_context
    if not ctx.triggered:
        return [CUSTOM_STYLES['metric_card']] * 6
    
    card_id = ctx.triggered[0]['prop_id'].split('.')[0]
    base_style = CUSTOM_STYLES['metric_card'].copy()
    hover_style = CUSTOM_STYLES['metric_card'].copy()
    hover_style.update(CUSTOM_STYLES['metric_card_hover'])
    
    styles = [base_style] * 6
    card_index = ['card-ca', 'card-profit', 'card-employees', 'card-stores', 'card-satisfaction', 'card-basket'].index(card_id)
    styles[card_index] = hover_style
    
    return styles

@app.callback(
    [Output('ca-value', 'children'),
     Output('profit-value', 'children'),
     Output('employees-value', 'children'),
     Output('stores-value', 'children'),
     Output('satisfaction-value', 'children'),
     Output('basket-value', 'children'),
     Output('ca-trend', 'children'),
     Output('profit-trend', 'children'),
     Output('last-update', 'children')],
    [Input('interval-component', 'n_intervals'),
     Input('refresh-btn', 'n_clicks')]
)
def update_main_stats(n_intervals, n_clicks):
    if n_clicks:
        global financial_data
        last_date = financial_data['Date'].iloc[-1]
        new_date = last_date + timedelta(days=1)
        new_data = ninja_simulator.generate_financial_data(
            start_date=new_date.strftime('%Y-%m-%d'),
            end_date=new_date
        )
        financial_data = pd.concat([financial_data, new_data], ignore_index=True)
    
    latest = financial_data.iloc[-1]
    
    # Formater les valeurs avec style
    ca_total = f"{latest['Chiffre_d_affaires']:,.0f}".replace(',', ' ')
    profit_total = f"{latest['Bénéfice_net']:,.0f}".replace(',', ' ')
    employees = f"{latest['Effectifs']:.0f}"
    stores = f"{latest['Nbre_magasins']:.0f}"
    satisfaction = f"{latest['Satisfaction_client']:.1f}"
    basket = f"{latest['Panier_moyen']:.1f}"
    
    # Tendances
    if len(financial_data) > 1:
        prev = financial_data.iloc[-2]
        daily_ca = latest['Chiffre_d_affaires'] - prev['Chiffre_d_affaires']
        daily_profit = latest['Bénéfice_net'] - prev['Bénéfice_net']
        
        ca_trend_text = f"↗️ {daily_ca:,.0f}€/jour".replace(',', ' ')
        profit_trend_text = f"↗️ {daily_profit:,.0f}€/jour".replace(',', ' ')
    else:
        ca_trend_text = "→ Données en cours"
        profit_trend_text = "→ Données en cours"
    
    update_time = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
    
    return ca_total, profit_total, employees, stores, satisfaction, basket, ca_trend_text, profit_trend_text, update_time

@app.callback(
    Output('financial-trend', 'figure'),
    [Input('interval-component', 'n_intervals')]
)
def update_financial_trend(n_intervals):
    fig = go.Figure()
    
    # Courbe du CA cumulé
    fig.add_trace(go.Scatter(
        x=financial_data['Date'],
        y=financial_data['Chiffre_d_affaires'],
        mode='lines',
        name='CA Cumulé',
        line=dict(color=COLORS['success'], width=4, shape='spline'),
        fill='tozeroy',
        fillcolor=f'rgba({int(COLORS["success"][1:3], 16)}, {int(COLORS["success"][3:5], 16)}, {int(COLORS["success"][5:7], 16)}, 0.1)'
    ))
    
    # Courbe des bénéfices
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

@app.callback(
    Output('territory-breakdown', 'figure'),
    [Input('interval-component', 'n_intervals')]
)
def update_territory_breakdown(n_intervals):
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

@app.callback(
    Output('territory-performance', 'figure'),
    [Input('interval-component', 'n_intervals')]
)
def update_territory_performance(n_intervals):
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

@app.callback(
    Output('type-comparison', 'figure'),
    [Input('interval-component', 'n_intervals')]
)
def update_type_comparison(n_intervals):
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

@app.callback(
    Output('stores-analysis', 'figure'),
    [Input('interval-component', 'n_intervals')]
)
def update_stores_analysis(n_intervals):
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

@app.callback(
    Output('performance-gauges', 'figure'),
    [Input('interval-component', 'n_intervals')]
)
def update_performance_gauges(n_intervals):
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

@app.callback(
    Output('transaction-table', 'data'),
    [Input('interval-component', 'n_intervals'),
     Input('refresh-btn', 'n_clicks')]
)
def update_transaction_table(n_intervals, n_clicks):
    if n_clicks:
        global transactions_data
        transactions_data = ninja_simulator.generate_real_transactions(15)
    
    return transactions_data

if __name__ == '__main__':
    print("🚀 Dashboard GBH Premium démarré!")
    print("🎨 Design professionnel activé")
    print(f"📊 {len(financial_data)} jours de données financières")
    print(f"🌍 {kpi_summary['total_territoires']} territoires couverts")
    print(f"🏪 {kpi_summary['total_magasins']} points de vente")
    print("💎 Interface premium accessible sur: http://localhost:8050")
    
    app.run (debug=True, host='0.0.0.0', port=8050)