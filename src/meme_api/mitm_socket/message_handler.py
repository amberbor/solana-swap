import json
import msgpack
from src.costum_mitm_logger import logg


class StreamHandler:

    def __init__(self, stream_name):
        self.stream_name = stream_name
        self.unpacker = msgpack.Unpacker(
            raw=False,
            strict_map_key=False,
            use_list=True,
            # timestamp=3,
        )

        # json_start = message.find(b'\x1a') + 2
        # json_end = message.find(b'\x1a') + 1
        #
        # json_part = message[json_start:json_end].decode('utf-8')
        # decoded_json = json.loads(json_part)
        #
        # channel = decoded_json.get('channel', False)
        # if channel is False:
        #     del self
        #     return
        # self.channel_name = channel
        # self.unpacker = msgpack.Unpacker()
        # id = decoded_json.get('id', False)

    def process_stream(self, message):
        print("==============================")
        # print(f"{message}")
        print("==============================")

        offset = 0
        length = len(message)
        while offset < length:
            try:
                self.unpacker.feed(message)
                for msg in self.unpacker:
                    logg.info("---------------")
                    logg.info(f"Decoded message from {self.stream_name}:", msg)
                    logg.info("---------------")

                    offset += self.unpacker.tell()
                    break  # Process one valid MessagePack object at a time

            except msgpack.exceptions.ExtraData as e:
                # Skip non-MessagePack data by adjusting the offset
                logg.info(f"ExtraData error at offset {offset}: {e}")
                offset += 1

            except UnicodeDecodeError as e:
                # Handle potential Unicode errors gracefully
                print(f"UnicodeDecodeError at offset {offset}: {e}")
                offset += 1

            except Exception as e:
                # Print any other errors and break the loop
                logg.info(f"General error at offset {offset}: {e}")
                break
