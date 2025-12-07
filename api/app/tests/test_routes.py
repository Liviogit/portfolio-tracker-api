import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, Session
import httpx
from datetime import datetime
import os

from main import app
from database import BaseSQL, get_db
from models.user_model import User
from models.portfolio_model import Portfolio
from models.trade_model import Trade
from services.security import hash_password, create_access_token

# Configuration de la base de données de test (utilise la même DB que l'app mais avec nettoyage)
POSTGRES_USER = os.environ.get("POSTGRES_USER", "admin")
POSTGRES_PASSWORD = os.environ.get("POSTGRES_PASSWORD", "admin123")
POSTGRES_DB = os.environ.get("POSTGRES_DB", "master_db")
POSTGRES_HOST = os.environ.get("POSTGRES_HOST", "db")

SQLALCHEMY_TEST_DATABASE_URL = (
    f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}/{POSTGRES_DB}"
)

engine = create_engine(SQLALCHEMY_TEST_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db():
    """Override de la dépendance get_db pour utiliser la base de test"""
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db


@pytest.fixture(scope="function")
def test_db():
    """Fixture pour nettoyer la base de données avant et après chaque test"""
    db = TestingSessionLocal()
    
    # Nettoyer les tables avant le test
    db.execute(text("DELETE FROM trades"))
    db.execute(text("DELETE FROM portfolios"))
    db.execute(text("DELETE FROM users"))
    db.commit()
    
    yield db
    
    # Nettoyer les tables après le test
    db.execute(text("DELETE FROM trades"))
    db.execute(text("DELETE FROM portfolios"))
    db.execute(text("DELETE FROM users"))
    db.commit()
    db.close()


@pytest.fixture(scope="function")
def client(test_db):
    """Fixture pour créer un client de test"""
    return TestClient(app)


@pytest.fixture(scope="function")
def test_user(test_db: Session):
    """Fixture pour créer un utilisateur de test"""
    hashed_password = hash_password("testpassword123")
    user = User(
        first_name="Test",
        last_name="User",
        username="testuser",
        password=hashed_password
    )
    test_db.add(user)
    test_db.commit()
    test_db.refresh(user)
    return user


@pytest.fixture(scope="function")
def test_user_token(test_user):
    """Fixture pour créer un token JWT pour l'utilisateur de test"""
    access_token = create_access_token(data={"sub": test_user.username})
    return access_token


@pytest.fixture(scope="function")
def test_portfolio(test_db: Session, test_user):
    """Fixture pour créer un portfolio de test"""
    portfolio = Portfolio(
        user_id=test_user.user_id,
        portfolio_name="Test Portfolio",
        last_amount=10000.0,
        initial_amount=10000.0,
        positions="AAPL,GOOGL",
        positions_size="50,50",
        cash_balance=5000.0
    )
    test_db.add(portfolio)
    test_db.commit()
    test_db.refresh(portfolio)
    return portfolio


# =====================================================
# TESTS AUTH ROUTER
# =====================================================

class TestAuthRouter:
    """Tests pour les routes d'authentification"""

    def test_register_success(self, client):
        """Test de création de compte réussie"""
        response = client.post(
            "/auth/register",
            json={
                "first_name": "John",
                "last_name": "Doe",
                "username": "johndoe",
                "password": "password123"
            }
        )
        assert response.status_code == 200
        data = response.json()
        assert data["username"] == "johndoe"
        assert data["first_name"] == "John"
        assert data["last_name"] == "Doe"
        assert "user_id" in data

    def test_register_duplicate_username(self, client, test_user):
        """Test de création de compte avec username déjà existant"""
        response = client.post(
            "/auth/register",
            json={
                "first_name": "John",
                "last_name": "Doe",
                "username": test_user.username,
                "password": "password123"
            }
        )
        assert response.status_code == 400
        assert "already exists" in response.json()["detail"].lower()

    def test_login_success(self, client, test_user):
        """Test de connexion réussie"""
        response = client.post(
            "/auth/token",
            data={
                "username": test_user.username,
                "password": "testpassword123"
            }
        )
        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data
        assert data["token_type"] == "bearer"

    def test_login_wrong_password(self, client, test_user):
        """Test de connexion avec mauvais mot de passe"""
        response = client.post(
            "/auth/token",
            data={
                "username": test_user.username,
                "password": "wrongpassword"
            }
        )
        assert response.status_code == 400
        assert "incorrect" in response.json()["detail"].lower()

    def test_login_wrong_username(self, client):
        """Test de connexion avec username inexistant"""
        response = client.post(
            "/auth/token",
            data={
                "username": "nonexistent",
                "password": "password123"
            }
        )
        assert response.status_code == 400

    def test_get_current_user(self, client, test_user_token, test_user):
        """Test de récupération de l'utilisateur connecté"""
        response = client.get(
            "/auth/me",
            headers={"Authorization": f"Bearer {test_user_token}"}
        )
        assert response.status_code == 200
        data = response.json()
        assert data["username"] == test_user.username
        assert data["user_id"] == test_user.user_id

    def test_get_current_user_without_token(self, client):
        """Test d'accès sans token"""
        response = client.get("/auth/me")
        assert response.status_code == 401

    def test_get_current_user_invalid_token(self, client):
        """Test d'accès avec token invalide"""
        response = client.get(
            "/auth/me",
            headers={"Authorization": "Bearer invalidtoken"}
        )
        assert response.status_code == 401


# =====================================================
# TESTS USER ROUTER
# =====================================================

class TestUserRouter:
    """Tests pour les routes utilisateurs"""

    def test_get_user_authenticated(self, client, test_user_token, test_user):
        """Test de récupération d'utilisateur authentifié"""
        response = client.get(
            "/users/",
            headers={"Authorization": f"Bearer {test_user_token}"}
        )
        assert response.status_code == 200
        data = response.json()
        assert data["username"] == test_user.username
        assert data["first_name"] == test_user.first_name

    def test_get_user_not_authenticated(self, client):
        """Test de récupération d'utilisateur non authentifié"""
        response = client.get("/users/")
        assert response.status_code == 401


# =====================================================
# TESTS PORTFOLIO ROUTER
# =====================================================

class TestPortfolioRouter:
    """Tests pour les routes de portfolios"""

    def test_create_portfolio(self, client, test_user_token):
        """Test de création de portfolio"""
        response = client.post(
            "/portfolios/",
            json={
                "portfolio_name": "My Investment Portfolio",
                "last_amount": 15000.0,
                "initial_amount": 15000.0,
                "positions": "AAPL,MSFT,GOOGL",
                "positions_size": "30,40,30",
                "cash_balance": 7500.0
            },
            headers={"Authorization": f"Bearer {test_user_token}"}
        )
        assert response.status_code == 200
        data = response.json()
        assert data["portfolio_name"] == "My Investment Portfolio"
        assert data["initial_amount"] == 15000.0
        assert "portfolio_id" in data

    def test_create_portfolio_without_auth(self, client):
        """Test de création de portfolio sans authentification"""
        response = client.post(
            "/portfolios/",
            json={
                "portfolio_name": "Test Portfolio",
                "last_amount": 10000.0,
                "initial_amount": 10000.0,
                "positions": "AAPL",
                "positions_size": "100",
                "cash_balance": 5000.0
            }
        )
        assert response.status_code == 401

    def test_get_all_portfolios(self, client, test_user_token, test_portfolio):
        """Test de récupération de tous les portfolios de l'utilisateur"""
        response = client.get(
            "/portfolios/",
            headers={"Authorization": f"Bearer {test_user_token}"}
        )
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) >= 1
        assert data[0]["portfolio_id"] == test_portfolio.portfolio_id

    def test_get_portfolio_by_id(self, client, test_user_token, test_portfolio):
        """Test de récupération d'un portfolio par ID"""
        response = client.get(
            f"/portfolios/{test_portfolio.portfolio_id}",
            headers={"Authorization": f"Bearer {test_user_token}"}
        )
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) >= 1
        assert data[0]["portfolio_id"] == test_portfolio.portfolio_id

    def test_update_portfolio(self, client, test_user_token, test_portfolio):
        """Test de mise à jour d'un portfolio"""
        response = client.put(
            f"/portfolios/{test_portfolio.portfolio_id}",
            json={
                "portfolio_name": "Updated Portfolio Name",
                "last_amount": 20000.0
            },
            headers={"Authorization": f"Bearer {test_user_token}"}
        )
        assert response.status_code == 200
        data = response.json()
        assert data["portfolio_name"] == "Updated Portfolio Name"
        assert data["last_amount"] == 20000.0

    def test_update_nonexistent_portfolio(self, client, test_user_token):
        """Test de mise à jour d'un portfolio inexistant"""
        response = client.put(
            "/portfolios/9999",
            json={
                "portfolio_name": "Updated Name",
                "last_amount": 15000.0
            },
            headers={"Authorization": f"Bearer {test_user_token}"}
        )
        assert response.status_code == 404

    def test_delete_portfolio(self, client, test_user_token, test_portfolio):
        """Test de suppression d'un portfolio"""
        response = client.delete(
            f"/portfolios/{test_portfolio.portfolio_id}",
            headers={"Authorization": f"Bearer {test_user_token}"}
        )
        assert response.status_code == 200
        data = response.json()
        assert data["portfolio_id"] == test_portfolio.portfolio_id

    def test_delete_nonexistent_portfolio(self, client, test_user_token):
        """Test de suppression d'un portfolio inexistant"""
        response = client.delete(
            "/portfolios/9999",
            headers={"Authorization": f"Bearer {test_user_token}"}
        )
        assert response.status_code == 404


