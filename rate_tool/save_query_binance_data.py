import requests
import json
import statistics
import datetime
from time import sleep
import os


def save_sell_orders_to_file(fiat, asset, trade_type):
    url = "https://c2c.binance.com/bapi/c2c/v2/friendly/c2c/adv/search"
    headers = {
        "Content-Type": "application/json"
    }

    page = 1
    rows = 20
    records = []

    while True:
        payload = {
            "page": page,
            "rows": rows,
            "payTypes": [],
            "asset": asset,
            "fiat": fiat,
            "tradeType": trade_type
        }

        response = requests.post(url, headers=headers, data=json.dumps(payload))
        if response.status_code != 200:
            print(f"❌ 请求失败，状态码：{response.status_code}")
            break

        data = response.json().get("data", [])
        if not data:
            break

        for ad in data:
            adv = ad["adv"]
            price = float(adv["price"])
            amount = float(adv["surplusAmount"])
            records.append((price, amount))
        sleep(1)

        page += 1

    # 生成文件名
    timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M")
    filename = f"{fiat}_{asset}_{timestamp}_{trade_type}.rat"

    # 保存到文件
    with open(filename, "w") as f:
        for price, amount in records:
            f.write(f"{price},{amount}\n")

    print(f"✅ 数据已保存到文件：{filename}")
    return filename


if __name__ == '__main__':
    # 爬取数据, 不要频繁调用, 防止封IP
    filename = save_sell_orders_to_file(fiat="LAK", asset="USDT", trade_type="BUY")
