rm cuckoo.pickle
jskiner --in-path data/small.jsonl --verbose true --out result/small.schema --nworkers 2 --format true --split 2 --split-path ./small_split
jskiner --in-path data/big.jsonl --verbose true --out result/big.schema --split 5
jskiner --in-path data/pypi --verbose true --nworkers 2 --out result/pypi.schema --cuckoo-size 1000 --batch-size 2
