from flask import Flask, request, jsonify
from flask_cors import CORS
from forex_python.converter import CurrencyRates
from helpers import DatabaseHandler
from yahoo_fin import stock_info as si

app = Flask(__name__)
CORS(app)
app.config["DEBUG"] = True


@app.route("/login", methods=["POST"])
def login():
    """This function handles `POST` requests done on `SERVER_ADDRESS/login`."""
    username = request.form["username"]
    password = request.form["password"]
    return DatabaseHandler.verify_user(username, password, db_price_func)


@app.route("/signup", methods=["POST"])
def signup():
    """
    This function handles `POST` requests done on `SERVER_ADDRESS/signup`.
    """
    name = request.form["name"]
    username = request.form["username"]
    password = request.form["password"]
    email = request.form["email"]
    return DatabaseHandler.create_user(name, username, email, password)


@app.route("/live_price", methods=["POST"])
def live_price():
    """
    This function handles `POST` requests done on `SERVER_ADDRESS/live_price`.
    """
    stock_ticker = request.form["stock_ticker"]
    price = float(si.get_live_price(stock_ticker))
    if ".NS" in stock_ticker or ".BO" in stock_ticker:
        price = price / CurrencyRates().get_rate("USD", "INR")
    return jsonify({"price": price})


@app.route("/update_portfolio", methods=["POST"])
def update_portfolio():
    """
    This function handles `POST` requests done on
    `SERVER_ADDRESS/update_portfolio`.
    """
    username = request.form["username"]
    action_type = request.form["action_type"]
    stock_ticker = request.form["stock_ticker"]
    quantity = int(request.form["quantity"])
    try:
        stock_price = float(si.get_live_price(stock_ticker))
        if ".NS" in stock_ticker or ".BO" in stock_ticker:
            stock_price = stock_price / CurrencyRates().get_rate("USD", "INR")
    except AssertionError:
        return jsonify({"error": "This stock is not available."})
    return DatabaseHandler.update_portfolio(
        username,
        action_type,
        stock_ticker,
        quantity,
        stock_price,
        db_price_func,
    )


def db_price_func(stock_ticker):
    """
    This function provides most recent price of the given stock.

    Args:
        stock_ticker: Stock Ticker

    Returns:
        Latest price of the given stock (in $).
    """
    stock_price = float(si.get_live_price(stock_ticker))
    if ".NS" in stock_ticker or ".BO" in stock_ticker:
        stock_price = stock_price / CurrencyRates().get_rate("USD", "INR")
    return stock_price


def main():
    """
    This function is the entry point of this program.

    Args:
        None

    Returns:
        None
    """
    app.run()


if __name__ == "__main__":
    # Run this only if this file is executed directly.
    main()
