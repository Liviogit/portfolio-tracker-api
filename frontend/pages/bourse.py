from dash import html, dcc, Input, Output, callback
import plotly.graph_objs as go
import requests
from datetime import datetime
from dateutil.relativedelta import relativedelta

API_URL = "http://api:5001/tickers"  # à adapter si ton backend tourne sur un autre port

def create_bourse():
    layout = html.Div([
        html.Div([html.H2("Recherche d’un actif", style={'textAlign': 'center', 'color': '#000'}),dcc.Dropdown(
            id="period-selector",
            options=[
                {"label": "1j (A ne pas utiliser le weekend)", "value": "1d"},
                {"label": "1s", "value": "1wk"},
                {"label": "1m", "value": "1mo"},
                {"label": "3m", "value": "3mo"},
                {"label": "6m", "value": "6mo"},
                {"label": "1an", "value": "1y"},
                {"label": "Tout", "value": "max"}
            ],
            value="1wk",
            clearable=False,
            style={"width": "100%"}
        )]),
        html.Div([
            dcc.Input(
                id='ticker-input',
                type='text',
                placeholder='Ex: AAPL',
                style={
                    'marginRight': '10px',
                    'padding': '5px',
                    'borderRadius': '5px',
                    'border': '1px solid #ccc'
                }
            ),
            html.Button(
                'Afficher',
                id='search-button',
                n_clicks=0,
                style={
                    'padding': '5px 15px',
                    'borderRadius': '5px',
                    'backgroundColor': '#1e90ff',
                    'color': 'white',
                    'border': 'none',
                    'cursor': 'pointer'
                }
            )
        ], style={'textAlign': 'center'}),
        html.Div(id='error-message', style={'textAlign': 'center', 'color': 'red', 'marginTop': '10px'}),
        dcc.Graph(id='graph-bourse', style={'marginTop': '30px'})
    ])
    return layout


@callback(
    [Output('graph-bourse', 'figure'),
     Output('error-message', 'children')],
    [Input('search-button', 'n_clicks'),
     Input('ticker-input', 'value'),
     Input('period-selector', 'value')],
)
def update_graph(n_clicks, ticker, period):
    if not ticker or n_clicks == 0:
        return go.Figure(), ""
    today = datetime.today()
    label = period
    start_date = None
    interval = "1d"
    if label == "1d":
        # minimum interval = 1m
        start_date = today - relativedelta(days=1)
        interval = "1m"
    elif label == "1wk":
        # minimum interval = 5m
        start_date = today - relativedelta(weeks=1)
        interval = "1d"
    elif label == "1mo":
        # minimum interval = 15m
        start_date = today - relativedelta(months=1)
        interval = "1d"
    elif label == "3mo":
        # minimum interval = 30m
        start_date = today - relativedelta(months=3)
        interval = "1d"
    elif label == "6mo":
        # minimum interval = 1h
        start_date = today - relativedelta(months=6)
        interval = "1d"
    elif label == "1y":
        # minimum interval = 1d
        start_date = today - relativedelta(years=1)
        interval = "1d"
    elif label == "max":
        # maximum historique disponible
        start_date = None
        interval = "1d"
    try:
        # Requête à ton API
        if start_date:
            response = requests.get(f"{API_URL}/{ticker.strip().upper()}/?interval={interval}&start={start_date.strftime('%Y-%m-%d')}")
        else:
            response = requests.get(f"{API_URL}/{ticker.strip().upper()}/?period=max")
        if response.status_code != 200:
            return go.Figure(), f"Erreur API ({response.status_code}) : {response.text}"

        data = response.json()

        # Vérifie si la réponse contient des données
        if not data or len(data) == 0:
            return go.Figure(), "Aucune donnée trouvée pour ce ticker."

        # Conversion des données
        data=data[ticker.strip().upper()]
        x = [d["Date"] for d in data if "Date" in d]
        y = [d["Close"] for d in data if "Close" in d]

        fig = go.Figure(data=[
            go.Scatter(x=x, y=y, mode='lines', name=ticker.upper())
        ])
        fig.update_layout(
            title=f"Évolution de {ticker.upper()}",
            xaxis_title="Date",
            yaxis_title="Prix (€)",
            paper_bgcolor='#303030',
            plot_bgcolor='#303030',
            font=dict(color='white')
        )

        return fig, ""

    except Exception as e:
        return go.Figure(),""
