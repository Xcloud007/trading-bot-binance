import typer
from bot.client import BinanceFuturesClient
from bot.logging_config import setup_logging

app = typer.Typer()
logger = setup_logging()

@app.command()
def trade(
    symbol: str = typer.Option(..., help="Trading symbol (e.g., BTCUSDT)"),
    side: str = typer.Option(..., help="BUY or SELL"),
    order_type: str = typer.Option(..., help="MARKET or LIMIT"),
    quantity: float = typer.Option(..., help="Order quantity"),
    price: float = typer.Option(None, help="Price (required for LIMIT orders)"),
):
    """
    Place a trading order on Binance Futures Testnet
    
    Example:
    python cli.py --symbol BTCUSDT --side BUY --order_type MARKET --quantity 0.001
    python cli.py --symbol ETHUSDT --side SELL --order_type LIMIT --quantity 0.1 --price 2000
    """
    
    logger.info("=" * 50)
    logger.info("ORDER REQUEST SUMMARY")
    logger.info("=" * 50)
    logger.info(f"Symbol: {symbol}")
    logger.info(f"Side: {side}")
    logger.info(f"Order Type: {order_type}")
    logger.info(f"Quantity: {quantity}")
    if order_type.upper() == "LIMIT":
        logger.info(f"Price: {price}")
    logger.info("=" * 50)
    
    try:
        client = BinanceFuturesClient()
        response = client.place_order(
            symbol=symbol,
            side=side,
            order_type=order_type,
            quantity=quantity,
            price=price
        )
        
        if response:
            logger.info("ORDER SUCCESSFUL!")
            logger.info("=" * 50)
            logger.info("ORDER RESPONSE DETAILS")
            logger.info("=" * 50)
            logger.info(f"Order ID: {response.get('orderId', 'N/A')}")
            logger.info(f"Status: {response.get('status', 'N/A')}")
            logger.info(f"Executed Qty: {response.get('executedQty', 'N/A')}")
            logger.info(f"Avg Price: {response.get('avgPrice', 'N/A')}")
            logger.info(f"Side: {response.get('side', 'N/A')}")
            logger.info(f"Type: {response.get('type', 'N/A')}")
            logger.info("=" * 50)
            logger.info("SUCCESS: Order placed successfully on Testnet")
        else:
            logger.error("FAILURE: Order could not be placed")
            
    except Exception as e:
        logger.error(f"FAILURE: {str(e)}")
        raise

if __name__ == "__main__":
    app()