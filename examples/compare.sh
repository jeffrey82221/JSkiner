rm data/huge.jsonl
pip install jsonschema-inference
for i in {1..100}; do cat data/big.jsonl >> data/huge.jsonl; done
echo "start comparison..."
for i in 1 2 4 8;
    do 
        echo "nworkers=$i";
        time jsonschema-inference --in-path data/huge.jsonl --verbose true --out result/huge.schema --nworkers $i;
        time jskiner --in-path data/huge.jsonl --verbose true --out result/huge.schema --nworkers $i;
done
rm data/huge.jsonl