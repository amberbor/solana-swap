class CoinAudit:
    def __init__(self, audit):
        self.mint_authority = audit.get("mint_authority", None)
        self.freeze_authority = audit.get("freeze_authority", None)
        self.lb_burned_authority = audit.get("lb_burned_authority", None)
        self.top_holders_authority = audit.get("top_holders_authority", None)


class InitLiquidity:

    def __init__(self, liquidity):
        self.quote = liquidity.get("quote", None)
        self.usd = liquidity.get("quote", None)
        self.token = liquidity.get("token", None)
        self.timestamp = liquidity.get("timestamp", None)


class CurrentLiquidity:

    def __init__(self, liquidity):
        self.quote = liquidity.get("quote", None)
        self.usd = liquidity.get("quote", None)


class Socials:

    def __init__(self, socials):
        self.reddit = socials.get("reddit", None)
        self.twitter = socials.get("twitter", None)
        self.website = socials.get("website", None)
        self.telegram = socials.get("telegram", None)
        self.medium = socials.get("medium", None)


class CoinInfo(CoinAudit):
    def __init__(self, message):
        self.id = message.get("id", None)
        self.type = message.get("type", None)

        attrs = message.get("attributes")

        self.volume = attrs.get("volume", 0)
        self.name = attrs.get("name", "")
        self.symbol = attrs.get("symbol", "")
        self.price_usd = attrs.get("price_usd", 0)
        self.buys_count = attrs.get("buys_count", 0)
        self.sells_count = attrs.get("sells_count", 0)
        self.address = attrs.get("address", False)
        self.tokenAddress = attrs.get("tokenAddress", False)

        self.fdv = attrs.get("fdv", False)

        self.from_pump = attrs.get("fromPump", None)

        self.socials = Socials(attrs.get("socials", {}))
        self.audit = CoinAudit(attrs.get("audit", {}))
        self.init_liq = InitLiquidity(attrs.get("init_liq", {}))
        self.curr_liq = CurrentLiquidity(attrs.get("init_liq", {}))

        self.dex_i = attrs.get("dex_i", False)
        self.ignored = attrs.get("ignored", False)

        self.open_timestamp = attrs.get("open_timestamp", False)
        self.created_timestamp = attrs.get("created_timestamp", False)

    def __str__(self):
        return (
            f"COIN: {self.name} : {self.symbol} \n"
            f"Address: {self.address}\n"
            f"Price: {self.price_usd}\n"
            f"Volume: {self.volume}"
        )
