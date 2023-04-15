use std::collections::HashSet;
use std::hash::{Hash, Hasher};
use crate::op::reduce::reduce;
use super::atomic::atomic::RustAtomic;
use super::array::RustArray;
use super::record::{RustRecord, RustFieldSet};
use super::unions::RustUnion;
use super::unknown::RustUnknown;
//////////////////// JsonSchema ///////////////////////////
#[derive(Clone, Eq, PartialEq)]
pub enum RustJsonSchema {
    Unknown(RustUnknown),
    Atomic(RustAtomic),
    Array(RustArray),
    Record(RustRecord),
    Union(RustUnion) // Advance Json Schema
}
impl RustJsonSchema {
    pub fn repr(&self) -> String {
        match self {
            RustJsonSchema::Unknown(un_val) => un_val.repr(),
            RustJsonSchema::Atomic(atom_val) => atom_val.repr(),
            RustJsonSchema::Array(array_val) => array_val.repr(),
            RustJsonSchema::Record(record_val) => record_val.repr(),
            RustJsonSchema::Union(union_val) => union_val.repr(),
        }
    }
    pub fn merge(self, other:RustJsonSchema) -> RustJsonSchema {
        match self {
            RustJsonSchema::Unknown(_) => {
                other
            },
            RustJsonSchema::Atomic(_) => {
                self.merge_into_atomic(other)
            },
            RustJsonSchema::Array(_) => {
                self.merge_into_array(other)
            },
            RustJsonSchema::Record(_) => {
                self.merge_into_record(other)
            },
            RustJsonSchema::Union(_) => {
                self.merge_into_union(other)
            }   
        }
    }
    fn merge_into_atomic(self, other:RustJsonSchema) -> RustJsonSchema {
        match other {
            RustJsonSchema::Unknown(_) => {
                self
            },
            RustJsonSchema::Atomic(_) => {
                if self.repr() == other.repr() {
                    self
                } else {
                    let mut content = HashSet::new();
                    content.insert(self.clone());
                    content.insert(other.clone());
                    RustJsonSchema::Union(RustUnion {content: content})
                }
            },
            RustJsonSchema::Array(_) => {                        
                let mut content = HashSet::new();
                content.insert(self.clone());
                content.insert(other.clone());
                RustJsonSchema::Union(RustUnion {content: content})                        
            },
            RustJsonSchema::Record(_) => {                        
                let mut content = HashSet::new();
                content.insert(self.clone());
                content.insert(other.clone());
                RustJsonSchema::Union(RustUnion {content: content})                        
            },
            RustJsonSchema::Union(_) => {
                other.merge(self)
            },
        }
    }
    fn merge_into_array(self, other:RustJsonSchema) -> RustJsonSchema {
        match self {
            RustJsonSchema::Array(ref l) => {
                match other {
                    RustJsonSchema::Unknown(_) => {
                        self
                    },
                    RustJsonSchema::Atomic(_) => {
                        other.merge(self)
                    },
                    RustJsonSchema::Array(ref r) => {
                        RustJsonSchema::Array( RustArray { content: Box::new(l.content.clone().merge(*r.clone().content))} )
                    },
                    RustJsonSchema::Record(_) => {                        
                        let mut content = HashSet::new();
                        content.insert(self.clone());
                        content.insert(other.clone());
                        RustJsonSchema::Union(RustUnion {content: content})                        
                    },
                    RustJsonSchema::Union(_) => {
                        other.merge(self)
                    },
                }
            },
            _ => panic!("merge_into_array only support Array object")
        }
        
    }
    fn merge_into_record(self, other:RustJsonSchema) -> RustJsonSchema {
        match self {
            RustJsonSchema::Record(ref l) => {
                match other {
                    RustJsonSchema::Unknown(_) => {
                        self
                    },
                    RustJsonSchema::Atomic(_) => {
                        other.merge(self)
                    },
                    RustJsonSchema::Array(_) => {
                        other.merge(self)
                    },
                    RustJsonSchema::Record(_r) => {
                        // A field schema recorder:
                        let mut field_schema = l.field_schema.clone();
                        for (key, r_schema) in _r.field_schema.iter() {
                            match l.field_schema.get(key) {
                                Some(l_schema) => {
                                    let merged_schema = l_schema.clone().merge(r_schema.clone());
                                    field_schema.insert(key.to_string(), merged_schema);
                                },
                                None => {
                                    field_schema.insert(key.to_string(), r_schema.clone());
                                }
                            }
                        }
                        let mut field_counter = l.field_counter.clone();
                        for (key, r_cnt) in _r.field_counter.iter() {
                            match l.field_counter.get(key) {
                                Some(l_cnt) => {
                                    field_counter.insert(key.to_string(), r_cnt.clone() + l_cnt.clone());
                                },
                                None => {
                                    field_counter.insert(key.to_string(), r_cnt.clone());
                                }
                            }
                        }
                        let mut field_comb_counter = l.field_comb_counter.clone();
                        for (key, r_cnt) in _r.field_comb_counter.iter() {
                            match l.field_comb_counter.get(key) {
                                Some(l_cnt) => {
                                    field_comb_counter.insert(key.clone(), r_cnt.clone() + l_cnt.clone());
                                },
                                None => {
                                    field_comb_counter.insert(key.clone(), r_cnt.clone());
                                }
                            }
                        }
                        RustJsonSchema::Record(RustRecord{
                            field_schema: field_schema,
                            field_comb_counter: field_comb_counter,
                            field_counter: field_counter
                        })
                    },
                    RustJsonSchema::Union(_) => {
                        other.merge(self)
                    },
                }
            },
            _ => panic!("merge_into_record only support Record object")
        }
    }
    fn merge_into_union(self, other:RustJsonSchema) -> RustJsonSchema {
        match self {
            RustJsonSchema::Union(ref l) => {
                match other {
                    RustJsonSchema::Unknown(_) => {
                        self
                    },
                    RustJsonSchema::Atomic(_) => {
                        let mut content = l.content.clone();
                        content.insert(other.clone());
                        RustJsonSchema::Union(RustUnion {content: content})
                    },
                    RustJsonSchema::Union(_r) => {
                        let mut schemas = Vec::new();
                        schemas.extend(l.content.clone());
                        schemas.extend(_r.content.clone());
                        reduce(schemas)
                        // If two Union both has two List type, 
                        // the two will be merged.
                    },
                    _ => { //l: Union, r: Array | Record
                        let mut content = HashSet::new();
                        let mut total_has_same_type: u8 = 0;
                        for jsonschema in l.content.iter() {
                            match &jsonschema {
                                RustJsonSchema::Union(_) => {
                                    panic!("Union in Union Error.\n self: \n{}\n internal schema: \n{}\n other: \n{}\n", self.repr(), jsonschema.repr(), other.repr())
                                },
                                RustJsonSchema::Unknown(_) => {},
                                _ => {
                                    let is_same_type = match (&other, &jsonschema) {
                                        (RustJsonSchema::Array(_), RustJsonSchema::Array(_)) => true,
                                        (RustJsonSchema::Record(_), RustJsonSchema::Record(_)) => true,
                                        (_, _) => false
                                    };
                                    if is_same_type {
                                        // TODO:
                                        // 1. [X] Must check whether the merged result is 'Union'
                                        // If the merged result is Union, it can lead to "Union in Union Error" later.
                                        // 2. [-] total_has_same_type -> merge_count
                                        // 3. [X] must avoid repeat merge into more than one element in the left Union.
                                        let merged = other.clone().merge(jsonschema.clone());
                                        match merged {
                                            RustJsonSchema::Union(_) => {
                                                panic!("Merge Array or Record into Union Error. \n self: \n{}\n internal schema: \n{}\n other: \n{}\n", self.repr(), jsonschema.repr(), other.repr())
                                            },
                                            _ => {
                                                content.insert(merged);
                                                total_has_same_type += 1;
                                                if total_has_same_type > 1 {
                                                    panic!("More than 1 Array or Record Error. \n self: \n{}\n internal schema: \n{}\n other: \n{}\n", self.repr(), jsonschema.repr(), other.repr())
                                                }
                                            }
                                        }
                                    } else {
                                        content.insert(jsonschema.clone());
                                    }
                                }
                            }
                        }
                        if total_has_same_type == 0 {
                            content.insert(other.clone());
                        }
                        RustJsonSchema::Union(RustUnion {content: content})
                    },
                }
            },
            _ => panic!("merge_into_union only support Union object")
        }
    }
}
impl Hash for RustJsonSchema {
    fn hash<H: Hasher>(&self, state: &mut H) {
        self.repr().hash(state)
    }
}

