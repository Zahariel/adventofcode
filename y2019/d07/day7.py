from y2019.intcode import IntComp, InputFunction
from itertools import permutations
from queue import SimpleQueue
from threading import Thread

with open("input.txt") as f:
    line = f.readline()

initial_cells = [int(x) for x in line.split(",")]

max_signal = 0
max_settings = (-1, -1, -1, -1, -1)

class Signal():
    def __init__(self):
        self.val = 0

    def __call__(self, new_val):
        self.val = new_val

def try_settings(settings):
    signal = Signal()
    for i in range(5):
        comp = IntComp(list(initial_cells), input_fn=InputFunction([settings[i], signal.val]), output_fn=signal)
        comp.run()
    return signal.val

print(max(try_settings(settings) for settings in permutations([0, 1, 2, 3, 4])))


def make_get_message(queue):
    def get_message(prompt):
        return queue.get(block=True)
    return get_message

def make_send_message(queue):
    def send_message(message):
        queue.put(message)
    return send_message

def try_feedback(settings):
    message_queues = [SimpleQueue() for i in range(5)]
    # settings
    for i in range(5):
        message_queues[i - 1].put(settings[i])
    # initial value
    message_queues[4].put(0)
    threads = []
    for i in range(5):
        comp = IntComp(list(initial_cells), input_fn=make_get_message(message_queues[i - 1]),
                       output_fn=make_send_message(message_queues[i]))
        comp_thread = Thread(target=comp)
        threads.append(comp_thread)
        comp_thread.start()
    for i in range(5):
        threads[i].join()
    return message_queues[4].get()

print(max(try_feedback(settings) for settings in permutations([5, 6, 7, 8, 9])))
