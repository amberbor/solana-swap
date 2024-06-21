from mitmproxy import ctx, http
from mitmproxy.script import concurrent
import json
import certifi
import ssl
from src.meme_api.app.entity.coin import CoinInfo
from src.meme_api.mitm_socket.message_handler import StreamHandler

from src.costum_mitm_logger import logg

ctx.log.level = "error"

WEBSOCKET_URL = "https://ws-token-sol-lb.tinyastro.io/cable"
MAIN_URL = "photon-sol.tinyastro.io"
PATHS = {
    "search": f"/api/discover/search",
}


class WebSocketInterceptor:
    buffer = b""

    channels = {
        "LpChannel": StreamHandler("LpChannel"),
        "DiscoverLpChannel": StreamHandler("DiscoverLpChannel"),
        "UsersChannel": StreamHandler("UsersChannel"),
    }

    endpoints = [
        "https://photon-sol.tinyastro.io/api/lp/events_stats?pool_id=1096522"  # Check specific Coin Page
        "https://photon-sol.tinyastro.io/api/lp/get_dev_purchases?pool_id=1096522&address=Bh6BuUCEXSDys5e5EMZaVrmY74mk6SnWvoPu9HENHEMH"  # Get Dev Puchases
    ]

    def __init__(self):
        self.ssl_ctx = ssl.create_default_context(cafile=certifi.where())
        self.ssl_ctx.verify_mode = ssl.CERT_REQUIRED
        # self.executor = ProcessPoolExecutor(max_workers=cpu_count() - 5)
        # self.thread_executor = ThreadPoolExecutor()

    def load(self, loader):
        # Set the SSL context to use certifi's CA bundle
        options = ctx.options
        options.certs.append(f"*={certifi.where()}")

    def configure(self, updated):
        # Update the SSL context if options are updated
        if "upstream_cert" in updated:
            ctx.options.certs.append(f"*=certifi.where()")

    @concurrent
    def websocket_start(self, flow: http.HTTPFlow):
        if flow.request.pretty_url == WEBSOCKET_URL:
            logg.info(
                f"WebSocket handshake started: {flow.client_conn.address} -> {flow.server_conn.address}"
            )

    @concurrent
    async def websocket_end(self, flow: http.HTTPFlow):
        if flow.request.pretty_url == WEBSOCKET_URL:
            logg.info(
                f"WebSocket connection closed: {flow.client_conn.address} -> {flow.server_conn.address} : {flow.websocket.close_code} {flow.websocket.close_reason}"
            )

    @concurrent
    async def response(self, flow: http.HTTPFlow):
        request = flow.request
        if request.host == MAIN_URL and PATHS.get("search") in request.path:
            decoded_response = flow.response.content.decode("utf-8")
            json_response = json.loads(decoded_response)
            # self.thread_executor.submit(self.process_search_response, json_response)
            self.process_search_response(json_response)

    def process_search_response(self, json_response):
        for icoin in json_response["data"]:
            coin = CoinInfo(icoin)
            logg.info(coin)

    # if flow.request

    # @concurrent
    # async def websocket_message(self, flow: http.HTTPFlow):
    #     if flow.request.url == WEBSOCKET_URL:
    #         message = flow.websocket.messages[-1]
    #         if not message.from_client and message is not None:
    #             channel, _id, content = self.extract_msgpack_data(message.content)
    #             stream_handler = self.channels.get(channel, False)
    #             if stream_handler:
    #                 # if channel == 'DiscoverLpChannel':
    #                 # self.executor.submit(stream_handler.process_stream, content)
    #                 stream_handler.process_stream(content)

    def extract_msgpack_data(self, content):
        # Find the start of the MessagePack data
        json_start = content.find(b"\x1a") + 2
        json_end = content.find(b"}") + 1
        json_part = content[json_start:json_end].decode("utf-8")
        try:
            decoded_json = json.loads(json_part)
        except json.JSONDecodeError as e:
            return False, False, False

        channel_name = decoded_json.get("channel", False)
        if not channel_name:
            return False, False, False
        _id = decoded_json.get("id", False)

        return channel_name, _id, content[json_end + 1 :]


addons = [WebSocketInterceptor()]
