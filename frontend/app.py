import dash
from dash import dcc, html, Input, Output, callback, State
from pages.home import create_home
from pages.portfolio import create_portfolio
from pages.trades import create_trades
from pages.bourse import create_bourse
from pages.login import create_login_page
from pages.register import create_register_page
# Initialisation de l’application
app = dash.Dash(__name__, suppress_callback_exceptions=True)

# --- Layout principal ---
app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    dcc.Store(id='user-data'),  # Stockage des données utilisateur (token, etc.),
    dcc.Store(id='portfolio-data'),  # Stockage des données du portefeuille

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
        ),
    ], style={
        'display': 'flex',
        'justifyContent': 'center',
        'padding': '10px',
        'backgroundColor': '#333'
    }),
    html.Div(id='login-logout-button-container', style={'position': 'absolute', 'right': '20px', 'top': '15px'}),
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
    elif pathname == '/login':
        return create_login_page()
    elif pathname == '/register':
        return create_register_page()
    else:
        return html.Div("404 - Page introuvable", style={'textAlign': 'center', 'color': '#555'})

@app.callback(
    Output('login-logout-button-container', 'children'),
    Input('user-data', 'data')
)
def update_login_button(user_data):
    if user_data:  # Si utilisateur connecté
        return html.Button("Déconnexion", id='logout-button', 
                           style={'padding': '10px 20px', 'backgroundColor': '#dc3545', 'color': '#fff', 'border': 'none', 'borderRadius': '5px', 'cursor': 'pointer'})
    else:  # Sinon
        return dcc.Link(html.Button("Se connecter", 
                                    style={'padding': '10px 20px', 'backgroundColor': '#007BFF', 'color': '#fff', 'border': 'none', 'borderRadius': '5px', 'cursor': 'pointer'}), 
                        href='/login')


# Callback pour vider le dcc.Store au clic sur déconnexion
@app.callback(
    Output('user-data', 'data',allow_duplicate=True),
    Input('logout-button', 'n_clicks'),
    State('user-data', 'data'),
    prevent_initial_call=True
)
def logout(n_clicks, user_data):
    if n_clicks and user_data:
        return None  # vide le store
    return dash.no_update
# --- Lancement ---
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8050)
