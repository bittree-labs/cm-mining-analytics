"""Mining Portfolio 行情快报 — 拉取 + 异动检测 + Telegram推送"""
import urllib.request, json, sys, os

def api(url):
    req = urllib.request.Request(url, headers={"User-Agent": "MiningBot/1.0"})
    return json.loads(urllib.request.urlopen(req, timeout=20).read())

def send_tg(text):
    token = "8964342406:AAEcWUH8ChXsAPGvS_PuIw9_EtEIKVPO2vI"
    chat = "478575303"
    body = json.dumps({"chat_id": chat, "text": text, "parse_mode": "HTML", "disable_web_page_preview": True}).encode()
    req = urllib.request.Request("https://api.telegram.org/bot%s/sendMessage" % token, data=body, headers={"Content-Type": "application/json"})
    urllib.request.urlopen(req, timeout=10)

def fmt(n):
    if abs(n) >= 1e9: return "$%.2fB" % (n/1e9)
    if abs(n) >= 1e6: return "$%.2fM" % (n/1e6)
    if abs(n) >= 1e3: return "$%.0fK" % (n/1e3)
    return "$%.0f" % n

print("Mining Portfolio 行情快报")
print("=" * 60)

# POW 类别
try:
    pow_data = api("https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&category=proof-of-work-pow&order=market_cap_desc&per_page=50&page=1&sparkline=false&price_change_percentage=24h,7d,30d")
    print("PoW: %d coins" % len(pow_data))
except Exception as e:
    print("PoW API fail: %s" % e)
    pow_data = []

# Storage 类别
try:
    storage_data = api("https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&category=storage&order=market_cap_desc&per_page=30&page=1&sparkline=false&price_change_percentage=24h,7d,30d")
    print("Storage: %d coins" % len(storage_data))
except Exception as e:
    print("Storage API fail: %s" % e)
    storage_data = []

# 合并去重
seen = set()
all_coins = []
for c in pow_data + storage_data:
    if c["id"] not in seen:
        seen.add(c["id"])
        all_coins.append(c)

all_coins.sort(key=lambda x: x.get("market_cap", 0) or 0, reverse=True)

# 异动检测
alerts_24h = []
alerts_7d = []

for c in all_coins[:30]:
    chg24 = c.get("price_change_percentage_24h_in_currency") or 0
    chg7d = c.get("price_change_percentage_7d_in_currency") or 0
    mcap = c.get("market_cap", 0) or 0
    if abs(chg24) > 10 and mcap > 1e6:
        alerts_24h.append((c["name"], c["symbol"].upper(), chg24, mcap))
    if abs(chg7d) > 25 and mcap > 1e6:
        alerts_7d.append((c["name"], c["symbol"].upper(), chg7d, mcap))

# 输出 Top 15
print("\n%-4s %-20s %-7s %12s %10s %7s %7s" % ("#", "Name", "Sym", "MCap", "Price", "24h%", "7d%"))
print("-" * 65)
for i, c in enumerate(all_coins[:15], 1):
    name = c["name"][:19]
    sym = c["symbol"].upper()[:6]
    mcap = c.get("market_cap", 0) or 0
    price = c.get("current_price", 0) or 0
    chg24 = c.get("price_change_percentage_24h_in_currency") or 0
    chg7d = c.get("price_change_percentage_7d_in_currency") or 0
    flag = " !" if abs(chg24) > 10 else ""
    print("%-4d %-20s %-7s %12s %10s %+6.1f%% %+6.1f%%%s" % (i, name, sym, fmt(mcap), "$%.4f" % price, chg24, chg7d, flag))

# Telegram 汇总
if alerts_24h or alerts_7d:
    lines = ["Mining Portfolio 异动告警\n"]
    if alerts_24h:
        lines.append("<b>24h 涨跌 > 10%:</b>")
        for name, sym, chg, mcap in alerts_24h[:8]:
            lines.append("  %s (%s): %+.1f%%  [%s]" % (name, sym, chg, fmt(mcap)))
    if alerts_7d:
        lines.append("\n<b>7d 涨跌 > 25%:</b>")
        for name, sym, chg, mcap in alerts_7d[:8]:
            lines.append("  %s (%s): %+.1f%%  [%s]" % (name, sym, chg, fmt(mcap)))
    msg = "\n".join(lines)
    try:
        send_tg(msg)
        print("\nTelegram 已推送 %d 条异动" % (len(alerts_24h)+len(alerts_7d)))
    except Exception as e:
        print("\nTelegram 推送失败: %s" % e)
else:
    print("\n无显著异动")

# 保存配置
config = {
    "name": "Mining Portfolio Monitor",
    "updated": "2026-08-04",
    "categories": ["proof-of-work-pow", "storage"],
    "coin_ids": [c["id"] for c in all_coins],
    "total": len(all_coins),
    "alert_thresholds": {"24h_pct": 10, "7d_pct": 25}
}
with open("/Users/bittree/mining_portfolio.json", "w") as f:
    json.dump(config, f, indent=2)
print("已保存: mining_portfolio.json (%d coins)" % len(all_coins))
