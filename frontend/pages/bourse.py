from dash import html, dcc, Input, Output, callback
import plotly.graph_objs as go
import requests

API_URL = "http://api:5001/tickers"  # à adapter si ton backend tourne sur un autre port

def create_bourse():
    layout = html.Div([
        html.H2("Recherche d’un actif", style={'textAlign': 'center', 'color': '#fff'}),
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
     Input('ticker-input', 'value')]
)
def update_graph(n_clicks, ticker):
    if not ticker or n_clicks == 0:
        return go.Figure(), ""

    try:
        # Requête à ton API
        response = requests.get(f"{API_URL}/{ticker.strip().upper()}")
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
            go.Scatter(x=x, y=y, mode='lines+markers', name=ticker.upper())
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
        return go.Figure(), f"Erreur lors de la récupération des données : {str(e)}"
