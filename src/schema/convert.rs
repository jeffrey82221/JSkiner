use pyo3::prelude::*;
use super::top::RustJsonSchema;
use super::atomic::atomic::Atomic;
use super::array::Array;
use super::record::{Record, UniformRecord, UnionRecord};
use super::unions::{Union, Optional};
use super::unknown::Unknown;
pub fn py2rust(value: &PyAny) -> RustJsonSchema {
    /*
    Convert PyAny to its Rust Counterpart: 
    */
    let rust_schema = match (
        value.extract::<Atomic>(), 
        value.extract::<Array>(), 
        value.extract::<Record>(), 
        value.extract::<UniformRecord>(), 
        value.extract::<UnionRecord>(), 
        value.extract::<Union>(), 
        value.extract::<Optional>(), 
        value.extract::<Unknown>()
    ) {
        (Ok(a), _, _, _, _, _, _, _) => RustJsonSchema::Atomic(a.rust_obj),
        (_, Ok(b), _, _, _, _, _, _) => RustJsonSchema::Array(b.rust_obj),
        (_, _, Ok(c), _, _, _, _, _) => RustJsonSchema::Record(c.rust_obj),
        (_, _, _, Ok(d), _, _, _, _) => RustJsonSchema::Record(d.rust_obj),
        (_, _, _, _, Ok(e), _, _, _) => RustJsonSchema::Record(e.rust_obj),
        (_, _, _, _, _, Ok(f), _, _) => RustJsonSchema::Union(f.rust_obj),
        (_, _, _, _, _, _, Ok(g), _) => RustJsonSchema::Union(g.rust_obj),
        (_, _, _, _, _, _, _, Ok(h)) => RustJsonSchema::Unknown(h.rust_obj),
        _ => panic!("Expect Atomic, Array, Record, UniformRecord, UnionRecord, Union, Optional, or Unknown")
    };
    rust_schema
}