import yfinance as yf
import ta
import pandas as pd
from datetime import date

tickers = ['BBAI', 'RXRX', 'SOUN', 'UPST', 'SYM']
alertas = []

for t in tickers:
    df = yf.download(t, period='30d')
    rsi = ta.momentum.RSIIndicator(df['Close']).rsi().iloc[-1]
    if rsi < 30:
        alertas.append(f'{t}: RSI {rsi:.2f} (⚠️ Sobreventa)')
    elif rsi > 70:
        alertas.append(f'{t}: RSI {rsi:.2f} (⚠️ Sobrecompra)')

# Guardar resultado
pd.DataFrame({'Alerta': alertas}).to_csv(f'alertas_{date.today()}.csv', index=False)