use super::atomic::num::*;
use super::atomic::atomic::*;
#[cfg(test)]
mod tests {
    use super::*;
    use std::collections::HashMap;
    #[test]
    fn test_merge() {
        // Unknown | Unknown
        let unknown = RustJsonSchema::Unknown(RustUnknown{});
        assert_eq!(unknown.clone().merge(unknown.clone()).repr(), "Unknown()");
        // Unknown | Any
        let non_atom = RustJsonSchema::Atomic(RustAtomic::Non(RustNon{}));
        assert_eq!(unknown.clone().merge(non_atom.clone()).repr(), "Atomic(Non())");
    }
    #[test]
    fn test_merge_into_atomic() {
        let non_atom = RustJsonSchema::Atomic(RustAtomic::Non(RustNon{}));
        let unknown_atom = RustJsonSchema::Unknown(RustUnknown{});
        let str_atom = RustJsonSchema::Atomic(RustAtomic::Str(RustStr{}));
        let array = RustJsonSchema::Array(RustArray{ content: Box::new(RustJsonSchema::Atomic(RustAtomic::Str(RustStr{})))});
        // Atomic | Unknown
        assert_eq!(non_atom.clone().merge(unknown_atom.clone()).repr(), "Atomic(Non())");
        // Atomic | Atomic (1)
        assert_eq!(non_atom.clone().merge(str_atom.clone()).repr(), "Optional(Atomic(Str()))");
        // Atomic | Atomic (2)
        assert_eq!(str_atom.clone().merge(str_atom.clone()).repr(), "Atomic(Str())");
        // Atomic | Array
        assert_eq!(str_atom.clone().merge(array.clone()).repr(), "Union({Array(Atomic(Str())), Atomic(Str())})");
        // Atomic | Union (1)
        let uni = array.clone().merge(non_atom.clone());
        assert_eq!(str_atom.clone().merge(uni).repr(), "Union({Array(Atomic(Str())), Atomic(Non()), Atomic(Str())})");
        // Atomic | Union (2)
        let uni = str_atom.clone().merge(array.clone().merge(non_atom.clone()));
        assert_eq!(str_atom.clone().merge(uni).repr(), "Union({Array(Atomic(Str())), Atomic(Non()), Atomic(Str())})");
        // Atomic | Union (3)
        let uni = str_atom.clone().merge(array.clone().merge(non_atom.clone()));
        assert_eq!(uni.clone().merge(str_atom.clone()).repr(), "Union({Array(Atomic(Str())), Atomic(Non()), Atomic(Str())})");
    }
    #[test]
    fn test_merge_into_array() {
        let non_atom = RustJsonSchema::Atomic(RustAtomic::Non(RustNon{}));
        let unknown_atom = RustJsonSchema::Unknown(RustUnknown{});
        let str_atom = RustJsonSchema::Atomic(RustAtomic::Str(RustStr{}));
        let array = RustJsonSchema::Array(RustArray{ content: Box::new(RustJsonSchema::Atomic(RustAtomic::Str(RustStr{})))});
        let mut map = HashMap::new();
        map.insert("banana".to_owned(), non_atom.clone());
        map.insert("apple".to_owned(), str_atom.clone());
        let record = RustJsonSchema::Record(RustRecord::new(map));
        let unknown_array = RustJsonSchema::Array(RustArray::new(RustJsonSchema::Unknown(RustUnknown{})));
        // Array | Unknown
        assert_eq!(unknown_array.clone().merge(unknown_atom.clone()).repr(), "Array(Unknown())");
        // Array[Unknown] | Array[Atomic]
        assert_eq!(unknown_array.clone().merge(array.clone()).repr(), "Array(Atomic(Str()))");
        assert_eq!(array.clone().merge(unknown_array.clone()).repr(), "Array(Atomic(Str()))");
        // Array | Atomic 
        assert_eq!(array.clone().merge(str_atom.clone()).repr(), "Union({Array(Atomic(Str())), Atomic(Str())})");
        // Array | Array 
        let str_array = RustJsonSchema::Array(RustArray{ content: Box::new(RustJsonSchema::Atomic(RustAtomic::Str(RustStr{})))});
        let non_array = RustJsonSchema::Array(RustArray{ content: Box::new(RustJsonSchema::Atomic(RustAtomic::Non(RustNon{})))});
        assert_eq!(str_array.clone().merge(non_array.clone()).repr(), "Array(Optional(Atomic(Str())))");
        // Array | Union (1)
        let uni = str_atom.clone().merge(non_atom.clone());
        assert_eq!(array.clone().merge(uni).repr(), "Union({Array(Atomic(Str())), Atomic(Non()), Atomic(Str())})");
        // Array | Union (2)
        let uni = str_atom.clone().merge(non_atom.clone()).merge(non_array.clone());
        assert_eq!(str_array.clone().merge(uni).repr(), "Union({Array(Optional(Atomic(Str()))), Atomic(Non()), Atomic(Str())})");
        // Array | Record
        assert_eq!(str_array.clone().merge(record).repr(), "Union({Array(Atomic(Str())), Record({\"apple\": Atomic(Str()), \"banana\": Atomic(Non())})})");
    }
    #[test]
    fn test_merge_into_record() {
        let non_atom = RustJsonSchema::Atomic(RustAtomic::Non(RustNon{}));
        let unknown_atom = RustJsonSchema::Unknown(RustUnknown{});
        let str_atom = RustJsonSchema::Atomic(RustAtomic::Str(RustStr{}));
        let array = RustJsonSchema::Array(RustArray{ content: Box::new(RustJsonSchema::Atomic(RustAtomic::Str(RustStr{})))});
        let mut map = HashMap::new();
        map.insert("banana".to_owned(), non_atom.clone());
        map.insert("apple".to_owned(), str_atom.clone());
        let rr1 = RustJsonSchema::Record(RustRecord::new(map));
        // Record | Unknown
        assert_eq!(rr1.clone().merge(unknown_atom.clone()).repr(), "Record({\"apple\": Atomic(Str()), \"banana\": Atomic(Non())})");
        // Record | Atomic
        assert_eq!(rr1.clone().merge(non_atom.clone()).repr(), "Optional(Record({\"apple\": Atomic(Str()), \"banana\": Atomic(Non())}))");
        // Record | Array
        assert_eq!(rr1.clone().merge(array.clone()).repr(), "Union({Array(Atomic(Str())), Record({\"apple\": Atomic(Str()), \"banana\": Atomic(Non())})})");
        // Record | Union
        let uni1 = str_atom.clone().merge(non_atom.clone()).merge(rr1.clone());
        let mut map = HashMap::new();
        map.insert("can".to_owned(), str_atom.clone());
        map.insert("banana".to_owned(), non_atom.clone());
        let rr2 = RustJsonSchema::Record(RustRecord::new(map));
        assert_eq!(rr2.merge(uni1).repr(), "Union({Atomic(Non()), Atomic(Str()), Record({\"apple\": Atomic(Str()), \"banana\": Atomic(Non()), \"can\": Atomic(Str())})})");
        // Record | Record 1
        let mut map = HashMap::new();
        map.insert("apple".to_owned(), str_atom.clone());
        map.insert("banana".to_owned(), str_atom.clone());
        let ab_record = RustJsonSchema::Record(RustRecord::new(map));
        let mut map = HashMap::new();
        map.insert("can".to_owned(), str_atom.clone());
        map.insert("dance".to_owned(), str_atom.clone());
        let cd_record = RustJsonSchema::Record(RustRecord::new(map));
        assert_eq!(ab_record.merge(cd_record).repr(), "UniformRecord(FieldSet({\"apple\", \"banana\", \"can\", \"dance\"}), Atomic(Str()))");
        // Record | Record 2
        let mut map = HashMap::new();
        map.insert("banana".to_owned(), non_atom.clone());
        map.insert("apple".to_owned(), str_atom.clone());
        let rr1 = RustJsonSchema::Record(RustRecord::new(map));
        let mut map = HashMap::new();
        map.insert("can".to_owned(), str_atom.clone());
        map.insert("banana".to_owned(), non_atom.clone());
        let rr2 = RustJsonSchema::Record(RustRecord::new(map));
        assert_eq!(rr1.clone().merge(rr2.clone()).repr(), "Record({\"apple\": Atomic(Str()), \"banana\": Atomic(Non()), \"can\": Atomic(Str())})");
        // Check detail
        let r = rr1.clone().merge(rr2.clone());
        let mut apple_banana = HashSet::new();
        apple_banana.insert("apple".to_string());
        apple_banana.insert("banana".to_string());
        match r {
            RustJsonSchema::Record(record) => {
                assert_eq!(record.field_counter.len(), 3);
                match record.field_counter.get("apple") {
                    Some(cnt) => {
                        assert_eq!(cnt.to_owned(), 1);
                    },
                    None => {
                        panic!();
                    }
                }
                match record.field_counter.get("banana") {
                    Some(cnt) => {
                        assert_eq!(cnt.to_owned(), 2);
                    },
                    None => {
                        panic!();
                    }
                }
                match record.field_counter.get("can") {
                    Some(cnt) => {
                        assert_eq!(cnt.to_owned(), 1);
                    },
                    None => {
                        panic!();
                    }
                }
                assert_eq!(record.field_comb_counter.len(), 2);
                match record.field_comb_counter.get(&RustFieldSet {content: apple_banana} ) {
                    Some(cnt) => {
                        assert_eq!(cnt.to_owned(), 1);
                    },
                    None => {
                        panic!();
                    }
                }
            }
            _ => {
                panic!();
            }
        }

    }

