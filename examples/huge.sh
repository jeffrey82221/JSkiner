# unzip data/train.jsonl.zip data/train.jsonl
time jsonschema-inference --jsonl data/train.jsonl --verbose 0 --out result/train.schema --nworkers 8
time jshow --jsonl data/train.jsonl --verbose 0 --out result/train.schema --nworkers 8
# rm data/train.jsonl
