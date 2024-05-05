




import re
class Message:
    attribute_map = {
        'Mint': 'mint_address',
        'Name': 'name',
        'Symbol': 'symbol',
        'Creator': 'creator',
        'Cap': 'cap',
        'Dev': 'dev_percentage',
        'Bought': 'bought'
    }
    def __init__(self, message):
        self.id = message.id
        self.mint_address : str= None
        self.name : str = None
        self.symbol : str= None
        self.creator : str = None
        self.cap : float= None
        self.dev_percentage : float= None
        self.bought = None

        self.parse_message(message.text)


    def parse_message(self, message):
        kwargs = {}

        if message.strip():
            key, value = message.split(': ', 1)
            key = key.split(' ')[-1]
            if key in self.attribute_map:
                if key == 'Dev' or key == 'Whale':
                    percentage = re.search(r'[\d.]+%', value)
                    if percentage:
                        value_group = percentage.group()
                        if value_group == '0%':
                            value = "0"
                        else:
                            self.value = self.convert_to_float(value_group.replace("%", ""))

                    else:
                        value = "0"
                elif key == 'Cap':
                    self.cap = self.convert_to_float(value.replace("$", ""))
                kwargs[self.attribute_map[key]] = value.strip("`")
        return Message(**kwargs)

    def convert_to_float(self, value):
        try:
            return float(value)
        except ValueError:
            return 0.0

