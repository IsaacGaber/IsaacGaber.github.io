import pyscript
# import nltk
# print(nltk)
# display("Hello, World!", target="output", append=False)
# display(nltk.__file__, target="output", append=False)
# display("AAHH", target="output", append=False)
import os
print("Printing Structure: ")
for f in os.walk(""):
    print(f)
print("Printing NLTK: ")
from js import fetch
nltk = await fetch("https://isaacgaber.github.io/projects/pyscript-hello-world/nltk")

print(nltk)

# def list_files(startpath):
#     for root, dirs, files in os.walk(startpath):
#         level = root.replace(startpath, '').count(os.sep)
#         indent = ' ' * 4 * (level)
#         print('{}{}/'.format(indent, os.path.basename(root)))
#         subindent = ' ' * 4 * (level + 1)
#         for f in files:
#             print('{}{}'.format(subindent, f))
# list_files("../")

pyscript.display(pyscript.__file__, target="output", append=False)
