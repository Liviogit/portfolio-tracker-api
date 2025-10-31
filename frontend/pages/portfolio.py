from dash import html, dcc

def create_portfolio():
    mock_data = [
        {"Ticker": "AAPL", "Quantité": 5, "Prix (€)": 175},
        {"Ticker": "TSLA", "Quantité": 2, "Prix (€)": 240},
        {"Ticker": "MSFT", "Quantité": 3, "Prix (€)": 320},
    ]

    table = html.Table([
        html.Thead(html.Tr([html.Th(k) for k in mock_data[0].keys()])),
        html.Tbody([
            html.Tr([html.Td(v) for v in row.values()]) for row in mock_data
        ])
    ], style={
        'margin': 'auto',
        'borderCollapse': 'collapse',
        'border': '1px solid #ccc'
    })

    return html.Div([
        html.H2("Composition du portefeuille", style={'textAlign': 'center'}),
        table
    ])
