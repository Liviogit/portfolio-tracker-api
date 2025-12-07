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
                        f"à {trade['price']}€ le {trade['trade_date']}: {trade.get('description', 'Aucune description')}"
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
            dcc.Textarea(id='trade-description',placeholder='Entrez votre texte…',style={'width': '100%','height': '150px','margin': '5px'}),
            html.Button('Ajouter', id='add-trade', n_clicks=0),
        ], style={'textAlign': 'center'}),
        html.Div(id='trade-output', style={'marginTop': '20px', 'textAlign': 'center'})
    ])

def check_balance(trade_type, price, quantity,ticker,user_data,portfolio_id):
    api_url = f"http://api:5001/portfolios/{portfolio_id}"  # ton endpoint
    token = user_data["access_token"]
    token_type = user_data.get("token_type", "bearer")
    headers = {
        "Authorization": f"{token_type.capitalize()} {token}"
    }
    try:
        response = requests.get(api_url, headers=headers)

        if response.status_code == 200:
            data=response.json()
            data=data[0]
            cash_balance = data.get("cash_balance", 0)
            required_amount = price * quantity
            if trade_type == 'BUY':
                if cash_balance >= required_amount:
                    tickers = data.get("positions", "").lower().split(",")
                    tickers_size = data.get("positions_size", "").split(",")
                    if ticker.lower() not in tickers:
                        tickers.append(ticker.lower())
                        tickers_size.append(str(quantity))
                        positions_str = ",".join(tickers).replace('[','').replace(']','')
                        positions_size_str = ",".join(tickers_size).replace('[','').replace(']','')
                        return update_portfolio(portfolio_id, cash_balance - required_amount, positions_str, positions_size_str, user_data)
                    else:
                        index = tickers.index(ticker.lower())
                        tickers_size[index] = str(int(tickers_size[index]) + quantity)
                        positions_size_str = ",".join(tickers_size).replace('[','').replace(']','')
                        return update_portfolio(portfolio_id, cash_balance - required_amount, data.get("positions", ""), positions_size_str, user_data)
                return "Pas assez de cash pour cet achat."
            elif trade_type == 'SELL':
                if ticker.lower() in data.get("positions", "").lower().split(","):
                    tickers = data.get("positions", "").lower().split(",")
                    tickers_size = data.get("positions_size", "").split(",")
                    index = tickers.index(ticker.lower())
                    if int(tickers_size[index]) >= quantity:
                        tickers_size[index] = str(int(tickers_size[index]) - quantity)
                        if int(tickers_size[index]) == 0:
                            tickers.pop(index)
                            tickers_size.pop(index)
                        positions_str = ",".join(tickers).replace('[','').replace(']','')
                        positions_size_str = ",".join(tickers_size).replace('[','').replace(']','')
                        return update_portfolio(portfolio_id, cash_balance + required_amount, positions_str, positions_size_str, user_data)
                    return "Pas assez de titres pour cette vente."
                return "Vous ne possédez pas ce titre."
        return False
    except requests.exceptions.RequestException:
        return f"Impossible de contacter l'API."
def update_portfolio(portfolio_id, new_balance, positions_str, positions_size_str, user_data):
    api_url = f"http://api:5001/portfolios/{portfolio_id}"  # ton endpoint
    token = user_data["access_token"]
    token_type = user_data.get("token_type", "bearer")
    headers = {
        "Authorization": f"{token_type.capitalize()} {token}",
        "Content-Type": "application/json"
    }
    payload = {
        "cash_balance": new_balance,
        "positions": positions_str,
        "positions_size": positions_size_str
    }
    try:
        response = requests.put(api_url, headers=headers, json=payload)

        if response.status_code == 200:
            return True
        return f"Impossible de contacter l'API.{response.text}{payload}"
    except requests.exceptions.RequestException:
        return f"Impossible de contacter l'API.{response.text}{payload}"
@callback(
    Output('trade-output', 'children'),
    Input('add-trade', 'n_clicks'),
    State('trade-type', 'value'),
    State('trade-ticker', 'value'),
    State('trade-quantite', 'value'),
    State('trade-prix', 'value'),
    State('trade-description', 'value'),
    State('user-data', 'data'),
    State('portfolio-data', 'data')
)
def add_trade(n_clicks, trade_type, ticker, quantite, prix, description, user_data,portfolio_data):
    if not (n_clicks > 0 and trade_type and ticker and quantite>0 and prix>0):
        return "Veuillez remplir tous les champs."
    
    balance_check = check_balance(trade_type, prix, quantite,ticker,user_data,portfolio_data)
    if balance_check is False:
        return "Solde insuffisant pour effectuer cet achat."
    if isinstance(balance_check, str):
        return balance_check
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
    "portfolio_id": portfolio_data,
    "description": description
    }
    try:
        response = requests.post(api_url, headers=headers,json=payload)

        if response.status_code == 200:
            return f"Trade ajouté : {trade_type} {quantite}x {ticker} à {prix}€ {description}"

        return f"Impossible de contacter l'API."
    except requests.exceptions.RequestException:
        return f"Impossible de contacter l'API."
    