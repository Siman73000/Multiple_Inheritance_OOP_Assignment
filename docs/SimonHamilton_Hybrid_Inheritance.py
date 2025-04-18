# This script demonstrates hybrid inheritance in Python through a stock trading application.
import tkinter as tk # This line imports the tkinter package for creating GUI applications.
from tkinter import messagebox # This line imports the messagebox module from tkinter for displaying message boxes.
class MarketEntity: # This defines a new class called MarketEntity.
    def __init__(self, symbol, price): # This is the constructor method that initializes the class.
        self.symbol = symbol # This line sets the symbol of the market entity.
        self.price = price # This line sets the price of the market entity.
class Tradable: # This defines a new class called Tradable.
    def buy(self, portfolio, qty): # This method allows buying a quantity of the tradable entity.
        cost = self.price * qty # This line calculates the cost of buying the quantity.
        if portfolio.cash_balance < cost: # This line checks if there is enough cash in the portfolio.
            raise ValueError(f"Not enough cash (${portfolio.cash_balance:.2f}) to buy {qty} of {self.symbol} (cost ${cost:.2f}).") # This line raises an error if there is not enough cash.
        portfolio.cash_balance -= cost # This line deducts the cost from the cash balance.
        portfolio.add_position(self.symbol, qty) # This line adds the position to the portfolio.
    def sell(self, portfolio, qty): # This method allows selling a quantity of the tradable entity.
        revenue = self.price * qty # This line calculates the revenue from selling the quantity.
        portfolio.remove_position(self.symbol, qty) # This line removes the position from the portfolio.
        portfolio.cash_balance += revenue # This line adds the revenue to the cash balance.
class DividendPaying: # This defines a new class called DividendPaying.
    def calculate_dividend(self, qty):  # This method calculates the dividend for a given quantity.
        return qty * self.price * self.dividend_yield # This line calculates the dividend based on the quantity, price, and dividend yield.
class Stock(MarketEntity, Tradable, DividendPaying): # This defines a new class called Stock that inherits from MarketEntity, Tradable, and DividendPaying. This is the first instance of hybrid inheritance.
    def __init__(self, symbol, price, dividend_yield=0.0): # This is the constructor method that initializes the class.
        MarketEntity.__init__(self, symbol, price) # This line initializes the MarketEntity class.
        self.dividend_yield = dividend_yield # This line sets the dividend yield of the stock.
class CommonStock(Stock): # This defines a new class called CommonStock that inherits from Stock.
    pass # This line does not add any new functionality to the Stock class.
class PreferredStock(Stock): # This defines a new class called PreferredStock that inherits from Stock.
    def calculate_dividend(self, qty): # This method overrides the calculate_dividend method from the Stock class.
        print(f"[{self.symbol}] Preferred dividend calc:") # This line prints a message indicating that the preferred dividend calculation is being performed.
        return super().calculate_dividend(qty) # This line calls the calculate_dividend method from the Stock class.
