from alpaca.trading.client import TradingClient
from alpaca.trading.requests import MarketOrderRequest
from alpaca.trading.enums import OrderSide, TimeInForce
from dotenv import load_dotenv
import os

load_dotenv()

tradingClient = TradingClient(os.getenv('ALPACA_API_KEY'), os.getenv('ALPACA_API_SECRET'))

orderData = MarketOrderRequest(
    symbol='SPY',
    qty=1,
    side=OrderSide.BUY,
    time_in_force=TimeInForce.DAY
)

marketOrder = tradingClient.submit_order(orderData)
print(marketOrder)