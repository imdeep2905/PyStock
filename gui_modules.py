import tkinter as tk
import pathlib
import requests
import re
import finplot as fplt
import matplotlib.pyplot as plt
import yfinance as yf

from datetime import datetime
from ttkthemes import ThemedTk
from tkinter import messagebox
from tkinter import ttk

API_ENDPOINT = "http://127.0.0.1:5000/"


def verify_email(email):
    """
    This function validates the given email using regular expression.

    Args:
        email: Email to be verified.

    Returns:
        True if email format is correct otherwise False.
    """
    email_rule = r"^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$"
    return re.search(email_rule, email)


class LoginFrame(ttk.Frame):
    """This class provides styled Login Frame"""

    def __init__(self, master):
        """
        Constructor for LoginFrame

        Args:
            master: Parent widget.

        Returns:
            None
        """
        ttk.Frame.__init__(self, master)
        self._master = master
        ttk.Label(text="Username: ").grid(
            row=0, column=0, padx=(50, 0), pady=(50, 5)
        )
        self.username_entry = ttk.Entry()
        self.username_entry.grid(row=0, column=1, padx=(0, 50), pady=(50, 0))
        ttk.Label(text="Password: ").grid(
            row=1, column=0, padx=(50, 0), pady=(5, 5)
        )
        self.password_entry = ttk.Entry(show="•")
        self.password_entry.grid(row=1, column=1, padx=(0, 50), pady=(5, 5))
        ttk.Button(text="Login", command=self.init_login).grid(
            row=2, column=0, padx=(50, 0), pady=(5, 5)
        )
        ttk.Button(
            text="New User? SignUp",
            command=lambda: self._master.switch_frame(
                SignUpFrame, "PyStock | SignUp"
            ),
        ).grid(row=2, column=1, padx=(0, 50), pady=(5, 5))
        themes = [
            "yaru",
            "classic",
            "xpnative",
            "scidpink",
            "breeze",
            "alt",
            "scidgreen",
            "clearlooks",
            "black",
            "scidmint",
            "equilux",
            "adapta",
            "winxpblue",
            "scidgrey",
            "ubuntu",
            "kroc",
            "keramik",
            "scidpurple",
            "arc",
            "itft1",
            "scidsand",
            "clam",
            "plastik",
            "scidblue",
            "default",
            "smog",
            "winnative",
            "elegance",
            "vista",
            "radiance",
            "aquativo",
            "blue",
        ]
        self.select_theme = ttk.Combobox(self._master)
        self.select_theme["values"] = themes
        self.select_theme.bind(
            "<<ComboboxSelected>>",
            lambda _: self._master.change_theme(self.select_theme.get()),
        )
        ttk.Label(text="Change Theme: ").grid(
            row=3, column=0, padx=(50, 0), pady=(5, 50)
        )
        self.select_theme.current(0)
        self.select_theme.grid(row=3, column=1, padx=(0, 50), pady=(5, 50))

    def init_login(self):
        """
        This function initiates login process and verify credentials with
        server using API. This function automatically opens Dashboard Frame if
        login is successful.

        Args:
            None

        Returns:
            None
        """
        if self.password_entry == "":
            messagebox.showerror(
                "Login Error", "password field can't be empty."
            )
            return
        payload = {
            "username": self.username_entry.get(),
            "password": self.password_entry.get(),
        }
        response = requests.post(API_ENDPOINT + "login", payload).json()
        if response.get("error") is not None:
            messagebox.showerror("Login Error", response["error"])
        else:
            self._master.switch_frame(
                DashboardFrame, "PyStock | Dashboard", response
            )


