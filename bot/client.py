import requests
import hmac
import hashlib
import time
import os
from dotenv import load_dotenv
from bot.logging_config import setup_logging
from bot.validators import validate_symbol, validate_side, validate_order_type, validate_quantity, validate_price

# Load .env file FIRST
load_dotenv()

logger = setup_logging()

class BinanceFuturesClient:
    def __init__(self):
        self.api_key = os.getenv("BINANCE_API_KEY")
        self.secret_key = os.getenv("BINANCE_SECRET_KEY")
        self.base_url = os.getenv("BINANCE_TESTNET_URL", "https://testnet.binancefuture.com")
        
        # Check credentials ONCE at initialization
        if not self.api_key or not self.secret_key:
            logger.error("API credentials not found in .env file")
            logger.error(f"API Key: {self.api_key}")
            logger.error(f"Secret Key: {self.secret_key}")
            raise ValueError("Missing API credentials")
        
        logger.info("Binance Futures Testnet client initialized")

    def _generate_signature(self, params):
        """Generate HMAC signature for API request"""
        query_string = '&'.join([f"{k}={v}" for k, v in params.items()])
        signature = hmac.new(
            self.secret_key.encode('utf-8'),
            query_string.encode('utf-8'),
            hashlib.sha256
        ).hexdigest()
        return signature

    def place_order(self, symbol: str, side: str, order_type: str, quantity: float, price: float = None):
        """Place a market or limit order on Binance Futures Testnet"""
        
        # Validate inputs
        if not validate_symbol(symbol):
            return None
        if not validate_side(side):
            return None
        if not validate_order_type(order_type):
            return None
        if not validate_quantity(quantity):
            return None
        if not validate_price(price, order_type):
            return None
        
        try:
            logger.info(f"Placing {order_type} {side} order for {symbol} qty: {quantity}")
            
            # Prepare order parameters
            params = {
                "symbol": symbol,
                "side": side.upper(),
                "type": order_type.upper(),
                "quantity": quantity,
                "newOrderRespType": "FULL"
            }
            
            # Add price for LIMIT orders
            if order_type.upper() == "LIMIT" and price:
                params["price"] = price
            
            # Add timestamp
            params["timestamp"] = int(time.time() * 1000)
            
            # Generate signature
            params["signature"] = self._generate_signature(params)
            
            # Make API request
            response = requests.post(
                f"{self.base_url}/fapi/v1/order",
                params=params,
                headers={"X-MBX-APIKEY": self.api_key}
            )
            
            result = response.json()
            logger.info(f"Order Response: {result}")
            return result

        except Exception as e:
            logger.error(f"API Error: {str(e)}")
            raise