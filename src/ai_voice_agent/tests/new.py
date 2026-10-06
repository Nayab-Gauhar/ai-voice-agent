import asyncio, time
start = time.time()
def log(msg): print(f"{time.time()-start:.0f}s  {msg}")

async def work(name):
    log(f"{name} start")
    await asyncio.sleep(2)
    log(f"{name} end")

async def main_await():
    await work("A")
    await work("B")

async def main_task():
    ta = asyncio.create_task(work("A"))
    tb = asyncio.create_task(work("B"))
    await ta
    await tb

asyncio.run(main_await())   # ya main_task()