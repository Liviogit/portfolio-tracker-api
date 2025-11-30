from dash import html, dcc, Input, Output, State, callback
import requests
def create_trades(user_data, portfolio_id):
    api_url = f"http://api:5001/trades/portfolio/{portfolio_id}"  # ton endpoint
    token = user_data["access_token"]
    token_type = user_data.get("token_type", "bearer")
    headers = {
        "Authorization": f"{token_type.capitalize()} {token}"
    }
    try:
        response = requests.get(api_url, headers=headers, timeout=5)

        if response.status_code == 200:
            data = response.json()   # liste de trades

            trades = data  # pas data[0], ta réponse est déjà une liste

            if not trades:
                trade_items = [html.Div("Aucun trade pour ce portefeuille.")]
            else:
                trade_items = [
                    html.Li(
                        f"{trade['action']} {trade['quantity']}x {trade['asset_name']} "
                        f"à {trade['price']}€ le {trade['trade_date']}"
                    )
                    for trade in trades
                ]


        else:
            return html.Div(f"Erreur API : {response.status_code} - {response.text} {api_url}")

    except requests.exceptions.RequestException:
        return html.Div("Impossible de contacter l'API.")
    return html.Div(trade_items+[
        html.H2("Ajouter un trade", style={'textAlign': 'center'}),
        html.Div([
            dcc.Dropdown(id='trade-type',options=[{'label': 'BUY', 'value': 'BUY'},{'label': 'SELL', 'value': 'SELL'}],placeholder="Type d’ordre",style={'width': '150px', 'margin': '5px'}),
            dcc.Input(id='trade-ticker', type='text', placeholder='Ticker', style={'margin': '5px'}),
            dcc.Input(id='trade-quantite', type='number', placeholder='Quantité', style={'margin': '5px'}),
            dcc.Input(id='trade-prix', type='number', placeholder='Prix (€)', style={'margin': '5px'}),
            html.Button('Ajouter', id='add-trade', n_clicks=0),
        ], style={'textAlign': 'center'}),
        html.Div(id='trade-output', style={'marginTop': '20px', 'textAlign': 'center'})
    ])

@callback(
    Output('trade-output', 'children'),
    Input('add-trade', 'n_clicks'),
    State('trade-type', 'value'),
    State('trade-ticker', 'value'),
    State('trade-quantite', 'value'),
    State('trade-prix', 'value'),
    State('user-data', 'data'),
    State('portfolio-data', 'data')
)
def add_trade(n_clicks, trade_type, ticker, quantite, prix, user_data,portfolio_data):
    if not (n_clicks > 0 and trade_type and ticker and quantite>0 and prix>0):
        return "Veuillez remplir tous les champs."
    
    api_url = f"http://api:5001/trades/"  # ton endpoint
    token = user_data["access_token"]
    token_type = user_data.get("token_type", "bearer")
    headers = {
        "Authorization": f"{token_type.capitalize()} {token}"
    }
    payload = {
    "asset_name":ticker,
    "action": trade_type,
    "price": prix,
    "quantity": quantite,
    "portfolio_id": portfolio_data
    }
    try:
        response = requests.post(api_url, headers=headers,json=payload)

        if response.status_code == 200:
            return f"Trade ajouté : {trade_type} {quantite}x {ticker} à {prix}€"

        return f"Impossible de contacter l'API.{payload}"
    except requests.exceptions.RequestException:
        return f"Impossible de contacter l'API.{payload}"
    