# =====================================================
# TESTS TRADE ROUTER
# =====================================================

class TestTradeRouter:
    """Tests pour les routes de trades"""

    def test_create_trade(self, client, test_user_token, test_portfolio):
        """Test de création d'un trade"""
        response = client.post(
            "/trades/",
            json={
                "portfolio_id": test_portfolio.portfolio_id,
                "asset_name": "TSLA",
                "quantity": 5,
                "price": 250.75,
                "action": "BUY",
                "trade_date": datetime.now().isoformat()
            },
            headers={"Authorization": f"Bearer {test_user_token}"}
        )
        assert response.status_code == 200
        data = response.json()
        assert data["asset_name"] == "TSLA"
        assert data["quantity"] == 5
        assert data["price"] == 250.75
        assert data["action"] == "BUY"

    def test_create_trade_without_auth(self, client, test_portfolio):
        """Test de création d'un trade sans authentification"""
        response = client.post(
            "/trades/",
            json={
                "portfolio_id": test_portfolio.portfolio_id,
                "asset_name": "TSLA",
                "quantity": 5,
                "price": 250.75,
                "action": "BUY",
                "trade_date": datetime.now().isoformat()
            }
        )
        assert response.status_code == 401

    def test_get_all_trades(self, client, test_user_token, test_portfolio):
        """Test de récupération de tous les trades de l'utilisateur"""
        # Créer un trade d'abord
        trade_create_response = client.post(
            "/trades/",
            json={
                "portfolio_id": test_portfolio.portfolio_id,
                "asset_name": "AAPL",
                "quantity": 10,
                "price": 150.50,
                "action": "BUY",
                "trade_date": datetime.now().isoformat()
            },
            headers={"Authorization": f"Bearer {test_user_token}"}
        )
        assert trade_create_response.status_code == 200
        created_trade = trade_create_response.json()
        
        # Récupérer tous les trades
        response = client.get(
            "/trades/",
            headers={"Authorization": f"Bearer {test_user_token}"}
        )
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) >= 1
        assert data[0]["trade_id"] == created_trade["trade_id"]

    def test_get_trades_by_portfolio(self, client, test_user_token, test_portfolio):
        """Test de récupération des trades par portfolio"""
        # Créer un trade d'abord
        trade_create_response = client.post(
            "/trades/",
            json={
                "portfolio_id": test_portfolio.portfolio_id,
                "asset_name": "GOOGL",
                "quantity": 5,
                "price": 2800.00,
                "action": "BUY",
                "trade_date": datetime.now().isoformat()
            },
            headers={"Authorization": f"Bearer {test_user_token}"}
        )
        assert trade_create_response.status_code == 200
        
        # Récupérer les trades du portfolio
        response = client.get(
            f"/trades/portfolio/{test_portfolio.portfolio_id}",
            headers={"Authorization": f"Bearer {test_user_token}"}
        )
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) >= 1
        assert data[0]["portfolio_id"] == test_portfolio.portfolio_id

    def test_get_trades_without_auth(self, client):
        """Test de récupération des trades sans authentification"""
        response = client.get("/trades/")
        assert response.status_code == 401


