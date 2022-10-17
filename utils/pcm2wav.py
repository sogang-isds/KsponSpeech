import argparse
import os
import subprocess


def pcm2wav(data_path, dest_path='./', remove_pcm=False):
    for curdir, dirs, files in os.walk(data_path):
        for file in os.listdir(curdir):

            filename, file_extension = os.path.splitext(os.path.basename(file))

            if file_extension != '.pcm':
                continue

            dest_dir = os.path.join(curdir, dest_path)

            if not os.path.isdir(dest_dir):
                os.mkdir(dest_dir)

            source_file = os.path.join(curdir, file)

            dest_file = os.path.join(dest_dir, filename + '.wav')

            subprocess.call(['ffmpeg', '-f', 's16le', '-ar', '16000', '-ac', '1', '-i', source_file, dest_file, '-y'])

            if remove_pcm:
                os.remove(source_file)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--data_path',
                        required=True,
                        type=str,
                        help='data path to convert')
    parser.add_argument('--remove_pcm',
                        action="store_true",
                        required=False,
                        default=False,
                        help='remove pcm file')

    args = parser.parse_args()
    print(args)

    pcm2wav(data_path=args.data_path, remove_pcm=args.remove_pcm)
