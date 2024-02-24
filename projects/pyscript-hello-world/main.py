import pyscript
import mip

mip.install("http://localhost:8080/nltk.whl", "nltk")
from nltk import *
test = open("test.txt", "r")
lines = test.readlines()
test.close()
pyscript.display(lines[0], target="output", append=False)
# import nltk
# print(ntlk)