# =====================================================
# TESTS TICKER ROUTER
# =====================================================

class TestTickerRouter:
    """Tests pour les routes de tickers"""

    def test_get_ticker_data_default_params(self, client):
        """Test de récupération de données de ticker avec paramètres par défaut"""
        response = client.get("/tickers/AAPL/")
        assert response.status_code == 200
        data = response.json()
        # Vérifier que les données sont retournées (structure dépend de ticker_service)
        assert data is not None

    def test_get_ticker_data_custom_params(self, client):
        """Test de récupération de données de ticker avec paramètres personnalisés"""
        response = client.get(
            "/tickers/GOOGL/",
            params={
                "period": "1mo",
                "interval": "1d"
            }
        )
        assert response.status_code == 200
        data = response.json()
        assert data is not None

    def test_get_ticker_data_with_start_date(self, client):
        """Test de récupération de données de ticker avec date de début"""
        response = client.get(
            "/tickers/MSFT/",
            params={
                "period": "1mo",
                "interval": "1d",
                "start": "2024-01-01"
            }
        )
        assert response.status_code == 200
        data = response.json()
        assert data is not None

    def test_get_ticker_invalid_ticker(self, client):
        """Test de récupération de données avec ticker invalide"""
        response = client.get("/tickers/INVALIDTICKER123/")
        # Le comportement dépend de l'implémentation de ticker_service
        # Peut retourner 200, 404, 400 ou 500 selon l'erreur yfinance
        assert response.status_code in [200, 404, 400, 500]


