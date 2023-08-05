[![Continuous Integration](https://github.com/jeffrey82221/JSkiner/actions/workflows/ci.yml/badge.svg?branch=main)](https://github.com/jeffrey82221/JSkiner/actions/workflows/ci.yml)

# JSkiner 

This is a python **Js**on **Sch**ema **In**ference **E**ngine with **R**ust core. Its inferencing speed is about 10 times of its pure-python counterpart ([jsonschema-inference](https://pypi.org/project/jsonschema-inference/)).

# Installation 

```bash
pip install jskiner
```

# Usage

## Checking the Json Schema of a Large .jsonl file

```bash
jskiner \
    --in <path_to_jsonl> 
    --verbose <false/true> 
    --out <output_file_path>
    --nworkers <number_of_cpu_core>
    --split <number_of_split_batch_size>
    --split-path <path_to_store_the_split_files>
```

## Checking the Json Schema for a folder of json files

```bash
jskiner \
    --in <path_to_jsons> 
    --verbose <false/true> 
    --out <output_file_path>
    --nworkers <number_of_cpu_core>
    --batch-size <batch_size_for_inferencing>
    --cuckoo-path <path_to_store_the_cuckoo_filter>
    --cuckoo-size <approximated_size_of_the_cuckoo_filter (Recommend using 10X of current json count)>
    --cuckoo-fpr <false_positive_rate_of_the_cuckoo_filter>
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
schema = engine.run([Atomic(Int()), Atomic(Non()])
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

- [X] Enable inference from a folder of json files
- [X] Enable ignoring of existing json files using cuckoo filter
- [X] Enable add starting schema file
- [X] Enable batch-by-batch process on large jsonl file
- [X] FIX: make sure __repr__ escape special characters. 
- [X] Auto Formatting Using Black
- [X] Enable sampling of json files
- [X] Debug: show input that causing panick. (alter panic str / alter reduce.py exception logging) 
- [X] Fix: adding UnionRecord schema object
- [ ] Enable direct inferencing from API online. (able to avoid repeat download of json)
- [ ] Enable Regex to represent patterned FieldSet
