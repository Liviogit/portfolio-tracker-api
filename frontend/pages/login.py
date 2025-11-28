import requests
from dash import html, dcc, Input, Output, State, callback

LOGIN_URL="http://api:5001/auth/token"  # URL de l’API d’authentification
def create_login_page():
    return html.Div([
        html.H2("Connexion", style={'textAlign': 'center'}),
        dcc.Input(
            id='username-input',
            type='text',
            placeholder='Nom d\'utilisateur',
            style={'display': 'block', 'margin': '10px auto', 'width': '50%'}
        ),
        dcc.Input(
            id='password-input',
            type='password',
            placeholder='Mot de passe',
            style={'display': 'block', 'margin': '10px auto', 'width': '50%'}
        ),
        html.Button(
            'Se connecter',
            id='login-button',
            n_clicks=0,
            style={'display': 'block', 'margin': '10px auto'}
        ),
        html.Div(id='login-output', style={'textAlign': 'center', 'color': 'red', 'marginTop': '10px'}
        ),
        dcc.Link("Vous n'avez pas de compte ? S'inscire ici.", href='/register', style={'textAlign': 'center', 'marginTop': '20px'})

    ])
@callback(
    Output('login-output', 'children'),
    Output('user-data', 'data',allow_duplicate=True),   # ici on stocke la réponse si OK
    Input('login-button', 'n_clicks'),
    State('username-input', 'value'),
    State('password-input', 'value'),
    prevent_initial_call=True
)
def handle_login(n_clicks, username, password):
    if not n_clicks:
        return "", None

    # Vérification champs vides
    if not username or not password:
        return "Veuillez remplir les deux champs.", None

    try:
        # Requête API
        response = requests.post(
                LOGIN_URL,
                data={
                    "grant_type": "password",
                    "username": username,
                    "password": password,
                    "scope": "",
                    "client_id": "",
                    "client_secret": ""
                },
                headers={"Content-Type": "application/x-www-form-urlencoded"}
                )

        # Cas succès
        if response.status_code == 200:
            data = response.json()  # token, info user, etc.
            return "Connexion réussie !", data
        
        # Cas erreur côté API
        elif response.status_code in [400, 401, 403]:
            return "Identifiants incorrects.", None
        
        else:
            return f"Erreur serveur ({response.status_code}).", None

    except requests.exceptions.RequestException:
        return "Impossible de contacter le serveur.", None