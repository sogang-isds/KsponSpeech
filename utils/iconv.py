import os
import subprocess

DATA_PATH = './'
DEST_PATH = './'

for curdir, dirs, files in os.walk(DATA_PATH):
    if './origin' in curdir:
        continue
        
    for file in os.listdir(curdir):

        filename, file_extension = os.path.splitext(os.path.basename(file))

        if file_extension != '.txt':
            continue

        dest_dir = os.path.join(curdir, DEST_PATH)

        if not os.path.isdir(dest_dir):
            os.mkdir(dest_dir)

        source_file = os.path.join(curdir, file)

        dest_file = os.path.join(dest_dir, filename + '.txt')
        

        with open(dest_file, 'w', encoding='utf-8') as f:
            subprocess.call(['iconv', '-f', 'cp949', '-t', 'utf-8', source_file], stdout=f)

        print(dest_file)
        exit()
