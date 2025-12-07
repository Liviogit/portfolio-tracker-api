"""
Configuration pytest pour les tests API
"""
import pytest
import os

# Configuration des variables d'environnement pour les tests
os.environ.setdefault("POSTGRES_USER", "admin")
os.environ.setdefault("POSTGRES_PASSWORD", "admin123")
os.environ.setdefault("POSTGRES_DB", "master_db")
os.environ.setdefault("POSTGRES_HOST", "db")


def pytest_configure(config):
    """Configuration globale de pytest"""
    config.addinivalue_line("markers", "integration: marque les tests d'intégration")
    config.addinivalue_line("markers", "unit: marque les tests unitaires")
    config.addinivalue_line("markers", "slow: marque les tests lents")


@pytest.fixture(scope="session", autouse=True)
def setup_test_environment():
    """Setup exécuté une fois avant tous les tests"""
    print("\n🔧 Configuration de l'environnement de test...")
    yield
    print("\n✨ Nettoyage de l'environnement de test...")
