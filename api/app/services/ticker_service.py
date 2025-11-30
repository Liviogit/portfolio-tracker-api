from fastapi import HTTPException
import yfinance as yf
import math

def clean_json_values(data):
    if isinstance(data, dict):
        return {k: clean_json_values(v) for k, v in data.items()}
    elif isinstance(data, list):
        return [clean_json_values(v) for v in data]
    elif isinstance(data, float):
        if math.isnan(data) or math.isinf(data):
            return None
        return data
    return data
def get_tickers_data(
    ticker: str,
    period: str = "5d",
    interval: str = "1d",
    start: str | None = None,
):
    try:
        # Vérifie si plusieurs tickers ont été passés
        if ',' in ticker:
            tickers = [t.strip().upper() for t in ticker.split(',')]
            if start:
                data = yf.download(
                    tickers=" ".join(tickers),
                    start=start,
                    interval=interval,
                    group_by="ticker",
                    auto_adjust=True,
                    threads=True
                )
            else:
                data = yf.download(
                    tickers=" ".join(tickers),
                    period=period,
                    interval=interval,
                    group_by="ticker",
                    auto_adjust=True,
                    threads=True
                )
            if data.empty:
                raise HTTPException(status_code=404, detail="Aucune donnée trouvée pour les tickers fournis")

            # Formatage propre du retour
            data_dict = {}
            for t in tickers:
                if t in data.columns.levels[0]:
                    df_t = data[t].reset_index()
                    data_dict[t] = df_t.to_dict(orient="records")
            data_dict = clean_json_values(data_dict)
            return data_dict

        # Cas d’un seul ticker
        else:
            ticker = ticker.strip().upper()
            t = yf.Ticker(ticker)
            if start:
                hist = t.history(interval=interval, start=start, auto_adjust=True)
            else:
                hist = t.history(period=period, interval=interval, auto_adjust=True)

            if hist.empty:
                raise HTTPException(status_code=404, detail=f"Aucune donnée trouvée pour {ticker}")
            hist = clean_json_values(hist)
            return {ticker: hist.reset_index().to_dict(orient="records")}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
