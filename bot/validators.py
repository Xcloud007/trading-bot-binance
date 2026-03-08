from bot.logging_config import setup_logging

logger = setup_logging()

def validate_symbol(symbol: str) -> bool:
    """Validate trading symbol format"""
    if not symbol:
        logger.error("Symbol cannot be empty")
        return False
    if not symbol.endswith("USDT"):
        logger.warning(f"Symbol {symbol} may not be a USDT pair")
    return True

def validate_side(side: str) -> bool:
    """Validate order side"""
    valid_sides = ["BUY", "SELL"]
    if side.upper() not in valid_sides:
        logger.error(f"Invalid side: {side}. Must be BUY or SELL")
        return False
    return True

def validate_order_type(order_type: str) -> bool:
    """Validate order type"""
    valid_types = ["MARKET", "LIMIT"]
    if order_type.upper() not in valid_types:
        logger.error(f"Invalid order type: {order_type}. Must be MARKET or LIMIT")
        return False
    return True

def validate_quantity(quantity: float) -> bool:
    """Validate order quantity"""
    if quantity <= 0:
        logger.error("Quantity must be greater than 0")
        return False
    return True

def validate_price(price: float, order_type: str) -> bool:
    """Validate price for LIMIT orders"""
    if order_type.upper() == "LIMIT" and price <= 0:
        logger.error("Price must be greater than 0 for LIMIT orders")
        return False
    return True