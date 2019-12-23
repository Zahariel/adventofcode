from threading import Thread, Lock
from queue import SimpleQueue, Empty
from y2019.intcode import IntComp, FrameInput, FrameOutput

print_lock = Lock()
def safe_print(*args, **kwargs):
    with print_lock:
        print(*args, **kwargs)

with open("input.txt") as f:
    cells = [int(c) for c in f.readline().strip().split(",")]

NUM_COMPS = 50

queues = {i : SimpleQueue() for i in range(NUM_COMPS)}

idle = set()

def get_message(queue, i):
    def inner():
        try:
            # the instructions say that this doesn't block, but it slows down WAY too much if it really doesn't block
            # so block for a little bit just to give someone else a chance
            return queue.get(timeout=0.01)
        except Empty:
            idle.add(i)
            return -1,
    return inner

def send_message(sender):
    def send(target, x, y):
        # safe_print("send", target, x, y)
        idle.discard(sender)
        queues[target].put_nowait((x, y))
    return send

comps = [IntComp(cells, input_fn=FrameInput(get_message(queue, i)), output_fn=FrameOutput(3, send_message(i))) for i, queue in queues.items()]

for i, queue in queues.items():
    queue.put((i,))

queues[255] = SimpleQueue()

threads = []
for comp in comps:
    comp_thread = Thread(target=comp)
    threads.append(comp_thread)
    comp_thread.start()

x, y = 0, 0
sent_x, sent_y = 0, 0
while True:
    try:
        x, y = queues[255].get(timeout=0.01)
        print(x, y)
    except Empty:
        if len(idle) == NUM_COMPS:
            if y == sent_y:
                safe_print("sent", y, "again")
                exit(0)
            safe_print("revived", x, y)
            sent_x, sent_y = x, y
            queues[0].put((x, y))

