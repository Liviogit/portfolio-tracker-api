# Tests Unitaires API

Ce fichier contient tous les tests unitaires pour les routes de l'API.

## Installation des dépendances

```bash
pip install -r requirements.txt
```

## Exécution des tests dans Docker

### 1. Reconstruire le conteneur API (première fois ou après modification)
```bash
docker-compose build api
```

### 2. Démarrer les conteneurs
```bash
docker-compose up -d
```

### 3. Attendre que la base de données soit prête (10 secondes)
```bash
# Linux/Mac
sleep 10

# Windows PowerShell
Start-Sleep -Seconds 10
```

### 4. Exécuter tous les tests dans le conteneur API
```bash
docker-compose exec api pytest tests/ -v
```

### Alternative rapide : Tout en une seule commande
```bash
# Linux/Mac
docker-compose up -d && sleep 10 && docker-compose exec api pytest tests/ -v

# Windows PowerShell
docker-compose up -d; Start-Sleep -Seconds 10; docker-compose exec api pytest tests/ -v
```

### Utiliser le script automatique
```bash
# Linux/Mac
./run_tests.sh

# Windows PowerShell
.\run_tests.ps1
```

## Exécution des tests en local (hors Docker)

### Exécuter tous les tests
```bash
pytest app/tests/ -v
```

### Exécuter les tests d'une classe spécifique (Docker)
```bash
docker-compose exec api pytest tests/test_routes.py::TestAuthRouter -v
docker-compose exec api pytest tests/test_routes.py::TestUserRouter -v
docker-compose exec api pytest tests/test_routes.py::TestPortfolioRouter -v
docker-compose exec api pytest tests/test_routes.py::TestTradeRouter -v
docker-compose exec api pytest tests/test_routes.py::TestTickerRouter -v
docker-compose exec api pytest tests/test_routes.py::TestIntegration -v
```

### Exécuter un test spécifique (Docker)
```bash
docker-compose exec api pytest tests/test_routes.py::TestAuthRouter::test_register_success -v
```

### Exécuter avec couverture de code (Docker)
```bash
docker-compose exec api pip install pytest-cov
docker-compose exec api pytest tests/ --cov=. --cov-report=term-missing
```

### Exécuter les tests d'intégration uniquement (Docker)
```bash
docker-compose exec api pytest tests/test_routes.py::TestIntegration -v
```

### Voir les logs en temps réel pendant les tests
```bash
docker-compose exec api pytest tests/ -v -s
```

## Structure des tests

### TestAuthRouter
- `test_register_success`: Test d'inscription réussie
- `test_register_duplicate_username`: Test d'inscription avec username existant
- `test_login_success`: Test de connexion réussie
- `test_login_wrong_password`: Test avec mauvais mot de passe
- `test_login_wrong_username`: Test avec username inexistant
- `test_get_current_user`: Test de récupération de l'utilisateur connecté
- `test_get_current_user_without_token`: Test sans token
- `test_get_current_user_invalid_token`: Test avec token invalide

### TestUserRouter
- `test_create_user`: Test de création d'utilisateur
- `test_get_user_authenticated`: Test de récupération avec authentification
- `test_get_user_not_authenticated`: Test sans authentification

### TestPortfolioRouter
- `test_create_portfolio`: Test de création de portfolio
- `test_create_portfolio_without_auth`: Test sans authentification
- `test_get_all_portfolios`: Test de récupération de tous les portfolios
- `test_get_portfolio_by_id`: Test de récupération par ID
- `test_update_portfolio`: Test de mise à jour
- `test_update_nonexistent_portfolio`: Test de mise à jour d'un portfolio inexistant
- `test_delete_portfolio`: Test de suppression
- `test_delete_nonexistent_portfolio`: Test de suppression d'un portfolio inexistant

### TestTradeRouter
- `test_create_trade`: Test de création de trade
- `test_create_trade_without_auth`: Test sans authentification
- `test_get_all_trades`: Test de récupération de tous les trades
- `test_get_trades_by_portfolio`: Test de récupération par portfolio
- `test_get_trades_without_auth`: Test sans authentification

### TestTickerRouter
- `test_get_ticker_data_default_params`: Test avec paramètres par défaut
- `test_get_ticker_data_custom_params`: Test avec paramètres personnalisés
- `test_get_ticker_data_with_start_date`: Test avec date de début
- `test_get_ticker_invalid_ticker`: Test avec ticker invalide

### TestIntegration
- `test_full_user_workflow`: Test du workflow complet (register → login → portfolio → trade)
- `test_unauthorized_access_to_other_user_portfolio`: Test de sécurité inter-utilisateurs

## Configuration

Les tests utilisent la base de données PostgreSQL du conteneur Docker. Chaque test nettoie automatiquement les données avant et après son exécution pour garantir l'isolation.

### Variables d'environnement
Les tests utilisent les mêmes variables d'environnement que l'application :
- `POSTGRES_USER`: admin
- `POSTGRES_PASSWORD`: admin123
- `POSTGRES_DB`: master_db
- `POSTGRES_HOST`: db

## Résolution des problèmes

### Les tests échouent avec "connection refused"
Assurez-vous que les conteneurs sont démarrés :
```bash
docker-compose up -d
docker-compose ps
```

### Nettoyer complètement la base de données
```bash
docker-compose down -v
docker-compose up -d
```

### Voir les logs du conteneur API
```bash
docker-compose logs -f api
```

## Fixtures disponibles

- `test_db`: Base de données de test
- `client`: Client de test FastAPI
- `test_user`: Utilisateur de test
- `test_user_token`: Token JWT pour l'utilisateur de test
- `test_portfolio`: Portfolio de test
- `test_trade`: Trade de test

## Notes

- Les tests sont isolés et peuvent être exécutés dans n'importe quel ordre
- La base de données est nettoyée entre chaque test (DELETE sur toutes les tables)
- Les tests d'authentification utilisent des tokens JWT réels
- Les tests de ticker peuvent échouer si l'API yfinance est indisponible
- Les tests utilisent la vraie base PostgreSQL du conteneur Docker pour une meilleure fidélité

## Exemple de workflow complet

```bash
# 1. Démarrer l'environnement
docker-compose up -d

# 2. Attendre que la base de données soit prête
sleep 5

# 3. Exécuter les tests
docker-compose exec api pytest test_routes.py -v

# 4. Voir les résultats détaillés d'un test spécifique
docker-compose exec api pytest test_routes.py::TestIntegration::test_full_user_workflow -v -s

# 5. Nettoyer (optionnel)
docker-compose down
```
