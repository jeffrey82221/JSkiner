[![Continuous Integration](https://github.com/jeffrey82221/JSkiner/actions/workflows/ci.yml/badge.svg?branch=main)](https://github.com/jeffrey82221/JSkiner/actions/workflows/ci.yml)

# JSkiner 

The is a python **Js**on **Sch**ema **In**ference **E**ngine with **R**ust's core. Its inferencing speed is about 10 times of its pure-python counterpart ([jsonschema-inference](https://pypi.org/project/jsonschema-inference/)).

# Installation 

```bash
pip install jskiner
```

# Usage

## Checking the Json Schema of a Large .jsonl file

```bash
jskiner \
    --jsonl <path_to_jsonl> 
    --verbose <0/1> 
    --out <output_file_path>
    --nworkers <number_of_cpu_core>
```

## Infering the Schema in Python

```python
from jskiner import InferenceEngine
cpu_cnt = 16
engine = InferenceEngine(cpu_cnt)
json_string_list = ["1", "1.2", "null", "{\"a\": 1}"]
schema = engine.run(json_string_list)
schema
```
>> Union({Atomic(Float()), Atomic(Int()), Atomic(Non()), Record({"a": Atomic(Int())})})

## Calculate the Union of a List of Schema 

```python
from jskiner import InferenceEngine
from jskiner.schema import Atomic, Int, Non
cpu_cnt = 16
engine = InferenceEngine(cpu_cnt)
schema = engine.run([Atomic(Int()), Atomic(Non)])
schema
```
>> Optional(Atomic(Int()))

## Using | Operation between Two Schema

```python
from jskiner import Atomic, Int, Non
schema = Atomic(Int()) | Atomic(Non())
schema
```
>> Optional(Atomic(Int()))

# TODO:

- [ ] Enable inference from a folder of json files
- [ ] Enable ignoring of existing json files using cuckoo filter
- [ ] Enable add starting schema file
- [X] Enable batch-by-batch process on large jsonl file
- [X] FIX: make sure __repr__ escape special characters. 
- [X] Auto Formatting Using Black