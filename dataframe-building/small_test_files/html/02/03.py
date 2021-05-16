import os
import glob

idx = 1
files = glob.glob('**/*.py', recursive=True)
for filename in files:
    print(idx, filename)
    idx += 1