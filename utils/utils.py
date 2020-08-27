import time

def sleep(t = 1):
    def sleepT(func):
        async def sleepTs():
            time.sleep(t)
            return await func()
        return sleepTs
    return sleepT