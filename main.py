import time
import random
from datetime import datetime
from typing import Dict, List, Tuple, Optional


class Exchange:
    """Simulates a cryptocurrency exchange with realistic price variations"""
    
    def __init__(self, name: str, trading_fee: float, price_variation: float):
        self.name = name
        self.trading_fee = trading_fee  # Trading fee as percentage (e.g., 0.1 = 0.1%)
        self.price_variation = price_variation  # How much prices differ from base (0.01 = 1%)
    
    def get_price(self, coin: str, base_price: float) -> float:
        """
        Get simulated price with exchange-specific variation
        Each exchange has slightly different prices to create arbitrage opportunities
        """
        # Apply exchange-specific variation to base price
        variation = 1 + random.uniform(-self.price_variation, self.price_variation)
        return base_price * variation
    
    def calculate_fee(self, amount: float) -> float:
        """Calculate trading fee for a given amount"""
        return amount * (self.trading_fee / 100)


class ArbitrageBot:
    """Simulated arbitrage trading bot for learning and testing strategies"""
    
    def __init__(self, initial_capital: float = 10000):
        self.capital = initial_capital  # Starting trading capital
        
        # Initialize exchanges with realistic fee structures and price variations
        # Higher price_variation = more arbitrage opportunities
        self.exchanges = [
            Exchange("Binance", trading_fee=0.1, price_variation=0.015),   # ±1.5% variation
            Exchange("Coinbase", trading_fee=0.5, price_variation=0.02),   # ±2.0% variation
            Exchange("Kraken", trading_fee=0.26, price_variation=0.018),   # ±1.8% variation
            Exchange("Bybit", trading_fee=0.1, price_variation=0.012)      # ±1.2% variation
        ]
        
        # Base prices for different cryptocurrencies (simulated market prices)
        self.base_prices = {
            'BTC': 45000.0,
            'ETH': 2500.0,
            'BNB': 320.0,
            'SOL': 100.0,
            'ADA': 0.50,
            'XRP': 0.60,
            'DOGE': 0.08,
            'MATIC': 0.85
        }
        
        self.coins = list(self.base_prices.keys())
        
        # Trading history and performance tracking
        self.trades = []
        self.total_profit = 0
        self.successful_trades = 0
        self.failed_trades = 0
    
    def update_market_prices(self):
        """
        Simulate market price movements
        Prices fluctuate slightly each iteration to simulate real market conditions
        """
        for coin in self.base_prices:
            # Simulate market movement: ±0.5% per iteration
            market_change = random.uniform(-0.005, 0.005)
            self.base_prices[coin] *= (1 + market_change)
    
    def find_arbitrage_opportunity(self, min_profit_threshold: float = 1.0) -> Optional[Tuple]:
        """
        Scan all exchanges to find the most profitable arbitrage opportunity
        
        Strategy: Buy low on one exchange, sell high on another
        Returns: Trade details if profitable opportunity found, None otherwise
        """
        best_opportunity = None
        best_profit_pct = 0
        
        # Check each coin across all exchanges
        for coin in self.coins:
            base_price = self.base_prices[coin]
            prices = {}
            
            # Get current price from each exchange
            for exchange in self.exchanges:
                price = exchange.get_price(coin, base_price)
                prices[exchange.name] = {
                    'price': price,
                    'exchange': exchange
                }
            
            # Sort exchanges by price (lowest to highest)
            sorted_prices = sorted(prices.items(), key=lambda x: x[1]['price'])
            
            # Identify buy and sell exchanges
            buy_exchange = sorted_prices[0][1]['exchange']  # Lowest price
            sell_exchange = sorted_prices[-1][1]['exchange']  # Highest price
            buy_price = sorted_prices[0][1]['price']
            sell_price = sorted_prices[-1][1]['price']
            
            # Calculate fees for both transactions
            buy_fee = buy_exchange.calculate_fee(buy_price)
            sell_fee = sell_exchange.calculate_fee(sell_price)
            
            # Calculate net prices after fees
            net_buy_price = buy_price + buy_fee
            net_sell_price = sell_price - sell_fee
            
            # Calculate profit percentage after all costs
            profit_pct = ((net_sell_price - net_buy_price) / net_buy_price) * 100
            
            # Update best opportunity if this is more profitable
            if profit_pct > best_profit_pct and profit_pct >= min_profit_threshold:
                best_profit_pct = profit_pct
                best_opportunity = (
                    coin, buy_exchange, sell_exchange, 
                    buy_price, sell_price, profit_pct,
                    buy_fee, sell_fee
                )
        
        return best_opportunity
    
    def execute_trade(self, opportunity: Optional[Tuple]) -> Optional[Dict]:
        """
        Execute an arbitrage trade and update portfolio
        Simulates the complete buy/sell process with realistic calculations
        """
        if not opportunity:
            self.failed_trades += 1
            return None
            
        coin, buy_ex, sell_ex, buy_price, sell_price, profit_pct, buy_fee, sell_fee = opportunity
        
        # Risk management: Only use 10% of capital per trade
        trade_amount = self.capital * 0.1
        quantity = trade_amount / buy_price  # How many coins to buy
        
        # Calculate total costs and revenue
        total_buy_cost = (buy_price * quantity) + (buy_fee * quantity)
        total_sell_revenue = (sell_price * quantity) - (sell_fee * quantity)
        net_profit = total_sell_revenue - total_buy_cost
        
        # Update capital with profit/loss
        self.capital += net_profit
        self.total_profit += net_profit
        self.successful_trades += 1
        
        # Record trade details for reporting
        trade_record = {
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'coin': coin,
            'quantity': quantity,
            'buy_exchange': buy_ex.name,
            'sell_exchange': sell_ex.name,
            'buy_price': buy_price,
            'sell_price': sell_price,
            'buy_fee': buy_fee * quantity,
            'sell_fee': sell_fee * quantity,
            'total_fees': (buy_fee + sell_fee) * quantity,
            'net_profit': net_profit,
            'profit_pct': profit_pct,
            'capital_after': self.capital
        }
        
        self.trades.append(trade_record)
        return trade_record
    
    def print_trade_summary(self, trade: Optional[Dict]):
        """Display detailed information about a completed trade"""
        if not trade:
            print("⚠️  No profitable arbitrage opportunity found (below threshold).\n")
            return
            
        print("=" * 80)
        print(f"✅ ARBITRAGE TRADE EXECUTED - {trade['timestamp']}")
        print("=" * 80)
        print(f"Coin Traded:        {trade['coin']}")
        print(f"Quantity:           {trade['quantity']:.6f}")
        print(f"\n📉 BUY ORDER:")
        print(f"  Exchange:         {trade['buy_exchange']}")
        print(f"  Price:            ${trade['buy_price']:,.2f}")
        print(f"  Fee:              ${trade['buy_fee']:,.2f}")
        print(f"  Total Cost:       ${(trade['buy_price'] * trade['quantity'] + trade['buy_fee']):,.2f}")
        print(f"\n📈 SELL ORDER:")
        print(f"  Exchange:         {trade['sell_exchange']}")
        print(f"  Price:            ${trade['sell_price']:,.2f}")
        print(f"  Fee:              ${trade['sell_fee']:,.2f}")
        print(f"  Total Revenue:    ${(trade['sell_price'] * trade['quantity'] - trade['sell_fee']):,.2f}")
        print(f"\n💰 RESULTS:")
        print(f"  Total Fees:       ${trade['total_fees']:,.2f}")
        print(f"  Net Profit/Loss:  ${trade['net_profit']:,.2f} ({trade['profit_pct']:+.2f}%)")
        print(f"  Capital After:    ${trade['capital_after']:,.2f}")
        print("=" * 80)
        print()
    
    def print_overall_summary(self):
        """Display overall trading performance statistics"""
        print("\n" + "=" * 80)
        print("📊 OVERALL TRADING SUMMARY")
        print("=" * 80)
        print(f"Total Iterations:   {self.successful_trades + self.failed_trades}")
        print(f"Successful Trades:  {self.successful_trades}")
        print(f"Missed Opportunities: {self.failed_trades}")
        print(f"Success Rate:       {(self.successful_trades / (self.successful_trades + self.failed_trades) * 100):.1f}%")
        print(f"\nTotal Profit/Loss:  ${self.total_profit:,.2f}")
        print(f"Final Capital:      ${self.capital:,.2f}")
        
        if self.capital - self.total_profit > 0:
            roi = (self.total_profit / (self.capital - self.total_profit)) * 100
            print(f"ROI:                {roi:+.2f}%")
        
        if self.successful_trades > 0:
            avg_profit = self.total_profit / self.successful_trades
            print(f"Avg Profit/Trade:   ${avg_profit:,.2f}")
        
        print("=" * 80)
    
    def run(self, num_iterations: int = 20, min_profit: float = 1.0):
        """
        Run the simulated arbitrage bot
        
        Args:
            num_iterations: Number of trading cycles to execute
            min_profit: Minimum profit percentage required to execute trade (e.g., 1.0 = 1%)
        """
        print("=" * 80)
        print("🤖 CRYPTO ARBITRAGE TRADING BOT (SIMULATION MODE)")
        print("=" * 80)
        print(f"💵 Initial Capital:  ${self.capital:,.2f}")
        print(f"📊 Min Profit:       {min_profit}%")
        print(f"🔄 Iterations:       {num_iterations}")
        print(f"📈 Coins Monitored:  {', '.join(self.coins)}")
        print(f"🏦 Exchanges:        {', '.join([ex.name for ex in self.exchanges])}")
        print("=" * 80)
        print()
        
        print("🔍 Starting arbitrage detection...\n")
        
        # Main trading loop
        for i in range(num_iterations):
            print(f"{'─' * 80}")
            print(f"⏱️  Iteration {i+1}/{num_iterations}")
            print(f"{'─' * 80}")
            
            # Simulate market price changes
            self.update_market_prices()
            
            # Find and execute arbitrage opportunity
            opportunity = self.find_arbitrage_opportunity(min_profit)
            trade = self.execute_trade(opportunity)
            self.print_trade_summary(trade)
            
            # Delay between trades (simulate real trading pace)
            time.sleep(1)
        
        # Display final performance summary
        self.print_overall_summary()


# ===== MAIN EXECUTION =====
def main():
    """Main entry point for the arbitrage bot"""
    print("\n" + "=" * 80)
    print("CRYPTO ARBITRAGE TRADING BOT - SIMULATION MODE")
    print("=" * 80)
    print("\n📝 ABOUT:")
    print("   This bot simulates cryptocurrency arbitrage trading across")
    print("   multiple exchanges. It uses realistic price variations and")
    print("   trading fees to demonstrate arbitrage opportunities.")
    print("\n✨ FEATURES:")
    print("   • Simulates 4 major exchanges (Binance, Coinbase, Kraken, Bybit)")
    print("   • Monitors 8 different cryptocurrencies")
    print("   • Realistic price movements and trading fees")
    print("   • Detailed trade reports and performance analytics")
    print("\n⚠️  NOTE:")
    print("   This is a SIMULATION for learning purposes.")
    print("   No real money or API connections are involved.")
    print("=" * 80)
    print()
    
    # Initialize bot with $10,000 starting capital
    bot = ArbitrageBot(initial_capital=10000)
    
    # Run 20 trading iterations with 1% minimum profit threshold
    bot.run(num_iterations=20, min_profit=1.0)


if __name__ == "__main__":
    main()