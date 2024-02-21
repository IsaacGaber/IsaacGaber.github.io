import pyscript
# import nltk
# print(nltk)
# display("Hello, World!", target="output", append=False)
# display(nltk.__file__, target="output", append=False)
# display("AAHH", target="output", append=False)
import os

# from js import fetch
# nltk = await fetch("https://isaacgaber.github.io/projects/pyscript-hello-world/nltk")
# files = ""
# for f in os.listdir("../mip.py"):
#     files += f + "\n"
 # python3 -m http.server 8080 --bin --d 127.0.0.1
test = open("test.txt", "r")
lines = test.readlines()
test.close()
pyscript.display(lines[0], target="output", append=False)
# import nltk
# print(ntlk)
