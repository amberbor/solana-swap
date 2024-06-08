from mitmproxy import ctx
from mitmproxy.websocket import WebSocketMessage
import msgpack
import json

class WebSocketInterceptor:
    def __init__(self):
        self.target_url = "https://ws-token-sol-lb.tinyastro.io/cable"

    def websocket_message(self, flow):
        print(
            f"Flow request URL is {flow.request.url}, target URL is {self.target_url}, match: {flow.request.url == self.target_url}")
        if flow.request.url == self.target_url:
            if flow.websocket is None:
                return
            for message in flow.websocket.messages:
                if not message.from_client:
                    self.process_server_message(message.content)

    def process_server_message(self, content):
        try:
            # Look for the MessagePack segment in the content
            if b'"channel":"DiscoverLpChannel"' in content:

                # Extract the MessagePack portion of the content
                msgpack_data = self.extract_msgpack_data(content)
                if msgpack_data:
                    # Decode the MessagePack content
                    offset = 0
                    length = len(msgpack_data)

                    # Loop to unpack all valid MessagePack objects
                    while offset < length:
                        try:
                            # Create a new unpacker for the current slice of the binary message
                            unpacker = msgpack.Unpacker(raw=False, strict_map_key=False, use_list=True)
                            unpacker.feed(msgpack_data[offset:])

                            # Unpack and print each MessagePack object
                            for decoded_message in unpacker:
                                print(f"Decoded message: {decoded_message}")

                                # Update the offset to the current position in the buffer
                                offset += unpacker.tell()
                                break  # Process one valid MessagePack object at a time

                        except msgpack.exceptions.ExtraData as e:
                            # Skip non-MessagePack data by adjusting the offset
                            offset += 1

                        except UnicodeDecodeError as e:
                            # Handle potential Unicode errors gracefully
                            offset += 1

                        except Exception as e:
                            # Print any other errors and break the loop
                            print(f"Error: {e}")
                            break

        except Exception as e:
            print(f"Error processing server message: {e}")

    def extract_msgpack_data(self, content):
        # Find the start of the MessagePack data
        start = content.find(b'\x1a\x1f')
        if start != -1:
            msgpack_data = content[start:]
            return msgpack_data
        else:
            print("No MessagePack data found in the content.")
            return None

addons = [
    WebSocketInterceptor()
]

#run with   command "mitmdump -s photon.py"
