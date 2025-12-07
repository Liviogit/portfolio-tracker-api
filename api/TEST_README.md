# Tests Unitaires API

Les tests unitaires pour toutes les routes de l'API sont organisés dans le dossier `app/tests/`.

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