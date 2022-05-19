# Holy Threads

This fork adds the ability for threads to declared as "holy."  For example:

```
import threading

# Some CPU intensive thread
def countdown(n):
    while n > 0:
        n -=1

threading.Thread(target=countdown, args=(100_000_000,), holy=True).start()
```

A "holy" thread will immediately sacrifice the GIL if another thread wants it.
This allows a CPU-bound thread to nicely co-exist with I/O bound threads
without starving I/O response time.

As alternative to using the `holy` option to `Thread()`, a thread can
change it's holiness explicitly using the `sys.setholiness()`
function:

```
import sys

# Some CPU intensive thing
def countdown(n):
    sys.setholiness(True)
    while n > 0:
        n -=1
```

There are two programs to test performance.  See `echoserver.py` and `echosender.py`.


