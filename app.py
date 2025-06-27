import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
import ta

# --- Configuración de la app ---
st.set_page_config(page_title="AI Stocks Monitor", layout="wide")
st.title("📊 Dashboard de acciones emergentes de IA")

# --- Selección de empresa ---
tickers = {
    "BigBear.ai (BBAI)": "BBAI",
    "Recursion Pharma (RXRX)": "RXRX",
    "Symbotic (SYM)": "SYM",
    "SoundHound AI (SOUN)": "SOUN",
    "Upstart (UPST)": "UPST"
}

empresa = st.selectbox("Selecciona una empresa:", list(tickers.keys()))
ticker = tickers[empresa]

# --- Descargar datos ---
df = yf.download(ticker, start="2024-01-01", end="2025-06-27")
df["RSI"] = ta.momentum.RSIIndicator(df["Close"]).rsi()
df["EMA_20"] = ta.trend.EMAIndicator(df["Close"], window=20).ema_indicator()

# --- Gráfico interactivo ---
fig = go.Figure()
fig.add_trace(go.Scatter(x=df.index, y=df["Close"], name="Precio", line=dict(color="royalblue")))
fig.add_trace(go.Scatter(x=df.index, y=df["EMA_20"], name="EMA 20", line=dict(dash="dot", color="green")))
fig.update_layout(title=f"{empresa} - Precio & EMA", template="plotly_white", height=450)

# --- Mostrar gráficos e indicadores ---
st.plotly_chart(fig, use_container_width=True)
st.markdown(f"""
**Precio actual:** ${df['Close'].iloc[-1]:.2f}  
**RSI actual:** {df['RSI'].iloc[-1]:.2f}  
""")

# --- Alerta automática ---
if df["RSI"].iloc[-1] < 30:
    st.warning("🔔 RSI indica sobreventa (RSI < 30): posible oportunidad de compra")
elif df["RSI"].iloc[-1] > 70:
    st.error("⚠️ RSI indica sobrecompra (RSI > 70): precaución antes de comprar")

# --- Opcional: Exportar CSV ---
st.download_button("📥 Exportar datos como CSV", df.to_csv().encode("utf-8"), file_name=f"{ticker}_historico.csv", mime="text/csv")

