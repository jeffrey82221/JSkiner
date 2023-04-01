import argparse
import subprocess
import os
import shutil
from .jskiner import InferenceEngine
from jskiner.schema import Unknown

exec("from jskiner.schema import *")


def get_args():
    parser = argparse.ArgumentParser(description="Inferencing Json Schema")

    parser.add_argument(
        "--jsonl",
        type=str,
        required=True,
        help="Inference Json Schema from .jsonl file",
    )

    parser.add_argument(
        "--nworkers", type=int, required=False, default=1, help="Inference Worker Count"
    )

    parser.add_argument(
        "--verbose",
        type=bool,
        required=False,
        default=False,
        help="Showing the Result by Pretty Print",
    )

    parser.add_argument(
        "--out",
        type=str,
        required=False,
        default="out.schema",
        help="Saving the json schema into a output file",
    )

    parser.add_argument(
        "--format",
        type=bool,
        required=False,
        default=True,
        help="formatting the output schema using `black`",
    )

    parser.add_argument(
        "--split",
        type=int,
        required=False,
        default=1,
        help="Number of splitted jsonl file (1 for no splitting)",
    )
    parser.add_argument(
        "--split_path",
        type=str,
        required=False,
        default="/tmp/split",
        help="Path to store the temporary splitted jsonl files",
    )
    args = parser.parse_args()
    return args


def run() -> None:
    args = get_args()
    if args.verbose:
        print(f"Loading {args.jsonl}")
    if args.split == 1:
        schema_str = get_schema_from_jsonl(args.jsonl, worker_cnt=args.nworkers)
    else:
        schema_str = get_schema_batchwise(
            args.jsonl, args.split_path, args.split, verbose=args.verbose
        )
    store(schema_str, output_path=args.out, verbose=args.verbose, format=args.format)


def get_schema_batchwise(src_path, split_path, split_cnt, verbose=False):
    try:
        refresh_split_path(split_path)
        split(src_path, split_path, split_cnt)
        schema = Unknown()
        file_iter = os.listdir(split_path)
        if verbose:
            try:
                import tqdm
            except ImportError:
                subprocess.run(["pip", "install", "tqdm"])
            file_iter = tqdm.tqdm(file_iter)
        for file_name in file_iter:
            selected_path = f"{split_path}/{file_name}"
            if verbose:
                print("Start Inferencing", selected_path)
            schema_str = get_schema_from_jsonl(selected_path)
            schema |= eval(schema_str)
            if verbose:
                print("Finish Inferencing", selected_path)
        schema_str = schema.__repr__()
        return schema_str
    except BaseException as e:
        with open("log", "w") as f:
            f.write(schema_str)
        raise e
    finally:
        refresh_split_path(split_path)


def refresh_split_path(path):
    if not os.path.exists(path):
        os.mkdir(path)
    else:
        shutil.rmtree(path)
        os.mkdir(path)


def split(src_path, split_path, split_cnt):
    total = get_total_json_count(src_path)
    cnt_per_file = int(total / split_cnt)
    subprocess.run(["split", "-l", str(cnt_per_file), src_path, split_path + "/"])


def get_total_json_count(path):
    out = subprocess.check_output(["wc", "-l", path])
    total = int(out.decode("utf-8").split(path)[0])
    return total


def get_schema_from_jsonl(jsonl_path, worker_cnt=1):
    with open(jsonl_path, "r") as f:
        json_list = [x for x in f]
    engine = InferenceEngine(worker_cnt)
    schema_str = engine.run(json_list)
    return schema_str


def store(schema_str, output_path="out.schema", verbose=False, format=True):
    if output_path != "":
        with open(output_path, "w") as f:
            f.write(schema_str)
        if verbose:
            print("Result saved into", output_path)
        if format:
            try:
                import black
            except ImportError:
                subprocess.run(["pip", "install", "black"])
            black
            subprocess.run(["black", output_path])
