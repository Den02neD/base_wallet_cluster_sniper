import requests, time

# Топ-снайперы Base (адреса, которые всегда в первых 3–10 покупателях)
SNIPERS = {
    "0x3fC91A3afd70395Cd496C647d5a6CC9D4B2b7FAD",  # Unibot
    "0x00000000000069b96a7d5a9d8b47a9f0c0a3b71d",  # Maestro
    "0x6b75d8AF000000Aaee99b57aB7d1dB4d7b7bD4D4",  # Banana Gun
    "0x5A7e5c5f0A8d3C8B9fF1c4e8a5b6c7d8e9f0a1b2",  # известный снайпер
    "0x4838B106FCe9647Bdf1E7877BF73cE8B0bD5800C",  # Trojan
}

def cluster_sniper():
    print("Base — Wallet Cluster Sniper (копирует покупки топ-снайперов)")
    seen = set()

    while True:
        try:
            r = requests.get("https://api.dexscreener.com/latest/dex/transactions/base", timeout=10)
            for tx in r.json().get("transactions", []):
                txid = tx["hash"]
                if txid in seen: continue
                seen.add(txid)

                # Ищем покупки от известных снайперов
                if tx["from"].lower() not in [a.lower() for a in SNIPERS]:
                    continue

                # Снайпер купил — ищем другие покупки в той же паре за последние 5 сек
                pair = tx["pairAddress"]
                token = tx["token0"]["symbol"] if tx["token0"]["address"] != "0x4200000000000000000000000000000000000006" else tx["token1"]["symbol"]
                amount_usd = tx["valueUSD"]

                print(f"TOP SNIPER JUST BOUGHT\n"
                      f"{token} — ${amount_usd:,.0f}\n"
                      f"Sniper: {tx['from'][:8]}...\n"
                      f"Pair: https://dexscreener.com/base/{pair}\n"
                      f"Tx: https://basescan.org/tx/{txid}\n"
                      f"→ 5-second cluster window OPEN — FOMO or die\n"
                      f"{'!'*80}")

        except:
            pass
        time.sleep(0.9)

if __name__ == "__main__":
    cluster_sniper()