class Portfolio: # This defines a new class called Portfolio.
    def __init__(self, initial_cash=10_000.0): # This is the constructor method that initializes the class.
        self.holdings = {} # This line initializes an empty dictionary to hold the portfolio's holdings.
        self.cash_balance = initial_cash # This line sets the initial cash balance of the portfolio.
    def add_position(self, symbol, qty): # This method adds a position to the portfolio.
        self.holdings[symbol] = self.holdings.get(symbol, 0) + qty # This line updates the holdings dictionary with the new quantity.
    def remove_position(self, symbol, qty): # This method removes a position from the portfolio.
        current = self.holdings.get(symbol, 0) # This line gets the current quantity of the symbol in the holdings.
        if qty > current: # This line checks if the quantity to sell is greater than the current quantity.
            raise ValueError(f"Not enough {symbol} to sell (have {current}).") # This line raises an error if there is not enough quantity to sell.
        self.holdings[symbol] = current - qty # This line updates the holdings dictionary with the new quantity.
    def view_positions(self): # This method returns the current positions in the portfolio.
        return dict(self.holdings) # This line returns a copy of the holdings dictionary.
    def deposit_cash(self, amount): # This method allows depositing cash into the portfolio.
        if amount <= 0: # This line checks if the deposit amount is positive.
            raise ValueError("Deposit must be positive.") # This line raises an error if the deposit amount is not positive.
        self.cash_balance += amount # This line adds the deposit amount to the cash balance.
    def display_cash(self): # This method returns the current cash balance of the portfolio.
        return self.cash_balance # This line returns the cash balance.
    def collect_dividends(self, market_map): # This method collects dividends from the holdings in the portfolio.
        total = 0.0 # This line initializes a variable to hold the total dividends collected.
        for sym, qty in self.holdings.items(): # This line iterates over the holdings in the portfolio.
            entity = market_map.get(sym) # This line gets the market entity from the market map.
            if isinstance(entity, DividendPaying): # This line checks if the entity is a dividend-paying stock.
                div = entity.calculate_dividend(qty) # This line calculates the dividend for the quantity held.
                total += div # This line adds the dividend to the total.
        self.cash_balance += total # This line adds the total dividends collected to the cash balance.
        return total # This line returns the total dividends collected.
class AnalyticsMixin: # This defines a new class called AnalyticsMixin.
    def total_value(self, market_map): # This method calculates the total value of the portfolio.
        return sum( # This line initializes a variable to hold the total value.
            market_map[s].price * q # This line calculates the total value of the holdings.
            for s, q in self.holdings.items() # This line iterates over the holdings in the portfolio.
            if s in market_map # This line checks if the symbol is in the market map.
        ) # Termination of the sum function.
class BasicPortfolio(Portfolio): # This defines a new class called BasicPortfolio that inherits from Portfolio.
    pass # This line does not add any new functionality to the Portfolio class.
class AdvancedPortfolio(BasicPortfolio, AnalyticsMixin): # This defines a new class called AdvancedPortfolio that inherits from BasicPortfolio and AnalyticsMixin, demonstrating multiple inheritance.
    pass # This line does not add any new functionality to the BasicPortfolio class.
class PremiumPortfolio(AdvancedPortfolio): # This defines a new class called PremiumPortfolio that inherits from AdvancedPortfolio.
    def risk_assessment(self, market_map): # This method assesses the risk of the portfolio.
        total = self.total_value(market_map) + self.cash_balance # This line calculates the total value of the portfolio including cash.
        if total == 0: # This line checks if the total value is zero.
            return "N/A" # This line returns "N/A" if the total value is zero.
        pref_value = sum( # This line initializes a variable to hold the total value of preferred stocks.
            market_map[s].price * q # This line calculates the total value of the preferred stocks.
            for s, q in self.holdings.items() # This line iterates over the holdings in the portfolio.
            if isinstance(market_map[s], PreferredStock) # This line checks if the entity is a preferred stock.
        ) # Termination of the sum function.
        pct = (pref_value / total) * 100 # This line calculates the percentage of preferred stocks in the portfolio.
        return f"{pct:.1f}% preferred holdings" # This line returns the percentage of preferred stocks in the portfolio formatted to one decimal place.
