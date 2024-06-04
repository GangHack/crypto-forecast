MENU_OPTIONS = {
    "app": "Market Forecast"
}

ML_MODELS = {
    "fbprophet": "Facebook Prophet",
    "neuralprophet": "Neural Prophet"
}

PERIODS = {
    "1d": "1 day", "5d": "5 days",
    "1mo": "1 month", "3mo": "3 months", "6mo": "6 months",
    "1y": "1 year", "2y": "2 years", "5y": "5 years", "10y": "10 years",
    "ytd": "year today", "max": "Max"
}

INTERVALS = {
    "1m": "1 minute", "2m": "2 minutes", "5m": "5 minutes", "15m": "15 minutes",
    "30m": "30 minutes", "60m": "60 minutes", "90m": "90 minutes",
    "1h": "1 hour",
    "1d": "1 day", "5d": "5 days",
    "1wk": "1 week",
    "1mo": "1 month", "3mo": "3 months"
}

TICKER_TYPE = ["Crypto", "Stock"]

CURRENCIES = ["USD", "EUR", "CAD", "GBP", "AUD", "JPY", "KRW"]

CRYPTOS = {
    None: "Виберіть криптовалюту",
    "BTC": "Bitcoin", "ETH": "Ethereum", "BNB": "BinanceCoin", "USDT": "Tether",
    "ADA": "Cardano", "XRP": "XRP", "DOGE": "DogeCoin", "DOT1": "Polkadot",
    "BCH": "BitcoinCash", "UNI3": "Uniswap", "USDC": "USDCoin", "LTC": "Litecoin",
    "LINK": "Chainlink", "SOL1": "Solana", "XLM": "Stellar", "MATIC": "MaticNetwork",
    "HEX": "HEX", "ETC": "EthereumClassic", "VET": "VeChain", "THETA": "THETA",
    "TRX": "TRON", "FIL": "FilecoinFutures", "EOS": "EOS", "AAVE": "Aave", "XMR": "Monero",
    "NEO": "NEO", "LUNA1": "Terra", "MKR": "Maker", "MIOTA": "IOTA", "BSV": "BitcoinSV",
    "XTZ": "Tezos", "KSM": "Kusama", "CRO": "CryptocomCoin", "ATOM1": "Cosmos",
    "ALGO": "Algorand", "AVAX": "Avalanche", "COMP": "Compound", "WAVES": "Waves"
}

HOLIDAYS = {
    None: "Свята не встановлені",
    "CA": "Canada", "CN": "China", "DE": "Germany", "IN": "India",
    "FR": "France", "GB": "United Kingdom", "HK": "Hong Kong",
    "NZ": "New Zealand", "SG": "Singapore", "KR": "South Korea",
    "US": "United States"
}

TICKER_DATA_COLUMN = ["Open", "High", "Low", "Close"]

SEASONALITY_OPTIONS = ["auto", True, False]

SEASONALITY_MODE_OPTIONS = ["multiplicative", "additive"]

VALIDATION_METRICS = ['mse', 'rmse', 'mae', 'mape', 'mdape', 'coverage']
