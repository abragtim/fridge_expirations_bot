import asyncio


async def func():
    while True:
        print('hello')
        await asyncio.sleep(1)

async def func2():
    while True:
        print('bb')
        await asyncio.sleep(1)


async def main():
    await asyncio.gather(func(), func2())

loop = asyncio.get_event_loop()
loop.run_until_complete(main())