import streamlit as st
import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
from prophet import Prophet

st.set_page_config(page_title="Stock Analysis Dashboard", page_icon="📈", layout="wide")
st.title("📈 Real-Time Stock Analysis Dashboard")

# ---------- Sidebar inputs ----------
with st.sidebar:
    st.header("Settings")
    ticker = st.text_input("Stock ticker", value="AAPL").upper().strip()
    period = st.selectbox("History", ["6mo", "1y", "2y", "5y", "10y"], index=2)
    ma_windows = st.multiselect("Moving averages (days)", [10, 20, 50, 100, 200], default=[20, 50])
    horizon = st.slider("Forecast horizon (days)", 30, 365, 90)


# ---------- Data helpers ----------
@st.cache_data(ttl=300)  # refresh every 5 minutes
def load_data(symbol: str, period: str) -> pd.DataFrame:
    df = yf.download(symbol, period=period, auto_adjust=True, progress=False)
    if df.empty:
        return df
    # Newer yfinance versions return MultiIndex columns
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = df.columns.get_level_values(0)
    df = df.reset_index()
    df["Date"] = pd.to_datetime(df["Date"]).dt.tz_localize(None)
    return df


@st.cache_data(ttl=3600)
def run_forecast(dates: pd.Series, prices: pd.Series, horizon: int) -> pd.DataFrame:
    train = pd.DataFrame({"ds": dates, "y": prices})
    model = Prophet(daily_seasonality=False)
    model.fit(train)
    future = model.make_future_dataframe(periods=horizon)
    return model.predict(future)


# ---------- Main ----------
if not ticker:
    st.info("Enter a ticker symbol in the sidebar to begin.")
    st.stop()

df = load_data(ticker, period)

if df.empty:
    st.error(f"No data found for '{ticker}'. Check the symbol and try again.")
    st.stop()

# Key metrics
last, prev = df["Close"].iloc[-1], df["Close"].iloc[-2]
change = last - prev
c1, c2, c3, c4 = st.columns(4)
c1.metric("Last close", f"{last:,.2f}", f"{change:+.2f} ({change / prev:+.2%})")
c2.metric("Period high", f"{df['High'].max():,.2f}")
c3.metric("Period low", f"{df['Low'].min():,.2f}")
c4.metric("Avg volume", f"{df['Volume'].mean():,.0f}")

tab_hist, tab_ma, tab_fc, tab_data = st.tabs(
    ["📊 Historical", "📉 Moving Averages", "🔮 Forecast", "🗂 Raw Data"]
)

# Tab 1: historical price
with tab_hist:
    st.subheader(f"{ticker} closing price")
    st.line_chart(df.set_index("Date")["Close"])
    st.subheader("Volume")
    st.bar_chart(df.set_index("Date")["Volume"])

# Tab 2: moving averages (matplotlib)
with tab_ma:
    st.subheader("Price with moving averages")
    fig, ax = plt.subplots(figsize=(11, 5))
    ax.plot(df["Date"], df["Close"], label="Close", linewidth=1.5)
    for w in ma_windows:
        ax.plot(df["Date"], df["Close"].rolling(w).mean(), label=f"MA {w}")
    ax.set_xlabel("Date")
    ax.set_ylabel("Price")
    ax.legend()
    ax.grid(alpha=0.3)
    st.pyplot(fig)

# Tab 3: Prophet forecast
with tab_fc:
    st.subheader(f"{horizon}-day forecast")
    with st.spinner("Training Prophet model..."):
        fc = run_forecast(df["Date"], df["Close"], horizon)

    fig2, ax2 = plt.subplots(figsize=(11, 5))
    ax2.plot(df["Date"], df["Close"], label="Actual", color="tab:blue")
    ax2.plot(fc["ds"], fc["yhat"], label="Forecast", color="tab:orange")
    ax2.fill_between(
        fc["ds"], fc["yhat_lower"], fc["yhat_upper"],
        color="tab:orange", alpha=0.2, label="Confidence interval",
    )
    ax2.axvline(df["Date"].iloc[-1], color="gray", linestyle="--", alpha=0.6)
    ax2.legend()
    ax2.grid(alpha=0.3)
    st.pyplot(fig2)

    st.dataframe(
        fc[["ds", "yhat", "yhat_lower", "yhat_upper"]].tail(horizon).rename(
            columns={"ds": "Date", "yhat": "Predicted", "yhat_lower": "Low", "yhat_upper": "High"}
        ),
        use_container_width=True,
    )
    st.caption("Forecasts are statistical projections, not financial advice.")

# Tab 4: raw data
with tab_data:
    st.dataframe(df, use_container_width=True)
    st.download_button("Download CSV", df.to_csv(index=False), f"{ticker}.csv", "text/csv")