class SignUpFrame(ttk.Frame):
    """This class provides styled SignUp Frame"""

    def __init__(self, master):
        """
        Constructor for SignUpFrame

        Args:
            master: Parent widget.

        Returns:
            None
        """
        ttk.Frame.__init__(self, master)
        self._master = master
        ttk.Label(text="Email: ").grid(
            row=0, column=0, padx=(50, 0), pady=(50, 5)
        )
        self.email_entry = ttk.Entry()
        self.email_entry.grid(row=0, column=1, padx=(0, 50), pady=(50, 5))
        ttk.Label(text="Name: ").grid(
            row=1, column=0, padx=(50, 0), pady=(5, 5)
        )
        self.name_entry = ttk.Entry()
        self.name_entry.grid(row=1, column=1, padx=(0, 50), pady=(5, 5))
        ttk.Label(text="Username: ").grid(
            row=2, column=0, padx=(50, 0), pady=(5, 5)
        )
        self.username_entry = ttk.Entry()
        self.username_entry.grid(row=2, column=1, padx=(0, 50), pady=(5, 5))
        ttk.Label(text="Password: ").grid(
            row=3, column=0, padx=(50, 0), pady=(5, 5)
        )
        self.password_entry = ttk.Entry(show="•")
        self.password_entry.grid(row=3, column=1, padx=(0, 50), pady=(5, 5))
        ttk.Label(text="Re-enter password: ").grid(
            row=4, column=0, padx=(50, 0), pady=(5, 5)
        )
        self.repassword_entry = ttk.Entry(show="•")
        self.repassword_entry.grid(row=4, column=1, padx=(0, 50), pady=(5, 5))
        ttk.Button(text="SignUp", command=self.init_signup).grid(
            row=5, column=0, columnspan=2, padx=(50, 0), pady=(5, 50)
        )

    def init_signup(self):
        """
        This function initiates sign-up process and register user with server
        using API. This function automatically opens Login if sign-up is
        successful.

        Args:
            None

        Returns:
            None
        """
        error_title = "SignUp Error"
        if not verify_email(self.email_entry.get()):
            messagebox.showerror(error_title, "Invalid email")
            return
        if (
            self.password_entry.get() == ""
            or self.name_entry.get() == ""
            or self.username_entry.get() == ""
        ):
            messagebox.showerror(error_title, "Some of the fields are empty.")
            return
        if self.password_entry.get() != self.repassword_entry.get():
            messagebox.showerror(error_title, "passwords don't match.")
            return
        payload = {
            "name": self.name_entry.get(),
            "username": self.username_entry.get(),
            "email": self.email_entry.get(),
            "password": self.password_entry.get(),
        }
        response = requests.post(API_ENDPOINT + "signup", payload).json()
        if response.get("error") is not None:
            messagebox.showerror(error_title, response["error"])
        else:
            messagebox.showinfo(
                "Registration done",
                "You have registered with PyStock successfully. Now click OK"
                " to login into PyStock",
            )
            self._master.switch_frame(LoginFrame, "PyStock | Login")


