from src.app.services.database import DatabaseManager
from src.database.orm import Configurations
from src.app.entity.tradepair import TradePairEntity


def get_configurations(db_manager: DatabaseManager):
    with db_manager as db:
        return db.get_last_record(entity=Configurations, order_by_field="created_at")


def parse_tradepair_response(response, txid=None):
    return TradePairEntity(
        txid=txid,
        txid_url=f"https://explorer.solana.com/tx/{txid}",
        amount_in=response["amountIn"],  #  Amount of Source Token (Solana)
        amount_out=response["amountOut"],  #  Amount Destination received
        min_amount_out=response[
            "minAmountOut"
        ],  # Min Amount  of destination token willing to receive
        current_price=response[
            "currentPrice"
        ],  # Current market price for the Token Pair
        execution_price=response[
            "executionPrice"
        ],  # The actual price the trade will be executed
        price_impact=response[
            "priceImpact"
        ],  # % of the Diff of current_price - execution price (Lack of Liquidity)
        fee=response["fee"],  # Trade fee charged for transaction
        platform_fee=response["platformFee"],  # Trade fee charged for transaction
        platform_fee_ui=response["platformFeeUI"],  # Trade fee charged for transaction
        base_currency=response["baseCurrency"][
            "mint"
        ],  # Fee charged by platform for the transaction
        quote_currency=response["quoteCurrency"]["mint"],  # Platform fee in SOL
        is_pump_fun=response["isPumpFun"],  # coin Amount
    )
