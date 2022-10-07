import os
import subprocess

DATA_PATH = './KsponSpeech_05'
DEST_PATH = './utf-8'

dest_dir = os.path.join(DEST_PATH)

if not os.path.isdir(dest_dir):
    os.mkdir(dest_dir)
    
for curdir, dirs, files in os.walk(DATA_PATH):
    if './origin' in curdir:
        continue
    
    print(curdir)
    
    dest_dir = os.path.join(DEST_PATH, curdir)

    if not os.path.isdir(dest_dir):
        os.mkdir(dest_dir)
            
    for file in os.listdir(curdir):

        filename, file_extension = os.path.splitext(os.path.basename(file))

        if file_extension != '.txt':
            continue

        source_file = os.path.join(curdir, file)
        dest_file = os.path.join(dest_dir, file)
        
        with open(source_file, 'r', encoding='cp949') as f:
            line = f.read()
#            print(line)
            
        with open(dest_file, 'w', encoding='utf-8') as f:
            f.write(line)
            
#        print(dest_file)
#        exit()

        
