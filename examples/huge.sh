# unzip data/test.jsonl.zip data/test.jsonl
# time jsonschema-inference --jsonl data/test.jsonl --verbose 0 --out result/test.schema --nworkers 8
# 2 min
time jshow --jsonl data/test.jsonl --verbose 0 --out result/test.schema --nworkers 8
# 11 s
time jshow --jsonl data/test.jsonl --verbose 0 --out result/test.schema --nworkers 4
# 12s
time jshow --jsonl data/test.jsonl --verbose 0 --out result/test.schema --nworkers 2
# 21s
time jshow --jsonl data/test.jsonl --verbose 0 --out result/test.schema --nworkers 1
# 39s