class DashboardFrame(ttk.Frame):
    """This class provides styled DashboardFrame Frame"""

    def __init__(self, master, user_data):
        """
        Constructor for DashboardFrame

        Args:
            master: Parent widget.
            user_data: Userdata in JSON format.

        Returns:
            None
        """
        ttk.Frame.__init__(self, master)
        self._master = master
        self._user_data = user_data
        self.info_frame = ttk.LabelFrame(text="User Info")
        self.info_frame.rowconfigure(0)
        self.info_frame.rowconfigure(1)
        self.info_frame.columnconfigure(0)
        self.info_frame.columnconfigure(1)
        ttk.Label(
            self.info_frame, text="Name: " + self._user_data["name"]
        ).grid(row=0, column=0, sticky="nsew", padx=(5, 10), pady=(5, 0))
        ttk.Label(
            self.info_frame, text="Email: " + self._user_data["email"]
        ).grid(row=0, column=1, sticky="nsew", padx=(5, 10), pady=(5, 0))
        ttk.Label(
            self.info_frame,
            text="Balance ($): " + str(round(self._user_data["balance"], 4)),
        ).grid(row=1, column=0, sticky="nsew", padx=(5, 10), pady=(5, 5))
        ttk.Label(
            self.info_frame,
            text="Total Portfolio Value ($): "
            + str(round(self._user_data["portfolio_value"], 4)),
        ).grid(row=1, column=1, sticky="nsew", padx=(5, 10), pady=(5, 5))
        self.info_frame.grid(
            row=0,
            column=0,
            sticky="nsew",
            padx=(5, 5),
            pady=(5, 0),
        )
        self.search_frame = ttk.LabelFrame(text="Search stock")
        self.search_frame.rowconfigure(0)
        self.search_frame.rowconfigure(1)
        self.search_frame.columnconfigure(0)
        self.search_frame.columnconfigure(1)
        ttk.Label(self.search_frame, text="Enter stock name: ").grid(
            row=0, column=0, padx=(5, 0), pady=(5, 0), sticky="nsew"
        )
        self.search_entry = ttk.Entry(self.search_frame)
        self.search_entry.grid(
            row=0, column=1, padx=(5, 5), pady=(5, 0), sticky="nsew"
        )
        ttk.Button(self.search_frame, text="Search", command=self.search).grid(
            row=1,
            column=0,
            columnspan=2,
            padx=(5, 5),
            pady=(5, 5),
            sticky="nsew",
        )
        self.search_frame.grid(
            row=0, column=1, padx=(0, 5), pady=(5, 0), sticky="nsew"
        )
        self.stock_table_frame = ttk.LabelFrame(text="Your Portfolio")
        self.stock_table_frame.rowconfigure(0)
        self.stock_table_frame.columnconfigure(0)
        self.stock_table = ttk.Treeview(
            self.stock_table_frame,
            columns=(
                "Sr.",
                "Name",
                "Quantity",
                "Investment",
                "Current Price",
                "State",
            ),
            show="headings",
            selectmode="browse",
        )
        for col in [
            "Sr.",
            "Name",
            "Quantity",
            "Investment",
            "Current Price",
            "State",
        ]:
            self.stock_table.column(col, width=100)
            self.stock_table.heading(col, text=col)
        self.stock_table.bind("<Double-1>", self.init_sell)
        for count, stock in enumerate(self._user_data["portfolio"], start=1):
            if (
                abs(
                    stock["cur_price"] * stock["quantity"]
                    - stock["investment"]
                )
                <= 0.01
            ):
                state = "BREAK EVEN"
            else:
                state = (
                    "PROFIT"
                    if stock["cur_price"] * stock["quantity"]
                    > stock["investment"]
                    else "LOSS"
                )
            self.stock_table.insert(
                "",
                "end",
                values=(
                    count,
                    stock["name"],
                    stock["quantity"],
                    round(stock["investment"], 4),
                    round(stock["cur_price"], 4),
                    state,
                ),
                tags=(state,),
            )

        self.stock_table.tag_configure(
            "PROFIT", background="#BEF558", foreground="black"
        )
        self.stock_table.tag_configure(
            "LOSS", background="#F3846C", foreground="black"
        )
        self.stock_table.tag_configure(
            "BREAK EVEN", background="#FFFD69", foreground="black"
        )

        self.stock_table.grid(row=0, column=0, columnspan=3, sticky="nsew")
        ttk.Button(
            self.stock_table_frame, text="Refresh", command=self.refresh
        ).grid(row=1, column=0, sticky="nsew")
        ttk.Button(
            self.stock_table_frame, text="Buy Stocks", command=self.init_buy
        ).grid(row=1, column=1, sticky="nsew")
        ttk.Button(
            self.stock_table_frame, text="Analyze", command=self.analyze
        ).grid(row=1, column=2, sticky="nsew")
        ttk.Label(
            self.stock_table_frame,
            text="Double click on the stock entry to sell that stock.",
        ).grid(row=2, column=0, columnspan=3)
        self.stock_table_frame.grid(
            row=1,
            column=0,
            columnspan=2,
            sticky="nsew",
            padx=(5, 5),
            pady=(5, 5),
        )

    def search(self):
        """
        This function displays given stock's history for the period of 4 years.

        Args:
            None

        Returns:
            None
        """
        try:
            df = yf.download(
                self.search_entry.get(),
                start="2017-01-01",
                end=datetime.today().strftime("%Y-%m-%d"),
            )
            fplt.candlestick_ochl(df[["Open", "Close", "High", "Low"]])
            fplt.plot(df.Close.rolling(50).mean())
            fplt.plot(df.Close.rolling(200).mean())
            fplt.show()
        except IndexError:
            messagebox.showerror("Stock Name Error", "Invalid Stock name")

    def refresh(self):
        """
        This function refreshes dashboard after getting new user data from the
        API. This function indirectly uses login to get updated user data.

        Args:
            None

        Returns:
            None
        """
        payload = {
            "username": self._user_data["username"],
            "password": self._user_data["password"],
        }
        response = requests.post(API_ENDPOINT + "login", payload).json()
        self._master.switch_frame(
            DashboardFrame, "PyStock | Dashboard", response
        )

    def analyze(self):
        """
        This function analyzes user's portfolio and displays it in the form of
        piechart.

        Args:
            None

        Returns:
            None
        """
        labels = []
        sizes = []
        for stock in self._user_data["portfolio"]:
            labels.append(stock["name"])
            sizes.append(stock["quantity"] * stock["cur_price"])
        _, ax = plt.subplots()
        ax.pie(sizes, labels=labels, autopct="%1.1f%%", startangle=90)
        ax.axis("equal")
        ax.set_title("Your portfolio distribution according to current prices")
        plt.show()

    def init_sell(self, event):
        """
        This function initiates the selling process by opening a new
        SellWindow with selected stock.

        Args:
            event: Double Click event captured from the tree view.

        Returns:
            None
        """
        item = self.stock_table.item(
            self.stock_table.identify("item", event.x, event.y)
        )
        SellWindow(self, item["values"][1])

    def init_buy(self):
        """
        This function initiates the buying process by opening a new
        BuyWindow.

        Args:
            None

        Returns:
            None
        """
        BuyWindow(self)


