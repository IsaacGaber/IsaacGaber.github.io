import asyncio
from pyscript import document, display
import js
# import nltk
# print(nltk)

async def foo():
    time = 0
    while True:
        await asyncio.sleep(.01)
        time += 1
        display(str(time), target="output", append=False)
# # await foo()
# output = document.getElementById("output")
# for key in output.dataset:
#     print(key)
# print(type(document.getElementById("output").dataset))
asyncio.ensure_future(foo())
