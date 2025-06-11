# InvestAI - Stock Trading Agent

A forward-looking AI-powered trading assistant that analyzes stock market data, generates signals based on technical indicators, backtests strategies, and executes trades via Alpaca. It also sends real-time alerts via Telegram.

## Features

- 📈 Live Intraday Signal Generation
- 🧠 Technical Strategy Backtesting
- 🤖 Auto Trading with Alpaca (Paper Account)
- 🔔 Real-Time Alerts via Telegram
- 📊 Portfolio Performance Dashboard (Planned)
- 🧪 Strategy Optimization (Planned)
- 📋 Multi-Ticker Scanning & Watchlist (Planned)

## Requirements

- Python 3.9+
- Streamlit
- yfinance, pandas, plotly, alpaca-trade-api, requests

## Setup

Create `.streamlit/secrets.toml`:

```toml
TELEGRAM_BOT_TOKEN = "your_bot_token"
TELEGRAM_CHAT_ID = "your_chat_id"
ALPACA_API_KEY = "your_alpaca_key"
ALPACA_SECRET_KEY = "your_alpaca_secret"
```

## Run the App

```bash
streamlit run stock_trading_agent.py
```