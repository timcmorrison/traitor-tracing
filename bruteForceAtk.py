import subprocess
from subprocess import run


for a in range(10):
    for b in range(10):
        for c in range(10):
            for d in range(10):
                print("{}{}{}{}".format(a, b, c, d))
                run(["python", "networkReg.py", "{}{}{}{}".format(a, b, c, d)])