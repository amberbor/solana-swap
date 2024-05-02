import asyncio
from dataclasses import dataclass
from solders.keypair import Keypair
from solanatracker import SolanaTracker
from dotenv import load_dotenv
import os

load_dotenv()
@dataclass(kw_only=True)
class Trade:
    ammountIn : float
    ammountOut: float
    minAmountOut: float
    currentPrice: float
    executionPrice: float
    priceImpact: int
    isPumpFun: int
    platformFee: int
    fee: float
    baseCurrency: str
    quoteCurrency: str
    tokenBought:str

    def __post_init__(self):
        rate_response = asyncio.run(self.calculate_rate_coin())
        self.ammountIn = rate_response['amountIn']
        self.ammountOut = rate_response['ammountOut']
        self.minAmountOut = rate_response['minAmountOut']
        self.currentPrice = rate_response['currentPrice']
        self.executionPrice = rate_response['executionPrice']
        self.priceImpact = rate_response['priceImpact']
        self.isPumpFun = rate_response['isPumpFun']
        self.platformFee = rate_response['platformFee']
        self.fee = rate_response['fee']
        self.baseCurrency = rate_response['baseCurrency']['mint']
        self.quoteCurrency = rate_response['quoteCurrency']['mint']
        # swap
        swap_response = asyncio.run(self.buy_coin())
        self.tokenBought = swap_response['rate']['quoteCurrency']['mint']
        self.amountSolana = swap_response['rate']['amountIn']
        self.amountTokenBought = swap_response['rate']['amountOut']

    """
        Get the data of one token
    """
    async def calculate_rate_coin(self) -> dict:
        keypair = Keypair.from_base58_string(
            "3xmbhcrVadA6vy1vtAdnJP7PjH7WogJ42YXR55NK4YZvjaJ22ypR3Xabnj2AEMhB9dgLwauLochDW2h9gJw9ERWn")

        solana_tracker = SolanaTracker(keypair, "https://rpc.solanatracker.io/public?advancedTx=true")

        rate_response = await solana_tracker.get_rate(
            os.getenv("SOLANA_WALLET_ADDRESS"),  # From Token
            "47p9s6G7mcAkELaq2kr2xLquLHgoJjEeHdcrf1xJkjnk",  # To Token
            os.getenv("AMOUNT_TO_BUY"),  # Amount to swap
            os.getenv("SLIPPAGE_RATE"),  # Slippage
        )

        return rate_response

    async def buy_coin(self) -> dict:
        keypair = Keypair.from_base58_string(os.getenv("PAYER_PUBLIC_KEY"))

        solana_tracker = SolanaTracker(keypair, os.getenv("RPC"))

        swap_response = await solana_tracker.get_swap_instructions(
            os.getenv("SOLANA_WALLET_ADDRESS"),  # From Token
            "47p9s6G7mcAkELaq2kr2xLquLHgoJjEeHdcrf1xJkjnk",  # To Token
            os.getenv("AMOUNT_TO_BUY"),  # Amount to swap
            os.getenv("SLIPPAGE_SWAP"),  # Slippage
            str(keypair.pubkey()),  # Payer public key
            0.00005,  # Priority fee (Recommended while network is congested)
            True,  # Force legacy transaction for Jupiter
        )

        txid = await solana_tracker.perform_swap(swap_response)

        if not txid:
            raise Exception("Swap failed")

        txid_url = f"https://explorer.solana.com/tx/{txid}"

        swap_response['txid'] = txid
        swap_response['txid_url'] = txid_url

        print("Transaction ID:", txid)
        print("Transaction URL:", f"https://explorer.solana.com/tx/{txid}")

        return swap_response

    async def sell_coin(self) -> dict:
        keypair = Keypair.from_base58_string(os.getenv("PAYER_PUBLIC_KEY"))

        solana_tracker = SolanaTracker(keypair, os.getenv("RPC"))

        swap_response = await solana_tracker.get_swap_instructions(
            os.getenv("SOLANA_WALLET_ADDRESS"),  # From Token
            "47p9s6G7mcAkELaq2kr2xLquLHgoJjEeHdcrf1xJkjnk",  # To Token
            os.getenv("AMOUNT_TO_BUY"),  # Amount to swap
            os.getenv("SLIPPAGE_SWAP"),  # Slippage
            str(keypair.pubkey()),  # Payer public key
            0.00005,  # Priority fee (Recommended while network is congested)
            True,  # Force legacy transaction for Jupiter
        )

        txid = await solana_tracker.perform_swap(swap_response)

        if not txid:
            raise Exception("Swap failed")

        txid_url = f"https://explorer.solana.com/tx/{txid}"

        swap_response['txid'] = txid
        swap_response['txid_url'] = txid_url

        print("Transaction ID:", txid)
        print("Transaction URL:", f"https://explorer.solana.com/tx/{txid}")

        return swap_response

    """
        Calculate the swap coin based on the trade data.
    """
    def calculate_swap_coin(self) -> str:
        return self.baseCurrency['mint'] if self.amountIn < self.amountOut else self.quoteCurrency['mint']

    """
        Calculate the total amount out after deducting fees.
    """
    def calculate_total_amount_out_after_fees(self) -> float:
        total_fee = self.platformFeeUI + self.fee
        return self.amountOut - total_fee

    """
        Calculate the percentage difference between the current price and the execution price.
    """
    def calculate_percentage_difference(self) -> float:
        return abs(self.currentPrice - self.executionPrice) / self.currentPrice * 100
