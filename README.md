# Crypto Arbitrage Trading Bot

A simulated cryptocurrency arbitrage trading bot for learning and testing trading strategies — no real money or API connections involved.

## Overview

This bot scans simulated prices across multiple cryptocurrency exchanges to identify and execute arbitrage opportunities: buying low on one exchange and selling high on another. It factors in trading fees, applies risk management rules, and tracks performance across all trades.

## Features

- **Multi-exchange simulation** — Binance, Coinbase, Kraken, and Bybit with realistic fee structures
- **8 cryptocurrencies monitored** — BTC, ETH, BNB, SOL, ADA, XRP, DOGE, MATIC
- **Realistic market simulation** — Exchange-specific price variations and live market drift per iteration
- **Fee-aware arbitrage detection** — Calculates net profit after all trading fees before executing
- **Risk management** — Limits each trade to 10% of available capital
- **Detailed reporting** — Per-trade breakdown and overall performance summary (ROI, success rate, avg profit)

## How It Works

1. Each iteration simulates a small market price movement (±0.5%) for all coins
2. The bot fetches simulated prices from all exchanges (each with its own price variation range)
3. It identifies the best buy/sell pair that exceeds the minimum profit threshold after fees
4. The trade is executed, capital is updated, and a detailed summary is printed
5. This repeats for the configured number of iterations

## Project Structure

```
main.py
├── Exchange        # Models an exchange with fees and price variation
├── ArbitrageBot    # Core bot logic: price scanning, trade execution, reporting
└── main()          # Entry point with bot configuration
```

## Usage

```bash
python main.py
```

To customise the simulation, edit the parameters in `main()`:

```python
bot = ArbitrageBot(initial_capital=10000)
bot.run(num_iterations=20, min_profit=1.0)
```

| Parameter | Description | Default |
|---|---|---|
| `initial_capital` | Starting capital in USD | `10000` |
| `num_iterations` | Number of trading cycles | `20` |
| `min_profit` | Minimum profit % to trigger a trade | `1.0` |

## Exchange Configuration

| Exchange | Trading Fee | Price Variation |
|---|---|---|
| Binance | 0.10% | ±1.5% |
| Coinbase | 0.50% | ±2.0% |
| Kraken | 0.26% | ±1.8% |
| Bybit | 0.10% | ±1.2% |

## Sample Output

```
ARBITRAGE TRADE EXECUTED - 2024-01-15 10:23:45
Coin Traded:        ETH
Quantity:           0.398123

BUY ORDER:
  Exchange:         Binance
  Price:            $2,489.50
  Fee:              $2.49

SELL ORDER:
  Exchange:         Coinbase
  Price:            $2,541.30
  Fee:              $12.71

RESULTS:
  Total Fees:       $6.03
  Net Profit/Loss:  $19.42 (+1.93%)
  Capital After:    $10,019.42
```

## Requirements

- Python 3.7+
- No external dependencies (uses only the standard library)

## Disclaimer

This project is a **simulation for educational purposes only**. It does not connect to any real exchange APIs and does not involve real funds. It is intended to demonstrate arbitrage concepts and trading bot architecture.
