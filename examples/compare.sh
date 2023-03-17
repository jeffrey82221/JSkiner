pip install jsonschema-inference
echo "start comparison..."
echo "\n\n\nworker=1"
time jsonschema-inference --jsonl data/big.jsonl --verbose 0 --out result/big.schema --nworkers 1
time jshow --jsonl data/big.jsonl --verbose 0 --out result/big.schema --nworkers 1
echo "\n\n\nworker=2"
time jsonschema-inference --jsonl data/big.jsonl --verbose 0 --out result/big.schema --nworkers 2
time jshow --jsonl data/big.jsonl --verbose 0 --out result/big.schema --nworkers 2
echo "\n\n\nworker=4"
time jsonschema-inference --jsonl data/big.jsonl --verbose 0 --out result/big.schema --nworkers 4
time jshow --jsonl data/big.jsonl --verbose 0 --out result/big.schema --nworkers 4
echo "\n\n\nworker=8"
time jsonschema-inference --jsonl data/big.jsonl --verbose 0 --out result/big.schema --nworkers 8
time jshow --jsonl data/big.jsonl --verbose 0 --out result/big.schema --nworkers 8
