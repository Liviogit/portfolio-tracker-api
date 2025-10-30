from fastapi import FastAPI
from contextlib import asynccontextmanager

from routers.user_router import user_router
from routers.portfolio_router import portfolio_router
from routers.trade_router import trade_router
from database import BaseSQL, engine

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Crée toutes les tables si elles n'existent pas
    BaseSQL.metadata.create_all(bind=engine)
    yield

app = FastAPI(
    title="Full Stack API",
    description="API pour gérer users, portfolios et trades",
    version="0.0.1",
    lifespan=lifespan,
)

# Inclusion des routers
app.include_router(user_router)
app.include_router(portfolio_router)
app.include_router(trade_router)
