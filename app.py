# Meme Coin Dashboard (Streamlit + Pump.fun via Moralis)
# This is Option 2: Python + Streamlit app with live updates

import streamlit as st
import requests
import time
import pandas as pd

# Page settings
st.set_page_config(page_title="Live Meme Coin Dashboard", layout="wide")
st.title("🚀 Live Meme Coin Launches from Pump.fun")

# API config (replace 'YOUR_API_KEY' with actual key from Moralis)
MORALIS_API_KEY = "YOUR_API_KEY"
HEADERS = {
    "accept": "application/json",
    "X-API-Key": MORALIS_API_KEY
}
API_URL = "https://solana-gateway.moralis.io/pumpfun/token/list"

# Polling interval
REFRESH_INTERVAL = 10  # in seconds

# Live loop
placeholder = st.empty()

while True:
    try:
        response = requests.get(API_URL, headers=HEADERS)
        data = response.json()

        tokens = data.get("result", [])

        # Convert to DataFrame
        df = pd.DataFrame(tokens)

        if df.empty:
            placeholder.warning("No tokens found.")
        else:
            # Optional filtering: only show meme-like tokens
            df = df[df["name"].str.contains("pepe|doge|inu|meme|cat", case=False, na=False)]

            # Show dashboard
            with placeholder.container():
                st.dataframe(
                    df[["name", "symbol", "marketCap", "price", "launchedAt"]]
                    .rename(columns={
                        "name": "Token Name",
                        "symbol": "Symbol",
                        "marketCap": "Market Cap",
                        "price": "Price",
                        "launchedAt": "Launch Time"
                    })
                    .sort_values(by="Launch Time", ascending=False),
                    use_container_width=True
                )

    except Exception as e:
        placeholder.error(f"Error fetching data: {e}")

    time.sleep(REFRESH_INTERVAL)