class SellWindow(tk.Toplevel):
    """This class provides Toplevel window to sell stocks"""

    def __init__(self, master, stock_name):
        """
        Constructor for SellWindow

        Args:
            master: Parent widget.
            stock_name: Stock ticker obtained from parent's (i.e. DashBoard)
            treeview.

        Returns:
            None
        """
        tk.Toplevel.__init__(self)
        self._master = master
        self.stock_name = stock_name
        self.title("PyStock | Sell stock")
        self.iconphoto(
            False, tk.PhotoImage(file=pathlib.Path("assets/icon.png"))
        )
        self.resizable(0, 0)
        tk.Label(self, text="Quantity: ").grid(
            row=0, column=0, padx=(50, 5), pady=(50, 5)
        )
        self.quantity_entry = tk.Entry(self)
        self.quantity_entry.grid(row=0, column=1, padx=(0, 50), pady=(50, 5))
        tk.Button(self, text="Sell", command=self.sell_stock).grid(
            row=1,
            column=0,
            columnspan=2,
            padx=(50, 50),
            pady=(0, 50),
            sticky="nsew",
        )

    def sell_stock(self):
        """
        This function sell stocks and register it with server using the API.

        Args:
            None

        Returns:
            None
        """
        try:
            payload = {
                "username": self._master._user_data["username"],
                "action_type": "SELL",
                "stock_ticker": self.stock_name,
                "quantity": int(self.quantity_entry.get()),
            }
            assert payload["quantity"] > 0, "Quantity must be positive."
        except (ValueError, AssertionError) as e:
            messagebox.showerror("Quantity Error", e)
            return
        response = requests.post(
            API_ENDPOINT + "update_portfolio", payload
        ).json()
        if response.get("error") is not None:
            messagebox.showerror("Sell Stock Error", response["error"])
        else:
            self._master._master.switch_frame(
                DashboardFrame, "PyStock | Dashboard", response
            )


