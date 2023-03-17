pip install jsonschema-inference
echo "start comparison..."
time jsonschema-inference --jsonl data/big.jsonl --verbose 0 --out result/big.schema
time jshow --jsonl data/big.jsonl --verbose 0 --out result/big.schema
