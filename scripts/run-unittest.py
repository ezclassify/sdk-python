import gc
import sys
import threading
import unittest
from unittest.mock import patch


def main():
    failed = False
    thread_hook = threading.excepthook
    unraisable_hook = sys.unraisablehook

    def thread_failed(args):
        nonlocal failed
        failed = True
        thread_hook(args)

    def cleanup_failed(args):
        nonlocal failed
        failed = True
        unraisable_hook(args)

    with (
        patch.object(threading, "excepthook", thread_failed),
        patch.object(sys, "unraisablehook", cleanup_failed),
    ):
        result = unittest.main(module=None, exit=False).result
        gc.collect()

    if failed:
        print(
            "Unexpected exception in a background thread or during cleanup.",
            file=sys.stderr,
        )
    return 0 if result.wasSuccessful() and not failed else 1


if __name__ == "__main__":
    sys.exit(main())
