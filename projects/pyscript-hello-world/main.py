# from pyscript import document, display
# # import mip
# #
# # # mip.install("http://localhost:8080/nltk.whl", "nltk")
# # # # from nltk import *
# # test = open("test.txt", "r")
# # lines = test.readlines()
# # # test.close()
# # a = "<button id='my_button'>Click me!</button>"
# # self = type(document.body)
# # mip.install("asyncio")
# import asyncio
# async def foo():
#     i = 0
#     while True:
#         await asyncio.sleep(.5)
#         # print(i)
#         display(i, target="output", append=False))
#         # Element("output").write(i)
#         i += 1
# pyscript.run_until_complete(foo())
# # print(document)
# # import nltk
# # print(ntlk)
import asyncio
from pyscript import document, display
# import js
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
