import os
import subprocess

DATA_PATH = './'
DEST_PATH = './'

for curdir, dirs, files in os.walk(DATA_PATH):
    for file in os.listdir(curdir):

        filename, file_extension = os.path.splitext(os.path.basename(file))

        if file_extension != '.pcm':
            continue

        dest_dir = os.path.join(curdir, DEST_PATH)

        if not os.path.isdir(dest_dir):
            os.mkdir(dest_dir)

        source_file = os.path.join(curdir, file)

        dest_file = os.path.join(dest_dir, filename + '.wav')

        subprocess.call(['ffmpeg', '-f', 's16le', '-ar', '16000', '-ac', '1', '-i', source_file, dest_file])

        # exit()
