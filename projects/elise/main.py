from pyscript import document, display
import asyncio

time = 0
async def foo():
  while True:
      await asyncio.sleep(1)
      time += 1
      display(str(time), target="output")
# # await foo()

asyncio.ensure_future(foo())
