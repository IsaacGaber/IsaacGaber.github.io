import pyscript
# import nltk
# print(nltk)
# display("Hello, World!", target="output", append=False)
# display(nltk.__file__, target="output", append=False)
# display("AAHH", target="output", append=False)
import os

# from js import fetch
# nltk = await fetch("https://isaacgaber.github.io/projects/pyscript-hello-world/nltk")
#
# print(nltk)
files = ""
for f in os.listdir():
    files += f + "\n"
pyscript.display(files, target="output", append=False)
