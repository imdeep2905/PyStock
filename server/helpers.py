import os
import json

from pathlib import Path
from flask import jsonify


class DatabaseHandler:
    """
    Database Handler class which have static functions to manipulate
    database.
    """

    @staticmethod
    def verify_user(username, password, price_func):
        """
        This function verifies credentials of the user. If they are correct
        their updated portfolio is returned is JSON format.

        Args:
            username: Username of the user.
            password: Supplied password.
            price_func: Function to be used for updating prices of portfolio.

        Returns:
            User's portfolio in JSON format if credentials are correct
            otherwise JSON object with an "error" field.
        """
        if not os.path.isfile(Path(f"userdata/{username}.json")):
            return jsonify({"error": "No such user exist."})
        else:
            with open(Path(f"userdata/{username}.json")) as file:
                data = json.load(file)
            if data["password"] != password:
                return jsonify({"error": "Incorrect password."})
            else:
                data = DatabaseHandler.update_prices(data, price_func)
                return jsonify(data)

    @staticmethod
    def create_user(name, username, email, password):
        """
        This function creates the new user with given information and stores
        it in the JSON format.

        Args:
            name: User's name.
            username: Selected username.
            email: User's email.
            password: Selected password.

        Returns:
            JSON with "ack" field if sign-up is successful other wise JSON
            with "error" field.
        """
        if os.path.isfile(Path(f"userdata/{username}.json")):
            return jsonify({"error": "Username already exists."})
        else:
            data = {
                "name": name,
                "username": username,
                "email": email,
                "password": password,
                "balance": 10000.0,
                "portfolio_value": 0.0,
                "portfolio": [],
            }
            with open(Path(f"userdata/{username}.json"), "w") as file:
                json.dump(data, file)
            return jsonify({"ack": "User has been added successfully."})

    @staticmethod
    def update_portfolio(
        username, action_type, stock_ticker, quantity, stock_price, price_func
    ):
        """
        This function updates the portfolio according to supplied action.

        Args:
            username: Username.
            action_type: "BUY" or "SELL".
            stock_ticker: Stock name.
            quantity: Stock quantity.
            stock_price: Stock's current price.
            price_func: Price function to be used for updating portfolio
            with current prices.

        Returns:
            Updated portfolio in JSON format if update is successfull
            otherwise JSON with an "error" field.
        """
        with open(Path(f"userdata/{username}.json")) as file:
            data = json.load(file)
        if action_type == "BUY":
            if data["balance"] < quantity * stock_price:
                return jsonify({"error": "You don't have enough balance."})
            data["balance"] -= quantity * stock_price
            index = [
                i
                for i in range(len(data["portfolio"]))
                if data["portfolio"][i]["name"] == stock_ticker
            ]
            if len(index) == 0:
                data["portfolio"].append(
                    {
                        "name": stock_ticker,
                        "quantity": quantity,
                        "investment": quantity * stock_price,
                        "cur_price": stock_price,
                    }
                )
            else:
                index = index[0]
                data["portfolio"][index]["quantity"] += quantity
                data["portfolio"][index]["investment"] += (
                    quantity * stock_price
                )
                data["portfolio"][index]["cur_price"] = stock_price
        else:
            data["balance"] += quantity * stock_price
            index = [
                i
                for i in range(len(data["portfolio"]))
                if data["portfolio"][i]["name"] == stock_ticker
            ][0]
            if quantity > data["portfolio"][index]["quantity"]:
                return jsonify({"error": "You don't have enough stocks."})
            data["portfolio"][index]["quantity"] -= quantity
            data["portfolio"][index]["investment"] -= quantity * stock_price
            data["portfolio"][index]["cur_price"] = stock_price
            if data["portfolio"][index]["quantity"] == 0:
                data["portfolio"].pop(index)
        data = DatabaseHandler.update_prices(data, price_func)
        with open(Path(f"userdata/{username}.json"), "w") as file:
            json.dump(data, file)
        return jsonify(data)

    @staticmethod
    def update_prices(data, price_func):
        """
        This function updates current prices of all stocks in portfolio.

        Args:
            data: User's data in JSON format.
            price_func: Price function to be used for updating stock prices.

        Returns:
            Updated data in JSON format.
        """
        data["portfolio_value"] = 0
        for stock in data["portfolio"]:
            stock["cur_price"] = price_func(stock["name"])
            data["portfolio_value"] += stock["quantity"] * stock["cur_price"]
        return data
