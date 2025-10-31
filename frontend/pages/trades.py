from dash import html, dcc, Input, Output, State, callback

def create_trades():
    return html.Div([
        html.H2("Ajouter un trade", style={'textAlign': 'center'}),
        html.Div([
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
    State('trade-ticker', 'value'),
    State('trade-quantite', 'value'),
    State('trade-prix', 'value')
)
def add_trade(n_clicks, ticker, quantite, prix):
    if n_clicks > 0 and ticker and quantite and prix:
        return f"Trade ajouté : {quantite}x {ticker} à {prix}€"
    return ""
