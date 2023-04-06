import subprocess
from sys import argv
from scipy.io.wavfile import write
import numpy as np

subprocess.run("python pass1.py " + argv[1])
subprocess.run("python pass2.py pass1.out")
subprocess.run("python pass3.py pass2.out")

samples = np.fromfile("audio.raw", np.float32)
write("output.wav", 44100, samples)