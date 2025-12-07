# Portfolio Tracker

Une application full-stack de gestion et suivi de portefeuilles d'investissement permettant de créer des portefeuilles, d'ajouter des trades avec descriptions détaillées, et d'analyser les performances de vos actions et portefeuilles en temps réel.

## 📋 Description du Projet

Portfolio Tracker est une solution complète pour gérer vos investissements boursiers :

- **Gestion de portefeuilles** : Créez et organisez plusieurs portefeuilles d'investissement
- **Suivi des trades** : Enregistrez vos transactions (achats/ventes) avec descriptions personnalisées
- **Analyse de performance** : Visualisez les performances de vos actions et portefeuilles en temps réel
- **Données financières** : Intégration avec Yahoo Finance pour des données de marché à jour
- **Sécurité** : Authentification utilisateur et routes sécurisées

## 🏗️ Architecture

### Base de Données (PostgreSQL)

La base de données utilise PostgreSQL avec la structure suivante :

```
┌─────────────────┐
│     USERS       │
│─────────────────│
│ id (PK)         │
│ username        │
│ email           │
│ password_hash   │
│ created_at      │
└─────────────────┘
         │
         │ 1:N
         ▼
┌─────────────────┐
│   PORTFOLIOS    │
│─────────────────│
│ id (PK)         │
│ user_id (FK)    │
│ name            │
│ description     │
│ created_at      │
└─────────────────┘
         │
         │ 1:N
         ▼
┌─────────────────┐
│     TRADES      │
│─────────────────│
│ id (PK)         │
│ portfolio_id(FK)│
│ ticker          │
│ quantity        │
│ price           │
│ trade_type      │
│ description     │
│ trade_date      │
└─────────────────┘
```

**Relations :**
- Un utilisateur peut avoir plusieurs portefeuilles
- Un portefeuille appartient à un seul utilisateur
- Un portefeuille peut contenir plusieurs trades
- Chaque trade est lié à un portefeuille spécifique

### API (FastAPI)

L'API REST est construite avec **FastAPI** et offre les fonctionnalités suivantes :

#### Caractéristiques principales :

- **Sécurité** : Routes protégées par authentification JWT
- **Documentation automatique** : Swagger UI disponible sur `/docs`
- **Données financières** : Intégration avec **yfinance** pour récupérer :
  - Prix actuels des actions
  - Historique des cours
  - Informations sur les entreprises
  - Calcul automatique des performances

#### Routes disponibles :

| Endpoint | Méthode | Sécurisé | Description |
|----------|---------|----------|-------------|
| `/auth/register` | POST | Non | Inscription d'un nouvel utilisateur |
| `/auth/login` | POST | Non | Connexion et obtention du token JWT |
| `/users/me` | GET | Oui | Informations de l'utilisateur connecté |
| `/portfolios` | GET/POST | Oui | Liste et création de portefeuilles |
| `/portfolios/{id}` | GET/PUT/DELETE | Oui | Gestion d'un portefeuille spécifique |
| `/trades` | GET/POST | Oui | Liste et création de trades |
| `/trades/{id}` | GET/PUT/DELETE | Oui | Gestion d'un trade spécifique |
| `/ticker/{symbol}` | GET | Oui | Informations sur une action via yfinance |
| `/ticker/{symbol}/history` | GET | Oui | Historique des prix d'une action |

**Sécurité** : Les routes nécessitant une authentification vérifient le token JWT et s'assurent que l'utilisateur a accès uniquement à ses propres données.

### Frontend (Dash)

Interface utilisateur développée avec **Dash**, privilégiant la simplicité et l'ergonomie :

#### Pages :

1. **Home** : Tableau de bord avec vue d'ensemble des portefeuilles
2. **Login/Register** : Authentification utilisateur
3. **Portfolio** : Gestion détaillée des portefeuilles
4. **Trades** : Visualisation et ajout de transactions
5. **Bourse** : Recherche et analyse d'actions en temps réel

#### Caractéristiques :

- Interface intuitive et responsive
- Graphiques interactifs pour les performances
- Navigation fluide entre les pages
- Formulaires simples pour l'ajout de données
- Affichage en temps réel des cours boursiers

## 🚀 Lancement du Projet

### Prérequis

- Docker et Docker Compose installés
- Git (pour cloner le projet)

### Installation

1. **Cloner le repository**
```bash
git clone <repository-url>
```

2. **Lancer l'application avec Docker Compose**
```bash
docker-compose up --build -d
```

Cette commande va :
- Construire les images Docker pour l'API et le frontend
- Démarrer le conteneur PostgreSQL avec initialisation de la base de données
- Lancer l'API sur le port 8000
- Lancer le frontend sur le port 8501

3. **Accéder à l'application**

- **Frontend** : http://localhost:8050
- **API Documentation** : http://localhost:5001/docs
- **API** : http://localhost:5001

### Commandes utiles

```bash
# Arrêter les conteneurs
docker-compose down

# Voir les logs
docker-compose logs -f

# Redémarrer un service spécifique
docker-compose restart api
docker-compose restart frontend

# Reconstruire les images
docker-compose up -d --build
```

## 🧪 Tests

Pour exécuter les tests de l'API et consulter la documentation des tests, référez-vous au fichier :

📄 **[TEST_README.md](./api/TEST_README.md)**

Ce document contient :
- Instructions pour lancer les tests
- Description des tests unitaires et d'intégration
- Configuration de pytest
- Couverture des tests

## 📁 Structure du Projet

```
Full_stack/
├── api/                    # Backend FastAPI
│   ├── app/
│   │   ├── routers/       # Endpoints API
│   │   ├── services/      # Logique métier
│   │   ├── models/        # Modèles SQLAlchemy
│   │   ├── serializers/   # Schémas Pydantic
│   │   ├── tests/         # Tests unitaires
│   │   └── data/          # Données initiales
│   └── requirements.txt
├── frontend/              # Frontend Streamlit
│   ├── pages/            # Pages de l'application
│   ├── app.py            # Point d'entrée
│   └── requirements.txt
├── database/             # Configuration PostgreSQL
│   └── app/init/
│       ├── init.sql      # Script d'initialisation
│       └── data/         # Données de démarrage
└── docker-compose.yml    # Orchestration des services
```

## 🛠️ Technologies Utilisées

- **Backend** : FastAPI, SQLAlchemy, PostgreSQL, yfinance, JWT
- **Frontend** : Dash, Pandas, Plotly
- **DevOps** : Docker, Docker Compose
- **Tests** : Pytest

## 📝 Licence

Ce projet est sous licence MIT.

---

**Développé avec ❤️ pour simplifier la gestion de vos investissements**

L'IA a été utilisé pour optimisé des fonctions de l'API et pour développer le frontend