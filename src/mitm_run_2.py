# import asyncio
# import multiprocessing
# from mitmproxy import ctx
# from mitmproxy import http
#
#
#
# def handle_other_requests(queue):
#     while True:
#         requests = queue.get()
#         if requests is None:
#             break
#
# queue = multiprocessing.Queue()
#
# def start_process():
#     global process
#     process = multiprocessing.Process(target=handle_other_requests, args=(queue,))
#     process.start()
# def cleanup():
#     global process
#     queue.put(None)
#     process.join()
#
# def websocket_message(flow: http.HTTPFlow):
#     assert flow.websocket is not None  # make type checker happy
#     last_message = flow.websocket.messages[-1]
#     if last_message.is_text and "secret" in last_message.text:
#         last_message.drop()
#         ctx.master.commands.call(
#             "inject.websocket", flow, last_message.from_client, b"ssssssh"
#         )
#
# async def inject_async(flow: http.HTTPFlow):
#     msg = "hello from mitmproxy! "
#     assert flow.websocket is not None  # make type checker happy
#     while flow.websocket.timestamp_end is None:
#         ctx.master.commands.call("inject.websocket", flow, True, msg.encode())
#         await asyncio.sleep(1)
#         msg = msg[1:] + msg[:1]
#
#
# # Python 3.11: replace with TaskGroup
# tasks = set()
#
#
# def websocket_start(flow: http.HTTPFlow):
#     # we need to hold a reference to the task, otherwise it will be garbage collected.
#     t = asyncio.create_task(inject_async(flow))
#     tasks.add(t)
#     t.add_done_callback(tasks.remove)




from __future__ import annotations

import logging

from mitmproxy import flowfilter
from mitmproxy import http
from mitmproxy.addonmanager import Loader


class Filter:
    filter: flowfilter.TFilter

    def configure(self, updated):
        if "flowfilter" in updated:
            self.filter = flowfilter.parse(".")

    def load(self, loader: Loader):
        loader.add_option("flowfilter", str, "", "Check that flow matches filter.")

    def response(self, flow: http.HTTPFlow) -> None:
        if flowfilter.match(self.filter, flow):
            logging.info("Flow matches filter:")
            logging.info(flow)


addons = [Filter()]