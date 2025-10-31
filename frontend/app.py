import dash
from dash import dcc, html, Input, Output, callback
from pages.home import create_home
from pages.portfolio import create_portfolio
from pages.trades import create_trades
from pages.bourse import create_bourse

# Initialisation de l’application
app = dash.Dash(__name__, suppress_callback_exceptions=True)

# --- Layout principal ---
app.layout = html.Div([
    dcc.Location(id='url', refresh=False),

    # HEADER
    html.Div([
        dcc.Link(
            html.H1("Suivi de Portefeuille", style={
                'textAlign': 'center',
                'color': '#ffffff',
                'fontWeight': 'bold',
                'font-family': 'Arial, sans-serif',
                'cursor': 'pointer',
                'textDecoration': 'none'
            }),
            href='/'
        )
    ], style={
        'display': 'flex',
        'justifyContent': 'center',
        'padding': '10px',
        'backgroundColor': '#333'
    }),

    # NAVIGATION
    html.Nav([
        dcc.Link('Accueil', href='/', style={'color': '#fff', 'textDecoration': 'none'}),
        dcc.Link('Portefeuille', href='/portfolio', style={'color': '#fff', 'textDecoration': 'none'}),
        dcc.Link('Trades', href='/trades', style={'color': '#fff', 'textDecoration': 'none'}),
        dcc.Link('Bourse', href='/bourse', style={'color': '#fff', 'textDecoration': 'none'}),
    ], style={
        'display': 'flex',
        'justifyContent': 'space-around',
        'padding': '10px',
        'backgroundColor': '#444',
        'font-family': 'Arial, sans-serif'
    }),

    html.Div(id='page-content', style={
        'backgroundColor': '#f4f4f4',
        'padding': '40px',
        'minHeight': '90vh'
    })
])

# --- ROUTING ---
@callback(Output('page-content', 'children'), Input('url', 'pathname'))
def display_page(pathname):
    if pathname == '/':
        return create_home()
    elif pathname == '/portfolio':
        return create_portfolio()
    elif pathname == '/trades':
        return create_trades()
    elif pathname == '/bourse':
        return create_bourse()
    else:
        return html.Div("404 - Page introuvable", style={'textAlign': 'center', 'color': '#555'})

# --- Lancement ---
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8050)