    #[test]
    fn test_merge_into_union() {
        let non_atom = RustJsonSchema::Atomic(RustAtomic::Non(RustNon{}));
        let unknown_atom = RustJsonSchema::Unknown(RustUnknown{});
        let str_atom = RustJsonSchema::Atomic(RustAtomic::Str(RustStr{}));
        let int_atom = RustJsonSchema::Atomic(RustAtomic::Num(RustNum::Int(RustInt{})));
        let str_array = RustJsonSchema::Array(RustArray{ content: Box::new(RustJsonSchema::Atomic(RustAtomic::Str(RustStr{})))});
        let non_array = RustJsonSchema::Array(RustArray{ content: Box::new(RustJsonSchema::Atomic(RustAtomic::Non(RustNon{})))});
        let array = RustJsonSchema::Array(RustArray{ content: Box::new(RustJsonSchema::Atomic(RustAtomic::Str(RustStr{})))});
        let uni = array.clone().merge(non_atom.clone());
        // Union | Unknown
        assert_eq!(uni.clone().merge(unknown_atom.clone()).repr(), "Optional(Array(Atomic(Str())))");
        // Union | Atomic 1
        assert_eq!(uni.merge(str_atom.clone()).repr(), "Union({Array(Atomic(Str())), Atomic(Non()), Atomic(Str())})");
        // Union | Atomic 2
        let uni = array.clone().merge(str_atom.clone());
        assert_eq!(uni.merge(str_atom.clone()).repr(), "Union({Array(Atomic(Str())), Atomic(Str())})");
        // Union | Array 1
        let uni = str_atom.clone().merge(non_atom.clone()).merge(non_array.clone());
        assert_eq!(uni.merge(str_array.clone()).repr(), "Union({Array(Optional(Atomic(Str()))), Atomic(Non()), Atomic(Str())})");
        // Union | Array 2
        let uni = str_array.clone().merge(int_atom.clone()).merge(non_array.clone());
        assert_eq!(uni.repr(), "Union({Array(Optional(Atomic(Str()))), Atomic(Int())})");
        // 
        // Union | Union (1)
        let uni1 = str_atom.clone().merge(non_atom.clone());
        let uni2 = int_atom.clone().merge(non_atom.clone());
        assert_eq!(uni1.clone().merge(uni2).repr(), "Union({Atomic(Int()), Atomic(Non()), Atomic(Str())})");
        // Union | Union (2)
        let uni3 = str_atom.clone().merge(non_atom.clone());
        assert_eq!(uni1.merge(uni3).repr(), "Optional(Atomic(Str()))");
        // Union with Atomic List | Union with another kind of Atomic List
        let uni1 = str_array.clone().merge(int_atom.clone());
        let uni2 = non_array.clone().merge(non_atom.clone());
        assert_eq!(uni1.merge(uni2).repr(), "Union({Array(Optional(Atomic(Str()))), Atomic(Int()), Atomic(Non())})");
    }
}