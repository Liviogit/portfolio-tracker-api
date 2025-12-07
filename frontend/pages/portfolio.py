# portfolio.py
from dash import html, callback, Output, Input, ALL, State, no_update, dcc
import requests
import dash_bootstrap_components as dbc
import json
import yfinance as yf
import pandas as pd
import plotly.graph_objs as go
from pages.trades import create_trades
from datetime import datetime
from dateutil.relativedelta import relativedelta

def ticker_exists(ticker: str) -> bool:
    try:
        data = yf.Ticker(ticker).history(period="1d")
        return not data.empty
    except Exception:
        return False

# -------------------------------
# Fonctions de création des composants
def create_sidebar():
    return html.Div([
        html.H2("Portefeuilles"),
        html.Div("Chargement...", id="portfolio-list-container")
    ])


def create_empty_output():
    """Zone d'affichage du portefeuille sélectionné"""
    return html.Div(
        id="portfolio-output",
        style={
            "width": "80%",
            "padding": "20px",
        }
    )

def create_portfolio():
    """Layout principal combinant sidebar et zone d'output"""
    return html.Div(
        style={"display": "flex", "flexDirection": "row"},
        children=[
            create_sidebar(),
            create_empty_output(),
        ]
    )

def create_portfolio_output(data,portfolio_id,user_data):
    API_URL="http://api:5001/tickers"
    last_amount = data.get("last_amount", "N/A")
    initial_amount = data.get("initial_amount", "N/A")
    cash= data.get("cash_balance", 0)
    tickers = data.get("positions", "").lower()
    tickers_list = tickers.split(",")
    positions_size = data.get("positions_size","").split(",")
    portfolio_dict=dict(zip(tickers_list, positions_size))
    response=requests.get(f"{API_URL}/{tickers.strip().upper()}")
    response=response.json()
    dates=[line['Date'] for line in response[next(iter(response))]]
    prices=[]
    for ticker, rows in response.items():
        ticker=ticker.lower()
        df = pd.DataFrame(rows)
        dates=df['Date'].to_list()
        df=df['Close']
        df=df*int(portfolio_dict.get(ticker,portfolio_dict.get(ticker.upper(),1)))
        prices = [round(a + b, 2) for a, b in zip(prices, df.tolist())] if not prices == [] else df.tolist()

    fig = go.Figure(data=[
            go.Scatter(x=dates, y=prices, mode='lines', name="Evolution du portefeuille")
        ])
    fig.update_layout(
        title=f"Évolution du portefeuille",
        xaxis_title="Date",
        yaxis_title="Prix (€)",
        paper_bgcolor='#303030',
        plot_bgcolor='#303030',
        font=dict(color='white')
    )
    if prices:
        last_amount=prices[-1]
        API_URL_portfolios=f"http://api:5001/portfolios/{portfolio_id}"
        token = user_data["access_token"]
        token_type = user_data.get("token_type", "bearer")
        headers = {
            "Authorization": f"{token_type.capitalize()} {token}"
        }
        playload = {
            "last_amount": last_amount
        }
        try:
            response = requests.put(API_URL_portfolios, headers=headers, json=playload, timeout=5)
        except requests.exceptions.RequestException:
            pass
    last_amount=round(last_amount,2)
    evolution= (last_amount + cash - initial_amount) / initial_amount * 100 if initial_amount !=0 else 0
    evolution_layout=html.P(f"Évolution du portefeuille depuis sa création: {round(evolution,1):.2f} %", style={'color': 'green' if evolution >=0 else 'red'})
    trades_layout=create_trades(user_data,portfolio_id)
    res=html.Div([html.Div([
                    html.H3(f"Détails du portefeuille {data.get('portfolio_name', '')}"),
                    html.Button(
                        "supprimer le portefeuille",
                        id="delete-portfolio-btn",
                        n_clicks=0,
                        className="btn btn-danger mb-3",
                        style={"float": "right", "color": "red"}
                    )
                ]),
            html.P(f"Montant initial investi : {initial_amount} €"),
            html.P(f"Montant actuel (cash inclus) : {last_amount} €"),
            html.P(f"Montant en cash dans le portefeuille: {data.get('cash_balance', 'Donnée indisponible')} €"),
            evolution_layout,
            html.H4("Positions actuelles dans le portefeuille :"),
            html.Ul([html.Li(f"{ticker} : {size} actions") for ticker, size in portfolio_dict.items()]),
            dcc.Dropdown(
            id="period-selector",
            options=[
                {"label": "1j (A ne pas utiliser le weekend)", "value": "1d"},
                {"label": "1s", "value": "1wk"},
                {"label": "1m", "value": "1mo"},
                {"label": "3m", "value": "3mo"},
                {"label": "6m", "value": "6mo"},
                {"label": "1an", "value": "1y"},
                {"label": "Tout", "value": "max"}
            ],value="1wk",clearable=False,style={"width": "100%"}),
            dcc.Graph(figure=fig,id="portfolio-graph"),
            html.H4("Trades associés au portefeuille :"),
            trades_layout
    ])
    return res