class BuyWindow(tk.Toplevel):
    """This class provides styled SignUp Frame"""

    def __init__(self, master):
        """
        Constructor for BuyWindow

        Args:
            master: Parent widget.

        Returns:
            None
        """
        tk.Toplevel.__init__(self)
        self._master = master
        self.title("PyStock | Buy stock")
        self.iconphoto(
            False, tk.PhotoImage(file=pathlib.Path("assets/icon.png"))
        )
        self.resizable(0, 0)
        tk.Label(self, text="Stock Name: ").grid(
            row=0, column=0, padx=(50, 0), pady=(50, 0)
        )
        self.name_entry = tk.Entry(self)
        self.name_entry.grid(row=0, column=1, padx=(0, 50), pady=(50, 0))
        tk.Label(self, text="Quantity: ").grid(
            row=1, column=0, padx=(50, 0), pady=(0, 0)
        )
        self.quantity_entry = tk.Entry(self)
        self.quantity_entry.grid(row=1, column=1, padx=(0, 50), pady=(0, 0))
        tk.Button(self, text="Buy", command=self.buy_stock).grid(
            row=2,
            column=0,
            columnspan=2,
            padx=(50, 50),
            pady=(0, 50),
            sticky="nsew",
        )

    def buy_stock(self):
        """
        This function buy stocks and register it with server using the API.

        Args:
            None

        Returns:
            None
        """
        try:
            payload = {
                "username": self._master._user_data["username"],
                "action_type": "BUY",
                "stock_ticker": self.name_entry.get(),
                "quantity": int(self.quantity_entry.get()),
            }
            assert payload["quantity"] > 0, "Quantity must be positive."
        except (ValueError, AssertionError) as e:
            messagebox.showerror("Quantity Error", e)
            return
        response = requests.post(
            API_ENDPOINT + "update_portfolio", payload
        ).json()
        if response.get("error") is not None:
            messagebox.showerror("Buy Stock Error", response["error"])
        else:
            self._master._master.switch_frame(
                DashboardFrame, "PyStock | Dashboard", response
            )


class RootWindow(ThemedTk):
    """This class provides styled RootWindow (i.e. tk.Tk)"""

    def __init__(self, frame, title, theme="yaru", user_data=None):
        """
        Constructor for RootWindow

        Args:
            frame: Frame to be contained in window.
            title: Window title.
            theme: Overall theme.
            user_data: If it is not None, it is supplied in DashboardFrame
            Constructor.

        Returns:
            None
        """
        ThemedTk.__init__(self, theme=theme, background=True)
        self._frame = None
        self._user_data = None
        self._theme = theme
        if user_data is not None:
            self._frame = frame(self, user_data)
            self._user_data = user_data
        else:
            self._frame = frame(self)
        self._frame.grid(row=0, column=0)
        self.title(title)
        self.iconphoto(
            False, tk.PhotoImage(file=pathlib.Path("assets/icon.png"))
        )
        self.resizable(0, 0)

    def switch_frame(self, frame, title, user_data=None):
        """
        This function destroys current window and opens a new one with given
        frame.

        Args:
            frame: New frame,.
            title: Window title.
            user_data: If it is not None, it is supplied in DashboardFrame
            if new frame is DashboardFrame.
        """
        self.destroy()
        self.__init__(frame, title, self._theme, user_data)

    def change_theme(self, theme):
        """
        This function changes the current theme of whole window and it's
        children.

        Args:
            theme: New theme name.

        Returns:
            None
        """
        self._theme = theme
        self.set_theme(theme)

    def run(self):
        """
        This function runs RootWindow by calling it's mainloop.

        Args:
            None

        Returns:
            None
        """
        self.mainloop()
