use std::env;
use std::process;
use std::error::Error;
use std::fs::File;
use std::io::prelude::*;
use std::path::Path;
use std::collections::HashSet;

fn compute(s: &str) -> i64 {
    let mut val = 0;
    let mut seen = HashSet::new();
    seen.insert(val);
    for line in s.lines().cycle() {
        val += line.parse::<i64>().unwrap();
        if seen.contains(&val) {
            return val;
        } else {
            seen.insert(val);
        }
    }
    panic!("unreachable")
}

fn main() {
    let args: Vec<String> = env::args().collect();
    if args.len() != 2 {
        println!("usage {} INPUT", args[0]);
        process::exit(1);
    }

    let path = Path::new(&args[1]);
    let display = path.display();

    let mut file = match File::open(&path) {
        Err(why) => panic!("couldn't open {}: {}", display, why.description()),
        Ok(file) => file,
    };

    // Read the file contents into a string, returns `io::Result<usize>`
    let mut s = String::new();
    match file.read_to_string(&mut s) {
        Err(why) => panic!("couldn't read {}: {}", display, why.description()),
        Ok(_) => println!("{}", compute(&s)),
    }
}
