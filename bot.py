import os
from binance.client import Client

MESSAGES = {
    "help": "Commands are:\n"
    "balance - shows your account balance\n"
    "trade - create a transaction on the exchange\n"
    "setcurrency - change trading currency of the bot. Example: setcurrency BNBBTC\n"
    "showpair - shows your current pair"
}

TRADE_COMMAND = "trade"
BALANCE_COMMAND = "balance"
SET_CURRENCY_COMMAND = "setcurrency"
HELP_COMMAND = "help"
SHOW_PAIR_COMMAND = "showpair"

GLOBAL_CONFIG = {
    "TRADING_PAIR": "BNBBTC"
}


def main():
    action, arg_1 = get_command()

    if action == TRADE_COMMAND:
        trade()
    elif action == BALANCE_COMMAND:
        get_balance()
    elif action == SHOW_PAIR_COMMAND:
        print("Current pair is", GLOBAL_CONFIG["TRADING_PAIR"])
    elif action == SET_CURRENCY_COMMAND:
        set_currency(arg_1)
    elif action == HELP_COMMAND:
        print(MESSAGES["help"])
    else:
        print("Invalid option")


def get_command():
    command = str(input("Command: ")).split()

    try:
        action = command[0]
    except IndexError:
        action = None

    try:
        arg_1 = command[1]
    except IndexError:
        arg_1 = None

    return action, arg_1


def trade():
    print("To buy or sell, type the action and amount. Example: buy 100, sell 300\n")
    command = str(input("type the operation and amount: ")).split()

    """It must always have 2 args"""
    if len(command) != 2:
        return 0

    operation = command[0]
    amount = float(command[1])

    try:
        if operation == "buy":
            order = client.order_market_buy(
                symbol=GLOBAL_CONFIG["TRADING_PAIR"],
                quantity=amount
            )
        elif operation == "sell":
            order = client.order_market_sell(
                symbol=GLOBAL_CONFIG["TRADING_PAIR"],
                quantity=amount
            )
        else:
            print("Invalid operation")
            return 0

        print("Success\n")
        print(order)
        return 1
    except Exception as e:
        print(e)


def get_balance():
    balances = client.get_account().get("balances")
    positive_balances = [balance for balance in balances if
                         float(balance["free"]) > 0 or float(balance["locked"]) > 0]
    for balance in positive_balances:
        print(balance)
    print("\n")


def get_valid_currencies():
    tickers = client.get_all_tickers()
    valid_currencies = [ticker["symbol"] for ticker in tickers]
    return valid_currencies


def set_currency(pair):
    if pair:
        pair = str(pair).upper()

    if pair not in get_valid_currencies():
        print("Please, choose a valid currency.")
    else:
        print("Pair %s set" % pair)
        GLOBAL_CONFIG["TRADING_PAIR"] = pair


if __name__ == '__main__':
    binance_key = os.environ.get("BINANCE_KEY")
    binance_secret = os.environ.get("BINANCE_SECRET")

    client = Client(binance_key, binance_secret, {"verify": False, "timeout": 20})

    print("Welcome to the simple trader!")
    print("What do you want to do?")
    print("Type help to see all commands\n")

    while True:
        if not binance_key or not binance_secret:
            print("Credentials were not found. Please, insert it")
            binance_key = input("BINANCE_KEY: ")
            binance_secret = input("BINANCE_SECRET: ")
        try:
            main()
        except KeyboardInterrupt:
            break
        except:
            print("Something went wrong.. Please, check your credentials again")
