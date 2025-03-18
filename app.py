import os
from flask import Flask, jsonify
from flask_cors import CORS
import yfinance as yf
from datetime import datetime

app = Flask(__name__)
CORS(app)

NSE_INDICES = {
    "NIFTY 50": "^NSEI",
    "NIFTY NEXT 50": "^NSMIDCP",
    "NIFTY BANK": "^NSEBANK",
    "NIFTY IT": "^CNXIT",
    "NIFTY FMCG": "^CNXFMCG",
    "NIFTY PHARMA": "^CNXPHARMA",
    "NIFTY AUTO": "^CNXAUTO",
    "NIFTY REALTY": "^CNXREALTY",
    "NIFTY MEDIA": "^CNXMEDIA",
    "NIFTY METAL": "^CNXMETAL",
    "NIFTY ENERGY": "^CNXENERGY",
    "NIFTY INFRA": "^CNXINFRA",
    "NIFTY PSE": "^CNXPSE",
    "NIFTY PSU BANK": "^CNXPSUBANK",
    "NIFTY SERV SECTOR": "^CNXSERVICE",
}

def is_market_open():
    now = datetime.now()
    return 9 <= now.hour < 15 or (now.hour == 15 and now.minute <= 30)

@app.route('/nse-indices')
def get_nse_indices():
    try:
        index_data = {}

        for name, symbol in NSE_INDICES.items():
            stock = yf.Ticker(symbol)
            history = stock.history(period="2d")  # Fetch last 2 days data

            if history.empty or len(history) < 2:
                index_data[name] = {"current_price": "N/A", "percent_change": "N/A"}
                continue

            prev_close = history["Close"].iloc[-2]  # Previous day close
            current_price = history["Close"].iloc[-1]  # Last traded price

            percent_change = ((current_price - prev_close) / prev_close) * 100 if prev_close else 0

            index_data[name] = {
                "current_price": round(current_price, 2),
                "percent_change": round(percent_change, 2)  # ✅ Broker-style percentage change
            }

        return jsonify(index_data)

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
