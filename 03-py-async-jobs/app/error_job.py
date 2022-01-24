from jetpack import jetroutine

class TestError(Exception):
    def __init__(self, message):
        self.message = message


@jetroutine
async def error_thrower():
    raise TestError("This is a passed error")
