from pyscript import document, display
import mip

# mip.install("http://localhost:8080/nltk.whl", "nltk")
# # from nltk import *
test = open("test.txt", "r")
lines = test.readlines()
# # test.close()
# a = "<button id='my_button'>Click me!</button>"
# self = type(document.body)
display(lines[0], target="output", append=False)
# print(document)
# import nltk
# print(ntlk)
