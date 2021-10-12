from jetpack import job
import sys


class TestError(Exception):
    def __init__(self, message):
        self.message = message


@job
def error_thrower():
    raise TestError("This is a passed error")
