jskiner --jsonl data/small.jsonl --verbose true --out result/small.schema --nworkers 2 --format true --split 2 --split_path ./small_split
jskiner --jsonl data/big.jsonl --verbose true --out result/big.schema --split 5
