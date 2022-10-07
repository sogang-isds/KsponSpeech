import os
import subprocess
import shutil

DATA_PATH = './utf-8'
DEST_PATH = './'

dest_dir = os.path.join(DEST_PATH)

if not os.path.isdir(dest_dir):
    os.mkdir(dest_dir)
            
for curdir, dirs, files in os.walk(DATA_PATH):
    
    print(curdir)
    
#    if not os.path.exists(os.path.join(dest_dir, curdir)):
#        os.mkdir(os.path.join(dest_dir, curdir))
            
    for file in os.listdir(curdir):

        filename, file_extension = os.path.splitext(os.path.basename(file))

        if file_extension != '.txt':
            continue

        
        source_file = os.path.join(curdir, file)
        dest_file = os.path.join(dest_dir, curdir.replace('utf-8/', ''), file)

        shutil.copy(source_file, dest_file)
            
#        print(source_file)
#        print(dest_file)
#        exit()

