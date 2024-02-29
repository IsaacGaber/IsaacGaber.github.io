from pyscript import document, display
import mip
#
# # mip.install("http://localhost:8080/nltk.whl", "nltk")
# # # from nltk import *
# test = open("test.txt", "r")
# lines = test.readlines()
# # test.close()
# a = "<button id='my_button'>Click me!</button>"
# self = type(document.body)
mip.install("asyncio")
import asyncio
async def foo():
    i = 0
    while True:
        await asyncio.sleep(.5)
        Element("output").write(i)
        i += 1
pyscript.run_until_complete(foo())
# print(document)
# import nltk
# print(ntlk)
