import subprocess
from sys import argv

subprocess.run("python pass1.py " + argv[1])
subprocess.run("python pass2.py pass1.out")
subprocess.run("python pass3.py pass2.out")