@callback(
    Output("portfolio-graph", "figure"),
    Input("period-selector", "value"),
    State("portfolio-data", "data"),
    State("user-data", "data"),
    prevent_initial_call=True
)
def update_portfolio_graph(period, portfolio_id, user_data):
    try:
        api_url = f"http://api:5001/portfolios/{portfolio_id}"  # ton endpoint
        token = user_data["access_token"]
        token_type = user_data.get("token_type", "bearer")
        headers = {
            "Authorization": f"{token_type.capitalize()} {token}"
        }
        try:
            response = requests.get(api_url,headers=headers, timeout=5)
            if response.status_code == 200:
                data = response.json()
            else:
                return no_update
        except requests.exceptions.RequestException:
            return no_update

        # Construction du tableau HTML
        if not data:
            return no_update
        data=data[0]
        API_URL="http://api:5001/tickers"
        tickers = data.get("positions", "").upper()
        tickers_list = tickers.split(",")
        positions_size = data.get("positions_size","").split(",")
        portfolio_dict=dict(zip(tickers_list, positions_size))

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
            start_date = data.get("portfolio_date", today - relativedelta(years=1))
            interval = "1d"
        elif label == "max":
            # minimum interval = 1d
            start_date = today - relativedelta(years=10)
            interval = "1d"
        response=requests.get(f"{API_URL}/{tickers.strip().upper()}/?interval={interval}&start={start_date.strftime('%Y-%m-%d')}")
        response=response.json()
        dates=[line['Date'] for line in response[next(iter(response))]]
        prices=[]
        for ticker, rows in response.items():
            df = pd.DataFrame(rows)
            dates=df['Date'].to_list()
            df=df['Close']
            df=df*int(portfolio_dict[ticker])
            prices=prices+df.tolist()

        fig = go.Figure(data=[
                go.Scatter(x=dates, y=prices, mode='lines', name="Evolution du portefeuille")
            ])
        fig.update_layout(
            title=f"Évolution du portefeuille",
            xaxis_title="Date",
            yaxis_title="Prix (€)",
            paper_bgcolor='#303030',
            plot_bgcolor='#303030',
            font=dict(color='white')
        )
        return fig
    except:
        return no_update
