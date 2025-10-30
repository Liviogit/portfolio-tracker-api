from fastapi import HTTPException
import yfinance as yf

def get_tickers_data(
    ticker: str,
    period: str = "5d",
    interval: str = "1d"
):
    try:
        # Vérifie si plusieurs tickers ont été passés
        if ',' in ticker:
            tickers = [t.strip().upper() for t in ticker.split(',')]
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

            return data_dict

        # Cas d’un seul ticker
        else:
            ticker = ticker.strip().upper()
            t = yf.Ticker(ticker)
            hist = t.history(period=period, interval=interval, auto_adjust=True)

            if hist.empty:
                raise HTTPException(status_code=404, detail=f"Aucune donnée trouvée pour {ticker}")

            return {ticker: hist.reset_index().to_dict(orient="records")}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