class StockApp(tk.Tk): # This defines a new class called StockApp that inherits from tk.Tk, which is the main window class in tkinter.
    def __init__(self, market_map, portfolio): # This is the constructor method that initializes the class.
        super().__init__() # This line initializes the parent class (tk.Tk).
        self.title("Hybrid Inheritance Stock App") # This line sets the title of the window.
        self.market_map = market_map # This line sets the market map for the application.
        self.portfolio = portfolio # This line sets the portfolio for the application.
        self._build_ui() # This line calls the method to build the user interface.
    def _build_ui(self): # This method builds the user interface for the application.
        tk.Label(self, text="Market Symbols:").grid(row=0, column=0) # This line creates a label for the market symbols.
        self.lst = tk.Listbox(self, height=6) # This line creates a listbox to display the market symbols.
        for sym in self.market_map: # This line iterates over the market map.
            self.lst.insert(tk.END, sym) # This line inserts the market symbols into the listbox.
        self.lst.grid(row=1, column=0, rowspan=6, padx=5, pady=5) # This line places the listbox in the grid.
        tk.Label(self, text="Qty / Amt:").grid(row=0, column=1) # This line creates a label for the quantity or amount.
        self.qty = tk.Entry(self) # This line creates an entry field for the quantity or amount.
        self.qty.grid(row=1, column=1, padx=5) # This line places the entry field in the grid.
        tk.Button(self, text="Buy",  command=self._buy).grid(row=2, column=1, sticky="we")  # This line creates a button to buy stocks.
        tk.Button(self, text="Sell", command=self._sell).grid(row=3, column=1, sticky="we") # This line creates a button to sell stocks.
        tk.Button(self, text="Deposit Cash", command=self._deposit_cash).grid(row=4, column=1, sticky="we", pady=(5,0)) # This line creates a button to deposit cash.
        tk.Button(self, text="Show Cash",    command=self._show_cash)   .grid(row=5, column=1, sticky="we") # This line creates a button to show the cash balance.
        # The line below creates a button to collect dividends.
        tk.Button(self, text="Collect Dividends", command=self._collect_dividends)\
            .grid(row=6, column=1, sticky="we", pady=(5,0)) # This line creates a button to collect dividends.
        # The line below creates buttons to view the portfolio, total value, and risk assessment.
        tk.Button(self, text="View Portfolio",    command=self._show_portfolio)\
            .grid(row=7, column=0, columnspan=2, sticky="we", pady=(10,0)) # This line creates a button to view the portfolio.
        # The line below creates a button to show the total value of the portfolio.
        tk.Button(self, text="Total Value",       command=self._show_value) \
            .grid(row=8, column=0, columnspan=2, sticky="we") # This line creates a button to show the total value of the portfolio.
        # The line below creates a button to show the risk assessment of the portfolio.
        tk.Button(self, text="Risk Assessment",   command=self._show_risk)\
            .grid(row=9, column=0, columnspan=2, sticky="we") # This line creates a button to show the risk assessment of the portfolio.
        self.output = tk.Text(self, height=10) # This line creates a text area to display output messages.
        self.output.grid(row=1, column=2, rowspan=9, padx=5, pady=5) # This line places the text area in the grid.
    def _get_qty(self): # This method retrieves the quantity or amount entered by the user.
        val = self.qty.get() # This line gets the value from the entry field.
        try: # This line attempts to convert the value to a number.
            if "." in val: # This line checks if the value contains a decimal point.
                n = float(val) # This line converts the value to a float.
            else: # This line checks if the value does not contain a decimal point.
                n = int(val) # This line converts the value to an integer.
            if n <= 0: # This line checks if the value is less than or equal to zero.
                raise ValueError ("Must be positive") # This line raises an error if the value is not positive.
            return n # This line returns the converted value.
        except: # This line handles any exceptions that occur during the conversion.
            messagebox.showerror("Invalid", "Enter a positive number") # This line shows an error message if the conversion fails.
            return None # This line returns None if the conversion fails.
    def _buy(self): # This method handles the buying of stocks.
        q = self._get_qty() # This line retrieves the quantity or amount entered by the user.
        if q is None: return # This line checks if the quantity is None.
        sym = self.lst.get(tk.ACTIVE) # This line gets the selected market symbol from the listbox.
        try: # This line attempts to buy the stock.
            self.market_map[sym].buy(self.portfolio, q) # This line calls the buy method of the selected stock.
            self._log(f"Bought {q} of {sym}") # This line logs the purchase.
        except Exception as e: # This line handles any exceptions that occur during the purchase.
            messagebox.showerror("Error", str(e)) # This line shows an error message if the purchase fails.
    def _sell(self): # This method handles the selling of stocks.
        q = self._get_qty() # This line retrieves the quantity or amount entered by the user.
        if q is None: return # This line checks if the quantity is None.
        sym = self.lst.get(tk.ACTIVE) # This line gets the selected market symbol from the listbox.
        try: # This line attempts to sell the stock.
            self.market_map[sym].sell(self.portfolio, q) # This line calls the sell method of the selected stock.
            self._log(f"Sold {q} of {sym}") # This line logs the sale.
        except Exception as e: # This line handles any exceptions that occur during the sale.
            messagebox.showerror("Error", str(e)) # This line shows an error message if the sale fails.
    def _deposit_cash(self): # This method handles the depositing of cash into the portfolio.
        amt = self._get_qty() # This line retrieves the quantity or amount entered by the user.
        if amt is None: return # This line checks if the amount is None.
        try: # This line attempts to deposit the cash.
            self.portfolio.deposit_cash(amt) # This line calls the deposit_cash method of the portfolio.
            self._log(f"Deposited cash: ${amt:.2f}") # This line logs the deposit. 
        except Exception as e: # This line handles any exceptions that occur during the deposit.
            messagebox.showerror("Error", str(e)) # This line shows an error message if the deposit fails.
    def _show_cash(self): # This method handles the displaying of the cash balance.
        cb = self.portfolio.display_cash() # This line retrieves the cash balance from the portfolio.
        self._log(f"Cash balance: ${cb:,.2f}") # This line logs the cash balance.
    def _collect_dividends(self): # This method handles the collecting of dividends from the portfolio.
        total = self.portfolio.collect_dividends(self.market_map) # This line collects dividends from the portfolio.
        self._log(f"Collected dividends: ${total:.2f}") # This line logs the total dividends collected.
    def _show_portfolio(self): # This method handles the displaying of the portfolio.
        pos = self.portfolio.view_positions() # This line retrieves the current positions in the portfolio.
        self._log(f"Holdings: {pos}") # This line logs the current positions in the portfolio.
    def _show_value(self): # This method handles the displaying of the total value of the portfolio.
        val = self.portfolio.total_value(self.market_map) # This line calculates the total value of the portfolio.
        self._log(f"Total portfolio value (excl. cash): ${val:,.2f}") # This line logs the total value of the portfolio.
    def _show_risk(self): # This method handles the displaying of the risk assessment of the portfolio.
        r = self.portfolio.risk_assessment(self.market_map) # This line assesses the risk of the portfolio.
        self._log(f"Risk assessment: {r}") # This line logs the risk assessment of the portfolio.
    def _log(self, msg): # This method handles logging messages to the output text area.
        self.output.insert(tk.END, msg + "\n") # This line inserts the message into the text area.
        self.output.see(tk.END) # This line scrolls the text area to the end to show the latest message.
if __name__ == "__main__": # This line checks if the script is being run directly (not imported as a module).
    market_map = { # This line initializes a dictionary to hold the market entities.
        "AAPL": CommonStock("AAPL", 150.0, dividend_yield=0.006), # This line creates a CommonStock object for Apple Inc.
        "GOOG": CommonStock("GOOG", 2800.0, dividend_yield=0.0), # This line creates a CommonStock object for Alphabet Inc.
        "PREF": PreferredStock("PREF", 100.0, dividend_yield=0.05), # This line creates a PreferredStock object.
    } # Termination point for the market_map dictionary.
    portfolio = PremiumPortfolio(initial_cash=20_000.0) # This line creates a PremiumPortfolio object with an initial cash balance.
    app = StockApp(market_map, portfolio) # This line creates an instance of the StockApp class.
    app.geometry("800x500") # This line sets the size of the window.
    app.mainloop() # This line starts the main event loop of the tkinter application.