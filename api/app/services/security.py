from datetime import datetime, timedelta
from jose import JWTError, jwt
import bcrypt  # Utilisation du package bcrypt natif

SECRET_KEY = "AZERTYUIOPQSDFGHJKLMWXCVBNAZERTYUIOP"  # 🔒 à stocker dans une variable d’environnement
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60


def hash_password(password: str) -> str:
    """
    Hash un mot de passe en utilisant bcrypt.
    Retourne le hash encodé en str pour stockage en DB.
    """
    password_bytes = password.encode('utf-8')
    salt = bcrypt.gensalt()  # rounds par défaut = 12
    hashed = bcrypt.hashpw(password_bytes, salt)
    return hashed.decode('utf-8')


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Vérifie un mot de passe en comparant le mot de passe en clair et le hash stocké.
    """
    password_bytes = plain_password.encode('utf-8')
    hashed_bytes = hashed_password.encode('utf-8')
    return bcrypt.checkpw(password_bytes, hashed_bytes)


def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
    """
    Crée un JWT avec expiration.
    """
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