@callback(
    Output("portfolio-list-container", "children"),
    Input("url", "pathname"),          # déclenché quand tu arrives sur /portfolio
    State("user-data", "data")         # on lit ton token stocké
)
def load_portfolios(pathname, user_data):
    if pathname != "/portfolio":
        return no_update

    if not user_data or "access_token" not in user_data:
        return "Vous devez être connecté pour voir vos portefeuilles.\n Connectez-vous via le menu en haut."

    token = user_data["access_token"]
    token_type = user_data.get("token_type", "bearer")
    headers = {"Authorization": f"{token_type.capitalize()} {token}"}

    try:
        r = requests.get("http://api:5001/portfolios", headers=headers, timeout=5)

        if r.status_code == 200:
            portfolios = r.json()
        else:
            return f"Erreur API {r.status_code} : {r.text}"
    except Exception as e:
        return f"Erreur requête : {e}"
    return html.Div(
        [
            dbc.Nav(
                    [html.Button("+Créer un nouveau portefeuille", id="create-portfolio-btn", n_clicks=0, className="btn btn-primary mb-3 w-100")]+
                    [
                        html.Div([html.Button(
                            str(portfolios[i]['portfolio_name']),
                            id={"type": "portfolio-btn", "index": portfolios[i]['portfolio_id']},
                            n_clicks=0,
                            className="btn btn-link w-100 text-center",
                            style={"width": "100%", "display": "block"}
                        )])
                        for i in range(len(portfolios))
                    ],
                    vertical=True
                )
        ],
        style={
            "width": "60%",
            "height": "100vh",
            "padding": "20px",
            "borderRight": "1px solid #ccc",
            "backgroundColor": "#f8f9fa",
        },
    )
# -------------------------------
# Callback pour gérer le clic sur un bouton

@callback(
    [Output("portfolio-output", "children",allow_duplicate=True),
     Output("portfolio-data", "data", allow_duplicate=True)],
    Input({"type": "portfolio-btn", "index": ALL}, "n_clicks_timestamp"),
    State({"type": "portfolio-btn", "index": ALL}, "id"),
    State("user-data", "data"),
    prevent_initial_call='initial_duplicate'
)
def show_portfolio_by_ts(n_clicks_ts_list, portfolio_ids,user_data):
    # aucun clic (toutes valeurs None)
    if not n_clicks_ts_list or all(v is None for v in n_clicks_ts_list):
        return [no_update,no_update]

    # remplacer None par 0 (plus petit timestamp)
    safe_ts = [0 if v is None else v for v in n_clicks_ts_list]

    # trouver le dernier clic (max timestamp)
    last_ts = max(safe_ts)
    idx = safe_ts.index(last_ts)
    clicked_portfolio_id = portfolio_ids[idx]["index"]
    if not user_data or "access_token" not in user_data:
        return [html.Div("⛔ Pas de token – vous devez être connecté." + str(user_data)), no_update]
    
    # --- Requête API dynamique ---

    api_url = f"http://api:5001/portfolios/{clicked_portfolio_id}"  # ton endpoint
    token = user_data["access_token"]
    token_type = user_data.get("token_type", "bearer")
    headers = {
        "Authorization": f"{token_type.capitalize()} {token}"
    }
    try:
        response = requests.get(api_url,headers=headers, timeout=5)
        if response.status_code == 200:
            data = response.json()
        else:
            return [html.Div(f"Erreur API : {response.status_code} - {response.text} {api_url}"), no_update]
    except requests.exceptions.RequestException:
        return [html.Div("Impossible de contacter l'API."), no_update]

    # Construction du tableau HTML
    if not data:
        return [html.Div("Aucune donnée pour ce portefeuille."), no_update]
    bloc_portfolio=create_portfolio_output(data[0],clicked_portfolio_id,user_data)
    return [bloc_portfolio,clicked_portfolio_id]

@callback(
    Output("portfolio-output", "children", allow_duplicate=True),
    Input("create-portfolio-btn", "n_clicks_timestamp"),  # timestamp au lieu de n_clicks
    State("user-data", "data"),
    prevent_initial_call=True
)
def show_portfolio_creator(timestamp, user_data):
    # Vérifie si le bouton a été cliqué
    if timestamp is None or timestamp == 0:
        return no_update  # aucun clic détecté
    if not user_data or "access_token" not in user_data:
        return "⛔ Pas de token – vous devez être connecté." + str(user_data)
    
    # Si clic détecté, afficher le formulaire
    return html.Div(
        id="portfolio-creator-form",
        children=[
            html.H2("Créer un nouveau portefeuille"),
            html.Hr(),
            html.Label("Nom du portefeuille"),
            dcc.Input(id="portfolio-name", type="text"),
            html.Hr(),
            html.Label("Montant initial investi"),
            dcc.Input(id="initial-amount", type="number", min=0),
            html.Hr(),
            html.Label("Montant en cash dans le portefeuille (optionnel)"),
            dcc.Input(id="cash-balance", type="number", min=0, value=0),

            html.Hr(),

            html.Div(id="positions-container", children=[]),

            html.Button("Ajouter une position", id="add-position-btn", n_clicks=0, className="mt-2"),
            html.Br(),

            html.Button("Créer le portefeuille", id="submit-portfolio-btn", n_clicks=0, className="mt-3")
        ]
    )

