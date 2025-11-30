from fastapi import APIRouter, Query
from services.ticker_service import get_tickers_data
ticker_router = APIRouter(prefix="/tickers", tags=["tickers"])

@ticker_router.get("/{ticker}/")
def tickers_read(
    ticker: str,
    period: str = Query("5d", description="Période de l'historique, ex: 5d, 1mo, 1y"),
    interval: str = Query("1d", description="Intervalle des données, ex: 1d, 1h"),
    start: str | None = Query(None, description="Date de début, ex: 2024-01-01")
):
    return get_tickers_data(ticker, period, interval, start)