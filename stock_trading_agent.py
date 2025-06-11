
import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go

# Parameters
TICKERS = ['AAPL', 'TSLA', 'MSFT', 'NVDA', 'AMZN']
STRATEGIES = ['Moving Average Crossover']

# Strategy function
def generate_signals(df, strategy='Moving Average Crossover'):
    df['MA10'] = df['Close'].rolling(window=10).mean()
    df['MA50'] = df['Close'].rolling(window=50).mean()
    df['Signal'] = 0
    df.loc[df['MA10'] > df['MA50'], 'Signal'] = 1
    df.loc[df['MA10'] < df['MA50'], 'Signal'] = -1
    return df

# Backtesting function
def backtest_strategy(df):
    df['Returns'] = df['Close'].pct_change()
    df['Strategy'] = df['Signal'].shift(1) * df['Returns']
    df['Cumulative Market Returns'] = (1 + df['Returns']).cumprod()
    df['Cumulative Strategy Returns'] = (1 + df['Strategy']).cumprod()
    return df

# Plot function
def plot_indicators(df, ticker):
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df.index, y=df['Close'], name='Close'))
    fig.add_trace(go.Scatter(x=df.index, y=df['MA10'], name='MA10'))
    fig.add_trace(go.Scatter(x=df.index, y=df['MA50'], name='MA50'))
    fig.update_layout(title=f'{ticker} Price with Indicators')
    return fig

# Streamlit UI
st.title("InvestAI: Stock Trading Agent")
selected_ticker = st.selectbox("Select Stock", TICKERS)
strategy = st.selectbox("Select Strategy", STRATEGIES)
period = st.selectbox("Select Period", ['1mo', '3mo', '6mo', '1y'])
interval = st.selectbox("Select Interval", ['1h', '30m', '15m'])

df_hist = yf.download(selected_ticker, period=period, interval=interval)
df_hist = generate_signals(df_hist, strategy)
bt = backtest_strategy(df_hist)

st.subheader("Backtest Results")
try:
    st.line_chart(bt[['Cumulative Market Returns', 'Cumulative Strategy Returns']])
except KeyError:
    st.warning("Backtest data not available for the selected combination.")

if st.button("Run Live Agent"):
    df_live = yf.download(selected_ticker, period='1d', interval='5m')
    df_live = generate_signals(df_live, strategy)
    if not df_live.empty and 'Signal' in df_live.columns:
        signal = df_live.iloc[-1]['Signal']
        if isinstance(signal, pd.Series):
            signal = signal.item()
        st.write("Latest Signal:", 'BUY' if signal == 1 else 'SELL' if signal == -1 else 'HOLD')
        st.plotly_chart(plot_indicators(df_live, selected_ticker))
    else:
        st.warning("Live data or signal generation failed.")
