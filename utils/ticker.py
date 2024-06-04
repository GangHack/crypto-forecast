import yfinance as yf
import streamlit as st


@st.cache_data(max_entries=50, ttl=900, show_spinner=False)
def fetch_stock_info(stock_params):
    stock_data = yf.Ticker(stock_params.ticker_name)

    stock_details = {
        "info": stock_data.info,
        "price_history": stock_data.history(
            period=stock_params.period,
            interval=stock_params.interval
        )
    }
    return stock_details


def display_stock_info(stock_params):
    stock_details = fetch_stock_info(stock_params)

    with st.expander(
        "Інформація про актив", expanded=True
    ):
        st.write(stock_details["info"])

    historical_prices = stock_details["price_history"]
    if historical_prices is not None:
        sorted_history = historical_prices.sort_index(ascending=False)
        st.subheader("Історія цін")
        st.write(sorted_history)

    return historical_prices
