import re
from meme_api.database.orm import (CoinInfo)


class CoinInfoEntity:
    attribute_map = {
        "Mint": "mint_address",
        "Name": "name",
        "Symbol": "symbol",
        "Creator": "creator",
        "Market Cap": "cap",
        "Dev": "dev_percentage",
        "Bought": "bought",
    }

    def __init__(self, message):
        self._message = message
        self.message_id = message.id
        self.sent_at = message.date
        self.mint_address: str
        self.name: str
        self.symbol: str
        self.creator: str
        self.cap: float
        self.dev_percentage: float = 30

        self.parse_message(message.text)

    def parse_message(self, message):
        lines = message.splitlines()
        for line in lines:
            match = re.match(r"^[^\s]+ \*\*([\w\s]+)\*\*: (.+)$", line)
            if match:
                key, value = match.groups()
                key = key.strip()
                value = value.strip().strip("`")
                if key in self.attribute_map:
                    if "Cap" in key:
                        value = self.convert_to_float(
                            value.replace("$", "").replace(",", "")
                        )
                    elif key == "Dev":
                        value = self.convert_to_float(value.replace("%", ""))
                    setattr(self, self.attribute_map[key], value)

    def convert_to_float(self, value):
        try:
            return float(value)
        except ValueError:
            return 0.0

    def to_dict(self):
        return {
            "message_id": self.message_id,
            "sent_at": self.sent_at,
            "mint_address": self.mint_address,
            "name": self.name,
            "symbol": self.symbol,
            "description": self.description,
            "creator": self.creator,
            "cap": self.cap,
            "dev_percentage": self.dev_percentage,
        }

    def db_entity(self):
        return CoinInfo(
            message_id=self.message_id,
            mint_address=self.mint_address,
            name=self.name,
            symbol=self.symbol,
            creator=self.creator,
            cap=self.cap,
            dev_percentage=self.dev_percentage,
        )