@callback(
    Output("positions-container", "children"),
    Input("add-position-btn", "n_clicks"),
    State("positions-container", "children"),
    prevent_initial_call=True
)
def add_position_row(n_clicks, current_children):

    new_index = len(current_children)

    new_row = html.Div([
        html.Label(f"Position {new_index+1} - Ticker"),
        dcc.Input(id={"type": "ticker", "index": new_index}, type="text"),

        html.Label("Taille (nombre d’actions)"),
        dcc.Input(id={"type": "size", "index": new_index}, type="number", min=0),
        html.Hr()
    ])

    return current_children + [new_row]

@callback(
    Output("portfolio-creator-form", "children",allow_duplicate=True),
    Input("submit-portfolio-btn", "n_clicks"),
    State("initial-amount", "value"),
    State({"type": "ticker", "index": ALL}, "value"),
    State({"type": "size", "index": ALL}, "value"),
    State("cash-balance", "value"),
    State("portfolio-name", "value"),
    State("user-data", "data"),
    prevent_initial_call=True
)
def submit_portfolio(n_clicks, initial_amount, tickers, sizes, cash_balance, portfolio_name, user_data):
    if not n_clicks:
        return no_update

    if not any(tickers) or not any(sizes) or initial_amount is None or initial_amount <= 0 or not portfolio_name:
        return "Veuillez remplir tous les champs"

    if not cash_balance or cash_balance < 0:
        cash_balance = 0

    for ticker in tickers:
        if not ticker_exists(ticker):
            return f"Le ticker '{ticker}' n'existe pas. Veuillez vérifier et réessayer.\n Il faut insérer le ticker de l'action et non le nom de l'entreprise."
    positions = json.dumps(tickers).replace('"', '').replace('[', '').replace(']', '')
    positions_size = json.dumps(sizes).replace('"', '').replace('[', '').replace(']', '')

    payload = {
        "last_amount": initial_amount,
        "initial_amount": initial_amount,
        "positions": positions.upper(),
        "positions_size": positions_size,
        "portfolio_name": portfolio_name,
        "cash_balance": cash_balance if cash_balance > 0 else 0
    }

    # appel API
    token = user_data["access_token"]
    token_type = user_data.get("token_type", "bearer")

    headers = {"Authorization": f"{token_type.capitalize()} {token}"}

    import requests

    res = requests.post("http://api:5001/portfolios", json=payload,headers=headers)

    if res.status_code != 200:
        return f"Erreur API : {res.text} \n {tickers} {sizes}"

    return "Portefeuille créé avec succès !"

@callback(
    Output("portfolio-output", "children", allow_duplicate=True),
    Input("delete-portfolio-btn", "n_clicks"),
    State("portfolio-data", "data"),
    State("user-data", "data"),
    prevent_initial_call=True
)
def delete_portfolio(n_clicks, portfolio_id, user_data):
    if not n_clicks or portfolio_id is None:
        return no_update

    # appel API
    token = user_data["access_token"]
    token_type = user_data.get("token_type", "bearer")

    headers = {"Authorization": f"{token_type.capitalize()} {token}"}

    import requests

    res = requests.delete(f"http://api:5001/portfolios/{portfolio_id}",headers=headers)

    if res.status_code != 200:
        return f"Erreur API : {res.text}"

    return "Portefeuille supprimé avec succès !"