from dash import html

def create_home():
    return html.Div([
        html.H2("Bienvenue sur ton tableau de bord financier", style={'textAlign': 'center'}),
        html.P(
            "Utilise le menu ci-dessus pour consulter ton portefeuille, tes trades ou suivre les marchés boursiers.",
            style={'textAlign': 'center', 'maxWidth': '600px', 'margin': 'auto'}
        )
    ])
