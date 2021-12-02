from jetpack import function

class TestError(Exception):
    def __init__(self, message):
        self.message = message


@function
async def error_thrower():
    raise TestError("This is a passed error")
