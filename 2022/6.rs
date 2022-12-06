use std::io::{self, BufRead};
use std::collections::HashSet;

fn main() {
    let stdin = io::stdin();
    let lines = stdin.lock().lines().map(|line| line.unwrap());

    for line in lines {
        let chars: Vec<_> = line.chars().collect();
        for (index, window) in chars.windows(4).enumerate() {
            let s: HashSet<_> = window.iter().collect();
            if s.len() == window.len() {
                println!("{}", index + window.len());
                break;
            }
        }
    }
}