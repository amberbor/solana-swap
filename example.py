from solders.keypair import Keypair
from meme_api.app import SolanaTracker

# async def swap():
#     keypair = Keypair.from_base58_string("3xmbhcrVadA6vy1vtAdnJP7PjH7WogJ42YXR55NK4YZvjaJ22ypR3Xabnj2AEMhB9dgLwauLochDW2h9gJw9ERWn")
#
#     solana_tracker = SolanaTracker(keypair, "https://rpc.solanatracker.io/public?advancedTx=true")
#
#     swap_response = await solana_tracker.get_swap_instructions(
#         "ELNTaN7aAAYM5BxUGXRXkHsULcBSvSj4sQeEQAerjMj2",  # From Token
#         "S5Q23QqqSSRrJ6G42nyyMkedFzBH6pojBH99HDbXLdo",  # To Token
#         0.0005,  # Amount to swap
#         10,  # Slippage
#         str(keypair.pubkey()),  # Payer public key
#         0.00005,  # Priority fee (Recommended while network is congested)
#         True,  # Force legacy transaction for Jupiter
#     )
#
#     txid = await solana_tracker.perform_swap(swap_response)
#
#     if not txid:
#         # Add retries / handle error as needed
#         raise Exception("Swap failed")
#
#     # Returns txid when the swap is successful or raises an exception if the swap fails
#     print("Transaction ID:", txid)
#     print("Transaction URL:", f"https://explorer.solana.com/tx/{txid}")


async def rate():
    keypair = Keypair.from_base58_string(
        "3xmbhcrVadA6vy1vtAdnJP7PjH7WogJ42YXR55NK4YZvjaJ22ypR3Xabnj2AEMhB9dgLwauLochDW2h9gJw9ERWn"
    )

    solana_tracker = SolanaTracker(
        keypair, "https://rpc.solanatracker.io/public?advancedTx=true"
    )

    rate_response = await solana_tracker.get_rate(
        "So11111111111111111111111111111111111111112",  # From Token
        "47p9s6G7mcAkELaq2kr2xLquLHgoJjEeHdcrf1xJkjnk",  # To Token
        0.0005,  # Amount to swap
        1000,  # Slippage
    )

    print(rate_response)


if __name__ == "__main__":
    import asyncio

    asyncio.run(rate())
