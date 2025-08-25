import os
import statistics

class OrderData:
    def __init__(self, price: float, amount: float):
        self.price = price
        self.amount = amount

    def __repr__(self):
        return f"OrderData(price={self.price}, amount={self.amount})"

class RatAnalyzer:
    def __init__(self, filename):
        self.filename = filename
        self.orders = []
        self._loaded = False

    def load_data(self):
        if not os.path.exists(self.filename):
            print(f"❌ 文件不存在：{self.filename}")
            return

        with open(self.filename, "r") as f:
            for line in f:
                try:
                    price_str, amount_str = line.strip().split(",")
                    price = float(price_str)
                    amount = float(amount_str)
                    self.orders.append(OrderData(price, amount))
                except ValueError:
                    continue

        if not self.orders:
            print("⚠️ 文件中没有有效数据")
            return

        # 按价格升序排序
        self.orders.sort(key=lambda x: x.price)
        self._loaded = True

    def get_total_amount(self):
        return sum(order.amount for order in self.orders) if self._loaded else None

    def get_average_price(self):
        return sum(order.price for order in self.orders) / len(self.orders) if self._loaded else None

    def get_median_price(self):
        prices = [order.price for order in self.orders]
        return statistics.median(prices) if self._loaded else None

    def get_percentile_price(self, percentile):
        if not self._loaded or not self.orders:
            return None
        index = int(len(self.orders) * percentile / 100)
        index = min(index, len(self.orders) - 1)
        return self.orders[index].price

    def print_all_deciles(self):
        if not self._loaded:
            print("⚠️ 数据尚未加载，请先调用 load_data()")
            return
        print("\n🔟 所有十分位数价格（TZS/USDT）：")
        for p in range(10, 100, 10):
            value = self.get_percentile_price(p)
            print(f"  - 第 {p} 百分位数：{value:.2f}")

    def print_summary(self):
        if not self._loaded:
            print("⚠️ 数据尚未加载，请先调用 load_data()")
            return

        trade_type = "买" if "BUY" in self.filename.upper() else "卖"
        print(f"\n📊 TZS兑USDT{trade_type}单统计结果：")
        print(f"🔢 总单量：{self.get_total_amount():.2f} USDT")
        print(f"📈 平均价格：{self.get_average_price():.2f} TZS/USDT")
        print(f"📊 中位数价格：{self.get_median_price():.2f} TZS/USDT")
        self.print_all_deciles()

if __name__ == '__main__':
    # analyzer = RatAnalyzer("TZS_USDT_202508252140_SELL.rat")
    analyzer = RatAnalyzer("LAK_USDT_202508252218_BUY.rat")
    analyzer.load_data()
    analyzer.print_summary()

    analyzer = RatAnalyzer("TZS_USDT_202508252216_SELL.rat")
    analyzer.load_data()
    analyzer.print_summary()
