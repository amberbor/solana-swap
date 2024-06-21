import multiprocessing
def handle_other_requests(queue):
    while True:
        requests = queue.get()
        if requests is None:
            break

queue = multiprocessing.Queue()

def start_process():
    global process
    process = multiprocessing.Process(target=handle_other_requests, args=(queue,))
    process.start()
def cleanup():
    global process
    queue.put(None)
    process.join()