import re


class Message:
    attribute_map = {
        "Mint": "mint_address",
        "Name": "name",
        "Symbol": "symbol",
        "Creator": "creator",
        "Cap": "cap",
        "Dev": "dev_percentage",
        "Bought": "bought",
    }

    def __init__(self, message):
        self.message_id = message.id
        self.sent_at = message.date
        self.mint_address: str = None
        self.name: str = None
        self.symbol: str = None
        self.creator: str = None
        self.cap: float = None
        self.dev_percentage: float = None
        self.bought = None

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
                    if key == "Cap":
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
