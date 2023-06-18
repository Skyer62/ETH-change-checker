import time

import requests


def get_eth_price():
    url = "https://api.binance.com/api/v3/ticker/price?symbol=ETHUSDT"
    response = requests.get(url)

    return float(response.json()["price"])


def get_btc_price():
    url = "https://api.binance.com/api/v3/ticker/price?symbol=BTCUSDT"
    response = requests.get(url)

    return float(response.json()["price"])


def calculate_changes(prices_eth, prices_btc):
    price_change_btc = (prices_btc[-1] - min(prices_btc)) / prices_btc[0] * 10000
    price_change_eth = (prices_eth[-1] - min(prices_eth)) / prices_eth[0] * 10000
    # Show actual price
    # print(f"Change eth: {price_change_eth:.2f}%")
    # print(f"Change btc: {price_change_btc:.2f}%")
    price_change_different = price_change_eth - price_change_btc
    if price_change_btc < price_change_eth and price_change_different > 0.7:
        if abs(price_change_eth) > 1:
            direction = "up" if price_change_eth > 0 else "down"
            print(
                f"Price of ETH has changed by {abs(price_change_eth):.2f}% {direction}"
            )
            prices_eth.clear()
            prices_btc.clear()


def main():
    update_rate = 5
    prices_eth = []
    prices_btc = []

    while True:
        eth_price = get_eth_price()
        prices_eth.append(eth_price)

        btc_price = get_btc_price()
        prices_btc.append(btc_price)

        calculate_changes(prices_eth, prices_btc)
        if len(prices_eth) > 3600 / update_rate:
            prices_eth.pop(0)
            prices_btc.pop(0)
        time.sleep(update_rate)


if __name__ == "__main__":
    main()