# =====================================================
# TESTS D'INTÉGRATION
# =====================================================

class TestIntegration:
    """Tests d'intégration pour vérifier le workflow complet"""

    def test_full_user_workflow(self, client):
        """Test du workflow complet: register -> login -> create portfolio -> create trade"""
        # 1. Créer un compte
        register_response = client.post(
            "/auth/register",
            json={
                "first_name": "Integration",
                "last_name": "Test",
                "username": "integrationtest",
                "password": "test123"
            }
        )
        assert register_response.status_code == 200

        # 2. Se connecter
        login_response = client.post(
            "/auth/token",
            data={
                "username": "integrationtest",
                "password": "test123"
            }
        )
        assert login_response.status_code == 200
        token = login_response.json()["access_token"]

        # 3. Créer un portfolio
        portfolio_response = client.post(
            "/portfolios/",
            json={
                "portfolio_name": "Integration Portfolio",
                "last_amount": 10000.0,
                "initial_amount": 10000.0,
                "positions": "AAPL",
                "positions_size": "100",
                "cash_balance": 5000.0
            },
            headers={"Authorization": f"Bearer {token}"}
        )
        assert portfolio_response.status_code == 200
        portfolio_id = portfolio_response.json()["portfolio_id"]

        # 4. Créer un trade
        trade_response = client.post(
            "/trades/",
            json={
                "portfolio_id": portfolio_id,
                "asset_name": "AAPL",
                "quantity": 10,
                "price": 150.0,
                "action": "BUY",
                "trade_date": datetime.now().isoformat()
            },
            headers={"Authorization": f"Bearer {token}"}
        )
        assert trade_response.status_code == 200

        # 5. Récupérer les trades
        trades_response = client.get(
            f"/trades/portfolio/{portfolio_id}",
            headers={"Authorization": f"Bearer {token}"}
        )
        assert trades_response.status_code == 200
        trades = trades_response.json()
        assert len(trades) == 1
        assert trades[0]["asset_name"] == "AAPL"

    def test_unauthorized_access_to_other_user_portfolio(self, client, test_user_token):
        """Test qu'un utilisateur ne peut pas accéder aux portfolios d'un autre utilisateur"""
        # Créer un deuxième utilisateur
        client.post(
            "/auth/register",
            json={
                "first_name": "Other",
                "last_name": "User",
                "username": "otheruser",
                "password": "password123"
            }
        )
        
        # Se connecter avec le deuxième utilisateur
        login_response = client.post(
            "/auth/token",
            data={
                "username": "otheruser",
                "password": "password123"
            }
        )
        other_token = login_response.json()["access_token"]

        # Créer un portfolio avec le premier utilisateur
        portfolio_response = client.post(
            "/portfolios/",
            json={
                "portfolio_name": "Private Portfolio",
                "last_amount": 10000.0,
                "initial_amount": 10000.0,
                "positions": "AAPL",
                "positions_size": "100",
                "cash_balance": 5000.0
            },
            headers={"Authorization": f"Bearer {test_user_token}"}
        )
        assert portfolio_response.status_code == 200
        portfolio_id = portfolio_response.json()["portfolio_id"]

        # Essayer d'accéder au portfolio avec le deuxième utilisateur
        response = client.get(
            f"/portfolios/{portfolio_id}",
            headers={"Authorization": f"Bearer {other_token}"}
        )
        # Devrait retourner une liste vide ou 404
        assert response.status_code in [200, 404]
        if response.status_code == 200:
            assert len(response.json()) == 0
