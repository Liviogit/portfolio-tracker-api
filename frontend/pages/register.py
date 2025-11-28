import requests
from dash import html, dcc, Input, Output, State, callback

REGISTER_URL = "http://api:5001/auth/register"

def create_register_page():
    return html.Div([
        html.H2("Inscription", style={'textAlign': 'center'}),

        dcc.Input(
            id='reg-firstname-input',
            type='text',
            placeholder='Prénom',
            style={'display': 'block', 'margin': '10px auto', 'width': '50%'}
        ),

        dcc.Input(
            id='reg-lastname-input',
            type='text',
            placeholder='Nom',
            style={'display': 'block', 'margin': '10px auto', 'width': '50%'}
        ),

        dcc.Input(
            id='reg-username-input',
            type='text',
            placeholder='Nom d\'utilisateur',
            style={'display': 'block', 'margin': '10px auto', 'width': '50%'}
        ),

        dcc.Input(
            id='reg-password-input',
            type='password',
            placeholder='Mot de passe',
            style={'display': 'block', 'margin': '10px auto', 'width': '50%'}
        ),

        dcc.Input(
            id='reg-password2-input',
            type='password',
            placeholder='Confirmer le mot de passe',
            style={'display': 'block', 'margin': '10px auto', 'width': '50%'}
        ),

        html.Button(
            "S'inscrire",
            id='register-button',
            n_clicks=0,
            style={'display': 'block', 'margin': '10px auto'}
        ),

        html.Div(
            id='register-output',
            style={'textAlign': 'center', 'color': 'red', 'marginTop': '10px'}
        ),

        dcc.Link(
            "Déjà un compte ? Connectez-vous ici.",
            href='/login',
            style={'textAlign': 'center', 'marginTop': '20px', 'display': 'block'}
        )
    ])

@callback(
    Output('register-output', 'children'),
    Input('register-button', 'n_clicks'),
    State('reg-firstname-input', 'value'),
    State('reg-lastname-input', 'value'),
    State('reg-username-input', 'value'),
    State('reg-password-input', 'value'),
    State('reg-password2-input', 'value'),
    prevent_initial_call=True
)
def handle_register(n_clicks, firstname, lastname, username, password, password2):

    if not n_clicks:
        return ""

    # Vérification basique
    if not firstname or not lastname or not username or not password or not password2:
        return "Veuillez remplir tous les champs."

    if password != password2:
        return "Les mots de passe ne correspondent pas."

    try:
        response = requests.post(
            REGISTER_URL,
            json={
                "first_name": firstname,
                "last_name": lastname,
                "username": username,
                "password": password
            },
            headers={"Content-Type": "application/json"}
        )

        # Succès (souvent 201)
        if response.status_code in [200, 201]:
            return "Compte créé avec succès ! Vous pouvez maintenant vous connecter."
        else:
            return f"Erreur serveur ({response.status_code})."

    except requests.exceptions.RequestException:
        return "Impossible de contacter le serveur."
