import json as jsonlib
from collections import deque
from time import ticks_ms, ticks_diff
import uasyncio as asyncio

## Public API


def enable():
    """
    Once enabled, all new asyncio tasks will be tracked.
    Existing tasks will not be tracked.
    """
    asyncio.create_task = asyncio.core.create_task = create_task


def inject():
    """
    This enables aioprof and attempts to hook into all existing tasks.
    """
    tasks = list()
    enable()
    try:
        while t := asyncio.core._task_queue.pop():
            tasks.append(t)
    except IndexError:
        pass

    for t in tasks:
        asyncio.create_task(t.coro)

def reset():
    """
    Reset all the accumlated task data
    """
    global timing
    timing = {}


def report():
    """
    Print a report to repl of task run count and timing.
    """
    if not timing:
        print("No timing data")
        return

    details = [
        (name, str(value[0]), str(value[1]), str(value[2]), str(value[3]))
        for name, value in reversed(sorted(timing.items(), key=lambda i: i[1][1]))
    ]

    nlen = max([len(n) for n, i, t, m, c in details])
    ilen = max((len("count"), max([len(i) for n, i, t, m, c in details])))
    tlen = max((len("ms"), max([len(t) for n, i, t, m, c in details])))
    mlen = max((len("max"), max([len(m) for n, i, t, m, c in details])))
    clen = max((len("last exec"), max([len(c) for n, i, t, m, c in details])))


    print("┌─" + "─" * nlen + "─┬─" + "─" * ilen + "─┬─" + "─" * tlen + "─┬─" + "─" * mlen + "─┬─" + "─" * clen +"─┐")
    print(f"│ function name {' '*(nlen-14)} │ count{' '*(ilen-5)} │ ms {' '*(tlen-2)}| max {' '*(mlen-3)}│ last exec {' '*(clen-9)}│")
    print("├─" + "─" * nlen + "─┼─" + "─" * ilen + "─┼─" + "─" * tlen + "─┼─" + "─" * mlen + "─┼─" + "─" * clen + "─┤")
    for name, i, t, m, c in details:
        npad = " " * (nlen - len(name))
        ipad = " " * (ilen - len(i))
        tpad = " " * (tlen - len(t))
        mpad = " " * (mlen - len(m))
        cpad = " " * (clen - len(c))
        print(f"│ {name}{npad} │ {i}{ipad} │ {t}{tpad} | {m}{mpad} │ {c}{cpad} │")
    print("└─" + "─" * nlen + "─┴─" + "─" * ilen + "─┴─" + "─" * tlen + "─┴─" + "─" * mlen + "─┴─" + "─" * clen +"─┘")


def json():
    """
    Directly dump the task [run-count,timing] details as json.
    """
    return jsonlib.dumps(timing)


## Internal functionality

Task = asyncio.Task
timing = {}
counter = 0
__create_task = asyncio.create_task

class Coro:
    def __init__(self, c) -> None:
        self.name = str(c)
        self.c = c

    def send(self, *args, **kwargs):
        t_name = self.name
        t_start = ticks_ms()
        try:
            ret = self.c.send(*args, **kwargs)
        except AttributeError:
            print(self, self.c)
            raise
        finally:
            if t_name not in timing:
                timing[t_name] = [0, 0, 0, 0]

            t = timing[t_name]
            taken = ticks_diff(ticks_ms(), t_start)
            t[0] += 1
            t[1] += taken
            t[2] = max(taken, t[2])
            global counter
            t[3] = counter
            counter += 1
        return ret

    def __getattr__(self, name: str):
        return getattr(self.c, name)


def create_task(coro):
    if not isinstance(coro, Coro):
        coro = Coro(coro)
    return __create_task(coro)
