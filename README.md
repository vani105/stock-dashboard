# 📈 Real-Time Stock Analysis Dashboard

An interactive financial analytics app built with **Streamlit**. Enter a stock ticker and the app pulls market data from Yahoo Finance, plots historical trends, calculates moving averages, and forecasts future prices using **Prophet**.

**Live demo:** https://stock-dashboard-zbfyk7jsmphkhsb6dwe5hp.streamlit.app/

## Features

- 🔍 Search any ticker (US stocks, Indian stocks, ETFs, indices, crypto)
- 📊 Historical price and volume charts
- 📉 Customizable moving averages (10, 20, 50, 100, 200 days)
- 🔮 Prophet-based forecast with confidence intervals (30–365 days)
- 📌 Key metrics: last close, daily change, period high/low, average volume
- 🗂 Raw data table with CSV download
- ⚡ Cached data fetching for faster reloads

## Tech Stack

| Tool | Purpose |
|---|---|
| Python 3.12 | Language |
| Streamlit | Web UI |
| yfinance | Yahoo Finance data |
| pandas | Data handling |
| matplotlib | Charts |
| Prophet | Time-series forecasting |

## Project Structure

```
stock-dashboard/
├── app.py              # Main Streamlit app
├── requirements.txt    # Python dependencies
├── .gitignore
└── README.md
```

## Run Locally

1. **Clone the repository**
   ```bash
   git clone https://github.com/vani105/stock-dashboard.git
   cd stock-dashboard
   ```

2. **Create and activate a virtual environment** (Python 3.11 or 3.12 recommended)
   ```bash
   python -m venv venv
   # Windows
   venv\Scripts\activate
   # Mac/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   python -m pip install -r requirements.txt
   ```

4. **Start the app**
   ```bash
   python -m streamlit run app.py
   ```
   The app opens at `http://localhost:8501`.

## Example Tickers

| Market | Examples |
|---|---|
| US stocks | `AAPL`, `MSFT`, `TSLA`, `NVDA`, `GOOGL` |
| Indian stocks (NSE) | `RELIANCE.NS`, `TCS.NS`, `INFY.NS`, `HDFCBANK.NS` |
| Indices | `^GSPC` (S&P 500), `^NSEI` (Nifty 50) |
| Crypto | `BTC-USD`, `ETH-USD` |

## Deployment

Deployed on [Streamlit Community Cloud](https://share.streamlit.io):

1. Push the repo to GitHub
2. Create a new app on Streamlit Community Cloud and select this repository
3. Set the main file to `app.py`
4. Under **Advanced settings**, choose **Python 3.12**
5. Deploy

## Troubleshooting

- **`No module named 'prophet'` or `'yfinance'`:** make sure `requirements.txt` is saved as UTF-8 and contains all packages.
- **Prophet fails to install:** use Python 3.11 or 3.12 (not 3.13+).
- **"No data found":** check the ticker spelling. Indian stocks need `.NS` or `.BO`.

## Disclaimer

This project is for educational purposes only. Forecasts are statistical projections based on past prices and are **not financial advice**.

## License

MIT
