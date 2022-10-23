import argparse
import numpy as np
import whisper
from pprint import pprint


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--file', required=True, type=str)
    parser.add_argument('--cuda', default='cuda:0', type=str)
    args = parser.parse_args()

    print("Loading model...")
    model = whisper.load_model("medium", device=args.cuda)
    print(
        f"Model is {'multilingual' if model.is_multilingual else 'English-only'} "
        f"and has {sum(np.prod(p.shape) for p in model.parameters()):,} parameters."
    )

    options = {
        'task': 'transcribe',
        'language': 'Korean'
    }

    result = model.transcribe(args.file, **options)
    pprint(result)