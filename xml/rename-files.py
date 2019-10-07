import os
path  = os.getcwd()
filenames = os.listdir(path)
for filename in filenames:
    filename_new = filename.replace('&', '-and-')
    filename_new = filename_new.replace('_', '-')
    filename_new = filename_new.replace('--', '-')
    filename_new = filename_new.replace(',', '')
    filename_new = filename_new.replace(' ', '-').lower()
    os.rename(os.path.join(path, filename), os.path.join(path, filename_new))
   