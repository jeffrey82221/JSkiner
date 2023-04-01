import argparse
from .jskiner import InferenceEngine



def run() -> None:
    args = get_args()
    print(f"Your json file is at: {args.jsonl}")
    print('verbose:', args.verbose)
    schema_str = get_schema_from_jsonl(args.jsonl, worker_cnt=args.nworkers)
    # Store result to `out` path
    if args.out != '':
        with open(args.out, 'w') as f:
            f.write(schema_str)
        print('Result saved into', args.out)

def get_args():
    parser = argparse.ArgumentParser(
        description='Inferencing Json Schema')

    parser.add_argument('--jsonl',
                        type=str, required=True,
                        help="Inference Json Schema from .jsonl file")

    parser.add_argument('--nworkers',
                        type=int, required=False, default=1,
                        help="Inference Worker Count")

    parser.add_argument('--verbose',
                        type=bool, required=False, default=False,
                        help="Showing the Result by Pretty Print")

    parser.add_argument('--out',
                        type=str, required=False, default='',
                        help="Saving the json schema into a output file")

    parser.add_argument('--split',
                        type=int, required=False, default=1,
                        help="Number of splitted jsonl file (1 for no splitting)"
    )
    parser.add_argument('--split_path',
                         type=str, required=False, default='/tmp/split',
                         help="Path to store the temporary splitted jsonl files"
    )
    args = parser.parse_args()
    return args

def get_schema_from_jsonl(jsonl_path, worker_cnt=1):
    with open(jsonl_path, 'r') as f:
        json_list = [x for x in f]
    engine = InferenceEngine(worker_cnt)
    schema_str = engine.run(json_list)
    return schema_str