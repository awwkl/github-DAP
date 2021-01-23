import os
import glob

# cwd = os.getcwd()
# idx = 1
# for subdir, dirs, files in os.walk(cwd):
#     for file in files:
#         if file.endswith('.py'):
#             print(f'No.{idx}: {file}')
#             idx += 1
#         else:
#             os.remove(file)

# for folder, subfolders, files in os.walk(os.getcwd()):
#     for file in files:
#         filePath = os.path.abspath(os.path.join(folder, file))
#         print(filePath, os.stat(file).st_uid)

idx = 1
files = glob.glob('**/*.py', recursive=True)
for filename in files:
    print(idx, filename)
    idx += 1